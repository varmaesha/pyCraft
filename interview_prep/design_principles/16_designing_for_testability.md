# Designing for Testability

## Definition

**Testability**: How easily a system can be tested. Well-designed code is easy to test.

**Goal**: Write code that's easy to unit test, mock, and verify.

## Real-World Examples

### Example 1: User Service

#### ❌ NOT TESTABLE
```python
class UserService:
    def register_user(self, username, email):
        # Mixed concerns - hard to test
        
        # Database operation - needs real database
        db = MySQLConnection()
        db.execute(f"INSERT INTO users VALUES ('{username}', '{email}')")
        
        # Email operation - needs real email server
        import smtplib
        smtplib.SMTP().sendmail(email, "Welcome!")
        
        # Logging - writes to file
        with open("users.log", "a") as f:
            f.write(f"User {username} registered\n")
        
        return True

# Problems:
# 1. Cannot test without database
# 2. Cannot test without email server
# 3. Creates files during testing
# 4. No way to verify behavior independently
```

#### ✅ TESTABLE
```python
# Extract dependencies as abstractions
class UserRepository:
    def save(self, user):
        pass

class EmailService:
    def send_welcome(self, email):
        pass

class Logger:
    def log(self, message):
        pass

class UserService:
    def __init__(self, repo: UserRepository, email: EmailService, logger: Logger):
        self.repo = repo
        self.email = email
        self.logger = logger
    
    def register_user(self, username, email):
        self.repo.save({"username": username, "email": email})
        self.email.send_welcome(email)
        self.logger.log(f"User {username} registered")
        return True

# NOW TESTABLE
class MockUserRepository(UserRepository):
    def __init__(self):
        self.saved_users = []
    
    def save(self, user):
        self.saved_users.append(user)

class MockEmailService(EmailService):
    def __init__(self):
        self.emails_sent = []
    
    def send_welcome(self, email):
        self.emails_sent.append(email)

class MockLogger(Logger):
    def __init__(self):
        self.logs = []
    
    def log(self, message):
        self.logs.append(message)

# Test
def test_register_user():
    repo = MockUserRepository()
    email = MockEmailService()
    logger = MockLogger()
    
    service = UserService(repo, email, logger)
    service.register_user("john", "john@example.com")
    
    assert len(repo.saved_users) == 1
    assert len(email.emails_sent) == 1
    assert len(logger.logs) == 1

test_register_user()  # PASSES!
```

### Example 2: Order Processing

#### ❌ NOT TESTABLE
```python
class OrderProcessor:
    def process_order(self, order_id):
        # Direct coupling to external services
        order = self._fetch_from_database(order_id)
        payment = self._charge_credit_card(order.total)  # REAL charge!
        self._send_email(order.customer_email)
        self._log_to_external_service()
        return True
    
    # Hard to test - calls real services
```

#### ✅ TESTABLE
```python
# Dependency injection + abstractions
class OrderRepository:
    def get(self, order_id):
        pass

class PaymentGateway:
    def charge(self, amount):
        pass

class NotificationService:
    def notify(self, email):
        pass

class OrderProcessor:
    def __init__(self, repo: OrderRepository, 
                 payment: PaymentGateway,
                 notifier: NotificationService):
        self.repo = repo
        self.payment = payment
        self.notifier = notifier
    
    def process_order(self, order_id):
        order = self.repo.get(order_id)
        self.payment.charge(order.total)
        self.notifier.notify(order.customer_email)
        return True

# Mocks for testing
class MockOrder:
    def __init__(self):
        self.total = 100
        self.customer_email = "test@example.com"

class MockRepository(OrderRepository):
    def get(self, order_id):
        return MockOrder()

class MockPayment(PaymentGateway):
    def __init__(self):
        self.charged = False
    
    def charge(self, amount):
        self.charged = True

class MockNotifier(NotificationService):
    def __init__(self):
        self.notified = False
    
    def notify(self, email):
        self.notified = True

# Test
def test_process_order():
    repo = MockRepository()
    payment = MockPayment()
    notifier = MockNotifier()
    
    processor = OrderProcessor(repo, payment, notifier)
    processor.process_order("ORD123")
    
    assert payment.charged
    assert notifier.notified

test_process_order()  # PASSES!
```

### Example 3: Calculator (Simple Testable Design)

#### ❌ NOT TESTABLE
```python
class Calculator:
    def add(self, a, b):
        # Logging to database
        import sqlite3
        conn = sqlite3.connect("operations.db")
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO operations VALUES ('{a}', '{b}', '{a+b}')")
        conn.commit()
        
        # Printing to console
        print(f"{a} + {b} = {a + b}")
        
        # External API call
        requests.post("https://analytics.com/log", data={"operation": "add"})
        
        return a + b

# Hard to test - side effects everywhere
```

#### ✅ TESTABLE
```python
class Calculator:
    def add(self, a, b):
        return a + b  # Pure function!

class OperationLogger:
    def log(self, operation_string):
        pass

class CalculatorWrapper:
    def __init__(self, calculator, logger):
        self.calc = calculator
        self.logger = logger
    
    def add_with_logging(self, a, b):
        result = self.calc.add(a, b)
        self.logger.log(f"{a} + {b} = {result}")
        return result

# Easy to test core logic
def test_add():
    calc = Calculator()
    assert calc.add(2, 3) == 5

# Easy to test with logger
class MockLogger(OperationLogger):
    def __init__(self):
        self.logged = False
    
    def log(self, operation_string):
        self.logged = True

def test_add_with_logging():
    calc = Calculator()
    logger = MockLogger()
    wrapper = CalculatorWrapper(calc, logger)
    
    result = wrapper.add_with_logging(2, 3)
    assert result == 5
    assert logger.logged
```

## Principles for Testability

### 1. Single Responsibility
```python
# BAD - multiple reasons to test
class UserManager:
    def register_and_send_email(self, user):
        pass

# GOOD - single reason
class UserRepository:
    def register(self, user):
        pass

class EmailService:
    def send_welcome(self, email):
        pass
```

### 2. Dependency Injection
```python
# BAD - creates dependencies
class Service:
    def __init__(self):
        self.db = Database()

# GOOD - receives dependencies
class Service:
    def __init__(self, db):
        self.db = db
```

### 3. Avoid Side Effects
```python
# BAD - side effects
def calculate_total(cart):
    total = sum(item.price for item in cart)
    db.save_calculation(total)  # Side effect!
    return total

# GOOD - pure function
def calculate_total(cart):
    return sum(item.price for item in cart)

# Logging separate
class CartService:
    def __init__(self, calculator, logger):
        self.calc = calculator
        self.logger = logger
    
    def calculate_and_log(self, cart):
        total = self.calc.calculate_total(cart)
        self.logger.log(f"Total: {total}")
        return total
```

### 4. Use Abstractions
```python
# BAD - concrete dependency
def process(mysql: MySQLDatabase):
    pass

# GOOD - abstract dependency
def process(db: Database):
    pass
```

## Anti-patterns (What to Avoid)

❌ **Hard-coded Dependencies**: new Database()
❌ **Hidden Dependencies**: Used in method, not passed in
❌ **Global State**: Used everywhere, hard to mock
❌ **Tight Coupling**: Direct dependencies
❌ **Static Methods**: Can't mock or override
❌ **Multiple Responsibilities**: Hard to test one thing

## Testing Strategies

### Unit Testing (Testable Design)
```python
# Test single class in isolation
def test_discount_calculation():
    discount = PercentageDiscount(10)
    assert discount.apply(100) == 90
```

### Mocking (Dependency Injection)
```python
# Replace dependencies with mocks
class MockPaymentGateway:
    def charge(self, amount):
        return True

processor = OrderProcessor(repo, MockPaymentGateway(), notifier)
processor.process_order("123")  # Uses mock
```

### Integration Testing (Separated Concerns)
```python
# Test multiple components together
def test_full_order_flow():
    processor = OrderProcessor(real_repo, real_payment, real_notifier)
    processor.process_order("123")
```

## Key Interview Questions

1. **Why is testability important?**
   - Catches bugs early, enables refactoring, increases confidence

2. **How do you design for testability?**
   - Dependency injection, separation of concerns, avoid side effects

3. **What makes code hard to test?**
   - Hidden dependencies, side effects, tight coupling

4. **How to test external dependencies?**
   - Mock them using abstract interfaces

## Important Points

- ✅ Design code to be testable from start
- ✅ Use dependency injection
- ✅ Separate concerns
- ✅ Avoid side effects
- ✅ Use abstractions
- ✅ Make classes small and focused
- ✅ Test one thing per test
