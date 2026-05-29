# Notification System Design

## Requirements

### Functional
- Send notifications across channels (Email, SMS, Push, InApp)
- Schedule notifications
- Track delivery status
- Handle retries/failures
- Batch notifications
- User preferences/subscriptions

### Non-Functional
- Deliver 99.9% of notifications
- Latency < 100ms
- Handle 1M notifications/hour
- Scale horizontally
- Handle peak load (news events)

## System Architecture

```
Event Sources          Notification Service        Channels
   |                          |                        |
Order Event -------> Event Processor -------> Email Service
User Event ------>   (Router/Queuing)  ----> SMS Provider
Payment Event ---                       ----> Push Service
                                        ----> In-App Storage
                                            
                     Delivery Tracking
                     Retry/Fallback
                     Analytics
```

## Core Classes

```python
class Notification:
    def __init__(self, notification_id, user_id, template_id):
        self.notification_id = notification_id
        self.user_id = user_id
        self.template_id = template_id
        self.channels = []  # EMAIL, SMS, PUSH, IN_APP
        self.params = {}  # Template parameters
        self.priority = "NORMAL"  # HIGH, NORMAL, LOW
        self.scheduled_time = datetime.now()
        self.status = "PENDING"  # PENDING, SENT, FAILED, BOUNCED
        self.attempts = 0
        self.max_retries = 3
    
    def add_channel(self, channel):
        self.channels.append(channel)
    
    def set_params(self, params):
        self.params = params
    
    def render_content(self):
        """Render template with parameters"""
        template = template_service.get_template(self.template_id)
        return template.render(self.params)

class NotificationTemplate:
    def __init__(self, template_id, name):
        self.template_id = template_id
        self.name = name
        self.subject = ""
        self.body = ""
        self.content_type = "TEXT"  # TEXT, HTML
    
    def render(self, params):
        """Render with parameters"""
        import jinja2
        template = jinja2.Template(self.body)
        return template.render(**params)

class Channel:
    def send(self, notification):
        pass

class EmailChannel(Channel):
    def send(self, notification):
        try:
            content = notification.render_content()
            
            # Send via email service
            result = email_service.send(
                to=get_user(notification.user_id).email,
                subject=notification.params.get("subject", "Notification"),
                body=content
            )
            
            return {"success": True, "message_id": result["id"]}
        
        except Exception as e:
            return {"success": False, "error": str(e)}

class SMSChannel(Channel):
    def send(self, notification):
        try:
            content = notification.render_content()
            user_phone = get_user(notification.user_id).phone
            
            result = sms_service.send(
                to=user_phone,
                message=content[:160]  # SMS length limit
            )
            
            return {"success": True, "message_id": result["id"]}
        
        except Exception as e:
            return {"success": False, "error": str(e)}

class PushChannel(Channel):
    def send(self, notification):
        try:
            user_devices = device_service.get_user_devices(
                notification.user_id)
            
            content = notification.render_content()
            
            for device in user_devices:
                push_service.send(
                    device_token=device.push_token,
                    title=notification.params.get("title"),
                    body=content
                )
            
            return {"success": True}
        
        except Exception as e:
            return {"success": False, "error": str(e)}

class InAppChannel(Channel):
    def send(self, notification):
        try:
            # Save to database
            content = notification.render_content()
            
            in_app_message = {
                "user_id": notification.user_id,
                "title": notification.params.get("title"),
                "message": content,
                "created_at": datetime.now(),
                "read": False,
                "action_url": notification.params.get("action_url")
            }
            
            database.save_in_app_message(in_app_message)
            
            return {"success": True}
        
        except Exception as e:
            return {"success": False, "error": str(e)}

class NotificationService:
    def __init__(self):
        self.queue = queue.PriorityQueue()  # Priority queue
        self.channels = {
            "EMAIL": EmailChannel(),
            "SMS": SMSChannel(),
            "PUSH": PushChannel(),
            "IN_APP": InAppChannel()
        }
        self.worker_threads = []
        self.start_workers()
    
    def send_notification(self, user_id, template_id, params, channels=None):
        """Queue notification for sending"""
        notification = Notification(
            generate_notification_id(),
            user_id,
            template_id
        )
        
        notification.set_params(params)
        
        # Get user preferences
        if channels is None:
            channels = self.__get_user_channels(user_id)
        
        for channel in channels:
            notification.add_channel(channel)
        
        # Get priority
        priority = params.get("priority", 5)  # Lower = higher
        
        # Queue for processing
        self.queue.put((priority, notification))
        
        return notification.notification_id
    
    def schedule_notification(self, user_id, template_id, params, 
                            scheduled_time, channels=None):
        """Schedule notification for later"""
        notification = Notification(
            generate_notification_id(),
            user_id,
            template_id
        )
        
        notification.scheduled_time = scheduled_time
        notification.set_params(params)
        
        if channels is None:
            channels = self.__get_user_channels(user_id)
        
        for channel in channels:
            notification.add_channel(channel)
        
        # Save to delayed queue
        scheduler.schedule(notification, scheduled_time)
        
        return notification.notification_id
    
    def process_queue(self):
        """Worker thread: process queued notifications"""
        while True:
            try:
                priority, notification = self.queue.get(timeout=1)
                
                self.__send_notification(notification)
            
            except queue.Empty:
                continue
            
            except Exception as e:
                print(f"Error: {e}")
    
    def __send_notification(self, notification):
        """Send through all channels"""
        user_prefs = user_preference_service.get_preferences(
            notification.user_id)
        
        for channel_name in notification.channels:
            # Check user opt-in
            if not user_prefs.get(f"opt_in_{channel_name}"):
                continue
            
            channel = self.channels[channel_name]
            
            try:
                result = channel.send(notification)
                
                if result["success"]:
                    # Track delivery
                    self.__track_delivery(notification, channel_name, "SENT")
                    notification.status = "SENT"
                else:
                    # Retry
                    self.__handle_failure(notification, channel_name)
            
            except Exception as e:
                self.__handle_failure(notification, channel_name)
    
    def __handle_failure(self, notification, channel_name):
        """Handle failed notification"""
        notification.attempts += 1
        
        if notification.attempts < notification.max_retries:
            # Exponential backoff
            delay = 2 ** notification.attempts
            
            # Re-queue with delay
            self.schedule_notification(
                notification.user_id,
                notification.template_id,
                notification.params,
                datetime.now() + timedelta(seconds=delay),
                [channel_name]
            )
        else:
            # Max retries exceeded
            notification.status = "FAILED"
            self.__track_delivery(notification, channel_name, "FAILED")
    
    def __get_user_channels(self, user_id):
        """Get user's enabled channels"""
        prefs = user_preference_service.get_preferences(user_id)
        
        channels = []
        if prefs.get("email_notifications"):
            channels.append("EMAIL")
        if prefs.get("sms_notifications"):
            channels.append("SMS")
        if prefs.get("push_notifications"):
            channels.append("PUSH")
        
        # Always add in-app
        channels.append("IN_APP")
        
        return channels
    
    def __track_delivery(self, notification, channel, status):
        """Track notification delivery"""
        delivery_log = {
            "notification_id": notification.notification_id,
            "user_id": notification.user_id,
            "channel": channel,
            "status": status,
            "timestamp": datetime.now()
        }
        
        database.save_delivery_log(delivery_log)
    
    def start_workers(self, num_workers=10):
        """Start worker threads"""
        for _ in range(num_workers):
            thread = threading.Thread(target=self.process_queue, daemon=True)
            thread.start()
            self.worker_threads.append(thread)
    
    def get_notification_status(self, notification_id):
        """Get status of notification"""
        return database.get_notification_status(notification_id)
```

## Event-Driven Architecture

```python
class EventDispatcher:
    def __init__(self, notification_service):
        self.notification_service = notification_service
        self.events = {}
    
    def subscribe(self, event_type, handler):
        """Subscribe to events"""
        if event_type not in self.events:
            self.events[event_type] = []
        self.events[event_type].append(handler)
    
    def dispatch(self, event_type, data):
        """Emit event"""
        if event_type in self.events:
            for handler in self.events[event_type]:
                handler(data)

# Usage
dispatcher = EventDispatcher(notification_service)

def on_order_placed(data):
    notification_service.send_notification(
        user_id=data["user_id"],
        template_id="order_confirmation",
        params={"order_id": data["order_id"]}
    )

dispatcher.subscribe("order_placed", on_order_placed)
```

## Batch Processing

```python
class BatchNotificationService:
    def send_batch(self, user_ids, template_id, params):
        """Send same notification to multiple users"""
        for user_id in user_ids:
            self.notification_service.send_notification(
                user_id,
                template_id,
                params,
                priority=10  # Batch = lower priority
            )
```

## Rate Limiting

```python
class RateLimiter:
    def __init__(self):
        self.user_limits = {}  # {user_id: {last_count, reset_time}}
    
    def allow_send(self, user_id, limit_per_hour=10):
        """Check if under rate limit"""
        now = datetime.now()
        
        if user_id not in self.user_limits:
            self.user_limits[user_id] = {
                "count": 0,
                "reset_time": now + timedelta(hours=1)
            }
        
        limit = self.user_limits[user_id]
        
        if now > limit["reset_time"]:
            # Reset
            limit["count"] = 0
            limit["reset_time"] = now + timedelta(hours=1)
        
        if limit["count"] < limit_per_hour:
            limit["count"] += 1
            return True
        
        return False
```

## Key Design Decisions

| Design | Reason |
|--------|--------|
| **Priority Queue** | High-priority notifications first |
| **Worker Threads** | Process notifications asynchronously |
| **Exponential Backoff** | Don't hammer failing services |
| **Channel Abstraction** | Easy to add new channels |
| **User Preferences** | Respect user opt-ins |
| **Delivery Tracking** | Debug/audit trail |

## Scalability Improvements

1. **Message Queue**: Kafka for events
2. **Service Separation**: Email, SMS, Push as separate services
3. **Rate Limiting**: Prevent spam
4. **Caching**: Template caching
5. **Sharding**: Shard by user_id

## Key Interview Questions

1. **How to handle 1M notifications/hour?**
   - Queue-based, worker threads, sharding

2. **Ensure 99.9% delivery?**
   - Retry logic, multiple channels, delivery tracking

3. **Handle peak load (news event)?**
   - Queue buffering, rate limiting, batch processing

4. **User unsubscribes mid-send?**
   - Check preferences before each send

5. **Failed sends?**
   - Exponential backoff, max retries, fallback providers
