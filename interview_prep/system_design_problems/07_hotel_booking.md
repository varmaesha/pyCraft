# Hotel Booking System

## Requirements

### Functional
- Browse hotels by location/dates
- Check room availability
- Reserve rooms
- Cancel reservations
- Process payments
- View booking history
- Admin manage rooms/prices

### Non-Functional
- High concurrency (peak booking times)
- Real-time availability
- Support multiple currencies
- 99.99% uptime
- Search response < 500ms

## System Architecture

```
Mobile/Web          API Gateway          Backend Services
   |                    |                     |
   |--search-------->   |----Route--------> Search Service
   |<--results------    |                  (Caching)
   |                    |
   |--book---------->   |----Route--------> Booking Service
   |                    |                  (Inventory)
   |--payment-------->  |----Route--------> Payment Service
   |<--confirmation-    |----Route--------> Notification Service
   |                    |                     |
                               Database/Cache
                                   and
                            Message Queue
```

## Core Classes

```python
class Hotel:
    def __init__(self, hotel_id, name, location, amenities):
        self.hotel_id = hotel_id
        self.name = name
        self.location = location  # City, coordinates
        self.amenities = amenities  # List of amenities
        self.rooms = {}  # {room_id: Room}
        self.ratings = []

class Room:
    def __init__(self, room_id, hotel_id, room_type):
        self.room_id = room_id
        self.hotel_id = hotel_id
        self.room_type = room_type  # SINGLE, DOUBLE, SUITE, DELUXE
        self.capacity = 0
        self.base_price = 0
        self.amenities = []
        self.bookings = []  # List of bookings
    
    def is_available(self, check_in, check_out):
        """Check if room available for date range"""
        for booking in self.bookings:
            if booking.status == "CONFIRMED":
                if self.__overlaps(check_in, check_out, 
                                  booking.check_in, booking.check_out):
                    return False
        return True
    
    def __overlaps(self, start1, end1, start2, end2):
        return start1 < end2 and start2 < end1

class Booking:
    def __init__(self, booking_id, user_id, room_id, check_in, check_out):
        self.booking_id = booking_id
        self.user_id = user_id
        self.room_id = room_id
        self.hotel_id = room.hotel_id
        self.check_in = check_in
        self.check_out = check_out
        self.num_nights = (check_out - check_in).days
        self.guests = []
        self.status = "PENDING"  # PENDING, CONFIRMED, CANCELLED
        self.total_price = 0
        self.cancellation_policy = "STANDARD"
    
    def calculate_price(self):
        room = get_room(self.room_id)
        
        # Base price
        price = room.base_price * self.num_nights
        
        # Seasonal pricing
        price = self.__apply_seasonal_pricing(price)
        
        # Discounts
        price = self.__apply_discounts(price)
        
        # Taxes
        price = self.__apply_taxes(price)
        
        self.total_price = price
        return price
    
    def __apply_seasonal_pricing(self, price):
        # Peak season multiplier
        peak_multiplier = 1.0
        
        for day in self.__get_date_range():
            if self.__is_peak_season(day):
                peak_multiplier = 1.3
                break
        
        return price * peak_multiplier
    
    def __apply_discounts(self, price):
        # Early bird, loyalty, group discounts
        discount = 0
        
        if self.is_early_booking():
            discount += 0.10  # 10% off
        
        if self.__is_loyalty_member():
            discount += 0.05  # 5% off
        
        if self.num_nights >= 7:
            discount += 0.15  # Long stay
        
        return price * (1 - discount)
    
    def __apply_taxes(self, price):
        # Add GST/taxes
        return price * 1.18  # 18% tax
    
    def __get_date_range(self):
        current = self.check_in
        while current < self.check_out:
            yield current
            current += timedelta(days=1)

class BookingService:
    def __init__(self):
        self.hotels = {}
        self.bookings = {}
        self.lock = threading.RLock()
        self.CANCELLATION_WINDOW = 48  # hours
    
    def search_hotels(self, location, check_in, check_out, guests):
        """Search available hotels"""
        # Query database with caching
        hotels = self.__query_hotels(location)
        
        # Filter by availability
        available = []
        for hotel in hotels:
            available_rooms = self.__get_available_rooms(
                hotel, check_in, check_out, guests)
            
            if available_rooms:
                available.append({
                    "hotel": hotel,
                    "available_rooms": available_rooms,
                    "price_range": self.__calculate_price_range(available_rooms)
                })
        
        # Sort by rating/price
        return sorted(available, key=lambda x: x["price_range"]["min"])
    
    def __get_available_rooms(self, hotel, check_in, check_out, guests):
        """Get available rooms for date range"""
        available = []
        
        for room in hotel.rooms.values():
            if (room.capacity >= guests and 
                room.is_available(check_in, check_out)):
                available.append(room)
        
        return available
    
    def book_room(self, user_id, room_id, check_in, check_out, guests):
        """Create booking"""
        with self.lock:
            room = get_room(room_id)
            
            # Verify still available
            if not room.is_available(check_in, check_out):
                return None, "Room not available"
            
            # Create booking
            booking = Booking(
                generate_booking_id(),
                user_id,
                room_id,
                check_in,
                check_out
            )
            
            # Calculate price
            booking.calculate_price()
            
            # Add to tentative bookings
            room.bookings.append(booking)
            self.bookings[booking.booking_id] = booking
            
            # Set 15-minute hold
            self.__schedule_hold_release(booking, 900)
            
            return booking, "Booking created"
    
    def confirm_booking(self, booking_id, payment_info):
        """Confirm booking after payment"""
        with self.lock:
            booking = self.bookings.get(booking_id)
            
            if not booking:
                return False, "Booking not found"
            
            if booking.status != "PENDING":
                return False, "Invalid booking status"
            
            # Process payment
            payment_result = self.__process_payment(booking, payment_info)
            
            if not payment_result["success"]:
                # Release hold
                self.__release_hold(booking)
                return False, payment_result["error"]
            
            # Confirm booking
            booking.status = "CONFIRMED"
            
            # Send confirmation
            self.__send_confirmation(booking)
            
            return True, "Booking confirmed"
    
    def cancel_booking(self, booking_id, user_id):
        """Cancel booking with refund"""
        with self.lock:
            booking = self.bookings.get(booking_id)
            
            if not booking or booking.user_id != user_id:
                return False, "Invalid booking"
            
            if booking.status != "CONFIRMED":
                return False, "Cannot cancel"
            
            # Calculate refund
            hours_before = (booking.check_in - datetime.now()).total_seconds() / 3600
            
            if hours_before >= 48:
                refund_amount = booking.total_price  # Full refund
            elif hours_before >= 24:
                refund_amount = booking.total_price * 0.5  # 50% refund
            else:
                refund_amount = 0  # No refund (too late)
            
            # Process refund
            if refund_amount > 0:
                self.__process_refund(booking, refund_amount)
            
            # Mark cancelled
            booking.status = "CANCELLED"
            
            return True, f"Cancelled. Refund: ${refund_amount}"
    
    def __schedule_hold_release(self, booking, timeout_seconds):
        """Release holding after timeout"""
        def release():
            time.sleep(timeout_seconds)
            with self.lock:
                if booking.status == "PENDING":
                    self.__release_hold(booking)
        
        thread = threading.Thread(target=release, daemon=True)
        thread.start()
    
    def __release_hold(self, booking):
        room = get_room(booking.room_id)
        room.bookings.remove(booking)
    
    def __process_payment(self, booking, payment_info):
        try:
            result = payment_gateway.charge(
                amount=booking.total_price,
                currency="USD",
                payment_info=payment_info
            )
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def __process_refund(self, booking, amount):
        payment_gateway.refund(
            booking_id=booking.booking_id,
            amount=amount
        )
    
    def __send_confirmation(self, booking):
        notification_service.send_email(
            to=get_user(booking.user_id).email,
            template="booking_confirmation",
            data=booking
        )
```

## Database Schema

```sql
CREATE TABLE hotels (
    hotel_id INT PRIMARY KEY,
    name VARCHAR(255),
    location VARCHAR(255),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    rating DECIMAL(2, 1),
    created_at TIMESTAMP
);

CREATE TABLE room_types (
    room_type_id INT PRIMARY KEY,
    hotel_id INT,
    room_type VARCHAR(50),
    capacity INT,
    base_price INT,
    FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id)
);

CREATE TABLE rooms (
    room_id INT PRIMARY KEY,
    hotel_id INT,
    room_type_id INT,
    room_number VARCHAR(10),
    floor INT,
    FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id),
    FOREIGN KEY (room_type_id) REFERENCES room_types(room_type_id)
);

CREATE TABLE bookings (
    booking_id INT PRIMARY KEY,
    user_id INT,
    room_id INT,
    check_in DATE,
    check_out DATE,
    total_price INT,
    status VARCHAR(20),
    created_at TIMESTAMP,
    confirmed_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (room_id) REFERENCES rooms(room_id),
    INDEX idx_user_status (user_id, status),
    INDEX idx_room_date (room_id, check_in, check_out)
);

CREATE TABLE payments (
    payment_id INT PRIMARY KEY,
    booking_id INT,
    amount INT,
    currency VARCHAR(3),
    status VARCHAR(20),
    processed_at TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id)
);
```

## Caching Strategy

```python
class CacheService:
    def __init__(self):
        self.redis = Redis()
    
    def get_hotels_in_location(self, location):
        cache_key = f"hotels:{location}"
        
        # Try cache
        cached = self.redis.get(cache_key)
        if cached:
            return json.loads(cached)
        
        # Query database
        hotels = database.query_hotels(location)
        
        # Cache for 1 hour
        self.redis.setex(cache_key, 3600, json.dumps(hotels))
        
        return hotels
    
    def check_availability(self, room_id, check_in, check_out):
        cache_key = f"availability:{room_id}:{check_in}:{check_out}"
        
        # Cache for 5 minutes (availability changes)
        # Short TTL because availability dynamic
        result = self.redis.get(cache_key)
        if result:
            return json.loads(result)
        
        available = database.check_availability(room_id, check_in, check_out)
        self.redis.setex(cache_key, 300, json.dumps(available))
        
        return available
```

## Scalability

1. **Database**: Sharding by location/hotel
2. **Cache**: Redis for searches, availability
3. **Queue**: Booking confirmation async
4. **CDN**: Hotel images/static content
5. **Load Balancer**: Distribute requests

## Key Design Decisions

| Factor | Decision | Reason |
|--------|----------|--------|
| **Hold timeout** | 15 minutes | Enough to pay, prevents stuck bookings |
| **Cancellation policy** | Time-based | Incentivize bookings |
| **Lock scope** | Per room | Avoid global lock |
| **Price calculation** | Compute on demand | Dynamic pricing |
| **Availability cache** | 5 minute TTL | Balance freshness vs performance |

## Key Interview Questions

1. **Handle 1M concurrent searches?**
   - Caching, read replicas, CDN, sharding

2. **Prevent double-booking?**
   - Locks, atomic operations, optimistic locking

3. **Dynamic pricing?**
   - Seasonal, demand-based, early-bird discounts

4. **Handle payment failures?**
   - Retry logic, timeout, release hold, notify user

5. **Timezone handling?**
   - Store UTC, convert on client side
