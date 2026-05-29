# Immutable Objects

## Definition

**Immutable Objects** cannot be changed after creation. State is fixed throughout lifetime.

## Benefits

1. **Thread-Safe**: No synchronization needed
2. **Hashable**: Can use as dictionary keys
3. **Caching**: Safe to cache
4. **Predictable**: No unexpected changes

## Real-World Examples

### Example 1: Immutable String
```python
# Strings are immutable in Python
s1 = "Hello"
s2 = s1.upper()  # Creates new string
print(s1)  # "Hello" - unchanged
print(s2)  # "HELLO" - new object

# Immutable integers
x = 5
y = x + 3  # Creates new integer, doesn't modify x
print(x)  # 5 - unchanged
```

### Example 2: Creating Immutable User Class
```python
from dataclasses import dataclass

@dataclass(frozen=True)  # Makes class immutable
class User:
    user_id: int
    name: str
    email: str

# Usage
user = User(1, "Alice", "alice@example.com")
print(user.name)  # Alice

# Cannot be modified
try:
    user.name = "Bob"  # TypeError
except TypeError as e:
    print(f"Cannot modify: {e}")
```

### Example 3: Immutable Point Class
```python
class ImmutablePoint:
    def __init__(self, x, y):
        self._x = x
        self._y = y
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    def move(self, dx, dy):
        # Return new Point instead of modifying
        return ImmutablePoint(self._x + dx, self._y + dy)
    
    def __eq__(self, other):
        return self._x == other._x and self._y == other._y
    
    def __hash__(self):
        return hash((self._x, self._y))
    
    def __str__(self):
        return f"Point({self._x}, {self._y})"

# Usage
p1 = ImmutablePoint(0, 0)
p2 = p1.move(3, 4)  # Creates new point

print(p1)  # Point(0, 0)
print(p2)  # Point(3, 4)

# Can use as dict key
points = {p1: "origin", p2: "somewhere"}
print(points[p1])  # origin
```

### Example 4: Immutable Configuration
```python
class AppConfig:
    def __init__(self, app_name, version, debug, port):
        self._app_name = app_name
        self._version = version
        self._debug = debug
        self._port = port
        # Prevent future attributes
        self.__dict__['_frozen'] = True
    
    @property
    def app_name(self):
        return self._app_name
    
    @property
    def version(self):
        return self._version
    
    @property
    def debug(self):
        return self._debug
    
    @property
    def port(self):
        return self._port
    
    def __setattr__(self, name, value):
        if hasattr(self, '_frozen'):
            raise AttributeError("Configuration is immutable")
        super().__setattr__(name, value)
    
    def with_debug(self, debug):
        # Return new config with changed value
        return AppConfig(self._app_name, self._version, debug, self._port)
    
    def __repr__(self):
        return f"AppConfig({self._app_name} v{self._version}, debug={self._debug})"

# Usage
config = AppConfig("MyApp", "1.0", False, 8000)
print(config)  # AppConfig(MyApp v1.0, debug=False)

# Cannot modify
try:
    config.port = 9000  # AttributeError
except AttributeError as e:
    print(f"Error: {e}")

# Create new config with change
debug_config = config.with_debug(True)
print(debug_config)  # AppConfig(MyApp v1.0, debug=True)
print(config)       # MyApp v1.0, debug=False (original unchanged)
```

### Example 5: Immutable Money Class
```python
class Money:
    def __init__(self, amount, currency):
        self._amount = amount
        self._currency = currency
    
    @property
    def amount(self):
        return self._amount
    
    @property
    def currency(self):
        return self._currency
    
    def add(self, other):
        if self._currency != other._currency:
            raise ValueError("Different currencies")
        return Money(self._amount + other._amount, self._currency)
    
    def subtract(self, other):
        if self._currency != other._currency:
            raise ValueError("Different currencies")
        return Money(self._amount - other._amount, self._currency)
    
    def __eq__(self, other):
        return self._amount == other._amount and self._currency == other._currency
    
    def __hash__(self):
        return hash((self._amount, self._currency))
    
    def __str__(self):
        return f"{self._currency} {self._amount}"

# Usage
money1 = Money(100, "USD")
money2 = Money(50, "USD")

total = money1.add(money2)
print(total)     # USD 150
print(money1)    # USD 100 (unchanged)
print(money2)    # USD 50 (unchanged)

# Can use in sets
wallet = {money1, money2}
print(len(wallet))  # 2
```

### Example 6: Thread-Safe Immutable Registry
```python
import threading

class UserRegistry:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._users = {}
        return cls._instance
    
    def register_user(self, user):
        # Immutable user objects
        self._users[user.user_id] = user
    
    def get_user(self, user_id):
        return self._users.get(user_id)
    
    def list_users(self):
        return tuple(self._users.values())  # Return tuple (immutable list)

@dataclass(frozen=True)
class User:
    user_id: int
    name: str
    email: str

# Usage - Thread-safe, no locks needed due to immutability
registry = UserRegistry()

user1 = User(1, "Alice", "alice@example.com")
user2 = User(2, "Bob", "bob@example.com")

registry.register_user(user1)
registry.register_user(user2)

print(registry.get_user(1))  # User(1, Alice, alice@example.com)
```

## Immutable vs Mutable

| Aspect | Immutable | Mutable |
|--------|-----------|---------|
| **Thread-Safe** | Yes (no locks) | No (needs sync) |
| **Hashable** | Yes | No (usually) |
| **Flexibility** | Less | More |
| **Performance** | Faster (no sync) | Slower (sync) |
| **Memory** | More (copies) | Less |

## When to Use Immutable Objects

- ✅ Configuration/settings
- ✅ Domain entities (value objects)
- ✅ Thread-safe collections
- ✅ Dictionary/set keys
- ✅ Multi-threaded applications
- ❌ Large collections (memory overhead)
- ❌ Frequently changing objects

## Key Interview Questions

1. **Why make objects immutable?**
   - Thread-safety, predictability, hashability

2. **How to make class immutable?**
   - Use dataclass(frozen=True) or override __setattr__

3. **Cost of immutability?**
   - Memory overhead from creating copies

4. **Immutable vs Encapsulation?**
   - Both control modifications, immutable prevents all changes

## Important Points

- ✅ Immutable objects are inherently thread-safe
- ✅ Can be used as dictionary keys
- ✅ Great for value objects
- ✅ Python: strings, tuples, frozen sets are immutable
- ✅ Use dataclasses for easy immutability
- ⚠️ Trade-off: memory vs safety and simplicity
