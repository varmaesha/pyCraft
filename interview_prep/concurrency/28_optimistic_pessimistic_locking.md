# Optimistic vs Pessimistic Locking

## Definition

**Pessimistic Locking**: Lock data before modifying (assume conflicts will happen).

**Optimistic Locking**: Assume no conflicts, check before committing (detect conflicts).

**Key Difference**: When to detect conflicts - before or during update.

## Pessimistic Locking

### How It Works
```
1. Request lock
2. Acquire exclusive lock
3. Read data
4. Modify data
5. Write data
6. Release lock
```

### Example: Database Transaction

```python
import threading
import time

class Account:
    def __init__(self, balance):
        self.balance = balance
        self.lock = threading.Lock()  # Pessimistic lock
    
    def transfer_pessimistic(self, amount):
        with self.lock:  # Acquire lock BEFORE reading
            balance = self.balance
            time.sleep(0.1)  # Simulate processing
            self.balance = balance - amount
            return True

account = Account(1000)

def transfer():
    for _ in range(10):
        account.transfer_pessimistic(10)

threads = [threading.Thread(target=transfer) for _ in range(5)]

for t in threads:
    t.start()
for t in threads:
    t.join()

print(f"Final balance: {account.balance}")  # Guaranteed 500
```

### Advantages
- ✅ Simple to implement
- ✅ Prevents conflicts
- ✅ Data always consistent

### Disadvantages
- ❌ High lock contention
- ❌ Reduced concurrency
- ❌ Risk of deadlock
- ❌ Waiting threads blocked

## Optimistic Locking

### How It Works
```
1. Read data + version
2. Modify data
3. Check version unchanged
4. If unchanged: commit
5. If changed: conflict! Retry
```

### Example: Version-Based Conflict Detection

```python
import threading
import time

class OptimisticAccount:
    def __init__(self, balance):
        self.balance = balance
        self.version = 0  # Track changes
    
    def transfer_optimistic(self, amount):
        while True:
            # Step 1: Read
            versions = self.version
            balance = self.balance
            
            # Step 2: Modify locally
            new_balance = balance - amount
            
            # Step 3-4: Update only if version hasn't changed
            if self.version == version:  # Check unchanged
                self.balance = new_balance
                self.version += 1  # Increment version
                return True
            
            # Step 5: Conflict, retry
            print("Conflict detected, retrying...")
            time.sleep(0.01)

account = OptimisticAccount(1000)

def transfer():
    for _ in range(10):
        account.transfer_optimistic(10)

threads = [threading.Thread(target=transfer) for _ in range(5)]

for t in threads:
    t.start()
for t in threads:
    t.join()

print(f"Final balance: {account.balance}")
```

### But Wait - This Has Race Condition!

```python
class SafeOptimisticAccount:
    def __init__(self, balance):
        self.balance = balance
        self.version = 0
        self.lock = threading.Lock()  # Only lock during update
    
    def transfer_optimistic(self, amount):
        while True:
            # Step 1: Read (no lock)
            read_version = self.version
            balance = self.balance
            
            # Step 2: Modify locally (no lock)
            new_balance = balance - amount
            
            # Step 3: Update atomically (with lock)
            with self.lock:
                if self.version == read_version:
                    self.balance = new_balance
                    self.version += 1
                    return True
            
            # Step 4: Retry on conflict
            print("Conflict, retrying...")
```

### Advantages
- ✅ Higher concurrency
- ✅ No blocking waits
- ✅ Fewer locks
- ✅ Better for read-heavy workloads

### Disadvantages
- ❌ Retry overhead
- ❌ More complex logic
- ❌ Can fail under high contention
- ❌ Version management needed

## Real-World Examples

### Example 1: Database Updates

#### Pessimistic Approach (SQL)
```sql
BEGIN TRANSACTION;
SELECT * FROM users WHERE id = 1 FOR UPDATE;  -- Lock
-- Only one transaction can hold this lock
UPDATE users SET balance = balance - 100 WHERE id = 1;
COMMIT;
```

#### Optimistic Approach (SQL)
```sql
-- Read version
SELECT id, name, balance, version FROM users WHERE id = 1;
-- version = 5

-- Update if version unchanged
UPDATE users 
SET balance = balance - 100, version = version + 1
WHERE id = 1 AND version = 5;

-- Check rows affected
-- If 0 rows: conflict, retry
-- If 1 row: success
```

### Example 2: Web Application - Collaborative Editing

#### Pessimistic
```python
class Document:
    def __init__(self, content):
        self.content = content
        self.edited_by = None
        self.lock = threading.Lock()
    
    def edit_pessimistic(self, user_id, new_content):
        with self.lock:  # Lock entire document
            if self.edited_by and self.edited_by != user_id:
                return False  # Already editing
            
            self.edited_by = user_id
            self.content = new_content
            self.edited_by = None
            return True

# Only one user can edit at a time
```

#### Optimistic
```python
class OptimisticDocument:
    def __init__(self, content):
        self.content = content
        self.version = 0
    
    def edit_optimistic(self, user_id, new_content, base_version):
        # User reads version 5, makes changes, submits with version 5
        
        if self.version == base_version:
            # No conflict, update
            self.content = new_content
            self.version += 1
            return True
        else:
            # Conflict! Server has version 6
            # Client must merge or retry
            return False  # Conflict

# Multiple users can edit simultaneously
# Conflicts detected and handled
```

### Example 3: Inventory Management

#### Pessimistic
```python
class Store:
    def __init__(self, stock):
        self.stock = stock
        self.lock = threading.Lock()
    
    def checkout_pessimistic(self, quantity):
        with self.lock:  # Hold lock during entire checkout
            if self.stock >= quantity:
                self.stock -= quantity
                return True
            return False

# Customer must wait for lock
# Blocks until checkout completes
```

#### Optimistic
```python
class OptimisticStore:
    def __init__(self, stock):
        self.stock = stock
        self.version = 0
    
    def checkout_optimistic(self, quantity, expected_version):
        if self.version == expected_version and self.stock >= quantity:
            self.stock -= quantity
            self.version += 1
            return True
        return False

# If version changed (someone else bought):
# Conflict detected, refresh version, retry
```

## Comparison Table

| Factor | Pessimistic | Optimistic |
|--------|------------|-----------|
| **Conflicts** | Prevented | Detected |
| **Concurrency** | Low | High |
| **Contention** | High lock contention | Low overhead |
| **Performance** (low conflict) | Average | Excellent |
| **Performance** (high conflict) | Decent | Poor (retry) |
| **Implementation** | Simple | Complex |
| **Use Case** | High contention | Low conflict, read-heavy |

## When to Use Each

### Use Pessimistic When:
- High conflict probability
- Short transactions
- Database supports well
- Simple implementation crucial

### Use Optimistic When:
- Low conflict probability
- Long transactions
- Read-heavy workload
- High concurrency needed

## Retry Logic (Optimistic)

```python
class OptimisticRetry:
    MAX_RETRIES = 3
    
    def update_with_retry(self, data, update_func):
        for attempt in range(self.MAX_RETRIES):
            try:
                return update_func(data)
            except ConflictError:
                if attempt == self.MAX_RETRIES - 1:
                    raise
                # Refresh data
                data = self.read_fresh()
        
        raise Exception("Failed after retries")
```

## Key Interview Questions

1. **Pessimistic vs Optimistic?**
   - Pessimistic: Lock before, Optimistic: Check after

2. **When to use each?**
   - Pessimistic: High contention, Optimistic: Read-heavy

3. **Optimistic conflict detection?**
   - Version numbers, timestamps, checksums

4. **Retry strategy?**
   - Exponential backoff, eventual success

## Important Points

- ✅ Pessimistic: Simple, proven approach
- ✅ Optimistic: Better for read-heavy workloads
- ✅ Version numbers for conflict detection
- ✅ Implement proper retry logic
- ✅ Choose based on conflict probability
- ✅ Document conflict handling
- ✅ Test both happy and conflict paths
