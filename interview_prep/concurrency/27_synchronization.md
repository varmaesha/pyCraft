# Synchronization Mechanisms

## Definition

**Synchronization**: Methods to control access to shared resources and prevent race conditions.

**Goal**: Ensure thread-safe, correct execution despite concurrent access.

## Core Mechanisms

### 1. Locks (Mutex)

#### Lock Basics
```python
import threading

class BankAccount:
    def __init__(self, balance):
        self.balance = balance
        self.lock = threading.Lock()
    
    def deposit(self, amount):
        with self.lock:  # Acquire lock
            self.balance += amount
        # Automatically release lock
    
    def withdraw(self, amount):
        with self.lock:
            if self.balance >= amount:
                self.balance -= amount
                return True
            return False
    
    def get_balance(self):
        with self.lock:
            return self.balance

# Only one thread can execute locked section
account = BankAccount(1000)
account.deposit(100)  # Safe
print(account.get_balance())

# Thread 1
t1 = threading.Thread(target=account.deposit, args=(100,))
# Thread 2
t2 = threading.Thread(target=account.withdraw, args=(50,))

t1.start()
t2.start()
t1.join()
t2.join()

# Expected: 1050, Actual: 1050
```

#### Reentrant Lock (RLock)
```python
import threading

class Payment:
    def __init__(self):
        self.lock = threading.RLock()  # Can acquire multiple times
    
    def process(self, amount):
        with self.lock:
            self._validate(amount)
            self._charge(amount)
    
    def _validate(self, amount):
        with self.lock:  # Same thread can acquire again
            print(f"Validating ${amount}")
    
    def _charge(self, amount):
        with self.lock:  # Same thread can acquire again
            print(f"Charging ${amount}")

# Regular Lock would deadlock here!
# RLock allows same thread to acquire multiple times
payment = Payment()
payment.process(100)
```

### 2. Semaphore

**Purpose**: Limit access to N resources.

```python
import threading
import time

class Pool:
    def __init__(self, size=3):
        self.semaphore = threading.Semaphore(size)
        self.resources = list(range(size))
        self.lock = threading.Lock()
    
    def acquire_resource(self, thread_id):
        self.semaphore.acquire()  # Wait until count > 0
        with self.lock:
            resource = self.resources.pop()
            print(f"Thread {thread_id} acquired resource {resource}")
        return resource
    
    def release_resource(self, thread_id, resource):
        with self.lock:
            self.resources.append(resource)
            print(f"Thread {thread_id} released resource {resource}")
        self.semaphore.release()  # Increment count

# Pool with 3 resources
pool = Pool(3)

def worker(thread_id):
    resource = pool.acquire_resource(thread_id)
    time.sleep(1)  # Use resource
    pool.release_resource(thread_id, resource)

# 5 threads but only 3 resources
threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]

for t in threads:
    t.start()
for t in threads:
    t.join()

# Output shows max 3 concurrent access
```

### 3. Condition Variable

**Purpose**: Wait for specific conditions.

```python
import threading
import time

class Buffer:
    def __init__(self, max_size=3):
        self.max_size = max_size
        self.items = []
        self.lock = threading.Lock()
        self.not_empty = threading.Condition(self.lock)
        self.not_full = threading.Condition(self.lock)
    
    def put(self, item):
        with self.lock:
            while len(self.items) >= self.max_size:
                self.not_full.wait()  # Wait until not full
            
            self.items.append(item)
            print(f"Produced: {item}, Buffer: {self.items}")
            self.not_empty.notify()  # Signal not empty
    
    def get(self):
        with self.lock:
            while len(self.items) == 0:
                self.not_empty.wait()  # Wait until not empty
            
            item = self.items.pop(0)
            print(f"Consumed: {item}, Buffer: {self.items}")
            self.not_full.notify()  # Signal not full
            return item

buffer = Buffer(2)

def producer():
    for i in range(5):
        buffer.put(f"Item{i}")
        time.sleep(0.5)

def consumer():
    for _ in range(5):
        buffer.get()
        time.sleep(1)

t1 = threading.Thread(target=producer)
t2 = threading.Thread(target=consumer)

t1.start()
t2.start()
t1.join()
t2.join()

# Producer waits when buffer full
# Consumer waits when buffer empty
```

### 4. Barrier

**Purpose**: Wait for N threads to reach point.

```python
import threading
import time

class TeamTask:
    def __init__(self, team_size=3):
        self.barrier = threading.Barrier(team_size)
    
    def task(self, worker_id):
        print(f"Worker {worker_id} preparing...")
        time.sleep(1)
        
        print(f"Worker {worker_id} ready")
        self.barrier.wait()  # Wait for all
        
        print(f"Worker {worker_id} starting task (all ready!)")

team = TeamTask(3)

threads = [threading.Thread(target=team.task, args=(i,)) for i in range(3)]

for t in threads:
    t.start()
for t in threads:
    t.join()

# All workers wait for others at barrier
# Then all proceed together
```

### 5. Event

**Purpose**: Signal that something happened.

```python
import threading
import time

class ServerStartup:
    def __init__(self):
        self.started = threading.Event()
    
    def startup(self):
        print("Server starting...")
        time.sleep(2)
        print("Server started!")
        self.started.set()  # Signal event
    
    def wait_for_startup(self, client_id):
        print(f"Client {client_id} waiting...")
        self.started.wait()  # Block until set
        print(f"Client {client_id} can connect!")

server = ServerStartup()

# Start server
t_server = threading.Thread(target=server.startup)

# Start clients that wait for server
clients = [threading.Thread(target=server.wait_for_startup, args=(i,))
           for i in range(3)]

t_server.start()
for t in clients:
    t.start()

t_server.join()
for t in clients:
    t.join()

# Clients blocked until server.started.set()
```

## Thread-Safe Collections

### Python's Queue Module
```python
import queue
import threading

# Thread-safe queue
q = queue.Queue(maxsize=3)

def producer():
    for i in range(5):
        q.put(i)  # Blocks if full
        print(f"Produced: {i}")

def consumer():
    for _ in range(5):
        item = q.get()  # Blocks if empty
        print(f"Consumed: {item}")

t1 = threading.Thread(target=producer)
t2 = threading.Thread(target=consumer)

t1.start()
t2.start()
t1.join()
t2.join()

# Built-in synchronization
```

### Python's concurrent.futures
```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def task(n):
    time.sleep(1)
    return n * n

with ThreadPoolExecutor(max_workers=3) as executor:
    # Submit tasks
    future_to_num = {executor.submit(task, n): n for n in range(5)}
    
    # Process completed tasks
    for future in as_completed(future_to_num):
        num = future_to_num[future]
        result = future.result()
        print(f"{num}^2 = {result}")

# Automatic thread management
```

## Synchronization Comparison

| Mechanism | Purpose | Use Case |
|-----------|---------|----------|
| **Lock/Mutex** | Exclusive access | Shared data |
| **RLock** | Recursive lock | Same thread multiple calls |
| **Semaphore** | Limit N resources | Pool of resources |
| **Condition** | Wait for condition | Producer-consumer |
| **Barrier** | Synchronize N threads | Group coordination |
| **Event** | Signal occurred | Startup/shutdown |
| **Queue** | Thread-safe queue | Message passing |

## Common Patterns

### Producer-Consumer
```python
buffer = []
lock = threading.Lock()
not_empty = threading.Condition(lock)

# Producer
def produce():
    with lock:
        buffer.append(item)
        not_empty.notify()

# Consumer
def consume():
    with lock:
        while not buffer:
            not_empty.wait()
        item = buffer.pop(0)
```

### Reader-Writer Lock
```python
class ReadWriteLock:
    def __init__(self):
        self.readers = 0
        self.writers = 0
        self.lock = threading.Lock()
        self.can_read = threading.Condition(self.lock)
        self.can_write = threading.Condition(self.lock)
    
    def acquire_read(self):
        self.lock.acquire()
        while self.writers > 0:
            self.can_read.wait()
        self.readers += 1
        self.lock.release()
    
    def release_read(self):
        with self.lock:
            self.readers -= 1
            if self.readers == 0:
                self.can_write.notify_all()
    
    def acquire_write(self):
        with self.lock:
            while self.readers > 0 or self.writers > 0:
                self.can_write.wait()
            self.writers += 1
    
    def release_write(self):
        with self.lock:
            self.writers -= 1
            self.can_write.notify_all()
            self.can_read.notify_all()
```

## Key Interview Questions

1. **What's synchronization?**
   - Control access to shared resources

2. **Lock vs Semaphore?**
   - Lock: 1 thread, Semaphore: N threads

3. **Condition variable use?**
   - Wait for specific condition to be true

4. **Producer-consumer pattern?**
   - Producers add, consumers remove, synchronized

## Important Points

- ✅ Choose right synchronization mechanism
- ✅ Keep locked sections short
- ✅ Document shared data
- ✅ Use thread-safe collections
- ✅ Test concurrency thoroughly
- ⚠️ Locks can cause deadlocks
- ✅ Consider lock-free alternatives
