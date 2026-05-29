# Movie Ticket Booking System

## Requirements

### Functional
- Search movies/shows
- Reserve seats
- Process payments
- Show confirmation
- Email receipt
- Cancel/refund booking

### Non-Functional
- Handle high concurrency (peak movie times)
- Show availability in real-time
- No double-bookings
- Process payment in < 5 seconds
- 99.9% uptime

## System Architecture

```
Frontend                API Server           Database
(Web/App)              (Booking Logic)       (Seats/Movies)
   |                        |                     |
   |--search movies-------->|--query---->|
   |<--list movies----------|<--results--|
   |                        |                     |
   |--select show--------->|                     |
   |<--available seats------|<--query---->|
   |                        |                     |
   |--book seats--------->|--reserve---->|
   |                        |--lock seats |
   |                        |             |
   |--payment-------->|--        |
   |        (payment gateway)    |
   |                        |--write---->|
   |<--confirmation--------|                     |
```

## Core Classes

```python
class Movie:
    def __init__(self, movie_id, title, duration, rating):
        self.movie_id = movie_id
        self.title = title
        self.duration = duration  # minutes
        self.rating = rating
        self.shows = []  # List of shows

class Show:
    def __init__(self, show_id, movie_id, screen_id, start_time, end_time):
        self.show_id = show_id
        self.movie_id = movie_id
        self.screen_id = screen_id
        self.start_time = start_time
        self.end_time = end_time
        self.seats = None  # SeatLayout

class SeatLayout:
    def __init__(self, show_id, rows=10, cols=15):
        self.show_id = show_id
        self.rows = rows
        self.cols = cols
        self.seats = {}  # {(row, col): Seat}
        self.__initialize_seats()
    
    def __initialize_seats(self):
        for row in range(self.rows):
            for col in range(self.cols):
                seat = Seat(row, col)
                self.seats[(row, col)] = seat
    
    def get_available_seats(self):
        return [seat for seat in self.seats.values() 
                if seat.status == "AVAILABLE"]
    
    def reserve_seats(self, seats_to_reserve):
        """Try to reserve seats - atomic operation"""
        for seat in seats_to_reserve:
            if seat.status != "AVAILABLE":
                return False
        
        # All available - reserve all
        for seat in seats_to_reserve:
            seat.status = "RESERVED"
        
        return True
    
    def confirm_booking(self, seats):
        for seat in seats:
            seat.status = "BOOKED"
    
    def cancel_booking(self, seats):
        for seat in seats:
            seat.status = "AVAILABLE"

class Seat:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.status = "AVAILABLE"  # AVAILABLE, RESERVED, BOOKED
        self.seat_type = self.__determine_type(row, col)
    
    def __determine_type(self, row, col):
        if row in [0, 1]:
            return "PREMIUM"
        elif row in [8, 9]:
            return "ECONOMY"
        else:
            return "STANDARD"
    
    def get_price(self):
        prices = {
            "PREMIUM": 200,
            "STANDARD": 150,
            "ECONOMY": 100
        }
        return prices[self.seat_type]

class Booking:
    def __init__(self, booking_id, user_id, show_id, seats):
        self.booking_id = booking_id
        self.user_id = user_id
        self.show_id = show_id
        self.seats = seats
        self.total_price = sum(seat.get_price() for seat in seats)
        self.status = "PENDING"  # PENDING, CONFIRMED, CANCELLED
        self.booking_time = time.time()
        self.confirmation_time = None
    
    def confirm(self):
        self.status = "CONFIRMED"
        self.confirmation_time = time.time()
    
    def cancel(self):
        self.status = "CANCELLED"

class BookingService:
    def __init__(self):
        self.movies = {}
        self.shows = {}
        self.bookings = {}
        self.seat_layouts = {}
        self.lock = threading.RLock()
        self.SEAT_HOLD_TIME = 300  # 5 minutes
    
    def search_movies(self, date, city):
        """Search available movies"""
        # Query database
        return self.__query_movies(date, city)
    
    def get_shows(self, movie_id, date):
        """Get shows for movie on date"""
        return [show for show in self.shows.values()
                if show.movie_id == movie_id and show.date == date]
    
    def get_available_seats(self, show_id):
        """Get available seats for show"""
        with self.lock:
            layout = self.seat_layouts[show_id]
            return layout.get_available_seats()
    
    def reserve_seats(self, show_id, seat_positions, user_id):
        """
        Reserve seats with timeout
        User has SEAT_HOLD_TIME to complete payment
        """
        with self.lock:
            layout = self.seat_layouts[show_id]
            seats = [layout.seats[pos] for pos in seat_positions]
            
            # Check all available
            if not all(s.status == "AVAILABLE" for s in seats):
                return None, "Seats not available"
            
            # Reserve all
            if not layout.reserve_seats(seats):
                return None, "Could not reserve all seats"
            
            # Create booking
            booking = Booking(
                generate_booking_id(),
                user_id,
                show_id,
                seats
            )
            
            self.bookings[booking.booking_id] = booking
            
            # Start timeout timer
            self.__schedule_timeout(booking.booking_id, self.SEAT_HOLD_TIME)
            
            return booking, "Seats reserved"
    
    def confirm_booking(self, booking_id, payment_info):
        """Confirm booking after payment"""
        with self.lock:
            booking = self.bookings.get(booking_id)
            
            if not booking:
                return False, "Booking not found"
            
            if booking.status != "PENDING":
                return False, "Booking already processed"
            
            # Process payment
            payment_result = self.__process_payment(booking, payment_info)
            
            if not payment_result["success"]:
                return False, payment_result["message"]
            
            # Confirm with seat layout
            layout = self.seat_layouts[booking.show_id]
            layout.confirm_booking(booking.seats)
            
            # Confirm booking
            booking.confirm()
            
            # Cancel timeout
            self.__cancel_timeout(booking_id)
            
            # Send confirmation
            self.__send_confirmation_email(booking)
            
            return True, f"Booking confirmed: {booking_id}"
    
    def cancel_booking(self, booking_id):
        """Cancel booking and refund"""
        with self.lock:
            booking = self.bookings.get(booking_id)
            
            if not booking or booking.status == "CANCELLED":
                return False, "Invalid booking"
            
            # Release seats
            layout = self.seat_layouts[booking.show_id]
            layout.cancel_booking(booking.seats)
            
            # Mark as cancelled
            booking.cancel()
            
            # Process refund
            self.__process_refund(booking)
            
            return True, "Booking cancelled"
    
    def __schedule_timeout(self, booking_id, timeout_seconds):
        """Release seats if payment not completed"""
        def timeout_handler():
            time.sleep(timeout_seconds)
            with self.lock:
                booking = self.bookings.get(booking_id)
                if booking and booking.status == "PENDING":
                    # Release seats
                    layout = self.seat_layouts[booking.show_id]
                    layout.cancel_booking(booking.seats)
        
        thread = threading.Thread(target=timeout_handler, daemon=True)
        thread.start()
    
    def __process_payment(self, booking, payment_info):
        """Call payment gateway"""
        try:
            result = payment_gateway.charge(
                amount=booking.total_price,
                card=payment_info["card"],
                user_id=booking.user_id
            )
            return result
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def __process_refund(self, booking):
        """Refund payment"""
        payment_gateway.refund(booking_id=booking.booking_id)
    
    def __send_confirmation_email(self, booking):
        """Send confirmation to user"""
        # Email service
        pass
    
    def __cancel_timeout(self, booking_id):
        """Cancel pending timeout"""
        pass
```

## Concurrency Handling

### Problem: Race Condition
```
Thread 1: Check seat available? YES
Thread 2: Check seat available? YES
Thread 1: Reserve seat
Thread 2: Reserve seat  <- DOUBLE BOOKED!
```

### Solution: Locks

```python
def reserve_seats_safe(show_id, seats):
    with lock:  # One thread at a time
        # Check
        for seat in seats:
            if seat.status != "AVAILABLE":
                return False
        
        # Reserve - all or nothing
        for seat in seats:
            seat.status = "RESERVED"
        
        return True
```

### Alternative: Optimistic Locking

```python
class Seat:
    def __init__(self):
        self.status = "AVAILABLE"
        self.version = 0

def reserve_seats_optimistic(show_id, seats_with_versions):
    # Read versions
    versions = {s: s.version for s in seats}
    
    # Do local processing
    
    # Atomic update
    with lock:
        for seat in seats:
            if seat.version != versions[seat]:
                return False  # Version changed!
        
        # All versions match - reserve
        for seat in seats:
            seat.status = "RESERVED"
            seat.version += 1
    
    return True
```

## Database Schema

```sql
CREATE TABLE movies (
    movie_id INT PRIMARY KEY,
    title VARCHAR(100),
    duration INT,
    rating VARCHAR(10)
);

CREATE TABLE shows (
    show_id INT PRIMARY KEY,
    movie_id INT,
    screen_id INT,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
);

CREATE TABLE seats (
    seat_id INT PRIMARY KEY,
    show_id INT,
    row_num INT,
    col_num INT,
    seat_type VARCHAR(20),
    price INT,
    status VARCHAR(20),  -- AVAILABLE, RESERVED, BOOKED
    FOREIGN KEY (show_id) REFERENCES shows(show_id)
);

CREATE TABLE bookings (
    booking_id INT PRIMARY KEY,
    user_id INT,
    show_id INT,
    total_price INT,
    status VARCHAR(20),
    created_at TIMESTAMP,
    confirmed_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (show_id) REFERENCES shows(show_id)
);

CREATE TABLE booking_seats (
    booking_id INT,
    seat_id INT,
    PRIMARY KEY (booking_id, seat_id),
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id),
    FOREIGN KEY (seat_id) REFERENCES seats(seat_id)
);
```

## Key Design Decisions

| Decision | Reason |
|----------|--------|
| **Seat hold timeout** | Prevent stuck reservations |
| **Lock per show** | Avoid global lock bottleneck |
| **Atomic reserve** | Prevent double-booking |
| **Payment async gateway** | External service |
| **Email async** | Decouple confirmation |

## Scalability Improvements

1. **Cache**: Redis for show availability
2. **Database**: Sharding by city/cinema
3. **Queue**: Message queue for bookings
4. **CDN**: Static content delivery
5. **Load Balancer**: Distribute requests

## Key Interview Questions

1. **How to prevent double-booking?**
   - Atomic operations, locks, pessimistic locking

2. **Payment integration?**
   - Third-party gateway, handle failures/retries

3. **Peak load (movie release day)?**
   - Scale horizontally, cache, queue requests

4. **Handle seat hold timeout?**
   - Background job, release after 5 minutes

5. **Time zone handling?**
   - Store as UTC, convert on display
