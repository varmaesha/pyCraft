# Interface vs Abstract Class

## Definitions

### Abstract Class
Partial implementation of a class. Can have concrete methods and state.

### Interface
Pure contract. All members are abstract (in most languages). No state/implementation.

## Key Differences

| Aspect | Abstract Class | Interface |
|--------|---|---|
| **Inheritance** | Single | Multiple |
| **Constructor** | Can have | Cannot have |
| **State** | Can have attributes | Cannot have attributes |
| **Access Modifiers** | All types | Usually public |
| **Methods** | Mix of abstract & concrete | All abstract (typically) |
| **Purpose** | IS-A relationship | Contract/capability |

## Real-World Examples

### Example 1: Payment Processing (Abstract Class)
```python
from abc import ABC, abstractmethod

# Abstract class - provides common functionality
class PaymentProcessor(ABC):
    def __init__(self, processor_name):
        self.processor_name = processor_name
        self.transaction_id = None
    
    # Concrete method - same for all
    def log_transaction(self, amount):
        print(f"{self.processor_name}: Processing ${amount}")
    
    # Abstract method - different for each
    @abstractmethod
    def process_payment(self, amount):
        pass
    
    # Concrete method - common logic
    def handle_payment(self, amount):
        self.log_transaction(amount)
        return self.process_payment(amount)

class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount):
        return f"Credit Card: ${amount} charged"

class PayPalProcessor(PaymentProcessor):
    def process_payment(self, amount):
        return f"PayPal: ${amount} charged"

# Usage
cc = CreditCardProcessor("Stripe")
print(cc.handle_payment(100))  # Uses shared log_transaction + specific process_payment
```

### Example 2: Shape Hierarchy (Abstract Class)
```python
import math

# Abstract class - shares common functionality
class Shape(ABC):
    def __init__(self, color):
        self.color = color
    
    # Concrete method - same for all shapes
    def describe(self):
        return f"I am {self.color} colored"
    
    # Abstract methods - different for each shape
    @abstractmethod
    def area(self):
        pass
    
    @abstractmethod
    def perimeter(self):
        pass

class Circle(Shape):
    def __init__(self, color, radius):
        super().__init__(color)
        self.radius = radius
    
    def area(self):
        return math.pi * self.radius ** 2
    
    def perimeter(self):
        return 2 * math.pi * self.radius

class Rectangle(Shape):
    def __init__(self, color, width, height):
        super().__init__(color)
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

# Usage
shapes = [
    Circle("red", 5),
    Rectangle("blue", 4, 6)
]

for shape in shapes:
    print(shape.describe())  # Common method
    print(f"Area: {shape.area()}")  # Specific implementation
```

### Example 3: Multiple Interfaces (Python Protocol)
```python
from typing import Protocol

# Interfaces - pure contracts
class Drawable(Protocol):
    def draw(self):
        pass

class Resizable(Protocol):
    def resize(self, scale):
        pass

class Movable(Protocol):
    def move(self, x, y):
        pass

# Class implementing multiple interfaces
class Shape:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def draw(self):
        print(f"Drawing at ({self.x}, {self.y})")
    
    def resize(self, scale):
        print(f"Resizing by {scale}")
    
    def move(self, x, y):
        self.x = x
        self.y = y
        print(f"Moved to ({self.x}, {self.y})")

class Button(Shape):
    def draw(self):
        print("Drawing button")
    
    def resize(self, scale):
        print(f"Resizing button by {scale}")

# Usage - any object implementing these protocols
def draw_and_move(obj: Drawable & Movable):
    obj.draw()
    obj.move(10, 20)

button = Button(0, 0)
draw_and_move(button)
```

### Example 4: Repository Pattern (Abstract Class vs Interface)
```python
# Abstract class with shared logic
class BaseRepository(ABC):
    def __init__(self):
        self.data = []
    
    def save_to_cache(self, item):
        # Common caching logic
        print(f"Caching {item}")
    
    @abstractmethod
    def save(self, item):
        pass
    
    @abstractmethod
    def find(self, id):
        pass

class UserRepository(BaseRepository):
    def save(self, user):
        self.save_to_cache(user)
        print(f"Saving user to database")
    
    def find(self, id):
        return f"User {id}"

class ProductRepository(BaseRepository):
    def save(self, product):
        self.save_to_cache(product)
        print(f"Saving product to database")
    
    def find(self, id):
        return f"Product {id}"

# Usage
user_repo = UserRepository()
user_repo.save("John")  # Uses common save_to_cache

product_repo = ProductRepository()
product_repo.save("Laptop")  # Uses common save_to_cache from base class
```

### Example 5: Database Interfaces
```python
# Interface - pure contract
class DataStore(ABC):
    @abstractmethod
    def connect(self):
        pass
    
    @abstractmethod
    def write(self, key, value):
        pass
    
    @abstractmethod
    def read(self, key):
        pass
    
    @abstractmethod
    def disconnect(self):
        pass

# Different implementations
class RedisStore(DataStore):
    def connect(self):
        print("Connecting to Redis")
    
    def write(self, key, value):
        print(f"Redis SET {key} = {value}")
    
    def read(self, key):
        print(f"Redis GET {key}")
        return "value"
    
    def disconnect(self):
        print("Disconnecting Redis")

class MongoStore(DataStore):
    def connect(self):
        print("Connecting to MongoDB")
    
    def write(self, key, value):
        print(f"MongoDB insert: {key} = {value}")
    
    def read(self, key):
        print(f"MongoDB find: {key}")
        return "value"
    
    def disconnect(self):
        print("Disconnecting MongoDB")

# Client code - works with any DataStore
def use_data_store(store: DataStore):
    store.connect()
    store.write("user_token", "abc123")
    store.read("user_token")
    store.disconnect()

# Use different stores
use_data_store(RedisStore())
print()
use_data_store(MongoStore())
```

## When to Use Each

### Use Abstract Class When:
- ✅ Related classes share code
- ✅ Need non-public members
- ✅ Need to define state (attributes)
- ✅ Need constructors with initialization
- ✅ IS-A relationship

### Use Interface When:
- ✅ Define a contract for unrelated classes
- ✅ Multiple inheritance needed
- ✅ Only method signatures matter
- ✅ HAS-A capability relationship
- ✅ Decoupling is priority

## Real-World Best Practices

```python
# ✅ GOOD - Abstract class with shared implementation
class DatabaseConnection(ABC):
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.is_connected = False
    
    def open(self):
        if not self.is_connected:
            self._connect_impl()
            self.is_connected = True
    
    @abstractmethod
    def _connect_impl(self):
        pass

# ✅ GOOD - Interface for capability
class Validatable(ABC):
    @abstractmethod
    def validate(self):
        pass

# ✅ GOOD - Combine both approaches
class UserValidator(Validatable):
    def validate(self):
        return True

class MySQLConnection(DatabaseConnection):
    def _connect_impl(self):
        print(f"MySQL: Connecting to {self.connection_string}")
```

## Key Interview Questions

1. **Difference between abstract class and interface?**
   - Abstract class: shared implementation, state | Interface: pure contract

2. **Can interface have methods with implementation?**
   - Python 3.6+: Yes, but ideally not

3. **Can class inherit from multiple abstract classes?**
   - Python: Yes, but usually bad design

4. **Can interface inherit from another interface?**
   - Yes, to extend contract

5. **When to use abstract class vs interface?**
   - Abstract: shared code (IS-A) | Interface: contract (HAS-A capability)

## Important Points

- ✅ Use abstract class for shared implementation
- ✅ Use interface for pure contracts
- ✅ Prefer composition over inheritance
- ✅ Program to interfaces, not implementations
- ✅ Minimize abstract base classes, maximize interfaces
