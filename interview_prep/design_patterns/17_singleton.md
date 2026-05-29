# Design Patterns - Singleton

## Definition

**Singleton** pattern ensures a class has only one instance and provides a global point of access to it.

## Use Cases

1. Database connections
2. Logger
3. Configuration manager
4. Thread pools
5. Cache managers

## Real-World Examples

### Example 1: Database Connection Pool
```python
class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = None
        return cls._instance
    
    def connect(self, db_url):
        if not self.connection:
            self.connection = f"Connected to {db_url}"
            print(f"Creating new connection: {self.connection}")
        return self.connection
    
    def query(self, sql):
        if self.connection:
            return f"Executing: {sql}"
        return "No connection"

# Usage
db1 = DatabaseConnection()
db2 = DatabaseConnection()

print(db1 is db2)  # True - same instance!
print(db1.connect("postgresql://localhost:5432"))
print(db2.query("SELECT * FROM users"))
# Both use the same connection
```

### Example 2: Logger System
```python
class Logger:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.logs = []
        return cls._instance
    
    def log(self, level, message):
        log_entry = f"[{level}] {message}"
        self.logs.append(log_entry)
        print(log_entry)
    
    def get_logs(self):
        return self.logs

# Usage
logger1 = Logger()
logger2 = Logger()

logger1.log("INFO", "Application started")
logger2.log("ERROR", "Database error")

print(logger1.get_logs())  # Both loggers share same list
# [INFO] Application started
# [ERROR] Database error
```

### Example 3: Configuration Manager
```python
import json

class ConfigManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.config = {}
        return cls._instance
    
    def load_config(self, config_file):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
    
    def get(self, key):
        return self.config.get(key)
    
    def set(self, key, value):
        self.config[key] = value

# Usage
config1 = ConfigManager()
config2 = ConfigManager()

config1.set("db_host", "localhost")
config1.set("db_port", 5432)

print(config2.get("db_host"))  # localhost - same config!
print(config2.get("db_port"))  # 5432
```

### Example 4: Thread-Safe Singleton (Using Metaclass)
```python
import threading

class SingletonMeta(type):
    _instances = {}
    _lock = threading.Lock()
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]

class APIClient(metaclass=SingletonMeta):
    def __init__(self):
        self.api_key = None
    
    def set_api_key(self, key):
        self.api_key = key
    
    def make_request(self, endpoint):
        return f"Calling {endpoint} with key {self.api_key}"

# Usage
api1 = APIClient()
api2 = APIClient()

print(api1 is api2)  # True - thread-safe singleton
api1.set_api_key("secret123")
print(api2.make_request("/users"))  # Uses same instance
```

### Example 5: Runtime-Secure Singleton (Decorator)
```python
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class EmailService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
    
    def send(self, to, subject, body):
        return f"Sending email to {to}: {subject}"

# Usage
email1 = EmailService()
email2 = EmailService()

print(email1 is email2)  # True
print(email1.send("user@example.com", "Welcome", "Hi there!"))
```

## Pros and Cons

| Pros | Cons |
|------|------|
| Single global instance | Hard to test (tightly coupled) |
| Lazy initialization possible | Hidden dependencies |
| Thread-safe (with proper impl) | Violates single responsibility |
| | Global state is evil |

## Anti-pattern Warning

```python
# ❌ BAD - Don't use for everything!
class BadSingleton:
    pass

# Just because something needs one instance 
# doesn't mean it should be a Singleton.
# Consider dependency injection instead.

# ✅ GOOD - Use dependency injection
class ServiceA:
    def __init__(self, logger):
        self.logger = logger

class ServiceB:
    def __init__(self, logger):
        self.logger = logger

# Inject same logger instance
logger = Logger()
service_a = ServiceA(logger)
service_b = ServiceB(logger)
```

## Key Interview Questions

1. **When should you use Singleton?**
   - Database connections, loggers, configuration managers

2. **Is Singleton a good pattern?**
   - Useful but can hide dependencies; prefer dependency injection

3. **How to make Singleton thread-safe?**
   - Use metaclass with locks or double-checked locking

4. **How to test code with Singleton?**
   - Difficult; consider using interfaces and dependency injection

## Important Points

- ✅ Ensures single instance
- ✅ Global access point
- ✅ Useful for shared resources
- ⚠️ Makes testing difficult
- ⚠️ Can hide dependencies
- ✅ Use with caution
