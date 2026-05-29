# Concurrency & Thread Safety

## Definition

**Thread Safety** ensures that shared resources are accessed in a way that prevents race conditions and maintains data consistency.

## Key Concepts

### Race Condition
Multiple threads access shared resource without synchronization, leading to unpredictable results.

```python
# ❌ BAD - Race Condition
import threading

class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance
    
    def withdraw(self, amount):
        # Not thread-safe!
        if self.balance >= amount:
            self.balance -= amount

account = BankAccount(1000)

def withdraw_worker():
    for _ in range(100):
        account.withdraw(10)

threads = [threading.Thread(target=withdraw_worker) for _ in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(account.balance)  # Could be any value!
```

### Solution 1: Lock/Mutex
```python
# ✅ GOOD - Using Lock
import threading

class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance
        self.lock = threading.Lock()
    
    def withdraw(self, amount):
        with self.lock:  # Acquire lock
            if self.balance >= amount:
                self.balance -= amount
                return True
        return False  # Release lock automatically

account = BankAccount(1000)

def withdraw_worker():
    for _ in range(100):
        account.withdraw(10)

threads = [threading.Thread(target=withdraw_worker) for _ in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(account.balance)  # Always consistent
```

## Synchronization Mechanisms

### 1. Lock (Mutual Exclusion)
```python
import threading

lock = threading.Lock()

def critical_section():
    with lock:
        # Only one thread can execute this at a time
        print("Critical section")

# Safe for concurrent access
threads = [threading.Thread(target=critical_section) for _ in range(5)]
for t in threads:
    t.start()
```

### 2. RLock (Reentrant Lock)
```python
# Allows same thread to acquire lock multiple times
rl = threading.RLock()

def recursive_function():
    with rl:
        print("Enter")
        # Can safely call itself
        nested_function()

def nested_function():
    with rl:  # Same thread can acquire again
        print("Nested")
```

### 3. Semaphore (Resource Pool)
```python
# Limit number of threads accessing resource
semaphore = threading.Semaphore(2)  # Max 2 concurrent

def use_resource():
    with semaphore:
        print("Using resource")
        # Only 2 threads at a time

threads = [threading.Thread(target=use_resource) for _ in range(10)]
for t in threads:
    t.start()
```

### 4. Condition Variable (Wait/Notify)
```python
import threading

condition = threading.Condition()
data = []

def producer():
    global data
    for i in range(5):
        with condition:
            data.append(i)
            print(f"Produced {i}")
            condition.notify_all()  # Wake up consumers

def consumer():
    global data
    while True:
        with condition:
            while not data:
                condition.wait()  # Sleep until notified
            item = data.pop()
            print(f"Consumed {item}")

# Run producers and consumers
producer_thread = threading.Thread(target=producer)
consumer_threads = [threading.Thread(target=consumer) for _ in range(2)]

producer_thread.start()
for t in consumer_threads:
    t.start()
```

## Real-World Example: Thread-Safe Counter

```python
class ThreadSafeCounter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()
    
    def increment(self):
        with self.lock:
            self.value += 1
    
    def decrement(self):
        with self.lock:
            self.value -= 1
    
    def get_value(self):
        with self.lock:
            return self.value

# Usage
counter = ThreadSafeCounter()

def increment_worker():
    for _ in range(1000):
        counter.increment()

threads = [threading.Thread(target=increment_worker) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(counter.get_value())  # Always 10000
```

## Deadlock Example & Solution

### ❌ BAD - Deadlock
```python
import threading

lock1 = threading.Lock()
lock2 = threading.Lock()

def thread1_action():
    with lock1:
        print("Thread 1 acquired lock1")
        # Thread 2 is holding lock2, waiting for lock1
        # Thread 1 will wait for lock2
        with lock2:
            print("Thread 1 acquired lock2")

def thread2_action():
    with lock2:
        print("Thread 2 acquired lock2")
        with lock1:  # Deadlock! Waiting for lock1
            print("Thread 2 acquired lock1")

t1 = threading.Thread(target=thread1_action)
t2 = threading.Thread(target=thread2_action)
t1.start()
t2.start()
# Program hangs - DEADLOCK!
```

### ✅ GOOD - Prevent Deadlock
```python
# Always acquire locks in same order
def thread1_action():
    with lock1:
        print("Thread 1 acquired lock1")
        with lock2:
            print("Thread 1 acquired lock2")

def thread2_action():
    with lock1:  # Same order!
        print("Thread 2 acquired lock1")
        with lock2:
            print("Thread 2 acquired lock2")
```

## Thread Pool for Efficiency

```python
from concurrent.futures import ThreadPoolExecutor
import time

def worker(task_id):
    print(f"Task {task_id} started")
    time.sleep(1)
    return f"Task {task_id} completed"

# Create pool of 3 threads
with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(worker, i) for i in range(10)]
    
    for future in futures:
        result = future.result()
        print(result)
```

## Key Interview Questions

1. **What's a race condition?**
   - Multiple threads access shared resource without synchronization

2. **How to prevent race conditions?**
   - Use locks, semaphores, atomic operations

3. **What causes deadlock?**
   - Circular wait for resources

4. **How to prevent deadlock?**
   - Always acquire locks in same order, use timeout

5. **When to use Lock vs RLock?**
   - RLock when same thread needs to acquire multiple times

## Important Points

- ✅ Use locks for shared mutable state
- ✅ Keep critical sections small
- ✅ Avoid nested locks if possible
- ✅ Always release locks (use context managers)
- ✅ Be aware of deadlock possibilities
- ✅ Use thread pools for efficiency
- ✅ Consider immutable objects
