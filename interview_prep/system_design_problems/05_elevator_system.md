# Elevator System Design

## Requirements

### Functional
- Multiple floors (30+)
- Multiple elevators (3-10)
- Passengers request floor
- Shows current floor
- Doors open/close
- Track occupied passengers

### Non-Functional
- Minimize wait time
- Optimal floor scheduling
- Handle peak hours
- Service all requests fairly

## System Architecture

```
     Floor Buttons (1-30)
            |
     Elevator Controller
            |
    ________+________
    |        |        |
  Elev1    Elev2    Elev3
```

## Core Classes

```python
class Floor:
    def __init__(self, floor_number):
        self.floor_number = floor_number
        self.up_button_pressed = False
        self.down_button_pressed = False

class Elevator:
    def __init__(self, elevator_id, total_floors):
        self.elevator_id = elevator_id
        self.current_floor = 1
        self.destination_floors = []  # Ordered list
        self.passengers_count = 0
        self.max_capacity = 10
        self.door_open = False
        self.direction = "IDLE"  # UP, DOWN, IDLE
    
    def add_destination(self, floor):
        if floor not in self.destination_floors:
            self.destination_floors.append(floor)
            self.__sort_destinations()
    
    def __sort_destinations(self):
        # Optimize elevator path
        if self.direction == "UP":
            self.destination_floors.sort()
        elif self.direction == "DOWN":
            self.destination_floors.sort(reverse=True)
    
    def move_to_next_floor(self):
        if not self.destination_floors:
            self.direction = "IDLE"
            return
        
        next_floor = self.destination_floors[0]
        
        if next_floor > self.current_floor:
            self.direction = "UP"
            self.current_floor += 1
        elif next_floor < self.current_floor:
            self.direction = "DOWN"
            self.current_floor -= 1
        else:
            # Arrived
            self.__open_door()
            self.destination_floors.pop(0)
            return True
        
        return False
    
    def __open_door(self):
        self.door_open = True
        # Simulate opening: 3 seconds
        # then close
        self.door_open = False
    
    def can_board_passenger(self):
        return self.passengers_count < self.max_capacity and self.door_open
    
    def board_passenger(self):
        if self.can_board_passenger():
            self.passengers_count += 1
            return True
        return False
    
    def unboard_passenger(self):
        if self.passengers_count > 0:
            self.passengers_count -= 1
            return True
        return False

class ElevatorController:
    def __init__(self, num_elevators, num_floors):
        self.elevators = [Elevator(i, num_floors) for i in range(num_elevators)]
        self.num_floors = num_floors
        self.floors = [Floor(i) for i in range(1, num_floors + 1)]
        self.request_queue = []
    
    def request_elevator(self, floor, direction):
        # Add to request queue
        self.request_queue.append({
            "floor": floor,
            "direction": direction,
            "timestamp": time.time()
        })
        
        # Find best elevator
        best_elevator = self.__find_best_elevator(floor, direction)
        return best_elevator
    
    def __find_best_elevator(self, floor, direction):
        # SCAN Algorithm: minimize wait time
        
        best_elevator = None
        min_wait = float('inf')
        
        for elevator in self.elevators:
            # Skip if full
            if elevator.passengers_count >= elevator.max_capacity:
                continue
            
            # Calculate wait time
            wait_time = self.__calculate_wait(elevator, floor, direction)
            
            if wait_time < min_wait:
                min_wait = wait_time
                best_elevator = elevator
        
        if best_elevator:
            best_elevator.add_destination(floor)
        
        return best_elevator
    
    def __calculate_wait(self, elevator, requested_floor, direction):
        # Estimate wait time
        distance = abs(elevator.current_floor - requested_floor)
        
        # Penalize if moving opposite direction
        if elevator.direction == "UP" and direction == "DOWN":
            distance += len(elevator.destination_floors)
        elif elevator.direction == "DOWN" and direction == "UP":
            distance += len(elevator.destination_floors)
        
        return distance
    
    def simulate_step(self):
        """Simulate one time unit"""
        for elevator in self.elevators:
            if elevator.current_floor == 1 and elevator.direction == "DOWN":
                elevator.direction = "UP"
            elif elevator.current_floor == self.num_floors and elevator.direction == "UP":
                elevator.direction = "DOWN"
            
            elevator.move_to_next_floor()
    
    def get_elevator_status(self):
        status = []
        for elev in self.elevators:
            status.append({
                "id": elev.elevator_id,
                "current_floor": elev.current_floor,
                "direction": elev.direction,
                "passengers": elev.passengers_count,
                "destinations": elev.destination_floors
            })
        return status

class Request:
    def __init__(self, user_id, source_floor, destination_floor):
        self.user_id = user_id
        self.source_floor = source_floor
        self.destination_floor = destination_floor
        self.state = "WAITING"  # WAITING, IN_ELEVATOR, COMPLETED
        self.timestamp = time.time()
```

## Scheduling Algorithms

### Algorithm 1: SCAN (Elevator Algorithm)
```python
def scan_algorithm(floor, direction):
    """
    Go in current direction until end,
    then reverse direction
    """
    for elevator in elevators:
        if elevator.direction == direction or elevator.direction == "IDLE":
            candidates.append(elevator)
    
    # Pick closest in current direction
    return min(candidates, key=lambda e: abs(e.current_floor - floor))
```

### Algorithm 2: LOOK (Better SCAN)
```python
def look_algorithm(floor, direction):
    """
    Only go to nearest request in direction,
    then reverse
    """
    active_elevators = [e for e in elevators if e.destination_floors]
    
    # If no destinations, go to nearest request
    if not active_elevators:
        return min(elevators, key=lambda e: abs(e.current_floor - floor))
    
    # Pick elevator that minimizes additional distance
    return min(active_elevators, key=lambda e: calculate_distance(e, floor))
```

### Algorithm 3: Nearest Call
```python
def nearest_call(floor, direction):
    """Assign to nearest idle or lightly loaded elevator"""
    
    # Prefer idle elevators
    idle = [e for e in elevators if e.direction == "IDLE"]
    if idle:
        return min(idle, key=lambda e: abs(e.current_floor - floor))
    
    # Otherwise choose by distance and load
    scores = []
    for e in elevators:
        distance = abs(e.current_floor - floor)
        load = e.passengers_count / e.max_capacity
        score = distance + (load * 10)  # Weight load heavier
        scores.append((e, score))
    
    return min(scores, key=lambda x: x[1])[0]
```

## System Flow

```
User presses floor button
        ↓
Request queued
        ↓
Controller selects best elevator
        ↓
Elevator moves to requested floor
        ↓
Doors open
        ↓
Passengers board
        ↓
Passenger selects destination
        ↓
Elevator adds to destination list
        ↓
Elevator moves to destination
        ↓
Doors open
        ↓
Passengers exit
        ↓
Repeat
```

## Optimization Techniques

| Technique | Impact | Complexity |
|-----------|--------|-----------|
| **SCAN Algorithm** | Reduces wait | Medium |
| **Predictive Dispatch** | Peak handling | High |
| **Load Balancing** | Fair distribution | Medium |
| **Destination Grouping** | Fewer stops | Medium |
| **Prefetching** | Anticipate requests | High |

## Key Metrics

- **Average wait time**: Target < 30 seconds
- **Average travel time**: From floor A to B
- **Passenger satisfaction**: Success rate
- **Elevator utilization**: % loaded
- **Request queue length**: Backlog at peak

## Extension Ideas

1. **Priority Floors**: VIP floors, emergency
2. **Maintenance Mode**: Remove elevator from service
3. **Energy Optimization**: Reduce unnecessary movements
4. **Smart Scheduling**: ML-based demand prediction
5. **Emergency Handling**: Auto-go-to-ground on fire alarm
6. **Load Balancing**: Distribute passengers across elevators

## Key Interview Questions

1. **How to minimize wait time?**
   - SCAN algorithm, look-ahead scheduling

2. **Handle peak hours (9 AM)?**
   - Predict demand, pre-position elevators

3. **Emergency scenario?**
   - Override scheduling, go to ground floor

4. **System with 100 floors?**
   - More elevators, zoning (1-50, 51-100)

5. **Stuck elevator?**
   - Alert system, reroute traffic, manual rescue
