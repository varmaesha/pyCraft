# Polymorphism

## Definition

**Polymorphism** means "many forms". It allows objects of different types to respond to the same method call in different ways. Enables flexible and extensible code.

## Types of Polymorphism

1. **Compile-time (Static)**: Method/Operator Overloading
2. **Runtime (Dynamic)**: Method Overriding

## Real-World Examples

### Example 1: Payment Processing (Method Overriding)
```python
from abc import ABC, abstractmethod

# Base class
class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass
    
    @abstractmethod
    def validate(self):
        pass

# Different implementations - same interface, different behavior
class CreditCardProcessor(PaymentProcessor):
    def __init__(self, card_number):
        self.card_number = card_number
    
    def validate(self):
        return len(self.card_number) == 16
    
    def process_payment(self, amount):
        if self.validate():
            return f"Credit Card: Processing ${amount}"
        return "Invalid card"

class PayPalProcessor(PaymentProcessor):
    def __init__(self, email):
        self.email = email
    
    def validate(self):
        return "@" in self.email
    
    def process_payment(self, amount):
        if self.validate():
            return f"PayPal: Processing ${amount} from {self.email}"
        return "Invalid email"

class CryptoProcessor(PaymentProcessor):
    def __init__(self, wallet_address):
        self.wallet_address = wallet_address
    
    def validate(self):
        return len(self.wallet_address) == 42
    
    def process_payment(self, amount):
        if self.validate():
            return f"Crypto: Processing ${amount} to {self.wallet_address}"
        return "Invalid wallet"

# Client code - works with any processor!
def checkout(processor: PaymentProcessor, amount):
    return processor.process_payment(amount)

# Usage - Polymorphism in action
processors = [
    CreditCardProcessor("4111111111111111"),
    PayPalProcessor("user@example.com"),
    CryptoProcessor("0x1234567890123456789012345678901234567890")
]

for processor in processors:
    print(checkout(processor, 99.99))
# Different classes, same method, different output!
```

### Example 2: Shape Area Calculation
```python
from abc import ABC, abstractmethod
import math

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass
    
    @abstractmethod
    def perimeter(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return math.pi * self.radius ** 2
    
    def perimeter(self):
        return 2 * math.pi * self.radius

class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width
    
    def area(self):
        return self.length * self.width
    
    def perimeter(self):
        return 2 * (self.length + self.width)

class Triangle(Shape):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
    
    def area(self):
        s = (self.a + self.b + self.c) / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))
    
    def perimeter(self):
        return self.a + self.b + self.c

# Polymorphic function
def print_shape_info(shape: Shape):
    print(f"Area: {shape.area():.2f}, Perimeter: {shape.perimeter():.2f}")

# Usage
shapes = [
    Circle(5),
    Rectangle(4, 6),
    Triangle(3, 4, 5)
]

for shape in shapes:
    print_shape_info(shape)
# Same function, different shapes, different calculations!
```

### Example 3: Notification System
```python
class Notification:
    def __init__(self, message):
        self.message = message
    
    def send(self):
        pass

class EmailNotification(Notification):
    def send(self):
        return f"Email sent: {self.message}"

class SMSNotification(Notification):
    def send(self):
        return f"SMS sent: {self.message}"

class PushNotification(Notification):
    def send(self):
        return f"Push notification sent: {self.message}"

class SlackNotification(Notification):
    def send(self):
        return f"Slack message sent: {self.message}"

# Polymorphic usage
notifications = [
    EmailNotification("Order confirmed"),
    SMSNotification("Your code: 12345"),
    PushNotification("New message received"),
    SlackNotification("Deployment started")
]

for notification in notifications:
    print(notification.send())
# Each notification type handles sending differently!
```

### Example 4: Database Operations
```python
class Database:
    def save(self, data):
        pass
    
    def retrieve(self, query):
        pass

class MySQLDatabase(Database):
    def save(self, data):
        print(f"MySQL: INSERT INTO table VALUES ({data})")
        return "Saved to MySQL"
    
    def retrieve(self, query):
        print(f"MySQL: SELECT * WHERE {query}")
        return "Retrieved from MySQL"

class MongoDatabase(Database):
    def save(self, data):
        print(f"MongoDB: db.collection.insertOne({data})")
        return "Saved to MongoDB"
    
    def retrieve(self, query):
        print(f"MongoDB: db.collection.findOne({query})")
        return "Retrieved from MongoDB"

class RedisDatabase(Database):
    def save(self, data):
        print(f"Redis: SET key {data}")
        return "Saved to Redis"
    
    def retrieve(self, query):
        print(f"Redis: GET {query}")
        return "Retrieved from Redis"

# Application layer - doesn't care about DB type
class UserRepository:
    def __init__(self, db: Database):
        self.db = db
    
    def create_user(self, user_data):
        return self.db.save(user_data)
    
    def find_user(self, user_id):
        return self.db.retrieve(f"id = {user_id}")

# Usage - swap databases easily!
mysql_db = MySQLDatabase()
mongo_db = MongoDatabase()
redis_db = RedisDatabase()

repos = [
    UserRepository(mysql_db),
    UserRepository(mongo_db),
    UserRepository(redis_db)
]

for repo in repos:
    print(repo.create_user("{'name': 'John'}"))
    print(repo.find_user(1))
```

## Operator Overloading (Compile-time Polymorphism)

```python
class ComplexNumber:
    def __init__(self, real, imaginary):
        self.real = real
        self.imaginary = imaginary
    
    def __add__(self, other):
        return ComplexNumber(
            self.real + other.real,
            self.imaginary + other.imaginary
        )
    
    def __str__(self):
        return f"{self.real} + {self.imaginary}i"

# Usage
c1 = ComplexNumber(3, 4)
c2 = ComplexNumber(1, 2)
c3 = c1 + c2  # Uses __add__ method
print(c3)     # Output: 4 + 6i
```

## Benefits of Polymorphism

| Benefit | Example |
|---------|---------|
| **Flexibility** | Same code works with different types |
| **Scalability** | Add new types without changing existing code |
| **Maintainability** | Changes localized to specific implementations |
| **Testability** | Easy to mock and test different implementations |

## Key Interview Questions

1. **What's the difference between overloading and overriding?**
   - Overloading: Same method name, different signatures | Overriding: Same signature, different implementation

2. **How does polymorphism enable loose coupling?**
   - Depend on abstract type, not concrete implementations

3. **Give real-world example of polymorphism**
   - Different payment methods with same `pay()` interface

4. **Can you achieve polymorphism without inheritance?**
   - Yes, through duck typing (if it quacks like a duck...)

## Important Points

- ✅ Use abstract base classes to define contracts
- ✅ Implement same interface differently in subclasses
- ✅ Code against interfaces, not implementations
- ✅ Enables clean, extensible architectures
- ✅ Makes testing easier with mocking
