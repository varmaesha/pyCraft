# Ride Sharing System Design (Uber/Lyft)

## Requirements

### Functional
- Rider requests ride
- Find nearby drivers
- Match rider-driver
- Real-time tracking
- Payment processing
- Rating system
- Surge pricing

### Non-Functional
- Match in < 30 seconds
- Real-time location updates
- Support 1M concurrent users
- 99.9% uptime
- Handle rush hours

## System Architecture

```
Rider App              Backend Services          Database
   |                        |                        |
Request Ride -------> Matching Service -------> Ride DB
   |                   Location Service         Driver DB
   |                   Pricing Service          User DB
   |<--Driver Location--Tracking Service
   |                        |
   |                   Payment Service
   |
Driver App
   |
Accept Request
   |
Update Location
   |
Complete Ride
```

## Core Classes

```python
class Location:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
    
    def distance_to(self, other):
        """Haversine distance in km"""
        from math import radians, cos, sin, asin, sqrt
        
        lon1, lat1, lon2, lat2 = map(radians, 
            [self.longitude, self.latitude, other.longitude, other.latitude])
        
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        
        return c * 6371  # Earth's radius in km

class Rider:
    def __init__(self, rider_id, name, phone):
        self.rider_id = rider_id
        self.name = name
        self.phone = phone
        self.current_location = None
        self.rating = 5.0
        self.total_rides = 0
        self.payment_method = None

class Driver:
    def __init__(self, driver_id, name, phone, vehicle):
        self.driver_id = driver_id
        self.name = name
        self.phone = phone
        self.vehicle = vehicle  # {model, color, plate}
        self.current_location = None
        self.is_available = False
        self.current_ride_id = None
        self.rating = 5.0
        self.total_rides = 0
        self.earnings = 0

class Ride:
    def __init__(self, ride_id, rider_id, pickup, dropoff):
        self.ride_id = ride_id
        self.rider_id = rider_id
        self.driver_id = None
        self.pickup_location = pickup
        self.dropoff_location = dropoff
        self.status = "REQUESTED"  # REQUESTED, ACCEPTED, IN_PROGRESS, COMPLETED, CANCELLED
        self.requested_at = datetime.now()
        self.accepted_at = None
        self.picked_up_at = None
        self.completed_at = None
        self.estimated_fare = 0
        self.actual_fare = 0
        self.distance_km = 0
        self.duration_minutes = 0
        self.route = []  # GPS coordinates

class RideMatchingService:
    def __init__(self):
        self.rides = {}
        self.drivers = {}
        self.active_drivers = {}  # {location_grid: [driver_ids]}
        self.lock = threading.RLock()
        self.MATCH_TIMEOUT = 30  # seconds
    
    def request_ride(self, rider_id, pickup, dropoff):
        """Rider requests ride"""
        with self.lock:
            # Validate rider
            rider = get_rider(rider_id)
            if not rider:
                return None, "Invalid rider"
            
            # Create ride
            ride = Ride(
                generate_ride_id(),
                rider_id,
                pickup,
                dropoff
            )
            
            # Calculate estimated fare
            distance = pickup.distance_to(dropoff)
            ride.distance_km = distance
            ride.estimated_fare = self.__calculate_fare(distance)
            
            self.rides[ride.ride_id] = ride
            
            # Match asynchronously
            self.__match_ride_async(ride)
            
            return ride, "Ride requested"
    
    def __match_ride_async(self, ride):
        """Find driver for ride"""
        def match():
            start_time = time.time()
            
            while time.time() - start_time < self.MATCH_TIMEOUT:
                with self.lock:
                    driver = self.__find_best_driver(ride)
                    
                    if driver:
                        # Send to driver
                        result = self.__send_to_driver(ride, driver)
                        
                        if result:
                            ride.driver_id = driver.driver_id
                            return
                
                time.sleep(1)  # Retry every second
            
            # Timeout - inform rider
            notification_service.notify(ride.rider_id,
                                       f"No drivers available for {ride.ride_id}")
        
        thread = threading.Thread(target=match, daemon=True)
        thread.start()
    
    def __find_best_driver(self, ride):
        """Find nearby available driver"""
        # Get nearby drivers using geospatial index
        nearby_drivers = self.__query_nearby_drivers(
            ride.pickup_location,
            radius_km=5
        )
        
        # Filter available
        available = [d for d in nearby_drivers if d.is_available]
        
        if not available:
            return None
        
        # Score drivers
        scores = []
        for driver in available:
            distance = ride.pickup_location.distance_to(driver.current_location)
            rating = driver.rating
            
            # Score: distance (lower better) vs rating (higher better)
            score = distance / rating
            
            scores.append((driver, score))
        
        # Return best match
        return min(scores, key=lambda x: x[1])[0]
    
    def __send_to_driver(self, ride, driver):
        """Send ride offer to driver"""
        try:
            # Send notification
            response = notification_service.notify_driver_for_offer(
                driver.driver_id,
                ride_id=ride.ride_id,
                pickup=ride.pickup_location,
                estimated_fare=ride.estimated_fare,
                timeout=15  # Driver has 15 seconds to accept
            )
            
            return response["accepted"]
        
        except Exception:
            return False
    
    def driver_accept_ride(self, driver_id, ride_id):
        """Driver accepts ride"""
        with self.lock:
            ride = self.rides.get(ride_id)
            driver = get_driver(driver_id)
            
            if not ride or ride.status != "REQUESTED":
                return False, "Invalid ride"
            
            if driver.current_ride_id:
                return False, "Driver already on ride"
            
            # Assign
            ride.driver_id = driver_id
            ride.status = "ACCEPTED"
            ride.accepted_at = datetime.now()
            
            driver.current_ride_id = ride_id
            driver.is_available = False
            
            # Notify rider
            notification_service.notify(ride.rider_id,
                                       f"Driver {driver.name} accepted")
            
            return True, "Ride accepted"
    
    def driver_location_update(self, driver_id, location):
        """Update driver location"""
        with self.lock:
            driver = get_driver(driver_id)
            driver.current_location = location
            
            # If on ride, update route
            if driver.current_ride_id:
                ride = self.rides[driver.current_ride_id]
                ride.route.append(location)
                
                # Notify rider of location
                notification_service.notify_rider_location(
                    ride.rider_id,
                    location
                )
    
    def start_ride(self, driver_id, ride_id):
        """Driver picked up rider"""
        with self.lock:
            ride = self.rides.get(ride_id)
            
            if ride.driver_id != driver_id:
                return False
            
            ride.status = "IN_PROGRESS"
            ride.picked_up_at = datetime.now()
            
            notification_service.notify(ride.rider_id, "Ride started")
            
            return True
    
    def complete_ride(self, driver_id, ride_id):
        """Complete ride"""
        with self.lock:
            ride = self.rides.get(ride_id)
            
            if ride.driver_id != driver_id:
                return False
            
            # Calculate actual fare
            duration = (datetime.now() - ride.picked_up_at).total_seconds() / 60
            ride.duration_minutes = duration
            ride.actual_fare = self.__calculate_fare(
                ride.distance_km,
                duration,
                ride.pickup_location,
                ride.dropoff_location
            )
            
            ride.status = "COMPLETED"
            ride.completed_at = datetime.now()
            
            # Process payment
            self.__process_payment(ride)
            
            # Free driver
            driver = get_driver(driver_id)
            driver.current_ride_id = None
            driver.is_available = True
            driver.earnings += ride.actual_fare
            
            # Update stats
            rider = get_rider(ride.rider_id)
            rider.total_rides += 1
            driver.total_rides += 1
            
            return True
    
    def __calculate_fare(self, distance_km, duration_minutes=None, 
                        pickup=None, dropoff=None):
        """Calculate ride fare"""
        # Base fare
        fare = 2.0
        
        # Distance charge
        fare += distance_km * 1.5  # $1.50/km
        
        # Time charge
        if duration_minutes:
            fare += duration_minutes * 0.25  # $0.25/minute
        
        # Surge pricing
        surge_multiplier = self.__calculate_surge(pickup, dropoff)
        fare *= surge_multiplier
        
        return round(fare, 2)
    
    def __calculate_surge(self, pickup, dropoff):
        """Calculate surge pricing multiplier"""
        # Check demand in area
        demand = self.__get_demand_level(pickup)
        
        # 1.0 = normal, 1.5 = high, 2.0+ = surge
        if demand > 100:
            return 2.0  # High surge
        elif demand > 50:
            return 1.5  # Medium surge
        else:
            return 1.0  # Normal
    
    def __get_demand_level(self, location):
        """Get ride requests in area"""
        # Count pending requests nearby
        count = 0
        for ride in self.rides.values():
            if ride.status == "REQUESTED":
                dist = location.distance_to(ride.pickup_location)
                if dist < 2:
                    count += 1
        
        return count
    
    def __process_payment(self, ride):
        rider = get_rider(ride.rider_id)
        
        result = payment_gateway.charge(
            rider.payment_method,
            ride.actual_fare
        )
        
        if result["success"]:
            ride.payment_status = "COMPLETED"
        else:
            ride.payment_status = "FAILED"
    
    def __query_nearby_drivers(self, location, radius_km):
        """Query nearby drivers using geospatial index"""
        # Use Redis geo or similar
        nearby = geo_index.radius_query(
            location.latitude,
            location.longitude,
            radius_km
        )
        
        return [get_driver(d) for d in nearby]
    
    def rate_ride(self, ride_id, user_id, rating, review):
        """Rate completed ride"""
        ride = self.rides.get(ride_id)
        
        if not ride:
            return False
        
        # Add rating
        if user_id == ride.rider_id:
            # Rider rating driver
            driver = get_driver(ride.driver_id)
            driver.rating = (driver.rating + rating) / 2
        else:
            # Driver rating rider
            rider = get_rider(ride.rider_id)
            rider.rating = (rider.rating + rating) / 2
        
        # Save review
        database.save_review({
            "ride_id": ride_id,
            "user_id": user_id,
            "rating": rating,
            "review": review
        })
        
        return True
```

## Geospatial Indexing

```python
class GeoSpatialIndex:
    def __init__(self):
        self.redis = Redis()
    
    def add_driver(self, driver_id, latitude, longitude):
        """Add driver to spatial index"""
        self.redis.geoadd(
            "drivers",
            longitude,
            latitude,
            driver_id
        )
    
    def radius_query(self, latitude, longitude, radius_km):
        """Find drivers within radius"""
        results = self.redis.georadius(
            "drivers",
            longitude,
            latitude,
            radius_km,
            unit="km"
        )
        
        return results
```

## Surge Pricing

```python
class SurgePricingService:
    def __init__(self):
        self.demand_grid = {}  # Grid-based demand tracking
    
    def calculate_multiplier(self, location):
        """Calculate surge pricing"""
        grid_cell = self.__get_grid_cell(location)
        demand = self.__get_demand_in_cell(grid_cell)
        supply = self.__get_supply_in_cell(grid_cell)
        
        if supply == 0:
            return 2.0  # Emergency surge
        
        ratio = demand / supply
        
        # 1.0 = normal, up to 3.0+ in extreme cases
        return min(3.0, 1.0 + (ratio - 1) * 0.5)
    
    def __get_grid_cell(self, location):
        """Map location to grid cell"""
        # Each cell = 1km x 1km
        return (int(location.latitude), int(location.longitude))
```

## Key Interview Questions

1. **Match rider to driver in < 30 seconds?**
   - Geospatial indexing, nearby queries, parallel matching

2. **Handle 1M concurrent rides?**
   - Sharding by city/zone, distributed matching, cache

3. **Real-time location updates?**
   - WebSocket, update every 2 seconds

4. **Surge pricing calculation?**
   - Demand/supply ratio in grid cells

5. **Driver availability management?**
   - Cache with TTL, update on location

## Important Features

- ✅ Smart matching algorithm
- ✅ Geospatial queries (Redis, PostGIS)
- ✅ Surge pricing
- ✅ Real-time tracking
- ✅ Rating/review system
- ✅ Payment integration
- ✅ Scalability by geography
