# SOLID Principles

## S - Single Responsibility Principle (SRP)

A class should have only one reason to change (one responsibility).

### ❌ BAD - Multiple Responsibilities
```python
class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
    
    def save_to_db(self):  # Responsibility 1: Database
        # Save to database
        pass
    
    def send_email(self):  # Responsibility 2: Email
        # Send email to user
        pass
    
    def generate_report(self):  # Responsibility 3: Reporting
        # Generate user report
        pass
```

### ✅ GOOD - Single Responsibility
```python
class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email

class UserRepository:
    def save(self, user):
        # Save user to database
        pass

class EmailService:
    def send_welcome_email(self, user):
        # Send email to user
        pass

class ReportGenerator:
    def generate_user_report(self, user):
        # Generate user report
        pass
```

---

## O - Open/Closed Principle (OCP)

Classes should be open for extension, closed for modification.

### ❌ BAD - Modification Required for New Type
```python
class PaymentProcessor:
    def process(self, payment_type, amount):
        if payment_type == "credit_card":
            # Process credit card
            pass
        elif payment_type == "paypal":
            # Process PayPal
            pass
        elif payment_type == "crypto":
            # Add new type requires modifying class!
            pass
```

### ✅ GOOD - Extension Without Modification
```python
from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

class CreditCardPayment(PaymentMethod):
    def pay(self, amount):
        return f"CC: ${amount}"

class PayPalPayment(PaymentMethod):
    def pay(self, amount):
        return f"PP: ${amount}"

# Add new payment type without modifying existing code
class CryptoPayment(PaymentMethod):
    def pay(self, amount):
        return f"Crypto: ${amount}"

class PaymentProcessor:
    def process(self, payment: PaymentMethod, amount):
        return payment.pay(amount)
```

---

## L - Liskov Substitution Principle (LSP)

Derived classes should be substitutable for base classes without breaking functionality.

### ❌ BAD - Violates LSP
```python
class Bird:
    def fly(self):
        return "Flying"

class Penguin(Bird):
    def fly(self):
        # Penguin can't fly!
        raise Exception("Penguins cannot fly")

# Code breaks because Penguin doesn't follow Bird's contract
def make_bird_fly(bird: Bird):
    return bird.fly()  # Might crash with Penguin!
```

### ✅ GOOD - Respects LSP
```python
class Bird:
    def move(self):
        return "Moving"

class FlyingBird(Bird):
    def fly(self):
        return "Flying"

class Penguin(FlyingBird):
    def move(self):
        return "Swimming"  # Correct behavior

def make_bird_move(bird: Bird):
    return bird.move()  # Always works!
```

---

## I - Interface Segregation Principle (ISP)

Clients should not depend on interfaces they don't use.

### ❌ BAD - Fat Interface
```python
class Worker(ABC):
    @abstractmethod
    def work(self):
        pass
    
    @abstractmethod
    def manage_team(self):
        pass
    
    @abstractmethod
    def eat_lunch(self):
        pass

class Developer(Worker):
    def work(self):
        return "Coding"
    
    def manage_team(self):
        # Developer doesn't manage!
        raise NotImplementedError()
    
    def eat_lunch(self):
        return "Eating"
```

### ✅ GOOD - Segregated Interfaces
```python
class Workable(ABC):
    @abstractmethod
    def work(self):
        pass

class Manageable(ABC):
    @abstractmethod
    def manage_team(self):
        pass

class Eatable(ABC):
    @abstractmethod
    def eat_lunch(self):
        pass

class Developer(Workable, Eatable):
    def work(self):
        return "Coding"
    
    def eat_lunch(self):
        return "Eating"

class Manager(Workable, Manageable, Eatable):
    def work(self):
        return "Managing"
    
    def manage_team(self):
        return "Leading team"
    
    def eat_lunch(self):
        return "Eating"
```

---

## D - Dependency Inversion Principle (DIP)

High-level modules should not depend on low-level modules. Both should depend on abstractions.

### ❌ BAD - Direct Dependency
```python
class SQLDatabase:
    def save(self, data):
        # Save to SQL DB
        pass

class UserService:
    def __init__(self):
        self.db = SQLDatabase()  # Direct dependency!
    
    def save_user(self, user):
        self.db.save(user)
    
    # If we want to use MongoDB, we need to change UserService!
```

### ✅ GOOD - Dependency Injection
```python
from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def save(self, data):
        pass

class SQLDatabase(Database):
    def save(self, data):
        return f"Saved to SQL: {data}"

class MongoDB(Database):
    def save(self, data):
        return f"Saved to Mongo: {data}"

class UserService:
    def __init__(self, db: Database):  # Depends on abstraction!
        self.db = db
    
    def save_user(self, user):
        return self.db.save(user)

# Usage - can switch databases easily
sql_db = SQLDatabase()
mongo_db = MongoDB()

service1 = UserService(sql_db)
service2 = UserService(mongo_db)
# UserService code never changes!
```

---

## Real-World Example: E-commerce Order System

```python
# S - Single Responsibility
class Order:
    def __init__(self, items, customer):
        self.items = items
        self.customer = customer
    
    def get_total(self):
        return sum(item.price for item in self.items)

class OrderRepository:  # Handles persistence
    def save(self, order):
        pass

class OrderNotifier:  # Handles notifications
    def notify_customer(self, order):
        pass

# O - Open/Closed
class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, amount):
        pass

class PercentageDiscount(DiscountStrategy):
    def __init__(self, percent):
        self.percent = percent
    
    def calculate(self, amount):
        return amount * (1 - self.percent/100)

# L - Liskov Substitution
class PaymentMethod(ABC):
    @abstractmethod
    def process(self, amount):
        pass

class CreditCard(PaymentMethod):
    def process(self, amount):
        return f"Credit card processed: ${amount}"

# I - Interface Segregation
class Validatable(ABC):
    @abstractmethod
    def validate(self):
        pass

class Processable(ABC):
    @abstractmethod
    def process(self):
        pass

class OrderValidator(Validatable):
    def validate(self):
        return True

class OrderProcessor(Processable):
    def process(self):
        return "Processing..."

# D - Dependency Inversion
class OrderService:
    def __init__(self, repository: OrderRepository, 
                 notifier: OrderNotifier,
                 payment: PaymentMethod):
        self.repo = repository
        self.notifier = notifier
        self.payment = payment
    
    def create_order(self, order):
        self.repo.save(order)
        self.payment.process(order.get_total())
        self.notifier.notify_customer(order)
```

## Benefits of SOLID

| Principle | Benefit |
|-----------|---------|
| **SRP** | Easy to understand, maintain, test |
| **OCP** | Easy to extend without modifying |
| **LSP** | Polymorphism works reliably |
| **ISP** | No fat interfaces, less coupling |
| **DIP** | Flexible, testable, maintainable |

## Key Interview Questions

1. **What's Single Responsibility?**
   - A class should have one reason to change

2. **How does Open/Closed help?**
   - Can add features without modifying existing code

3. **Real-world SOLID example?**
   - Database abstraction, payment processors, notification systems

4. **Most important SOLID principle?**
   - DIP - enables loose coupling and testability

## Important Points

- ✅ Follow SOLID for maintainable code
- ✅ SOLID enables flexibility and extensibility
- ✅ Makes testing easier
- ✅ Reduces code duplication
- ✅ Improves code readability
