# Abstraction

## Definition

**Abstraction** is showing only essential features and hiding unnecessary complexity. It allows users to interact with objects without needing to know how they work internally.

## Key Principle

Focus on WHAT an object does, not HOW it does it.

## Real-World Examples

### Example 1: ATM Machine
```python
from abc import ABC, abstractmethod

# Abstract class - user doesn't need to know internal details
class ATM(ABC):
    @abstractmethod
    def withdraw(self, amount):
        pass
    
    @abstractmethod
    def deposit(self, amount):
        pass
    
    @abstractmethod
    def check_balance(self):
        pass

# Concrete implementation - user doesn't see this complexity
class ATMImpl(ATM):
    def __init__(self, account_balance):
        self.__balance = account_balance
    
    def withdraw(self, amount):
        # Complex internal logic: database check, fraud detection, etc.
        if amount <= self.__balance:
            self.__balance -= amount
            return f"Withdrew ${amount}. New balance: ${self.__balance}"
        return "Insufficient funds"
    
    def deposit(self, amount):
        # Complex internal logic: validate, record
        self.__balance += amount
        return f"Deposited ${amount}. New balance: ${self.__balance}"
    
    def check_balance(self):
        return self.__balance

# User interaction - simple, clean interface
atm = ATMImpl(5000)
print(atm.withdraw(500))      # User doesn't know about validation logic
print(atm.check_balance())    # User just gets the balance
```

### Example 2: Database Connection
```python
from abc import ABC, abstractmethod

# Abstract Database - API that users interact with
class Database(ABC):
    @abstractmethod
    def connect(self):
        pass
    
    @abstractmethod
    def execute_query(self, query):
        pass
    
    @abstractmethod
    def close(self):
        pass

# Concrete MySQL Implementation
class MySQLDatabase(Database):
    def connect(self):
        # Complex connection logic: TCP/IP, SSL, authentication
        return "Connected to MySQL"
    
    def execute_query(self, query):
        # Query parsing, optimization, execution
        return "Query executed successfully"
    
    def close(self):
        return "Connection closed"

# Concrete PostgreSQL Implementation
class PostgreSQLDatabase(Database):
    def connect(self):
        return "Connected to PostgreSQL"
    
    def execute_query(self, query):
        return "Query executed successfully"
    
    def close(self):
        return "Connection closed"

# User code - same for both databases!
databases = [MySQLDatabase(), PostgreSQLDatabase()]
for db in databases:
    print(db.connect())
    print(db.execute_query("SELECT * FROM users"))
    print(db.close())
```

### Example 3: Payment Processing
```python
from abc import ABC, abstractmethod

# Abstract Payment Gateway
class PaymentGateway(ABC):
    @abstractmethod
    def process_payment(self, amount, card_info):
        pass

# Different implementations
class StripePayment(PaymentGateway):
    def process_payment(self, amount, card_info):
        # Stripe API: tokenization, encryption, fraud detection, etc.
        print(f"Processing ${amount} via Stripe...")
        # Complex logic hidden from user
        return "Payment successful via Stripe"

class PayPalPayment(PaymentGateway):
    def process_payment(self, amount, card_info):
        # PayPal API: authentication, account verification, etc.
        print(f"Processing ${amount} via PayPal...")
        return "Payment successful via PayPal"

# Business logic - doesn't care about payment details
def checkout(payment_gateway: PaymentGateway, amount, card_info):
    return payment_gateway.process_payment(amount, card_info)

# Usage
stripe = StripePayment()
paypal = PayPalPayment()

print(checkout(stripe, 99.99, "4111-1111-1111-1111"))
print(checkout(paypal, 99.99, "john@example.com"))
```

### Example 4: File Operations
```python
from abc import ABC, abstractmethod

# Abstract FileHandler
class FileHandler(ABC):
    @abstractmethod
    def read(self, filename):
        pass
    
    @abstractmethod
    def write(self, filename, data):
        pass

# JSON File Handler
class JSONFileHandler(FileHandler):
    def read(self, filename):
        import json
        with open(filename, 'r') as f:
            return json.load(f)
    
    def write(self, filename, data):
        import json
        with open(filename, 'w') as f:
            json.dump(data, f)

# CSV File Handler
class CSVFileHandler(FileHandler):
    def read(self, filename):
        import csv
        with open(filename, 'r') as f:
            return list(csv.DictReader(f))
    
    def write(self, filename, data):
        import csv
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

# Application code - doesn't care about file format
def save_data(handler: FileHandler, filename, data):
    handler.write(filename, data)

def load_data(handler: FileHandler, filename):
    return handler.read(filename)
```

## Abstraction vs Encapsulation

| Aspect | Abstraction | Encapsulation |
|--------|-------------|---------------|
| **Focus** | WHAT (interface) | HOW (hiding data) |
| **Purpose** | Reduce complexity | Control access |
| **Example** | Abstract class `Database` | Private `__balance` |

## Benefits

- ✅ **Reduces Complexity**: Users interact with simple interface
- ✅ **Flexibility**: Can change implementation without affecting users
- ✅ **Code Reusability**: Different implementations of same interface
- ✅ **Maintainability**: Easier to test and modify

## Key Interview Questions

1. **When should you use abstract classes vs interfaces?**
   - Abstract: Shared code, state | Interface: Only contracts

2. **Give real-world example of abstraction**
   - Car: driver doesn't know about engine complexity

3. **How does abstraction help in testing?**
   - Mock abstract classes for testing

## Important Points

- ✅ Use abstract base classes (ABC) for defining contracts
- ✅ Define abstract methods with `@abstractmethod`
- ✅ Hide implementation details from users
- ✅ Expose only necessary methods and properties
- ✅ Allow multiple implementations of same interface
