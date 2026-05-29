# Composition vs Inheritance

## Definition

- **Inheritance**: IS-A relationship (Car IS-A Vehicle)
- **Composition**: HAS-A relationship (Car HAS-A Engine)

## When to Use Each

### Use Inheritance When:
- Clear IS-A relationship
- Child extends parent's functionality
- Want to reuse code and establish type hierarchy

### Use Composition When:
- HAS-A relationship
- Want flexibility and runtime polymorphism
- Avoid tight coupling
- Multiple behaviors needed (composition over multiple inheritance)

## Real-World Example 1: Vehicle System

### ❌ BAD - Using Inheritance (Rigid)
```python
class Vehicle:
    def start(self):
        return "Starting..."

class Car(Vehicle):
    pass

class Truck(Vehicle):
    pass

class Boat(Vehicle):
    pass

# Problem: What if boat doesn't use wheels? Can't represent HAS-A
```

### ✅ GOOD - Using Composition (Flexible)
```python
# Components (has-a)
class Engine:
    def start(self):
        return "Engine started"

class Wheels:
    def __init__(self, count):
        self.count = count
    
    def rotate(self):
        return f"Rotating {self.count} wheels"

class Motor:
    def start(self):
        return "Motor started"

# Vehicles composed of different parts
class Car:
    def __init__(self, name):
        self.name = name
        self.engine = Engine()
        self.wheels = Wheels(4)
    
    def start(self):
        return f"{self.name}: {self.engine.start()}, {self.wheels.rotate()}"

class Boat:
    def __init__(self, name):
        self.name = name
        self.motor = Motor()
    
    def start(self):
        return f"{self.name}: {self.motor.start()}"

# Usage
car = Car("Toyota")
print(car.start())  # Toyota: Engine started, Rotating 4 wheels

boat = Boat("Yacht")
print(boat.start())  # Yacht: Motor started
```

## Real-World Example 2: Employee & Department

### ❌ Inheritance Problem
```python
class Person:
    pass

class Employee(Person):
    pass

class Manager(Employee):
    pass

class Department(Manager):  # Wrong! Department IS-NOT-A Manager
    pass

# This is conceptually wrong
```

### ✅ Composition Solution
```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Department:
    def __init__(self, name, budget):
        self.name = name
        self.budget = budget

class Employee:
    def __init__(self, name, age, department: Department):
        self.person = Person(name, age)  # Composition
        self.department = department  # Composition
    
    def get_info(self):
        return f"{self.person.name} works in {self.department.name}"

# Usage
engineering = Department("Engineering", 100000)
alice = Employee("Alice", 30, engineering)
print(alice.get_info())  # Alice works in Engineering
```

## Real-World Example 3: Phone Features

### ❌ Inheritance Hell
```python
class Phone:
    pass

class SmartPhone(Phone):
    pass

class CameraPhone(SmartPhone):
    pass

class GPSPhone(CameraPhone):
    pass

class MusicPhone(GPSPhone):
    pass

# Creating specific combinations becomes nightmare
# What if we want camera + gps but no music?
```

### ✅ Composition Solution
```python
class Camera:
    def take_photo(self):
        return "Photo taken"

class GPS:
    def get_location(self):
        return "Current location: 40.7128°N, 74.0060°W"

class MusicPlayer:
    def play(self, song):
        return f"Playing {song}"

class Phone:
    def __init__(self, name, has_camera=False, has_gps=False, has_music=False):
        self.name = name
        self.camera = Camera() if has_camera else None
        self.gps = GPS() if has_gps else None
        self.music = MusicPlayer() if has_music else None
    
    def take_photo(self):
        if self.camera:
            return self.camera.take_photo()
        return "No camera"
    
    def get_location(self):
        if self.gps:
            return self.gps.get_location()
        return "No GPS"
    
    def play_music(self, song):
        if self.music:
            return self.music.play(song)
        return "No music player"

# Usage - flexible combinations!
basic_phone = Phone("Nokia", has_music=True)
print(basic_phone.play_music("Song"))  # Playing Song
print(basic_phone.take_photo())        # No camera

smart_phone = Phone("iPhone", has_camera=True, has_gps=True, has_music=True)
print(smart_phone.take_photo())        # Photo taken
print(smart_phone.get_location())      # Current location: 40.7128°N, 74.0060°W
print(smart_phone.play_music("Song"))  # Playing Song
```

## Real-World Example 4: Restaurant Order System

### Using Composition
```python
class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Order:
    def __init__(self):
        self.items = []  # Composition: Order HAS-A list of MenuItems
    
    def add_item(self, item: MenuItem):
        self.items.append(item)
    
    def get_total(self):
        return sum(item.price for item in self.items)

class Restaurant:
    def __init__(self, name):
        self.name = name
        self.menu = []  # Composition: Restaurant HAS-A menu

class DeliveryService:
    def deliver(self, order: Order):
        return f"Delivering order with {len(order.items)} items"

# Usage
pizza = MenuItem("Pizza", 15)
coke = MenuItem("Coke", 2)

order = Order()
order.add_item(pizza)
order.add_item(coke)

service = DeliveryService()
print(service.deliver(order))  # Clean separation of concerns
```

## Comparison Table

| Aspect | Inheritance | Composition |
|--------|-------------|-------------|
| **Relationship** | IS-A | HAS-A |
| **Flexibility** | Less flexible | More flexible |
| **Coupling** | Tight | Loose |
| **Runtime Changes** | Impossible | Possible |
| **Complexity** | Simpler hierarchy | Slightly more code |
| **Multiple Behaviors** | Diamond problem | No problem |

## Key Interview Questions

1. **Why prefer composition over inheritance?**
   - More flexible, less coupling, avoids inheritance hierarchy problems

2. **Can you always replace inheritance with composition?**
   - Usually yes, but sometimes inheritance is semantically correct

3. **What's the diamond problem?**
   - Multiple inheritance from same base class (MRO complexity)

4. **Give example where inheritance is better**
   - Exception hierarchy, type systems where IS-A is semantically correct

## Important Points

- ✅ Use composition by default
- ✅ Use inheritance only for true IS-A relationships
- ✅ Composition gives runtime flexibility
- ✅ Avoid deep inheritance hierarchies (max 3 levels)
- ✅ "Favor composition over inheritance" - Gang of Four design patterns
