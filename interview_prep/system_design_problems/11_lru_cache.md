# LRU Cache System Design

## Requirements

### Functional
- Get value by key (O(1))
- Put key-value pair (O(1))
- Evict least recently used item when full
- Support any data types as values
- Thread-safe operations

### Non-Functional
- O(1) time complexity for get/put operations
- O(n) space where n = capacity
- Handle concurrent access
- No external caching libraries

## Core Concepts

**LRU (Least Recently Used)**: When cache is full, remove the item that hasn't been used for longest time.

**Recency Tracking**: Track access order - most recently used at front, least recently used at back.

## Architecture Approach

### Problem: Naive Solution
```python
# ❌ BAD - O(n) to find and remove LRU
class NaiveCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}  # {key: value}
        self.access_times = {}  # {key: timestamp}
    
    def get(self, key):
        if key in self.cache:
            self.access_times[key] = time.time()
            return self.cache[key]
        return -1
    
    def put(self, key, value):
        if len(self.cache) >= self.capacity:
            # O(n) to find min!
            lru_key = min(self.access_times, key=self.access_times.get)
            del self.cache[lru_key]
            del self.access_times[lru_key]
        
        self.cache[key] = value
        self.access_times[key] = time.time()
```

### Solution: Hash Map + Doubly Linked List
```python
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}  # {key: Node}
        
        # Dummy nodes for easy insertion/deletion
        self.head = Node(0, 0)  # Most recently used
        self.tail = Node(0, 0)  # Least recently used
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def get(self, key):
        """Get value - O(1)"""
        if key not in self.cache:
            return -1
        
        node = self.cache[key]
        self._move_to_head(node)  # Mark as recently used
        return node.value
    
    def put(self, key, value):
        """Put key-value pair - O(1)"""
        if key in self.cache:
            # Update existing - move to head
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            # Add new
            if len(self.cache) >= self.capacity:
                # Evict LRU (before tail)
                evicted = self._remove_tail()
                del self.cache[evicted.key]
            
            # Create and add node
            node = Node(key, value)
            self.cache[key] = node
            self._add_to_head(node)
    
    def _move_to_head(self, node):
        """Move node to head (most recently used)"""
        self._remove_node(node)
        self._add_to_head(node)
    
    def _remove_node(self, node):
        """Remove node from linked list"""
        node.prev.next = node.next
        node.next.prev = node.prev
    
    def _add_to_head(self, node):
        """Add node right after head"""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
    
    def _remove_tail(self):
        """Remove and return tail node (LRU)"""
        lru = self.tail.prev
        self._remove_node(lru)
        return lru

# Usage
cache = LRUCache(2)
cache.put(1, 1)      # {1=1}
cache.put(2, 2)      # {1=1, 2=2}
print(cache.get(1))  # 1 - move 1 to head
cache.put(3, 3)      # Evict 2 (LRU), add 3 → {1=1, 3=3}
print(cache.get(2))  # -1 (evicted)
cache.put(4, 4)      # Evict 3, add 4 → {1=1, 4=4}
print(cache.get(1))  # 1
print(cache.get(3))  # -1
print(cache.get(4))  # 4
```

## Time Complexity Analysis

| Operation | Complexity | Why |
|-----------|-----------|-----|
| **get(key)** | O(1) | HashMap lookup + list reordering |
| **put(key, value)** | O(1) | HashMap insert + list operations |
| **_move_to_head** | O(1) | Just pointer updates |
| **_remove_tail** | O(1) | Direct access via tail pointer |

## Space Complexity

- O(capacity) for storing nodes
- O(capacity) for HashMap
- Total: O(n) where n = capacity

## Thread-Safe LRU Cache

```python
import threading

class ThreadSafeLRUCache:
    def __init__(self, capacity):
        self.cache = {}
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.capacity = capacity
        self.lock = threading.RLock()
    
    def get(self, key):
        with self.lock:
            if key not in self.cache:
                return -1
            
            node = self.cache[key]
            self._move_to_head(node)
            return node.value
    
    def put(self, key, value):
        with self.lock:
            if key in self.cache:
                node = self.cache[key]
                node.value = value
                self._move_to_head(node)
            else:
                if len(self.cache) >= self.capacity:
                    evicted = self._remove_tail()
                    del self.cache[evicted.key]
                
                node = Node(key, value)
                self.cache[key] = node
                self._add_to_head(node)
    
    # ... other methods with lock
```

## Variations

### 1. LFU Cache (Least Frequently Used)
```python
class LFUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}  # {key: value}
        self.freq = {}   # {key: frequency}
        self.min_freq = 0
    
    def get(self, key):
        if key not in self.cache:
            return -1
        
        self.freq[key] += 1
        self.min_freq = min(self.min_freq, self.freq[key])
        return self.cache[key]
    
    def put(self, key, value):
        if key in self.cache:
            self.cache[key] = value
            self.freq[key] += 1
        else:
            # Evict item with min frequency
            if len(self.cache) >= self.capacity:
                lfu_key = min(self.cache.keys(), 
                             key=lambda k: self.freq[k])
                del self.cache[lfu_key]
                del self.freq[lfu_key]
            
            self.cache[key] = value
            self.freq[key] = 1
```

### 2. Time-Based Expiration
```python
class ExpiringLRUCache:
    def __init__(self, capacity, ttl_seconds=3600):
        self.cache = {}
        self.ttl = ttl_seconds
        self.timestamps = {}
    
    def get(self, key):
        if key not in self.cache:
            return -1
        
        # Check expiration
        if time.time() - self.timestamps[key] > self.ttl:
            del self.cache[key]
            del self.timestamps[key]
            return -1
        
        self.timestamps[key] = time.time()
        return self.cache[key]
    
    def put(self, key, value):
        self.cache[key] = value
        self.timestamps[key] = time.time()
```

## Real-World Applications

| Application | Use Case |
|-------------|----------|
| **CPU Cache** | L1/L2 cache eviction |
| **Browser Cache** | Recent page lookups |
| **Database Caching** | Query result caching |
| **CDN** | Edge content caching |
| **Redis** | Memory optimization |

## Interview Questions

1. **Why O(1) and how?**
   - HashMap for direct key lookup, Linked list for O(1) reordering

2. **Why not just use list/array?**
   - Array: O(n) to find and remove LRU item

3. **Thread safety considerations?**
   - Use lock for entire get/put operations

4. **Eviction strategies?**
   - LRU, LFU, FIFO, Random all possible

5. **What if same key accessed multiple times?**
   - Move to head each time (already most recent)

## Key Implementation Points

- ✅ Use HashMap + Doubly Linked List combo
- ✅ Head = most recently used, Tail = least recently used
- ✅ Dummy nodes avoid null checks
- ✅ Lock entire operation for thread safety
- ✅ Handle capacity overflow with eviction
- ✅ Move existing key to head on re-access
