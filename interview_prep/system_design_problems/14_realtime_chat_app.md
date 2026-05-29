# Real-Time Chat Application (WhatsApp) System Design

## Requirements

### Functional
- One-to-one messaging
- Group messaging
- Message delivery acknowledgment (sent, delivered, read)
- Typing indicators
- Online/offline status
- Message history
- File sharing
- Message search/filtering

### Non-Functional
- Sub-second message delivery
- 100M+ DAU, 1M+ concurrent users
- 99.99% availability
- Geographic distribution
- End-to-end encryption support
- Data consistency

## System Architecture

```
Client 1 (Sender)
    |
    v
[WebSocket]
    |
    v
[API Server] --> [Message Queue] --> [Processing Service]
    |                                      |
    |                                      v
    v                                 [Database]
[Cache]                                     |
    |                                       v
    +-------> [Notification Server] <-- [Analytics]
                      |
                      v
                   Client 2 (Receiver)
```

## Core Components

### 1. Connection Service

```python
import asyncio
import json
from typing import Set, Dict

class ConnectionManager:
    """Manage WebSocket connections for users"""
    
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self.user_status: Dict[str, str] = {}  # user_id -> "online"/"offline"
    
    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        
        self.active_connections[user_id].add(websocket)
        self.user_status[user_id] = "online"
        
        # Notify contacts of online status
        await self.broadcast_status(user_id, "online")
    
    async def disconnect(self, user_id: str, websocket: WebSocket):
        self.active_connections[user_id].discard(websocket)
        
        # Check if user has other connections
        if not self.active_connections[user_id]:
            self.user_status[user_id] = "offline"
            await self.broadcast_status(user_id, "offline")
    
    async def send_message(self, from_user: str, to_user: str, message: dict):
        """Send message to user"""
        if to_user in self.active_connections:
            for connection in self.active_connections[to_user]:
                try:
                    await connection.send_json({
                        "type": "message",
                        "from": from_user,
                        "content": message,
                        "timestamp": datetime.now().isoformat()
                    })
                except Exception as e:
                    print(f"Error sending message: {e}")
    
    async def broadcast_status(self, user_id: str, status: str):
        """Notify contacts of user status change"""
        contacts = await get_user_contacts(user_id)
        
        status_msg = {
            "type": "status_change",
            "user_id": user_id,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
        
        for contact_id in contacts:
            await self.send_message("system", contact_id, status_msg)

# Global connection manager
manager = ConnectionManager()

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(user_id, websocket)
    
    try:
        while True:
            data = await websocket.receive_json()
            
            if data["type"] == "message":
                # Save to database
                msg_id = await save_message(data)
                
                # Send to receiver
                await manager.send_message(
                    user_id, 
                    data["to_user"],
                    {"content": data["content"], "message_id": msg_id}
                )
                
                # Send delivery confirmation
                await websocket.send_json({
                    "type": "delivery_confirmation",
                    "message_id": msg_id,
                    "status": "delivered"
                })
            
            elif data["type"] == "typing":
                # Broadcast typing indicator
                await manager.send_message(
                    user_id,
                    data["to_user"],
                    {"type": "typing", "user_id": user_id}
                )
            
            elif data["type"] == "read_receipt":
                # Update message status
                await update_message_status(data["message_id"], "read")
                
                # Notify sender
                await manager.send_message(
                    user_id,
                    data["to_user"],
                    {"type": "read_receipt", "message_id": data["message_id"]}
                )
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        await manager.disconnect(user_id, websocket)
```

### 2. Message Service

```python
class MessageService:
    def __init__(self, db, cache, queue):
        self.db = db
        self.cache = cache
        self.queue = queue
    
    async def send_message(self, msg_data: dict) -> str:
        """Send message with reliability"""
        # Generate unique ID
        message_id = str(uuid.uuid4())
        
        # Create message object
        message = {
            "id": message_id,
            "from": msg_data["from"],
            "to": msg_data["to"],
            "content": msg_data["content"],
            "timestamp": datetime.now(),
            "status": "sent",  # sent -> delivered -> read
            "type": msg_data.get("type", "text")  # text, image, file
        }
        
        # Save to database
        await self.db.save_message(message)
        
        # Push to queue for delivery
        await self.queue.push("messages", message)
        
        # Cache recent messages
        cache_key = f"messages:{msg_data['to']}"
        await self.cache.lpush(cache_key, json.dumps(message))
        await self.cache.expire(cache_key, 86400 * 30)  # 30 days
        
        return message_id
    
    async def get_chat_history(self, user_id: str, other_user_id: str, 
                               limit: int = 50) -> list:
        """Get conversation history"""
        # Try cache first
        cache_key = f"chat:{user_id}:{other_user_id}"
        cached = await self.cache.get(cache_key)
        
        if cached:
            return json.loads(cached)[:limit]
        
        # Load from database
        messages = await self.db.get_messages(
            user_id=user_id,
            other_user_id=other_user_id,
            limit=limit
        )
        
        # Cache it
        await self.cache.set(cache_key, json.dumps(messages), ex=3600)
        
        return messages
    
    async def update_message_status(self, message_id: str, status: str):
        """Update delivery/read status"""
        await self.db.update_message_status(message_id, status)
        
        # Invalidate cache
        await self.cache.delete(f"msg:{message_id}")
```

### 3. Group Messaging

```python
class GroupService:
    def __init__(self, db, cache):
        self.db = db
        self.cache = cache
    
    async def send_group_message(self, group_id: str, from_user: str, 
                                  content: str) -> str:
        """Send message to group"""
        message_id = str(uuid.uuid4())
        
        message = {
            "id": message_id,
            "group_id": group_id,
            "from": from_user,
            "content": content,
            "timestamp": datetime.now(),
            "status": "sent"
        }
        
        # Save message
        await self.db.save_group_message(message)
        
        # Get group members
        members = await self.db.get_group_members(group_id)
        
        # Send to each member (excluding sender)
        for member_id in members:
            if member_id != from_user:
                # Queue for delivery
                await queue.push("group_messages", {
                    "message_id": message_id,
                    "recipient": member_id,
                    "message": message
                })
        
        return message_id
    
    async def create_group(self, creator_id: str, group_name: str, 
                           members: list):
        """Create new group"""
        group_id = str(uuid.uuid4())
        
        group = {
            "id": group_id,
            "name": group_name,
            "creator": creator_id,
            "members": members + [creator_id],
            "created_at": datetime.now(),
            "admin": [creator_id]
        }
        
        await self.db.save_group(group)
        
        # Notify members
        for member_id in members:
            # Send notification
            pass
        
        return group_id
```

## Database Schema

```sql
-- Users
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    phone_number VARCHAR(20) UNIQUE,
    username VARCHAR(100),
    profile_picture_url VARCHAR(2048),
    status_message VARCHAR(500),
    is_online BOOLEAN,
    last_seen TIMESTAMP,
    created_at TIMESTAMP
);

-- Messages (One-to-one)
CREATE TABLE messages (
    id VARCHAR(36) PRIMARY KEY,
    from_user_id VARCHAR(36),
    to_user_id VARCHAR(36),
    content TEXT,
    message_type VARCHAR(20),  -- text, image, file, etc
    status VARCHAR(20),  -- sent, delivered, read
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (from_user_id) REFERENCES users(id),
    FOREIGN KEY (to_user_id) REFERENCES users(id),
    INDEX idx_to_from (to_user_id, from_user_id, created_at),
    INDEX idx_created (created_at DESC)
);

-- Groups
CREATE TABLE groups (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100),
    description VARCHAR(500),
    creator_id VARCHAR(36),
    created_at TIMESTAMP,
    FOREIGN KEY (creator_id) REFERENCES users(id)
);

-- Group Members
CREATE TABLE group_members (
    group_id VARCHAR(36),
    user_id VARCHAR(36),
    role VARCHAR(20),  -- admin, member
    joined_at TIMESTAMP,
    PRIMARY KEY (group_id, user_id),
    FOREIGN KEY (group_id) REFERENCES groups(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Group Messages
CREATE TABLE group_messages (
    id VARCHAR(36) PRIMARY KEY,
    group_id VARCHAR(36),
    from_user_id VARCHAR(36),
    content TEXT,
    created_at TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES groups(id),
    FOREIGN KEY (from_user_id) REFERENCES users(id),
    INDEX idx_group_created (group_id, created_at DESC)
);

-- Message Read Receipts
CREATE TABLE message_read_receipts (
    message_id VARCHAR(36),
    user_id VARCHAR(36),
    read_at TIMESTAMP,
    PRIMARY KEY (message_id, user_id),
    FOREIGN KEY (message_id) REFERENCES messages(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## Scalability & Reliability

### Message Queue for Reliability
```python
# Kafka for message queueing
class MessageQueue:
    def __init__(self, bootstrap_servers):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode()
        )
        self.consumer = KafkaConsumer(
            'messages',
            bootstrap_servers=bootstrap_servers,
            group_id='message_delivery'
        )
    
    async def send_message_reliable(self, msg):
        """Send message with retry logic"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                self.producer.send('messages', value=msg)
                self.producer.flush()
                return True
            except Exception as e:
                retry_count += 1
                await asyncio.sleep(2 ** retry_count)  # Exponential backoff
        
        return False
```

### Geographically Distributed

```
Region: US-East
[API Server] <-> [WebSocket] <-> Client
     |
     v
[Database Replica]

Region: Europe
[API Server] <-> [WebSocket] <-> Client
     |
     v
[Database Replica]

Region: Asia
[API Server] <-> [WebSocket] <-> Client
     |
     v
[Database Replica]

All synced via: Kafka + Write-Ahead Log
```

## Interview Questions

1. **How to ensure message delivery?**
   - Message queue + persistent storage
   - Retry with exponential backoff

2. **How to handle user going offline?**
   - Queue messages in DB, deliver on reconnect
   - Use message status: sent (queued) -> delivered -> read

3. **Typing indicators without flooding?**
   - Throttle to 1 typing event per second
   - Stop signal after 3 seconds of inactivity

4. **End-to-end encryption?**
   - Sender encrypts with recipient's public key
   - Server never sees plaintext
   - Pre-key bundles for scalability

5. **Group message at 1M users?**
   - Fan-out to queue, not direct send
   - Batch delivery service consumes from queue

## Key Points

- ✅ Use WebSocket for real-time bidirectional communication
- ✅ Message queue for reliability and scaling
- ✅ Separate connection manager from message storage
- ✅ Cache recent messages in Redis
- ✅ Status transitions: sent → delivered → read
- ✅ Geographically distributed databases
- ✅ Async delivery for group messages
- ✅ Handle offline users gracefully
