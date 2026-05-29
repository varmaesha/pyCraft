# Encapsulation

## Definition

**Encapsulation** is hiding internal details and only exposing what's necessary. It's the bundling of data (attributes) and methods together, with controlled access.

## Key Principle: Data Hiding

Control access to object's internal state using:
- **Public**: Accessible from anywhere
- **Protected**: Accessible within class and subclasses (prefixed with `_`)
- **Private**: Accessible only within the class (prefixed with `__`)

## Real-World Examples

### Example 1: Bank Account (Security)
Without encapsulation, anyone could directly change balance (security risk):

```python
# BAD - No encapsulation
class BankAccount:
    def __init__(self, balance):
        self.balance = balance  # Anyone can modify!

account = BankAccount(1000)
account.balance = 10000  # Hack! No security

# GOOD - With encapsulation
class SecureBankAccount:
    def __init__(self, initial_balance):
        self.__balance = initial_balance  # Private attribute
    
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            return f"Deposited ${amount}"
        return "Invalid amount"
    
    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            return f"Withdrew ${amount}"
        return "Insufficient funds"
    
    def get_balance(self):
        return self.__balance  # Read-only access

account = SecureBankAccount(1000)
account.deposit(500)
print(account.get_balance())  # 1500
# account.__balance = 10000  # Error! Cannot access private attribute
```

### Example 2: E-commerce Order System
```python
class Order:
    def __init__(self, order_id, customer_name):
        self.__order_id = order_id
        self.__customer_name = customer_name
        self.__items = []
        self.__status = "pending"
        self.__total = 0
    
    def add_item(self, item_name, price, quantity):
        if price > 0 and quantity > 0:
            self.__items.append({
                "name": item_name,
                "price": price,
                "quantity": quantity
            })
            self.__total += price * quantity
            return f"Added {quantity} {item_name}(s)"
        return "Invalid input"
    
    def process_payment(self, amount):
        if amount >= self.__total:
            self.__status = "completed"
            return f"Payment successful. Order completed."
        return "Insufficient payment"
    
    def get_order_summary(self):
        return {
            "order_id": self.__order_id,
            "customer": self.__customer_name,
            "total": self.__total,
            "status": self.__status
        }

order = Order("ORD001", "Alice")
order.add_item("Laptop", 1200, 1)
order.add_item("Mouse", 50, 2)
order.process_payment(1300)
print(order.get_order_summary())
# Output: {'order_id': 'ORD001', 'customer': 'Alice', 'total': 1300, 'status': 'completed'}
```

### Example 3: User Authentication
```python
class User:
    def __init__(self, username, password):
        self.__username = username
        self.__password = self.__hash_password(password)
        self.__is_authenticated = False
    
    def __hash_password(self, password):
        # Simulated hashing
        return f"hashed_{password}"
    
    def login(self, password):
        if self.__password == self.__hash_password(password):
            self.__is_authenticated = True
            return "Login successful"
        return "Invalid credentials"
    
    def is_logged_in(self):
        return self.__is_authenticated
    
    def get_username(self):
        return self.__username

user = User("john_doe", "secret123")
print(user.login("secret123"))      # Login successful
print(user.is_logged_in())          # True
# user.__password = "new_hash"      # Error! Cannot access
```

## Benefits of Encapsulation

| Benefit | Example |
|---------|---------|
| **Security** | Prevents unauthorized access to sensitive data |
| **Control** | Validate data before changes (amount > 0) |
| **Flexibility** | Can change internal implementation without affecting clients |
| **Maintainability** | Changes to private attributes don't break external code |

## Key Interview Questions

1. **What's the difference between private, protected, and public?**
   - Private: Only within class | Protected: Class + subclasses | Public: Anywhere

2. **Why hide attributes if we expose them via methods anyway?**
   - Because methods can include validation and business logic

3. **How does encapsulation differ from abstraction?**
   - Encapsulation: HOW to hide data | Abstraction: WHAT to expose to user

## Important Points

- ✅ Use private attributes (`__`) for sensitive data
- ✅ Provide public methods (`get_`, `set_`) to access data safely
- ✅ Add validation in setter methods
- ✅ Don't expose implementation details
- ✅ Follow principle of least privilege
