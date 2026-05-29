# Proxy Pattern

## Definition

**Proxy Pattern**: Provide a surrogate/placeholder for another object to control access to it.

**Purpose**: Control access, add caching, lazy loading, logging, or security checks.

**Key Idea**: Pass requests through proxy before reaching real object.

## Real-World Examples

### Example 1: Lazy Loading (Expensive Resource)

#### ❌ WITHOUT PROXY
```python
class Image:
    def __init__(self, filename):
        self.filename = filename
        # Loads immediately - slow if many images
        self.data = self._load_from_disk()
    
    def _load_from_disk(self):
        print(f"Loading {self.filename} from disk...")
        import time
        time.sleep(2)  # Expensive operation
        return f"Image data: {self.filename}"
    
    def display(self):
        print(self.data)

# All images load immediately
images = [Image(f"photo_{i}.jpg") for i in range(100)]  # 200 seconds!
# Only display 1
images[0].display()

# Problem: Wasted resources
```

#### ✅ WITH PROXY (Lazy Loading)
```python
class Image:
    def __init__(self, filename):
        self.filename = filename
    
    def display(self):
        print("Displaying image...")

class ProxyImage:
    def __init__(self, filename):
        self.filename = filename
        self.real_image = None
    
    def display(self):
        # Load only when accessed
        if self.real_image is None:
            self.real_image = RealImage(self.filename)
        self.real_image.display()

class RealImage(Image):
    def __init__(self, filename):
        self.filename = filename
        self._load_from_disk()
    
    def _load_from_disk(self):
        print(f"Loading {self.filename} from disk...")
        import time
        time.sleep(0.5)
        self.data = f"Image data: {self.filename}"
    
    def display(self):
        print(self.data)

# Create proxies - no loading
images = [ProxyImage(f"photo_{i}.jpg") for i in range(100)]  # Instant!

# Load only when needed
images[0].display()  # Actually loads
images[0].display()  # Uses cached version

# Problem solved: Only load what's used
```

### Example 2: Access Control (Protection Proxy)

#### ❌ WITHOUT PROXY
```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance
    
    def withdraw(self, amount):
        self.balance -= amount
        return self.balance
    
    def get_balance(self):
        return self.balance

# Anyone can access
account = BankAccount("John", 1000)
account.withdraw(500)  # No permission check
print(account.balance)

# Problem: No security
```

#### ✅ WITH PROXY (Access Control)
```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance
    
    def withdraw(self, amount):
        self.balance -= amount
        return self.balance
    
    def get_balance(self):
        return self.balance

class BankAccountProxy:
    def __init__(self, account: BankAccount, password):
        self.account = account
        self.password = password
        self.authenticated = False
    
    def authenticate(self, pwd):
        if pwd == self.password:
            self.authenticated = True
            return True
        return False
    
    def withdraw(self, amount):
        if not self.authenticated:
            raise Exception("Not authenticated!")
        if amount > self.account.balance:
            raise Exception("Insufficient funds!")
        return self.account.withdraw(amount)
    
    def get_balance(self):
        if not self.authenticated:
            raise Exception("Not authenticated!")
        return self.account.get_balance()

# Usage with protection
account = BankAccountProxy(BankAccount("John", 1000), "secret123")

# Try without authentication
try:
    account.withdraw(500)  # Fails!
except Exception as e:
    print(f"Error: {e}")

# Authenticate first
account.authenticate("secret123")
print(account.withdraw(500))  # Success
print(account.get_balance())   # 500

# Problem solved: Secure access
```

### Example 3: Caching Proxy

#### ✅ WITH PROXY (Caching)
```python
class DataService:
    def get_user(self, user_id):
        print(f"Fetching user {user_id} from database...")
        import time
        time.sleep(1)  # Slow database query
        return {"id": user_id, "name": f"User {user_id}"}

class CachedDataService:
    def __init__(self, service: DataService):
        self.service = service
        self.cache = {}
    
    def get_user(self, user_id):
        if user_id in self.cache:
            print(f"Cache hit for user {user_id}")
            return self.cache[user_id]
        
        print(f"Cache miss for user {user_id}")
        user = self.service.get_user(user_id)
        self.cache[user_id] = user
        return user
    
    def clear_cache(self):
        self.cache.clear()

# Usage
service = CachedDataService(DataService())

# First call - slow (database)
user1 = service.get_user(1)  # Fetched from database

# Second call - fast (cache)
user2 = service.get_user(1)  # Cache hit!

# Different user - slow
user3 = service.get_user(2)  # Fetched from database

# Same user - fast
user4 = service.get_user(2)  # Cache hit!

# Problem solved: Reduce database calls
```

### Example 4: Remote Object Proxy

#### ✅ WITH PROXY (Remote Server Access)
```python
# Real object on remote server
class RemoteImageService:
    def __init__(self, server_url):
        self.server_url = server_url
    
    def download_image(self, image_id):
        print(f"Downloading image {image_id} from {self.server_url}...")
        import time
        time.sleep(1)  # Network latency
        return f"Image data: {image_id}"

# Proxy - local representation
class ImageProxy:
    def __init__(self, server_url):
        self.server_url = server_url
        self.remote_service = None
        self.cache = {}
    
    def get_image(self, image_id):
        # Use cache if available
        if image_id in self.cache:
            print(f"Using cached image {image_id}")
            return self.cache[image_id]
        
        # Lazy initialize remote service
        if self.remote_service is None:
            self.remote_service = RemoteImageService(self.server_url)
        
        # Download and cache
        image = self.remote_service.download_image(image_id)
        self.cache[image_id] = image
        return image

# Usage
proxy = ImageProxy("https://api.example.com")

# First request - downloads
image1 = proxy.get_image(1)

# Second request - cached
image2 = proxy.get_image(1)

# Different image - downloads
image3 = proxy.get_image(2)

# Problem solved: Efficient remote access
```

### Example 5: Logging Proxy

#### ✅ WITH PROXY (Logging)
```python
class PaymentProcessor:
    def process(self, amount, card):
        print(f"Processing ${amount} with card {card}")
        return {"status": "success", "transaction_id": "tx_123"}

class LoggingPaymentProxy:
    def __init__(self, processor: PaymentProcessor):
        self.processor = processor
    
    def process(self, amount, card):
        # Log before
        print(f"[LOG] Processing payment: ${amount}")
        print(f"[LOG] Card type: {card[:4]}****")
        
        try:
            result = self.processor.process(amount, card)
            print(f"[LOG] Payment successful")
            return result
        except Exception as e:
            print(f"[LOG] Payment failed: {e}")
            raise

# Usage
processor = LoggingPaymentProxy(PaymentProcessor())
result = processor.process(99.99, "4111111111111111")

# All operations are logged
```

## Types of Proxies

| Type | Purpose | Example |
|------|---------|---------|
| **Virtual Proxy** | Lazy loading | Image loading on demand |
| **Protection Proxy** | Access control | Password-protected account |
| **Remote Proxy** | Remote object access | Web API client |
| **Logging Proxy** | Audit trail | Transaction logging |
| **Caching Proxy** | Performance | Cached database results |
| **Smart Reference** | Reference counting | Garbage collection help |

## Proxy vs Decorator

| Aspect | Proxy | Decorator |
|--------|-------|-----------|
| **Purpose** | Control access | Add behavior |
| **Client Awareness** | Transparent | Intentional wrapping |
| **Modification** | May not call real | Always calls real |
| **Use Case** | Protection, lazy, caching | Enhancement |

## Key Interview Questions

1. **What does Proxy pattern do?**
   - Controls access to another object

2. **Types of proxy?**
   - Virtual, Protection, Remote, Logging, Caching

3. **Example of virtual proxy?**
   - Lazy loading images until needed

4. **Proxy vs Decorator?**
   - Proxy controls access, Decorator adds behavior

5. **When to use Proxy?**
   - Lazy loading, access control, caching, remote objects

## Important Points

- ✅ Use for lazy loading / caching
- ✅ Use for access control
- ✅ Use for remote object access
- ✅ Transparent to client
- ✅ Maintains same interface
- ⚠️ Adds complexity
- ✅ Performance optimization tool
- ✅ Security enforcement tool
