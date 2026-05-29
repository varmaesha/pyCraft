# OOP Fundamentals - Classes & Objects

## Core Concepts

**Object-Oriented Programming (OOP)** is a paradigm that organizes code around **objects** and **classes**. It models real-world entities and their interactions.

### Classes vs Objects
- **Class**: Blueprint or template for creating objects (defines structure and behavior)
- **Object**: Instance of a class (actual entity with state and behavior)

## Real-World Examples

### Example 1: Banking System
```python
# Class definition (Blueprint)
class BankAccount:
    def __init__(self, account_holder, balance=0):
        self.account_holder = account_holder
        self.balance = balance
    
    def deposit(self, amount):
        self.balance += amount
        return f"Deposited ${amount}. New balance: ${self.balance}"
    
    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return f"Withdrew ${amount}. New balance: ${self.balance}"
        return "Insufficient funds"

# Creating objects (Instances)
john_account = BankAccount("John Doe", 1000)
jane_account = BankAccount("Jane Smith", 5000)

print(john_account.deposit(500))  # Output: Deposited $500. New balance: $1500
print(jane_account.withdraw(200)) # Output: Withdrew $200. New balance: $4800
```

### Example 2: E-commerce Product System
```python
class Product:
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock
    
    def is_available(self):
        return self.stock > 0
    
    def purchase(self, quantity):
        if self.stock >= quantity:
            self.stock -= quantity
            return f"Purchased {quantity} {self.name}(s). Total: ${self.price * quantity}"
        return "Not enough stock"

laptop = Product("Dell XPS", 1200, 5)
print(laptop.purchase(2))  # Output: Purchased 2 Dell XPS(s). Total: $2400
print(laptop.stock)        # Output: 3
```

## Key Interview Questions

1. **What's the difference between a class and an object?**
   - Class is a template; object is an instance of that template

2. **Why do we use classes?**
   - Encapsulation, reusability, organization, maintainability

3. **What is constructors (__init__ in Python)?**
   - Special method called when creating an object instance

4. **Can you create objects without classes?**
   - In most languages no. Python allows some object creation without explicit classes

## Important Points

- ✅ Classes define the structure (attributes) and behavior (methods)
- ✅ Objects are instances of classes with actual values
- ✅ Constructor initializes object state
- ✅ Each object has its own independent state
- ✅ Classes promote code reusability

## Common Interview Scenarios

**Scenario**: Design a User Management System
```python
class User:
    user_count = 0  # Class variable (shared across all instances)
    
    def __init__(self, username, email):
        self.username = username  # Instance variable
        self.email = email
        self.created_at = None
        User.user_count += 1
    
    def update_profile(self, email):
        self.email = email
    
    @staticmethod
    def validate_email(email):
        return "@" in email

# Usage
user1 = User("john_doe", "john@example.com")
user2 = User("jane_smith", "jane@example.com")
print(User.user_count)  # Output: 2
```
