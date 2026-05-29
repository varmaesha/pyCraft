# Designing System: Parking Lot

## Requirements

### Functional Requirements
1. Display available spots
2. Park a vehicle
3. Unpark a vehicle
4. Track parking duration
5. Calculate fee (hourly/daily)
6. Support different vehicle types (car, bike, truck)
7. Support different spot types (compact, regular, large)

### Non-Functional Requirements
1. Multiple entry/exit points
2. Real-time availability
3. Efficient search for available spots
4. Scalability for large parking lots
5. High throughput during peak hours

## System Design

### 1. Level and Parking Spot Structure
```python
from enum import Enum
from datetime import datetime

class VehicleType(Enum):
    MOTORCYCLE = 1
    CAR = 2
    TRUCK = 3

class ParkingSpotType(Enum):
    COMPACT = 1
    REGULAR = 2
    LARGE = 3

class ParkingSpot:
    def __init__(self, spot_id, spot_type, level_id):
        self.spot_id = spot_id
        self.spot_type = spot_type
        self.level_id = level_id
        self.is_available = True
        self.vehicle = None
        self.entry_time = None
    
    def can_fit_vehicle(self, vehicle):
        """Check if vehicle can fit in this spot"""
        if self.spot_type == ParkingSpotType.MOTORCYCLE:
            return True
        elif self.spot_type == ParkingSpotType.COMPACT:
            return vehicle.vehicle_type in [VehicleType.MOTORCYCLE, VehicleType.CAR]
        elif self.spot_type == ParkingSpotType.REGULAR:
            return vehicle.vehicle_type in [VehicleType.MOTORCYCLE, VehicleType.CAR]
        elif self.spot_type == ParkingSpotType.LARGE:
            return True
        return False
    
    def park_vehicle(self, vehicle):
        if not self.is_available:
            raise Exception(f"Spot {self.spot_id} is not available")
        
        if not self.can_fit_vehicle(vehicle):
            raise Exception(f"Vehicle {vehicle.license_plate} cannot fit in spot {self.spot_id}")
        
        self.vehicle = vehicle
        self.is_available = False
        self.entry_time = datetime.now()
    
    def unpark_vehicle(self):
        if self.is_available:
            raise Exception(f"Spot {self.spot_id} is already empty")
        
        self.vehicle = None
        self.is_available = True
        self.entry_time = None

class ParkingLevel:
    def __init__(self, level_id, num_spots):
        self.level_id = level_id
        self.spots = {}
        self._create_spots(num_spots)
    
    def _create_spots(self, num_spots):
        """Create varied spot types"""
        for i in range(num_spots):
            if i < num_spots * 0.2:
                spot_type = ParkingSpotType.MOTORCYCLE
            elif i < num_spots * 0.6:
                spot_type = ParkingSpotType.CAR
            else:
                spot_type = ParkingSpotType.TRUCK
            
            self.spots[f"L{self.level_id}S{i+1}"] = ParkingSpot(
                f"L{self.level_id}S{i+1}",
                spot_type,
                self.level_id
            )
    
    def find_available_spot(self, vehicle):
        """Find first available spot for vehicle"""
        for spot in self.spots.values():
            if spot.is_available and spot.can_fit_vehicle(vehicle):
                return spot
        return None
    
    def get_available_count(self):
        return sum(1 for spot in self.spots.values() if spot.is_available)
```

### 2. Vehicle and Ticket
```python
class Vehicle:
    def __init__(self, license_plate, vehicle_type):
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type
    
    def __str__(self):
        return f"{self.vehicle_type.name}({self.license_plate})"

class Ticket:
    def __init__(self, ticket_id, vehicle, spot, entry_time):
        self.ticket_id = ticket_id
        self.vehicle = vehicle
        self.spot = spot
        self.entry_time = entry_time
        self.exit_time = None
        self.is_paid = False
    
    def mark_exit(self):
        self.exit_time = datetime.now()
    
    def get_duration_hours(self):
        if not self.exit_time:
            return 0
        duration = self.exit_time - self.entry_time
        return duration.total_seconds() / 3600
```

### 3. Parking Rate Calculator
```python
class ParkingRate:
    def __init__(self, vehicle_type, hourly_rate, daily_rate=None):
        self.vehicle_type = vehicle_type
        self.hourly_rate = hourly_rate
        self.daily_rate = daily_rate or hourly_rate * 24
    
    def calculate_fee(self, duration_hours):
        """Calculate parking fee based on duration"""
        full_days = int(duration_hours // 24)
        remaining_hours = duration_hours % 24
        
        fee = full_days * self.daily_rate
        if remaining_hours > 0:
            fee += remaining_hours * self.hourly_rate
        
        return fee

class RateCalculator:
    def __init__(self):
        self.rates = {
            VehicleType.MOTORCYCLE: ParkingRate(VehicleType.MOTORCYCLE, 2.0, 10.0),
            VehicleType.CAR: ParkingRate(VehicleType.CAR, 3.0, 15.0),
            VehicleType.TRUCK: ParkingRate(VehicleType.TRUCK, 5.0, 25.0)
        }
    
    def calculate_fee(self, vehicle, duration_hours):
        rate = self.rates[vehicle.vehicle_type]
        return rate.calculate_fee(duration_hours)
```

### 4. Parking Lot
```python
class ParkingLot:
    _instance = None  # Singleton
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, capacity_per_level=100, num_levels=5):
        if not hasattr(self, 'levels'):  # Initialize only once
            self.levels = {}
            self.tickets = {}
            self.rate_calculator = RateCalculator()
            self.ticket_counter = 0
            
            for level in range(1, num_levels + 1):
                self.levels[level] = ParkingLevel(level, capacity_per_level)
    
    def park_vehicle(self, vehicle):
        """Park a vehicle and return ticket"""
        spot = self._find_available_spot(vehicle)
        
        if not spot:
            raise Exception("No available spots for this vehicle type")
        
        spot.park_vehicle(vehicle)
        self.ticket_counter += 1
        ticket = Ticket(f"T{self.ticket_counter}", vehicle, spot, datetime.now())
        self.tickets[ticket.ticket_id] = ticket
        
        return ticket
    
    def unpark_vehicle(self, ticket_id):
        """Unpark vehicle and calculate fee"""
        if ticket_id not in self.tickets:
            raise Exception(f"Invalid ticket: {ticket_id}")
        
        ticket = self.tickets[ticket_id]
        ticket.mark_exit()
        
        # Calculate fee
        duration = ticket.get_duration_hours()
        fee = self.rate_calculator.calculate_fee(ticket.vehicle, duration)
        
        # Unpark from spot
        ticket.spot.unpark_vehicle()
        
        return {
            "ticket_id": ticket_id,
            "vehicle": str(ticket.vehicle),
            "duration_hours": round(duration, 2),
            "fee": round(fee, 2)
        }
    
    def _find_available_spot(self, vehicle):
        """Search for available spot across all levels"""
        for level in self.levels.values():
            spot = level.find_available_spot(vehicle)
            if spot:
                return spot
        return None
    
    def get_availability(self):
        """Get parking lot status"""
        availability = {}
        total = 0
        available = 0
        
        for level_id, level in self.levels.items():
            level_avail = level.get_available_count()
            level_total = len(level.spots)
            availability[f"Level {level_id}"] = f"{level_avail}/{level_total}"
            total += level_total
            available += level_avail
        
        availability["Overall"] = f"{available}/{total}"
        return availability
```

### 5. Entry and Exit Gates
```python
class EntryGate:
    def __init__(self, gate_id, parking_lot):
        self.gate_id = gate_id
        self.parking_lot = parking_lot
    
    def issue_ticket(self, vehicle_type, license_plate):
        vehicle = Vehicle(license_plate, vehicle_type)
        try:
            ticket = self.parking_lot.park_vehicle(vehicle)
            print(f"Gate {self.gate_id}: Vehicle {license_plate} parked at {ticket.spot.spot_id}")
            return ticket
        except Exception as e:
            print(f"Gate {self.gate_id}: Parking failed - {e}")
            return None

class ExitGate:
    def __init__(self, gate_id, parking_lot):
        self.gate_id = gate_id
        self.parking_lot = parking_lot
    
    def process_exit(self, ticket_id):
        try:
            result = self.parking_lot.unpark_vehicle(ticket_id)
            print(f"Gate {self.gate_id}: Vehicle {result['vehicle']} exiting")
            print(f"Duration: {result['duration_hours']} hours, Fee: ${result['fee']}")
            return result
        except Exception as e:
            print(f"Gate {self.gate_id}: Exit failed - {e}")
            return None
```

## Usage Example

```python
# Setup parking lot
parking_lot = ParkingLot(capacity_per_level=50, num_levels=3)

# Create gates
entry = EntryGate("ENTRY-1", parking_lot)
exit_gate = ExitGate("EXIT-1", parking_lot)

# Park vehicles
ticket1 = entry.issue_ticket(VehicleType.CAR, "ABC123")
ticket2 = entry.issue_ticket(VehicleType.TRUCK, "XYZ789")
ticket3 = entry.issue_ticket(VehicleType.MOTORCYCLE, "BIKE01")

# Check availability
print(parking_lot.get_availability())

# Process exits
exit_gate.process_exit(ticket1.ticket_id)
exit_gate.process_exit(ticket2.ticket_id)
```

## Design Patterns Used

1. **Singleton**: ParkingLot (single instance)
2. **Strategy**: Rate calculation (different vehicle types)
3. **Factory**: Vehicle creation

## Scalability Considerations

1. **Database**: Store tickets, vehicles, transactions
2. **Caching**: Cache available spots per level
3. **Message Queue**: Process exits asynchronously
4. **Load Balancing**: Multiple entry/exit gates
5. **Real-time Updates**: WebSocket for availability
