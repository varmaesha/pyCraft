# Loose Coupling vs Tight Coupling

## Definitions

**Tight Coupling**: Objects are highly dependent on each other. Changes in one require changes in others.

**Loose Coupling**: Objects interact through abstractions. Changes in one don't affect others.

## Real-World Examples

### Example 1: Customer & Email Service

#### ❌ TIGHT COUPLING
```python
class Customer:
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def register(self):
        # Directly sends email - tightly coupled!
        import smtplib
        smtp = smtplib.SMTP('smtp.gmail.com')
        smtp.send_message(f"Welcome {self.name}")
        
        # If email implementation changes, Customer class breaks
        # Hard to test without actual email server
        # Cannot switch email providers easily

# Problems:
# 1. Customer class knows about SMTP details
# 2. Testing requires real email server
# 3. Switching to Twilio or SendGrid means changing Customer class
```

#### ✅ LOOSE COUPLING
```python
from abc import ABC, abstractmethod

# Abstraction - contract
class NotificationService(ABC):
    @abstractmethod
    def send_welcome(self, user_name, recipient):
        pass

# Implementation 1
class GmailNotification(NotificationService):
    def send_welcome(self, user_name, recipient):
        # Gmail specific logic
        print(f"Gmail: Sending welcome email to {recipient}")

# Implementation 2
class TwilioNotification(NotificationService):
    def send_welcome(self, user_name, recipient):
        # Twilio specific logic
        print(f"Twilio: Sending SMS to {recipient}")

# Customer depends on abstraction, not concrete implementation
class Customer:
    def __init__(self, name, email, notification_service: NotificationService):
        self.name = name
        self.email = email
        self.notification_service = notification_service  # Injected
    
    def register(self):
        self.notification_service.send_welcome(self.name, self.email)
        # Customer doesn't know/care about implementation details

# Usage
gmail_service = GmailNotification()
customer1 = Customer("Alice", "alice@example.com", gmail_service)
customer1.register()

twilio_service = TwilioNotification()
customer2 = Customer("Bob", "bob@example.com", twilio_service)
customer2.register()

# Easy to test
class MockNotification(NotificationService):
    def send_welcome(self, user_name, recipient):
        self.sent = True

mock_service = MockNotification()
customer3 = Customer("Charlie", "charlie@example.com", mock_service)
customer3.register()
assert mock_service.sent
```

### Example 2: Order & Payment Processing

#### ❌ TIGHT COUPLING
```python
class Order:
    def __init__(self, items, total):
        self.items = items
        self.total = total
    
    def process_payment(self, card_number):
        # Order knows about Stripe - tightly coupled!
        import stripe
        stripe.api_key = "sk_test_..."
        charge = stripe.Charge.create(
            amount=int(self.total * 100),
            currency="usd",
            source=card_number
        )
        return charge.id

# Problems:
# - Order must import stripe
# - Cannot switch to PayPal without modifying Order
# - Cannot test without Stripe API credentials
# - Order class has responsibility it shouldn't have
```

#### ✅ LOOSE COUPLING
```python
class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, amount, card_info):
        pass

class StripeProcessor(PaymentProcessor):
    def process(self, amount, card_info):
        return f"Stripe processed: ${amount}"

class PayPalProcessor(PaymentProcessor):
    def process(self, amount, card_info):
        return f"PayPal processed: ${amount}"

class Order:
    def __init__(self, items, total, payment_processor: PaymentProcessor):
        self.items = items
        self.total = total
        self.payment_processor = payment_processor
    
    def process_payment(self, card_info):
        # Order doesn't know which processor is being used
        return self.payment_processor.process(self.total, card_info)

# Usage - Easy to switch
stripe = StripeProcessor()
order1 = Order(["Book"], 29.99, stripe)
print(order1.process_payment("4111-1111-1111-1111"))

paypal = PayPalProcessor()
order2 = Order(["Book"], 29.99, paypal)
print(order2.process_payment("user@example.com"))
```

### Example 3: Database Access

#### ❌ TIGHT COUPLING
```python
class UserService:
    def __init__(self):
        self.db = MySQLConnection()  # Hardcoded!
    
    def get_user(self, user_id):
        query = f"SELECT * FROM users WHERE id = {user_id}"
        return self.db.execute(query)
    
    # Problem: Switching to PostgreSQL requires changing UserService
```

#### ✅ LOOSE COUPLING
```python
class Database(ABC):
    @abstractmethod
    def execute(self, query):
        pass

class MySQLDatabase(Database):
    def execute(self, query):
        return f"MySQL: {query}"

class PostgreSQLDatabase(Database):
    def execute(self, query):
        return f"PostgreSQL: {query}"

class UserService:
    def __init__(self, database: Database):  # Injected
        self.db = database
    
    def get_user(self, user_id):
        query = f"SELECT * FROM users WHERE id = {user_id}"
        return self.db.execute(query)

# Usage
mysql = MySQLDatabase()
service1 = UserService(mysql)

postgresql = PostgreSQLDatabase()
service2 = UserService(postgresql)
# Same service, different databases!
```

## Coupling Levels

```
VERY TIGHT
    ↓
1. Direct object creation (new Service())
2. Concrete dependencies (Service service = new ServiceImpl())
3. Hardcoded values and configuration
    ↓
LOOSE
    ↓
1. Dependency injection (passed in constructor)
2. Abstract dependencies (interface, abstract class)
3. Configuration from external source
    ↓
VERY LOOSE
    ↓
1. Event-driven architecture
2. Message queues
3. Service discovery
```

## Comparison Table

| Aspect | Tight Coupling | Loose Coupling |
|--------|---|---|
| **Dependencies** | Direct, hardcoded | Injected, abstract |
| **Flexibility** | Hard to change | Easy to change |
| **Testability** | Difficult (need real deps) | Easy (can mock) |
| **Reusability** | Limited | High |
| **Understanding** | Need context | Self-contained |
| **Maintenance** | Ripple effects | Localized changes |

## How to Achieve Loose Coupling

### Technique 1: Dependency Injection
```python
# Bad
class Service:
    def __init__(self):
        self.logger = Logger()  # Creates dependency

# Good
class Service:
    def __init__(self, logger):
        self.logger = logger  # Receives dependency
```

### Technique 2: Use Interfaces/Abstractions
```python
# Bad
def use_mysql(mysql: MySQLDb):  # Depends on concrete class
    pass

# Good
def use_database(db: Database):  # Depends on interface
    pass
```

### Technique 3: Configuration Instead of Hardcoding
```python
# Bad
API_KEY = "hardcoded_key"

# Good
API_KEY = os.getenv("API_KEY")
```

### Technique 4: Avoid Cross-Module Imports
```python
# Bad - module_a directly imports module_b
# module_a.py
from module_b import SpecificClass

# Good - use interface
# Both implement ILogger
# module_a doesn't know about logger implementation
```

## Benefits of Loose Coupling

✅ **Easier Testing**: Mock dependencies
✅ **Easy to Change**: Switch implementations
✅ **Better Reusability**: Use in different contexts
✅ **Easier to Understand**: Less dependencies to know
✅ **Easier to Maintain**: Changes isolated
✅ **Teams Can Work Independently**: Different components by different teams

## Problems with Tight Coupling

❌ **Hard to Test**: Need real implementations
❌ **Fragile**: Breaking changes cascade
❌ **Not Reusable**: Too specific
❌ **Hard to Understand**: Need context
❌ **Difficult Maintenance**: Ripple effects
❌ **Can't Change Implementations**: Locked in

## Key Interview Questions

1. **How do you reduce coupling?**
   - Dependency Injection, use abstractions, configuration

2. **Why is loose coupling important?**
   - Flexibility, testability, maintainability

3. **Example of tight vs loose coupling?**
   - Tight: Customer knows about SMTP | Loose: Customer knows about service abstraction

4. **Trade-offs of loose coupling?**
   - More abstractions, slightly more code, better long-term

## Important Points

- ✅ Default to loose coupling
- ✅ Use dependency injection
- ✅ Depend on abstractions
- ✅ Avoid hardcoded values
- ✅ Think about changeability
- ❌ Don't over-engineer
