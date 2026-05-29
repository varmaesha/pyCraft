# Multi-User Concurrent Scenarios

## Definition

**Multi-User Concurrency**: Multiple users/processes simultaneously accessing and modifying shared resources.

**Challenge**: Maintain data consistency while maximizing concurrency and responsiveness.

## Real-World Scenarios

### Scenario 1: Bank Transfer Between Accounts

```python
import threading
import time

class Bank:
    def __init__(self):
        self.accounts = {
            "A": 1000,
            "B": 500,
            "C": 800
        }
        self.lock = threading.Lock()
        self.transaction_log = []
    
    def transfer(self, from_acc, to_acc, amount):
        with self.lock:
            if self.accounts[from_acc] < amount:
                return False
            
            self.accounts[from_acc] -= amount
            self.accounts[to_acc] += amount
            
            self.transaction_log.append({
                "from": from_acc,
                "to": to_acc,
                "amount": amount,
                "timestamp": time.time()
            })
            
            return True
    
    def get_balance(self, account):
        with self.lock:
            return self.accounts[account]
    
    def get_total(self):
        with self.lock:
            return sum(self.accounts.values())

bank = Bank()

def customer_transactions(customer_id):
    accounts = ["A", "B", "C"]
    
    for _ in range(10):
        from_acc = accounts[customer_id % len(accounts)]
        to_acc = accounts[(customer_id + 1) % len(accounts)]
        
        bank.transfer(from_acc, to_acc, 10)
        time.sleep(0.01)

# 5 customers doing transfers
threads = [threading.Thread(target=customer_transactions, args=(i,))
           for i in range(5)]

print(f"Total before: ${bank.get_total()}")

for t in threads:
    t.start()
for t in threads:
    t.join()

print(f"Total after: ${bank.get_total()}")  # Still 2300!
print(f"Transactions: {len(bank.transaction_log)}")
```

### Scenario 2: E-Commerce Shopping Cart

```python
import threading

class ShoppingCart:
    def __init__(self, user_id, inventory):
        self.user_id = user_id
        self.items = {}  # {product_id: quantity}
        self.inventory = inventory
        self.lock = threading.Lock()
    
    def add_item(self, product_id, quantity):
        with self.lock:
            if not self.inventory.reserve(product_id, quantity):
                return False
            
            if product_id in self.items:
                self.items[product_id] += quantity
            else:
                self.items[product_id] = quantity
            
            return True
    
    def remove_item(self, product_id, quantity):
        with self.lock:
            if product_id not in self.items:
                return False
            
            if self.items[product_id] <= quantity:
                del self.items[product_id]
                self.inventory.release(product_id, quantity)
            else:
                self.items[product_id] -= quantity
                self.inventory.release(product_id, quantity)
            
            return True
    
    def checkout(self):
        with self.lock:
            if not self._validate_inventory():
                return False
            
            total = sum(
                self.inventory.get_price(pid) * qty
                for pid, qty in self.items.items()
            )
            
            self.items.clear()
            return total

class Inventory:
    def __init__(self):
        self.stock = {
            "laptop": 5,
            "mouse": 20,
            "keyboard": 15
        }
        self.prices = {
            "laptop": 1000,
            "mouse": 25,
            "keyboard": 75
        }
        self.lock = threading.Lock()
    
    def reserve(self, product_id, quantity):
        with self.lock:
            if self.stock[product_id] >= quantity:
                self.stock[product_id] -= quantity
                return True
            return False
    
    def release(self, product_id, quantity):
        with self.lock:
            self.stock[product_id] += quantity
    
    def get_price(self, product_id):
        return self.prices[product_id]

inventory = Inventory()

def shopper(shopper_id):
    cart = ShoppingCart(shopper_id, inventory)
    
    # Add items
    cart.add_item("laptop", 1)
    cart.add_item("mouse", 2)
    
    time.sleep(0.1)
    
    # Checkout
    total = cart.checkout()
    if total:
        print(f"Shopper {shopper_id}: Spent ${total}")

threads = [threading.Thread(target=shopper, args=(i,))
           for i in range(10)]

for t in threads:
    t.start()
for t in threads:
    t.join()

# Only 5 laptops available - some shoppers fail
```

### Scenario 3: Social Media - Feed Updates

```python
import threading
from datetime import datetime

class SocialNetwork:
    def __init__(self):
        self.users = {}  # {user_id: user_data}
        self.feeds = {}  # {user_id: [posts]}
        self.followers = {}  # {user_id: [follower_ids]}
        self.lock = threading.Lock()
    
    def create_user(self, user_id):
        with self.lock:
            self.users[user_id] = {
                "id": user_id,
                "created_at": datetime.now()
            }
            self.feeds[user_id] = []
            self.followers[user_id] = []
    
    def post(self, user_id, content):
        with self.lock:
            post = {
                "user_id": user_id,
                "content": content,
                "timestamp": datetime.now(),
                "likes": 0
            }
            
            # Add to own feed
            self.feeds[user_id].append(post)
            
            # Add to followers' feeds
            for follower_id in self.followers[user_id]:
                self.feeds[follower_id].append(post)
            
            return post
    
    def follow(self, user_id, target_id):
        with self.lock:
            if target_id not in self.followers:
                return False
            
            self.followers[target_id].append(user_id)
            
            # Load past posts
            self.feeds[user_id].extend(self.feeds[target_id])
            
            return True
    
    def get_feed(self, user_id):
        with self.lock:
            return self.feeds[user_id].copy()
    
    def like_post(self, user_id, post_index):
        with self.lock:
            if post_index < len(self.feeds[user_id]):
                self.feeds[user_id][post_index]["likes"] += 1

network = SocialNetwork()

# Create users
for i in range(10):
    network.create_user(f"user_{i}")

# User 0 has followers
for i in range(1, 10):
    network.follow(f"user_{i}", "user_0")

def user_activity(user_id):
    for i in range(5):
        network.post(user_id, f"Post {i} from {user_id}")
        time.sleep(0.01)

# All users posting simultaneously
threads = [threading.Thread(target=user_activity, args=(f"user_{i}",))
           for i in range(10)]

for t in threads:
    t.start()
for t in threads:
    t.join()

print(f"Feed size for user_0: {len(network.get_feed('user_0'))}")
```

### Scenario 4: Collaborative Document Editing

```python
import threading

class Document:
    def __init__(self, content=""):
        self.content = content
        self.version = 0
        self.changes = []
        self.lock = threading.Lock()
    
    def edit(self, user_id, position, text, delete_count=0):
        with self.lock:
            # Perform edit
            before = self.content[:position]
            after = self.content[position + delete_count:]
            self.content = before + text + after
            
            # Track change
            self.version += 1
            self.changes.append({
                "user": user_id,
                "version": self.version,
                "position": position,
                "text": text,
                "delete_count": delete_count
            })
            
            return self.version
    
    def get_content(self):
        with self.lock:
            return self.content
    
    def get_history(self):
        with self.lock:
            return self.changes.copy()

doc = Document("Hello World")

def editor(editor_id):
    edits = [
        (5, " Beautiful", 0),
        (12, "!", 0),
        (13, "\nEdit by " + str(editor_id), 0)
    ]
    
    for pos, text, delete in edits:
        doc.edit(editor_id, pos, text, delete)
        time.sleep(0.01)

# Multiple editors
threads = [threading.Thread(target=editor, args=(i,))
           for i in range(5)]

for t in threads:
    t.start()
for t in threads:
    t.join()

print("Final content:")
print(doc.get_content())
print(f"\nTotal versions: {doc.get_content().version if hasattr(doc.get_content(), 'version') else len(doc.get_history())}")
```

### Scenario 5: Distributed Cache

```python
import threading
import time

class DistributedCache:
    def __init__(self, ttl=60):
        self.cache = {}
        self.ttl = ttl
        self.access_log = {}
        self.lock = threading.Lock()
    
    def get(self, key):
        with self.lock:
            if key not in self.cache:
                return None
            
            value, expiry = self.cache[key]
            
            if time.time() > expiry:
                del self.cache[key]
                return None
            
            # Log access
            self.access_log[key] = self.access_log.get(key, 0) + 1
            
            return value
    
    def set(self, key, value):
        with self.lock:
            expiry = time.time() + self.ttl
            self.cache[key] = (value, expiry)
    
    def delete(self, key):
        with self.lock:
            if key in self.cache:
                del self.cache[key]
                return True
            return False
    
    def stats(self):
        with self.lock:
            return {
                "total_keys": len(self.cache),
                "access_log": self.access_log.copy()
            }

cache = DistributedCache(ttl=5)

def worker(worker_id):
    for i in range(20):
        # Random operations
        key = f"key_{i % 5}"
        
        if i % 3 == 0:
            cache.set(key, f"value_{worker_id}_{i}")
        else:
            cache.get(key)
        
        time.sleep(0.01)

threads = [threading.Thread(target=worker, args=(i,))
           for i in range(5)]

for t in threads:
    t.start()
for t in threads:
    t.join()

stats = cache.stats()
print(f"Cache keys: {stats['total_keys']}")
print(f"Access log: {stats['access_log']}")
```

## Common Patterns

### Pattern 1: Optimistic Concurrency
```python
# Assume conflicts rare, check before commit
version = read_version()
data = read_data()
# ... process ...
if current_version == version:
    write_data()
```

### Pattern 2: Reader-Writer Lock
```python
# Multiple readers, single writer
class ReadWriteData:
    def read(self):
        with read_lock:
            return data
    
    def write(self, new_data):
        with write_lock:
            data = new_data
```

### Pattern 3: Queue-Based Processing
```python
# Serialize operations through queue
queue = Queue()

def worker():
    while True:
        operation = queue.get()
        process(operation)
        queue.task_done()
```

## Key Interview Questions

1. **Multi-user concurrency challenges?**
   - Data consistency, deadlocks, race conditions

2. **Real-world scenario design?**
   - Identify shared resources, apply appropriate locks

3. **When to use optimistic vs pessimistic?**
   - Optimistic: Low conflict, Pessimistic: High contention

4. **Scale strategies?**
   - Sharding, partitioning, distributed locks

## Important Points

- ✅ Identify all shared resources
- ✅ Apply appropriate synchronization
- ✅ Keep locks short
- ✅ Test edge cases and race conditions
- ✅ Use appropriate data structures
- ✅ Plan for scalability
- ✅ Monitor for deadlocks
- ✅ Document concurrency design
