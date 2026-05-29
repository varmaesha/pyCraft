# Race Conditions

## Definition

**Race Condition**: When multiple threads access shared data simultaneously and the result depends on execution order.

**Problem**: Unpredictable behavior, data corruption, crashes.

**Root Cause**: Unsynchronized access to shared mutable state.

## Real-World Examples

### Example 1: Bank Account (Classic)

#### ❌ RACE CONDITION
```python
import threading

class BankAccount:
    def __init__(self, balance):
        self.balance = balance
    
    def withdraw(self, amount):
        # NOT THREAD-SAFE
        if self.balance >= amount:
            # Between check and update, another thread can run!
            self.balance -= amount
            return True
        return False

acc = BankAccount(1000)

def worker(account, amount):
    for _ in range(100):
        account.withdraw(amount)

# Two threads withdrawing
t1 = threading.Thread(target=worker, args=(acc, 10))
t2 = threading.Thread(target=worker, args=(acc, 10))

t1.start()
t2.start()
t1.join()
t2.join()

print(f"Expected: 0, Actual: {acc.balance}")
# Actual could be any number between 0-1000!
# RACE CONDITION!

# Race: 
# T1: if 1000 >= 10? YES
# T2: if 1000 >= 10? YES (T2 checks before T1 updates!)
# T1: balance = 1000 - 10 = 990
# T2: balance = 990 - 10 = 980
# Expected: 800, Actual: 980
```

#### ✅ SYNCHRONIZED
```python
import threading

class SafeBankAccount:
    def __init__(self, balance):
        self.balance = balance
        self.lock = threading.Lock()  # Add lock
    
    def withdraw(self, amount):
        with self.lock:  # Acquire lock
            if self.balance >= amount:
                self.balance -= amount
                return True
            return False
        # Lock released

acc = SafeBankAccount(1000)

# Same code...
def worker(account, amount):
    for _ in range(100):
        account.withdraw(amount)

t1 = threading.Thread(target=worker, args=(acc, 10))
t2 = threading.Thread(target=worker, args=(acc, 10))

t1.start()
t2.start()
t1.join()
t2.join()

print(f"Expected: 0, Actual: {acc.balance}")
# Now ALWAYS: 0
# NO RACE CONDITION!
```

### Example 2: Inventory Management

#### ❌ RACE CONDITION
```python
class Inventory:
    def __init__(self, stock):
        self.stock = stock
    
    def check_and_sell(self, quantity):
        # Race condition!
        if self.stock >= quantity:
            # Gap here - another sale can happen
            self.stock -= quantity
            return True
        return False

inv = Inventory(10)

def customer_transaction():
    for _ in range(5):
        inv.check_and_sell(3)  # Try to buy 3 units

# Multiple concurrent customers
threads = [threading.Thread(target=customer_transaction) for _ in range(5)]

for t in threads:
    t.start()
for t in threads:
    t.join()

# Tried to sell: 5 customers × 5 items × 3 units = 75 units
# Actual stock: 10 units!
# Could be negative!
print(f"Stock: {inv.stock}")  # Likely negative!
```

#### ✅ SYNCHRONIZED
```python
class SafeInventory:
    def __init__(self, stock):
        self.stock = stock
        self.lock = threading.Lock()
    
    def check_and_sell(self, quantity):
        with self.lock:
            if self.stock >= quantity:
                self.stock -= quantity
                return True
            return False

inv = SafeInventory(10)

# Same transaction code...
def customer_transaction():
    for _ in range(5):
        if inv.check_and_sell(3):
            print("Sale successful")
        else:
            print("Insufficient stock")

threads = [threading.Thread(target=customer_transaction) for _ in range(5)]

for t in threads:
    t.start()
for t in threads:
    t.join()

print(f"Stock: {inv.stock}")  # exactly 10! (blocked after 0)
```

### Example 3: Counter Increment

#### ❌ RACE CONDITION
```python
class Counter:
    def __init__(self):
        self.value = 0
    
    def increment(self):
        # This is NOT atomic!
        # Internally: READ value, ADD 1, WRITE value
        self.value += 1

counter = Counter()

def increment_100_times():
    for _ in range(100):
        counter.increment()

# 10 threads, each increments 100 times
# Expected: 1000
threads = [threading.Thread(target=increment_100_times) for _ in range(10)]

for t in threads:
    t.start()
for t in threads:
    t.join()

print(f"Expected: 1000, Actual: {counter.value}")
# Actual: Maybe 873, 945, 621...
# RACE CONDITION!

# Race:
# T1: READ value (100)
# T2: READ value (100) <- T2 sees same data!
# T1: ADD 1 → 101
# T2: ADD 1 → 101
# T1: WRITE 101
# T2: WRITE 101
# Lost one increment!
```

#### ✅ SYNCHRONIZED
```python
class SafeCounter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()
    
    def increment(self):
        with self.lock:
            self.value += 1  # Atomic now

counter = SafeCounter()

def increment_100_times():
    for _ in range(100):
        counter.increment()

threads = [threading.Thread(target=increment_100_times) for _ in range(10)]

for t in threads:
    t.start()
for t in threads:
    t.join()

print(f"Expected: 1000, Actual: {counter.value}")
# Now ALWAYS: 1000
```

### Example 4: Shared List Operations

#### ❌ RACE CONDITION
```python
class UnsafeQueue:
    def __init__(self):
        self.items = []
    
    def enqueue(self, item):
        self.items.append(item)
    
    def dequeue(self):
        if len(self.items) > 0:  # Check
            item = self.items[0]
            self.items = self.items[1:]  # Update
            return item
        return None

queue = UnsafeQueue()

def enqueuer():
    for i in range(50):
        queue.enqueue(i)

def dequeuer():
    for _ in range(50):
        queue.dequeue()

# Race: dequeuer might check empty, enqueuer adds, dequeuer finds item
# Or: dequeuer checks len > 0, but items gets popped before this line

t1 = threading.Thread(target=enqueuer)
t2 = threading.Thread(target=dequeuer)

t1.start()
t2.start()
t1.join()
t2.join()

# Items may be lost or duplicated!
```

#### ✅ SYNCHRONIZED
```python
import queue  # Python's thread-safe queue

# Or implement safely:
class SafeQueue:
    def __init__(self):
        self.items = []
        self.lock = threading.Lock()
    
    def enqueue(self, item):
        with self.lock:
            self.items.append(item)
    
    def dequeue(self):
        with self.lock:
            if len(self.items) > 0:
                item = self.items[0]
                self.items = self.items[1:]
                return item
        return None

# Now safe
```

## Race Condition Patterns

### Pattern 1: Check-Then-Act
```python
# ❌ BAD
if collection.contains(item):  # T2 removes before...
    collection.remove(item)    # ...we remove

# ✅ GOOD
with lock:
    if collection.contains(item):
        collection.remove(item)
```

### Pattern 2: Read-Modify-Write
```python
# ❌ BAD
value = shared_data  # T2 modifies after read
value += 1           # but before write
shared_data = value  # stale data written

# ✅ GOOD
with lock:
    shared_data += 1  # Atomic
```

### Pattern 3: Lazy Initialization
```python
# ❌ BAD
if instance is None:          # T2 checks at same time
    instance = create_object()

# ✅ GOOD
with lock:
    if instance is None:
        instance = create_object()
```

## Detecting Race Conditions

### Signs of Race Conditions
1. **Intermittent failures** - Works sometimes, fails randomly
2. **Timing-dependent bugs** - Slowing down revealing issues
3. **Data corruption** - Unexpected values
4. **Non-deterministic output** - Different results each run

### Testing for Race Conditions
```python
# Run many times
for i in range(1000):
    counter = Counter()
    threads = [threading.Thread(target=lambda: counter.increment()) 
               for _ in range(10)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    assert counter.value == 10, f"Failed at iteration {i}"
```

## Prevention Techniques

| Technique | Use Case | Cost |
|-----------|----------|------|
| **Locks** | Simple shared data | Overhead, deadlock risk |
| **Atomic Operations** | Read-modify-write | Fast, limited operations |
| **Immutable Data** | Shared objects | Memory, functional style |
| **Thread-Local Storage** | Per-thread data | Limits sharing |
| **Message Passing** | Complex interactions | Complexity |

## Key Interview Questions

1. **What's a race condition?**
   - Multiple threads access shared data, outcome depends on timing

2. **Example of race condition?**
   - Bank account (check-then-withdraw), counter increment

3. **How to prevent?**
   - Synchronization (locks), atomic operations, immutability

4. **Check-then-act problem?**
   - Between check and action, state can change - use locks together

## Important Points

- ✅ Lock before shared data access
- ✅ Keep locks short
- ✅ Use synchronized/concurrent collections
- ✅ Test concurrent code thoroughly
- ✅ Combine check + action atomically
- ⚠️ Locks can cause deadlocks
- ✅ Consider immutable data
- ✅ Use thread-safe structures (Queue, etc.)
