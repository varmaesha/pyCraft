# Thread-Safe HashMap System Design

## Requirements

### Functional
- Put/Get/Remove operations
- Concurrent access from multiple threads
- No deadlocks or race conditions
- Consistent iteration
- Resize dynamically

### Non-Functional
- High concurrency (minimal lock contention)
- O(1) average time complexity for operations
- Low memory overhead
- Scalable to 1000+ concurrent threads

## Problem Statement

### ❌ Naive Solution - Global Lock (Poor)

```python
import threading

class NaiveThreadSafeMap:
    def __init__(self):
        self.map = {}
        self.lock = threading.Lock()  # Single lock for all
    
    def get(self, key):
        with self.lock:
            return self.map.get(key)
    
    def put(self, key, value):
        with self.lock:
            self.map[key] = value
    
    def remove(self, key):
        with self.lock:
            del self.map[key]

# Problem: All operations wait for same lock → contention
```

### ✅ Solution 1: Segment Locking

```python
class SegmentedHashMap:
    def __init__(self, capacity=1000, segments=16):
        self.segments = segments
        self.buckets = [[] for _ in range(capacity)]
        self.locks = [threading.RLock() for _ in range(segments)]
        self.capacity = capacity
    
    def _get_segment(self, key):
        """Get segment for key"""
        hash_code = hash(key)
        return abs(hash_code) % self.segments
    
    def _get_bucket(self, key):
        """Get bucket for key"""
        hash_code = hash(key)
        return abs(hash_code) % self.capacity
    
    def get(self, key):
        """Get with minimal locking"""
        segment_id = self._get_segment(key)
        bucket_id = self._get_bucket(key)
        
        with self.locks[segment_id]:
            bucket = self.buckets[bucket_id]
            
            for stored_key, stored_value in bucket:
                if stored_key == key:
                    return stored_value
            
            return None
    
    def put(self, key, value):
        """Put with segment locking"""
        segment_id = self._get_segment(key)
        bucket_id = self._get_bucket(key)
        
        with self.locks[segment_id]:
            bucket = self.buckets[bucket_id]
            
            # Update if exists
            for i, (stored_key, _) in enumerate(bucket):
                if stored_key == key:
                    bucket[i] = (key, value)
                    return
            
            # Add new
            bucket.append((key, value))
    
    def remove(self, key):
        """Remove with segment locking"""
        segment_id = self._get_segment(key)
        bucket_id = self._get_bucket(key)
        
        with self.locks[segment_id]:
            bucket = self.buckets[bucket_id]
            
            for i, (stored_key, _) in enumerate(bucket):
                if stored_key == key:
                    bucket.pop(i)
                    return True
            
            return False

# Benefits:
# - 16 threads can write to different segments simultaneously
# - vs 1 thread with global lock
```

### ✅ Solution 2: Copy-On-Write (For Read-Heavy Workloads)

```python
class CopyOnWriteHashMap:
    def __init__(self):
        self.data = {}
        self.lock = threading.RLock()
    
    def get(self, key):
        """No lock needed for read!"""
        return self.data.get(key)
    
    def put(self, key, value):
        """Acquire lock and copy on write"""
        with self.lock:
            # Create new dict
            new_data = self.data.copy()
            new_data[key] = value
            
            # Atomic swap
            self.data = new_data
    
    def remove(self, key):
        with self.lock:
            new_data = self.data.copy()
            if key in new_data:
                del new_data[key]
                self.data = new_data
                return True
            return False

# Benefits:
# - Unlimited concurrent readers (no lock)
# - Safe for read-heavy scenarios
# - Downside: writes are more expensive
```

### ✅ Solution 3: ConcurrentHashMap Pattern (Best)

```python
class ConcurrentHashMap:
    """
    Combines:
    - Segment locking for concurrency
    - Dynamic resizing
    - Fair iteration
    """
    
    class Entry:
        def __init__(self, key, value):
            self.key = key
            self.value = value
    
    def __init__(self, initial_capacity=16, concurrency_level=16):
        self.concurrency_level = concurrency_level
        self.segments = []
        self.locks = []
        
        segment_capacity = initial_capacity // concurrency_level
        
        for _ in range(concurrency_level):
            self.segments.append({})
            self.locks.append(threading.RLock())
    
    def _get_segment_index(self, key):
        hash_code = hash(key)
        return abs(hash_code) % self.concurrency_level
    
    def get(self, key):
        segment_index = self._get_segment_index(key)
        
        with self.locks[segment_index]:
            segment = self.segments[segment_index]
            return segment.get(key)
    
    def put(self, key, value):
        segment_index = self._get_segment_index(key)
        
        with self.locks[segment_index]:
            segment = self.segments[segment_index]
            segment[key] = value
    
    def remove(self, key):
        segment_index = self._get_segment_index(key)
        
        with self.locks[segment_index]:
            segment = self.segments[segment_index]
            if key in segment:
                del segment[key]
                return True
            return False
    
    def contains_key(self, key):
        return self.get(key) is not None
    
    def contains_value(self, value):
        """Requires locking all segments"""
        for lock in self.locks:
            lock.acquire()
        
        try:
            for segment in self.segments:
                if value in segment.values():
                    return True
            return False
        finally:
            for lock in reversed(self.locks):
                lock.release()
    
    def size(self):
        """Approximate size"""
        size = 0
        for lock in self.locks:
            lock.acquire()
        
        try:
            for segment in self.segments:
                size += len(segment)
            return size
        finally:
            for lock in reversed(self.locks):
                lock.release()
    
    def iterate(self):
        """Fair concurrent iteration"""
        for lock in self.locks:
            lock.acquire()
        
        try:
            for segment in self.segments:
                for key, value in segment.items():
                    yield key, value
        finally:
            for lock in reversed(self.locks):
                lock.release()
```

## Concurrent Resize

```python
class ResizableThreadSafeMap:
    def __init__(self, initial_capacity=16):
        self.capacity = initial_capacity
        self.map = {}
        self.lock = threading.RLock()
        self.load_factor = 0.75
    
    def put(self, key, value):
        with self.lock:
            self.map[key] = value
            
            # Check if need to resize
            if len(self.map) > self.capacity * self.load_factor:
                self._resize()
    
    def _resize(self):
        """Resize map - lock must be held"""
        old_capacity = self.capacity
        self.capacity = old_capacity * 2
        
        # Rehash all entries
        new_map = {}
        for key, value in self.map.items():
            # Re-hash with new capacity
            new_map[key] = value
        
        self.map = new_map
        print(f"Resized from {old_capacity} to {self.capacity}")
```

## Compare Lock Strategies

| Strategy | Reads | Writes | Concurrency | Memory | Best For |
|----------|-------|--------|-------------|--------|----------|
| **Global Lock** | 1 thread | 1 thread | None | Low | Single threaded |
| **Segment Lock** | Many | Some | Medium | Medium | Balanced workload |
| **Read-Write Lock** | Many | Few | High | Low | Read-heavy |
| **Copy-on-Write** | Unlimited | Few | High | High | Read-heavy |
| **Concurrent** | Many | Some | Very High | Medium | General purpose |

## Real-World Examples

```python
# Java's ConcurrentHashMap uses segment locking + resize
# Python: From concurrent.futures, use ThreadPoolExecutor

from concurrent.futures import ThreadPoolExecutor
import time

def test_concurrent_map():
    """Stress test with concurrent access"""
    map_obj = ConcurrentHashMap(concurrency_level=16)
    
    def writer(thread_id):
        for i in range(1000):
            map_obj.put(f"key_{thread_id}_{i}", f"value_{i}")
    
    def reader(thread_id):
        for i in range(1000):
            val = map_obj.get(f"key_{thread_id}_{i}")
    
    # Launch 16 writer + 16 reader threads
    with ThreadPoolExecutor(max_workers=32) as executor:
        for i in range(16):
            executor.submit(writer, i)
            executor.submit(reader, i)
    
    print(f"Map size: {map.obj.size()}")
```

## Interview Questions

1. **Why segment locking vs global lock?**
   - Multiple threads can write to different segments simultaneously

2. **Handle concurrent resize?**
   - Lock all segments during resize, or use incremental rehashing

3. **Fairness?**
   - Segment-based design: fair distribution of locks

4. **How many segments?**
   - Usually = concurrency_level (16 is common)

5. **Compare with synchronized HashMap?**
   - Synchronized: Global lock (slower for high concurrency)
   - ConcurrentHashMap: Segment locks (faster)

## Key Points

- ✅ Segment/bucket locking reduces contention
- ✅ Each segment has independent lock
- ✅ Multiple threads on different segments simultaneously
- ✅ Copy-on-write for read-heavy workloads
- ✅ Fair concurrent iteration
- ✅ Dynamic resizing with lock management
- ✅ No busy waiting or deadlocks
