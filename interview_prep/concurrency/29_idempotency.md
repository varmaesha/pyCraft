# Idempotency in Distributed Systems

## Definition

**Idempotent Operation**: Calling it multiple times produces same result as calling once.

**Formula**: f(f(x)) = f(x)

**Purpose**: Safe retries in distributed systems without side effects.

## Real-World Examples

### Example 1: Payment Processing

#### ❌ NOT IDEMPOTENT
```python
class PaymentProcessor:
    def __init__(self):
        self.charges = []
    
    def charge_card(self, card_id, amount):
        # NOT idempotent - charges multiple times
        self.charges.append({"card": card_id, "amount": amount})
        print(f"Charged ${amount}")
        return True

processor = PaymentProcessor()

# First attempt
result = processor.charge_card("card_123", 100)  # Charged: $100

# Network timeout - client retries
result = processor.charge_card("card_123", 100)  # Charged: $100 again!
result = processor.charge_card("card_123", 100)  # Charged: $100 AGAIN!

print(processor.charges)  # Three charges for one order!
# PROBLEM: Duplicate charges!
```

#### ✅ IDEMPOTENT
```python
class IdempotentPaymentProcessor:
    def __init__(self):
        self.charges = {}  # transaction_id -> charge
    
    def charge_card(self, transaction_id, card_id, amount):
        # Idempotent - check if already processed
        if transaction_id in self.charges:
            print(f"Already processed: {transaction_id}")
            return self.charges[transaction_id]
        
        # Process once
        charge = {"card": card_id, "amount": amount}
        self.charges[transaction_id] = charge
        print(f"Charged ${amount}")
        return charge

processor = IdempotentPaymentProcessor()

# First attempt
result = processor.charge_card("txn_001", "card_123", 100)
# Output: Charged $100

# Network timeout - client retries with SAME transaction_id
result = processor.charge_card("txn_001", "card_123", 100)
# Output: Already processed: txn_001 (No duplicate charge!)

result = processor.charge_card("txn_001", "card_123", 100)
# Output: Already processed: txn_001 (Still no duplicate!)

# Different transaction
result = processor.charge_card("txn_002", "card_123", 100)
# Output: Charged $100

print(processor.charges)  # Only TWO charges!
```

### Example 2: Create Resource (API)

#### ❌ NOT IDEMPOTENT
```python
class UserService:
    def __init__(self):
        self.users = {}
        self.next_id = 1
    
    def create_user(self, name, email):
        # NOT idempotent - creates new user each time
        user_id = self.next_id
        self.next_id += 1
        self.users[user_id] = {"name": name, "email": email}
        return {"id": user_id, "name": name}

service = UserService()

# First attempt
result = service.create_user("John", "john@example.com")
# Result: {"id": 1, "name": "John"}

# Network timeout - client retries
result = service.create_user("John", "john@example.com")
# Result: {"id": 2, "name": "John"}  # DIFFERENT ID!

result = service.create_user("John", "john@example.com")
# Result: {"id": 3, "name": "John"}  # YET ANOTHER!

print(service.users)  # Three users with same data!
```

#### ✅ IDEMPOTENT
```python
class IdempotentUserService:
    def __init__(self):
        self.users = {}
        self.next_id = 1
        self.request_log = {}  # request_id -> result
    
    def create_user(self, request_id, name, email):
        # Idempotent - check if already processed
        if request_id in self.request_log:
            print(f"Already processed: {request_id}")
            return self.request_log[request_id]
        
        # Create user
        user_id = self.next_id
        self.next_id += 1
        self.users[user_id] = {"name": name, "email": email}
        result = {"id": user_id, "name": name}
        
        # Log request
        self.request_log[request_id] = result
        return result

service = IdempotentUserService()

# First attempt
result = service.create_user("req_001", "John", "john@example.com")
# Result: {"id": 1, "name": "John"}

# Retry with SAME request_id
result = service.create_user("req_001", "John", "john@example.com")
# Output: Already processed: req_001
# Result: {"id": 1, "name": "John"}  # SAME ID!

result = service.create_user("req_001", "John", "john@example.com")
# Output: Already processed: req_001
# Result: {"id": 1, "name": "John"}  # STILL SAME!

# Different request
result = service.create_user("req_002", "Jane", "jane@example.com")
# Result: {"id": 2, "name": "Jane"}

print(service.users)  # Only TWO users!
```

### Example 3: HTTP Methods

#### HTTP Idempotency
```
GET        /users/1        # Idempotent - always returns same user
PUT        /users/1        # Idempotent - replaces user (same result each time)
DELETE     /users/1        # Idempotent - delete same resource (success or 404)
POST       /users          # NOT idempotent - creates new resource each time
PATCH      /users/1        # Typically NOT idempotent (applies changes)
```

#### Safe Design
```python
# ❌ Bad API
POST /users          # Creates new user

# Better version
POST /users?idempotency_key=unique_id  # Idempotent create

# Safe operations
GET    /users/1      # Always safe/idempotent
PUT    /users/1      # Safe - replaces entire resource
DELETE /users/1      # Safe - no side effects from retry
```

### Example 4: Distributed Transaction

#### Order Service Example
```python
class OrderService:
    def __init__(self):
        self.orders = {}
        self.processed_requests = {}
    
    def create_order(self, request_id, user_id, items):
        # Idempotent order creation
        if request_id in self.processed_requests:
            return self.processed_requests[request_id]
        
        # Create order atomically
        order_id = generate_id()
        order = {
            "id": order_id,
            "user_id": user_id,
            "items": items,
            "status": "created"
        }
        
        self.orders[order_id] = order
        result = {"order_id": order_id, "status": "success"}
        self.processed_requests[request_id] = result
        
        return result

# Usage
service = OrderService()

# First attempt
result = service.create_order("req_123", "user_456", ["item1", "item2"])
# Result: {"order_id": "ord_789", "status": "success"}

# Timeout - retry server
result = service.create_order("req_123", "user_456", ["item1", "item2"])
# Returns cached result: {"order_id": "ord_789", "status": "success"}
# Same order created!

# Retry client-side still works - same result
```

## Implementation Techniques

### Technique 1: Idempotency Keys

```python
import uuid
import hashlib

class Service:
    def  __init__(self):
        self.processed = {}
    
    def operation(self, idempotency_key, data):
        # Check if already processed
        if idempotency_key in self.processed:
            return self.processed[idempotency_key]
        
        # Perform operation
        result = self._do_operation(data)
        
        # Cache result
        self.processed[idempotency_key] = result
        return result
    
    def _do_operation(self, data):
        return {"status": "success"}

# Usage with UUID
service = Service()
key = str(uuid.uuid4())
result = service.operation(key, {"amount": 100})
result = service.operation(key, {"amount": 100})  # Same result
```

### Technique 2: Checksum/Hash

```python
class FileUploadService:
    def __init__(self):
        self.uploaded = {}
    
    def upload_file(self, user_id, filename, content):
        # Generate checksum
        checksum = hashlib.md5(content).hexdigest()
        key = f"{user_id}:{filename}:{checksum}"
        
        # Check if already uploaded
        if key in self.uploaded:
            return {"file_id": self.uploaded[key], "status": "already_exists"}
        
        # Upload
        file_id = save_to_storage(filename, content)
        self.uploaded[key] = file_id
        return {"file_id": file_id, "status": "uploaded"}

# Same file uploaded twice = only once in storage
```

### Technique 3: Natural Keys/IDs

```python
class UserService:
    def __init__(self):
        self.users = {}
    
    def create_or_update_user(self, email, name, age):
        # Email is natural key - idempotent!
        user = {
            "email": email,
            "name": name,
            "age": age
        }
        self.users[email] = user  # Overwrites if exists
        return user

# Create
service.create_or_update_user("john@example.com", "John", 30)
# Retry - same result
service.create_or_update_user("john@example.com", "John", 30)
# No duplicate!
```

## Idempotency in Design

### REST API Guidelines
```python
# Idempotent operations (safe for retry)
GET     /resource      # Query data
HEAD    /resource      # Check existence
PUT     /resource/:id  # Replace entire resource
DELETE  /resource/:id  # Remove resource

# Non-idempotent (needs idempotency key)
POST    /resource      # Create new

# Solution
POST    /resource?idempotency_key=unique_id  # Now idempotent
```

### Message Queue Example
```python
class MessageHandler:
    def __init__(self):
        self.processed_messages = set()
    
    def handle_message(self, message_id, data):
        # Check if already processed
        if message_id in self.processed_messages:
            return  # Skip duplicate
        
        # Process
        self._process(data)
        
        # Mark processed
        self.processed_messages.add(message_id)

# Even if message delivered twice, handle once
```

## When Idempotency Matters

| Scenario | Importance |
|----------|-----------|
| **Network Retries** | CRITICAL |
| **Distributed Systems** | CRITICAL |
| **Payment Processing** | CRITICAL |
| **Resource Creation** | HIGH |
| **Order Management** | HIGH |
| **Data Mutations** | MEDIUM |
| **Read Operations** | Not needed |

## Key Interview Questions

1. **What's idempotency?**
   - Operation produces same result regardless of repetition

2. **Why important in systems?**
   - Safe retries, handles network failures gracefully

3. **Implement idempotent payment?**
   - Use transaction ID, track processed transactions

4. **Idempotency key design?**
   - Unique per request, stable, deterministic

## Important Points

- ✅ Use idempotency keys for mutations
- ✅ Log processed requests
- ✅ Handle duplicates gracefully
- ✅ Design for safe retries
- ✅ Crucial for distributed systems
- ✅ Every mutation should be idempotent
- ✅ Test retry scenarios
