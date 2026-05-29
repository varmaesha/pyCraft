# Distributed Key-Value Store System Design

## Requirements

### Functional
- Get/Put/Delete operations
- Multiple data types (String, List, Hash, Set)
- Transactions/Multi-op support
- Key expiration
- Persistence to disk
- Replication

### Non-Functional
- Latency < 1ms (single node)
- Support TBs of data
- 99.99% availability
- Handle network partitions
- Horizontal scalability
- Strong consistency within partition

## Core Design: Single Node

### In-Memory Storage

```python
import threading
from datetime import datetime, timedelta
from collections import defaultdict
import hashlib

class KVStore:
    def __init__(self):
        self.data = {}  # {key: value}
        self.ttl = {}   # {key: expiration_timestamp}
        self.lock = threading.RLock()
    
    def get(self, key: str):
        """O(1) Get"""
        with self.lock:
            # Check expiration
            if key in self.ttl:
                if datetime.now() > self.ttl[key]:
                    del self.data[key]
                    del self.ttl[key]
                    return None
            
            return self.data.get(key)
    
    def put(self, key: str, value, ttl_seconds: int = None):
        """O(1) Put"""
        with self.lock:
            self.data[key] = value
            
            if ttl_seconds:
                self.ttl[key] = datetime.now() + timedelta(seconds=ttl_seconds)
    
    def delete(self, key: str):
        """O(1) Delete"""
        with self.lock:
            del self.data[key]
            if key in self.ttl:
                del self.ttl[key]
    
    def exists(self, key: str) -> bool:
        with self.lock:
            return key in self.data and self._is_valid(key)
    
    def _is_valid(self, key: str) -> bool:
        """Check if key expired"""
        if key not in self.ttl:
            return True
        
        if datetime.now() > self.ttl[key]:
            del self.data[key]
            del self.ttl[key]
            return False
        
        return True

# Usage
kv = KVStore()
kv.put("user:1", {"name": "Alice", "age": 30}, ttl_seconds=3600)
print(kv.get("user:1"))  # {"name": "Alice", "age": 30}
```

## Distributed Key-Value Store

### Consistent Hashing

```python
import bisect

class ConsistentHash:
    def __init__(self, nodes=None, replicas=3):
        self.replicas = replicas
        self.ring = {}  # {hash: node}
        self.sorted_keys = []
        
        if nodes:
            for node in nodes:
                self.add_node(node)
    
    def add_node(self, node):
        """Add node to ring with replicas"""
        for i in range(self.replicas):
            key = self._hash(f"{node}:{i}")
            self.ring[key] = node
            bisect.insort(self.sorted_keys, key)
    
    def remove_node(self, node):
        """Remove node from ring"""
        for i in range(self.replicas):
            key = self._hash(f"{node}:{i}")
            if key in self.ring:
                del self.ring[key]
                self.sorted_keys.remove(key)
    
    def get_node(self, key):
        """Get node for key"""
        if not self.ring:
            return None
        
        hash_key = self._hash(key)
        
        # Find next node clockwise
        idx = bisect.bisect_right(self.sorted_keys, hash_key)
        
        if idx == len(self.sorted_keys):
            return self.ring[self.sorted_keys[0]]
        
        return self.ring[self.sorted_keys[idx]]
    
    def get_nodes(self, key, count=3):
        """Get replicas for key"""
        if not self.ring:
            return []
        
        nodes = []
        hash_key = self._hash(key)
        
        idx = bisect.bisect_right(self.sorted_keys, hash_key)
        
        for i in range(count):
            idx_to_use = (idx + i) % len(self.sorted_keys)
            node = self.ring[self.sorted_keys[idx_to_use]]
            
            if node not in nodes:
                nodes.append(node)
        
        return nodes
    
    def _hash(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

# Usage
ch = ConsistentHash(nodes=["server1", "server2", "server3"])
print(ch.get_node("user:1"))  # Assigned server
print(ch.get_nodes("user:1", 3))  # Replicas
```

### Distributed Node Implementation

```python
class DistributedNode:
    def __init__(self, node_id: str, peers: list = None):
        self.node_id = node_id
        self.store = KVStore()
        self.peers = peers or []
        self.lock = threading.RLock()
    
    async def put(self, key: str, value, ttl_seconds: int = None):
        """Put with replication"""
        with self.lock:
            self.store.put(key, value, ttl_seconds)
        
        # Replicate to peers
        await self._replicate_to_peers("put", key, value, ttl_seconds)
    
    async def get(self, key: str):
        """Get with fallback to replicas"""
        value = self.store.get(key)
        
        if value is not None:
            return value
        
        # Try to get from replicas
        for peer in self.peers:
            try:
                value = await peer.get(key)
                if value is not None:
                    # Write back to local
                    self.store.put(key, value)
                    return value
            except Exception:
                continue
        
        return None
    
    async def _replicate_to_peers(self, operation: str, key: str, 
                                   value, ttl_seconds: int):
        """Async replication to peers"""
        for peer in self.peers:
            try:
                # Non-blocking send
                asyncio.create_task(
                    peer.replicate(operation, key, value, ttl_seconds)
                )
            except Exception:
                # Log and continue
                pass
```

## Database Schema

```sql
-- Main KV Store (key-value pairs)
CREATE TABLE key_value_store (
    key VARCHAR(256) PRIMARY KEY,
    value LONGTEXT,
    data_type VARCHAR(20),  -- string, list, hash, set, zset
    ttl_seconds INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed TIMESTAMP,
    access_count INT DEFAULT 0
);

-- Replication Log
CREATE TABLE replication_log (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    operation VARCHAR(20),  -- put, delete, expire
    key VARCHAR(256),
    value LONGTEXT,
    timestamp TIMESTAMP,
    node_id VARCHAR(50),
    INDEX idx_timestamp (timestamp),
    INDEX idx_node (node_id)
);

-- Snapshots (for persistence)
CREATE TABLE snapshots (
    snapshot_id VARCHAR(36) PRIMARY KEY,
    node_id VARCHAR(50),
    created_at TIMESTAMP,
    file_path VARCHAR(2048),
    row_count INT,
    compressed BOOLEAN
);
```

## Persistence & Recovery

### Write-Ahead Logging (WAL)

```python
class PersistentKVStore:
    def __init__(self, wal_file="wal.log"):
        self.store = KVStore()
        self.wal_file = wal_file
        self.wal_lock = threading.Lock()
    
    def put(self, key: str, value, ttl_seconds: int = None):
        """Put with WAL"""
        with self.wal_lock:
            # Write to WAL first
            self._write_wal("PUT", key, value, ttl_seconds)
            
            # Then update store
            self.store.put(key, value, ttl_seconds)
    
    def delete(self, key: str):
        with self.wal_lock:
            self._write_wal("DELETE", key)
            self.store.delete(key)
    
    def _write_wal(self, operation, key, value=None, ttl=None):
        """Write to WAL log"""
        entry = {
            "operation": operation,
            "key": key,
            "value": value,
            "ttl": ttl,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.wal_file, 'a') as f:
            f.write(json.dumps(entry) + "\n")
    
    def recover_from_wal(self):
        """Recover from WAL on startup"""
        if not os.path.exists(self.wal_file):
            return
        
        with open(self.wal_file, 'r') as f:
            for line in f:
                entry = json.loads(line)
                
                if entry["operation"] == "PUT":
                    self.store.put(
                        entry["key"], 
                        entry["value"], 
                        entry["ttl"]
                    )
                elif entry["operation"] == "DELETE":
                    self.store.delete(entry["key"])
```

### Snapshots

```python
class SnapshotManager:
    def __init__(self, snapshot_dir="snapshots/"):
        self.snapshot_dir = snapshot_dir
    
    def create_snapshot(self, store: KVStore) -> str:
        """Create snapshot of entire store"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_file = f"{self.snapshot_dir}snapshot_{timestamp}.json"
        
        # Dump all data
        with open(snapshot_file, 'w') as f:
            json.dump(store.data, f)
        
        return snapshot_file
    
    def load_snapshot(self, store: KVStore, snapshot_file: str):
        """Load snapshot into store"""
        with open(snapshot_file, 'r') as f:
            data = json.load(f)
            store.data.update(data)
```

## CAP Theorem & Consistency Models

```python
class ConsistencyMode:
    """
    CAP Theorem:
    - Consistency: All nodes see same data
    - Availability: All nodes can respond
    - Partition Tolerance: System works despite network split
    
    Choose 2 of 3
    """
    
    # CP: Consistency + Partition Tolerance
    # (Sacrifices availability)
    # - Wait for quorum writes
    # - Fail if quorum not reached
    class StrongConsistency:
        async def write(self, key, value, replicas):
            """Write to majority of replicas"""
            write_count = 0
            quorum = len(replicas) // 2 + 1
            
            for replica in replicas:
                try:
                    await replica.put(key, value)
                    write_count += 1
                except Exception:
                    pass
            
            if write_count >= quorum:
                return True
            raise Exception("Quorum write failed")
    
    # AP: Availability + Partition Tolerance
    # (Sacrifices consistency)
    # - Eventually consistent
    # - All writes accepted
    class EventualConsistency:
        async def write(self, key, value, replicas):
            """Write to primary, async replicate"""
            # Write to primary succeeds immediately
            primary_result = await replicas[0].put(key, value)
            
            # Replicate asynchronously
            for replica in replicas[1:]:
                asyncio.create_task(replica.put(key, value))
            
            return primary_result
```

## Interview Questions

1. **Why consistent hashing?**
   - Adding/removing node only requires rebalancing keys from that node

2. **How handle node failure?**
   - Replica on N nodes, read from any, write to quorum

3. **Replication strategy?**
   - Primary-replica or peer-to-peer

4. **Handle network partition?**
   - CAP: choose consistency (quorum) or availability (accept all)

5. **Persistence without losing async writes?**
   - WAL + snapshots + replication

## Key Design Points

- ✅ Consistent hashing for scalability
- ✅ In-memory with persistence
- ✅ Replication for availability
- ✅ WAL for durability
- ✅ Quorum reads/writes for consistency
- ✅ TTL for automatic cleanup
- ✅ Snapshots for recovery
- ✅ Multi-replica for fault tolerance
