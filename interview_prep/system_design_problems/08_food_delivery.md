# Food Delivery System

## Requirements

### Functional
- Browse restaurants/menu
- Place order
- Track delivery
- Rate/review
- Payment processing
- Cancel orders
- Driver assignment

### Non-Functional
- Real-time location tracking
- Order delivery < 30 minutes (target)
- Handle 100K concurrent orders
- Delivery partners app
- Customer notifications

## System Architecture

```
Customer App          Backend (Microservices)    Database/Cache
   |                         |                        |
   |--search restaurants-->  |--Catalog Service       |
   |<--list----------        |--Order Service         |
   |--place order----------> |--Payment Service       |
   |--track delivery-------> |--Notification Service  |
   |<--location updates--    |--Driver Assignment     |
   |                         |                        |
   |                      Message Queue
   |                    (RabbitMQ/Kafka)
   |
Partner App            Backend Services
   |                        |
   |--get orders----------> |--Driver Matching
   |<--order details------  |--Logistics Service
   |--update location-----> |
   |--mark delivered------->
   |--rate customer-------->
```

## Core Classes

```python
class Restaurant:
    def __init__(self, restaurant_id, name, location):
        self.restaurant_id = restaurant_id
        self.name = name
        self.location = location  # {lat, lng}
        self.menu_items = {}  # {item_id: MenuItem}
        self.avg_rating = 0
        self.delivery_time = 30  # minutes
        self.is_open = True
    
    def get_available_items(self):
        return [item for item in self.menu_items.values()
                if item.available]

class MenuItem:
    def __init__(self, item_id, name, price, category):
        self.item_id = item_id
        self.name = name
        self.price = price
        self.category = category
        self.available = True
        self.description = ""

class Order:
    def __init__(self, order_id, user_id, restaurant_id):
        self.order_id = order_id
        self.user_id = user_id
        self.restaurant_id = restaurant_id
        self.items = []  # {item_id: quantity}
        self.total_price = 0
        self.status = "CREATED"  # CREATED, CONFIRMED, PREPARING, READY, PICKED_UP, DELIVERED, CANCELLED
        self.created_at = datetime.now()
        self.delivery_time_estimate = 30
        self.driver_id = None
        self.special_instructions = ""
    
    def add_item(self, item_id, quantity):
        self.items[item_id] = quantity
    
    def calculate_total(self):
        menu_service = MenuService()
        subtotal = 0
        
        for item_id, quantity in self.items.items():
            item = menu_service.get_item(item_id)
            subtotal += item.price * quantity
        
        # Add delivery charges
        delivery_fee = 2  # Base fee
        if subtotal < 10:
            delivery_fee += 2  # Minimum order fee
        
        # Apply discounts/promotions
        discount = self.__apply_promos(subtotal)
        
        # Taxes
        tax = (subtotal + delivery_fee - discount) * 0.05
        
        self.total_price = subtotal + delivery_fee - discount + tax
        return self.total_price

class DeliveryPartner:
    def __init__(self, partner_id, name, phone):
        self.partner_id = partner_id
        self.name = name
        self.phone = phone
        self.current_location = None  # {lat, lng}
        self.is_available = True
        self.rating = 0
        self.total_deliveries = 0
        self.orders_assigned = []

class OrderService:
    def __init__(self):
        self.orders = {}
        self.lock = threading.RLock()
        self.message_queue = MessageQueue()
    
    def create_order(self, user_id, restaurant_id, items):
        """Create order"""
        with self.lock:
            # Validate restaurant
            restaurant = get_restaurant(restaurant_id)
            if not restaurant.is_open:
                return None, "Restaurant closed"
            
            # Verify items available
            for item_id in items:
                if not menu_service.is_available(item_id):
                    return None, f"Item {item_id} unavailable"
            
            # Create order
            order = Order(
                generate_order_id(),
                user_id,
                restaurant_id
            )
            
            for item_id, quantity in items.items():
                order.add_item(item_id, quantity)
            
            # Calculate total
            order.calculate_total()
            
            self.orders[order.order_id] = order
            
            return order, "Order created"
    
    def confirm_order(self, order_id, payment_info):
        """Confirm and pay for order"""
        with self.lock:
            order = self.orders.get(order_id)
            
            if not order or order.status != "CREATED":
                return False, "Invalid order"
            
            # Process payment
            payment_result = self.__process_payment(order, payment_info)
            
            if not payment_result["success"]:
                return False, payment_result["error"]
            
            # Confirm order
            order.status = "CONFIRMED"
            
            # Notify restaurant
            self.message_queue.publish(
                "order_confirmed",
                {"order_id": order_id, "restaurant_id": order.restaurant_id}
            )
            
            # Notify user
            notification_service.notify(order.user_id, 
                                       f"Order {order_id} confirmed")
            
            # Assign driver (async)
            self._assign_driver_async(order)
            
            return True, "Order confirmed"
    
    def _assign_driver_async(self, order):
        """Find and assign best driver"""
        def assign():
            driver = self.__find_best_driver(order)
            if driver:
                with self.lock:
                    order.driver_id = driver.partner_id
                    order.status = "CONFIRMED"
                    driver.orders_assigned.append(order.order_id)
                
                # Notify driver
                notification_service.notify_driver(
                    driver.partner_id,
                    f"New order: {order.order_id}"
                )
                
                # Notify customer
                notification_service.notify(
                    order.user_id,
                    f"Driver {driver.name} assigned"
                )
        
        thread = threading.Thread(target=assign, daemon=True)
        thread.start()
    
    def __find_best_driver(self, order):
        """Find nearest available driver"""
        # Get available drivers

        drivers = driver_service.get_available_drivers()
        
        restaurant = get_restaurant(order.restaurant_id)
        
        # Sort by distance
        candidates = []
        for driver in drivers:
            distance = self.__calculate_distance(
                driver.current_location,
                restaurant.location
            )
            candidates.append((driver, distance))
        
        candidates.sort(key=lambda x: x[1])
        
        if candidates:
            return candidates[0][0]
        
        return None
    
    def update_order_status(self, order_id, new_status):
        """Update order status"""
        with self.lock:
            order = self.orders.get(order_id)
            if not order:
                return False
            
            order.status = new_status
            
            # Notify user
            notification_service.notify(
                order.user_id,
                f"Order status: {new_status}"
            )
            
            # Publish event
            self.message_queue.publish(
                "order_status_changed",
                {"order_id": order_id, "status": new_status}
            )
            
            return True
    
    def cancel_order(self, order_id, user_id):
        """Cancel order with refund"""
        with self.lock:
            order = self.orders.get(order_id)
            
            if not order or order.user_id != user_id:
                return False, "Invalid order"
            
            # Can only cancel if not picked up
            if order.status in ["PICKED_UP", "DELIVERED"]:
                return False, "Cannot cancel"
            
            # Process refund
            self.__process_refund(order)
            
            # Mark cancelled
            order.status = "CANCELLED"
            
            # Notify restaurant
            self.message_queue.publish(
                "order_cancelled",
                {"order_id": order_id}
            )
            
            return True, "Order cancelled"
    
    def track_delivery(self, order_id):
        """Get real-time delivery info"""
        order = self.orders.get(order_id)
        if not order:
            return None
        
        if order.driver_id:
            driver = driver_service.get_driver(order.driver_id)
            return {
                "order_id": order_id,
                "status": order.status,
                "driver_name": driver.name,
                "driver_location": driver.current_location,
                "eta_minutes": self.__calculate_eta(driver, order)
            }
        
        return {
            "order_id": order_id,
            "status": order.status,
            "eta_minutes": 30  # Default estimate
        }
    
    def __process_payment(self, order, payment_info):
        try:
            result = payment_gateway.charge(
                amount=order.total_price,
                card=payment_info["card"]
            )
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def __process_refund(self, order):
        payment_gateway.refund(
            order_id=order.order_id,
            amount=order.total_price
        )
    
    def __calculate_distance(self, loc1, loc2):
        """Haversine distance"""
        # Calculate distance between two coordinates
        pass
    
    def __calculate_eta(self, driver, order):
        """Estimate delivery time"""
        current_location = driver.current_location
        restaurant = get_restaurant(order.restaurant_id)
        user_location = get_user(order.user_id).location
        
        # Distance to restaurant
        dist_to_restaurant = self.__calculate_distance(
            current_location, restaurant.location)
        
        # Distance from restaurant to user
        dist_to_user = self.__calculate_distance(
            restaurant.location, user_location)
        
        # Average speed: 5 km/min (30 km/hour)
        travel_time = (dist_to_restaurant + dist_to_user) / 5
        
        # Add prep time
        prep_time = 5
        
        return int(travel_time + prep_time)
```

## Real-Time Tracking

```python
class LocationTracker:
    def __init__(self):
        self.driver_locations = {}  # {driver_id: location}
    
    def update_location(self, driver_id, location):
        """Update driver location"""
        self.driver_locations[driver_id] = location
        
        # Broadcast to relevant customers
        orders = order_service.get_driver_orders(driver_id)
        
        for order in orders:
            notification_service.notify_customer_location(
                order.user_id,
                location
            )
    
    def get_driver_location(self, driver_id):
        return self.driver_locations.get(driver_id)
```

## Scalability Design

### Sharding Strategy
```python
# Shard by city/zone
shards = {
    "NYC": ["order_db_nyc_1", "order_db_nyc_2"],
    "SF": ["order_db_sf_1"],
    "LA": ["order_db_la_1", "order_db_la_2"]
}

def get_shard(city):
    return shards[city]
```

### Cache Strategy
```python
# Cache restaurants in city
cache.set(f"restaurants:NYC", restaurants, ttl=3600)

# Cache driver availability (short TTL)
cache.set(f"driver:available:{city}", drivers, ttl=60)

# Cache order status
cache.set(f"order:{order_id}", order, ttl=300)
```

## Key Interview Questions

1. **Real-time location tracking?**
   - WebSocket, update every 10 seconds

2. **Handle 100K concurrent orders?**
   - Sharding, message queue, worker threads

3. **Driver assignment algorithm?**
   - Nearest driver, rating, current load

4. **Handle driver disconnection?**
   - Retry assignment, customer notified

5. **ETA calculation?**
   - Distance + traffic + prep time

## Important Features

- ✅ Real-time tracking
- ✅ Smart driver assignment
- ✅ Accurate ETAs
- ✅ Async order processing
- ✅ Scalability by geography
- ✅ Fallback strategies
