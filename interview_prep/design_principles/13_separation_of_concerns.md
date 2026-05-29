# Separation of Concerns

## Definition

**Separation of Concerns (SoC)**: Each component should have a single, well-defined responsibility. Different concerns should be handled by different modules.

## Key Idea

Mix of multiple concerns in one place leads to:
- Hard to understand
- Hard to test
- Hard to reuse
- Hard to change

## Real-World Examples

### Example 1: E-commerce Order Processing

#### ❌ MIXED CONCERNS
```python
class Order:
    def __init__(self, items, customer_email):
        self.items = items
        self.customer_email = customer_email
        self.total = 0
    
    def process(self):
        # Business logic mixed with presentation, persistence, notification
        
        # Calculation (Business Logic)
        for item in self.items:
            self.total += item.price
        
        # Presentation (UI concern)
        print(f"Order Total: ${self.total}")
        
        # Persistence (Database concern)
        db = MySQLConnection()
        db.execute(f"INSERT INTO orders VALUES ('{self.total}')")
        
        # Notification (Email concern)
        import smtplib
        smtplib.SMTP().sendmail(self.customer_email, "Order confirmed")
        
        # Logging (Logging concern)
        with open("orders.log", "a") as f:
            f.write(f"Order processed: {self.total}")

# Problems:
# 1. Order class does 5 different things
# 2. Hard to test (need DB, email, file)
# 3. Hard to reuse (coupled to persistence)
# 4. Hard to change (ripple effects)
```

#### ✅ SEPARATED CONCERNS
```python
# 1. Business Logic - Order
class Order:
    def __init__(self, items):
        self.items = items
    
    def calculate_total(self):
        return sum(item.price for item in self.items)

# 2. Persistence - OrderRepository
class OrderRepository:
    def save(self, order, order_id):
        db = MySQLConnection()
        total = order.calculate_total()
        db.execute(f"INSERT INTO orders VALUES ('{order_id}', '{total}')")

# 3. Notification - OrderNotifier
class OrderNotifier:
    def notify_confirmation(self, customer_email, order):
        total = order.calculate_total()
        send_email(customer_email, f"Order confirmed: ${total}")

# 4. Logging - OrderLogger
class OrderLogger:
    def log_order(self, order):
        total = order.calculate_total()
        with open("orders.log", "a") as f:
            f.write(f"Order processed: {total}\n")

# 5. Orchestration - OrderService
class OrderService:
    def __init__(self, repository, notifier, logger):
        self.repository = repository
        self.notifier = notifier
        self.logger = logger
    
    def process_order(self, order, order_id, customer_email):
        self.repository.save(order, order_id)
        self.notifier.notify_confirmation(customer_email, order)
        self.logger.log_order(order)

# Usage
order = Order([Item("Book", 29.99), Item("Pen", 5.99)])
service = OrderService(OrderRepository(), OrderNotifier(), OrderLogger())
service.process_order(order, "ORD001", "customer@example.com")

# Now each class has single responsibility!
```

### Example 2: User Authentication & Authorization

#### ❌ MIXED CONCERNS
```python
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.roles = []
    
    def login(self, provided_password):
        # Authentication (verify identity)
        if self.password != self._hash(provided_password):
            return False
        
        # Authorization (check permissions)
        if "admin" not in self.roles:
            return False
        
        # Session management
        import time
        self.session_id = str(time.time())
        
        # Logging
        print(f"User {self.username} logged in")
        
        return True
    
    def _hash(self, password):
        return f"hashed_{password}"

# Problems: One class handles 4 concerns
```

#### ✅ SEPARATED CONCERNS
```python
# 1. Authentication - AuthenticationService
class AuthenticationService:
    def verify_credentials(self, username, password, stored_hash):
        return stored_hash == self._hash(password)
    
    def _hash(self, password):
        return f"hashed_{password}"

# 2. Authorization - AuthorizationService
class AuthorizationService:
    def has_permission(self, user_roles, required_role):
        return required_role in user_roles

# 3. Session Management - SessionManager
class SessionManager:
    def create_session(self, user_id):
        import time
        return str(time.time())

# 4. User - Just stores user data
class User:
    def __init__(self, user_id, username, password_hash, roles):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.roles = roles

# 5. Orchestration - LoginService
class LoginService:
    def __init__(self, auth_service, authz_service, session_mgr, logger):
        self.auth_service = auth_service
        self.authz_service = authz_service
        self.session_mgr = session_mgr
        self.logger = logger
    
    def login(self, user, provided_password):
        # Authenticate
        if not self.auth_service.verify_credentials(user.username, provided_password, user.password_hash):
            self.logger.log(f"Failed login for {user.username}")
            return None
        
        # Authorize
        if not self.authz_service.has_permission(user.roles, "user"):
            self.logger.log(f"Unauthorized: {user.username}")
            return None
        
        # Create session
        session_id = self.session_mgr.create_session(user.user_id)
        self.logger.log(f"Login successful: {user.username}")
        
        return session_id
```

### Example 3: MVC Pattern (Separation by Concern)

```python
# MODEL - Business Logic & Data
class Product:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price
    
    def calculate_discount(self, discount_percent):
        return self.price * (1 - discount_percent / 100)

class ProductRepository:
    def save(self, product):
        # Database persistence
        pass
    
    def find_by_id(self, id):
        # Database retrieval
        pass

# VIEW - Presentation
class ProductView:
    def display_product(self, product):
        return f"Product: {product.name} - ${product.price}"
    
    def display_discounted_price(self, product, discount):
        price = product.calculate_discount(discount)
        return f"Discounted Price: ${price}"

# CONTROLLER - Orchestration
class ProductController:
    def __init__(self, repository, view):
        self.repository = repository
        self.view = view
    
    def show_product(self, product_id):
        product = self.repository.find_by_id(product_id)
        return self.view.display_product(product)
    
    def show_discounted(self, product_id, discount):
        product = self.repository.find_by_id(product_id)
        return self.view.display_discounted_price(product, discount)

# Each layer has clear responsibility
```

## Concerns to Separate

| Concern | Responsible Component |
|---------|---------------------|
| **Business Logic** | Service/Domain class |
| **Persistence** | Repository/DAO |
| **Presentation** | View/Controller |
| **Logging** | Logger |
| **Configuration** | Config class |
| **Error Handling** | Exception handlers |
| **Validation** | Validator |
| **Authentication** | Auth service |
| **Authorization** | Authz service |
| **Caching** | Cache manager |

## Architecture Patterns Based on SoC

### Layered Architecture
```
┌─────────────────────┐
│  Presentation Layer │
├─────────────────────┤
│  Business Layer     │
├─────────────────────┤
│  Persistence Layer  │
├─────────────────────┤
│  Database           │
└─────────────────────┘
```

### Hexagonal Architecture (Ports & Adapters)
```
        Domain
           ↑
    ┌──────┴──────┐
    ↓             ↓
Controllers    Repositories
(UI Adapter)   (Database Adapter)
```

## Benefits of Separation of Concerns

✅ **Testability**: Test each concern independently
✅ **Reusability**: Reuse components in different contexts
✅ **Maintainability**: Changes isolated to one place
✅ **Clarity**: Each class has clear purpose
✅ **Team Collaboration**: Different teams handle different concerns
✅ **Scalability**: Easy to scale specific layers

## Anti-patterns (What to Avoid)

❌ **God Objects**: Do everything
❌ **Spaghetti Code**: Logic scattered everywhere
❌ **Transaction Scripts**: One function for one use case (with all logic)
❌ **Anemic Models**: Model with just getters/setters, logic elsewhere
❌ **Feature Envy**: Component accessing other component's internals

## Key Interview Questions

1. **What is Separation of Concerns?**
   - Each component should handle one responsibility

2. **How does SoC relate to Single Responsibility?**
   - SoC is broader (architectural) | SRP is narrower (class-level)

3. **Real-world example of SoC?**
   - MVC: Model, View, Controller are separate concerns

4. **How to identify if concerns are mixed?**
   - Class name has "and" (UserAndEmail) | Multiple reasons to change

## Important Points

- ✅ Each class should have one primary concern
- ✅ Separate persistence from business logic
- ✅ Separate presentation from business logic
- ✅ Use layers/modules to organize concerns
- ✅ Makes testing much easier
- ✅ Improves code reusability
