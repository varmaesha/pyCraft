# Data Consistency and Distributed Patterns

## ACID Properties Deep Dive

### Atomicity
**All or Nothing**: Transaction either completes fully or rolls back completely.

```sql
-- Either both succeed or both fail
BEGIN TRANSACTION;
  UPDATE account_from SET balance = balance - 100 WHERE id = 1;
  UPDATE account_to SET balance = balance + 100 WHERE id = 2;
COMMIT; -- or ROLLBACK
```

**Implementation**: Write-ahead logging (WAL)

### Consistency
Data moves from one valid state to another.

```sql
-- Rule: Total balance always equal
BEGIN TRANSACTION;
  -- If this fails, transaction rolls back (consistency maintained)
  UPDATE accounts SET total_deducted = total_deducted + 100 WHERE type = 'debit';
  UPDATE accounts SET total_deposited = total_deposited + 100 WHERE type = 'credit';
COMMIT;
```

### Isolation
Concurrent transactions don't interfere.

```
Transaction A: Read(x=100)
Transaction B: Write(x=200) 
Transaction A: Read(x=?) -- Should read 100 or 200 depending on isolation level
```

### Durability
Committed data persists even after failure.

**Implementation**: Fsync to persistent storage before confirming write

## Isolation Levels and Anomalies

### Read Phenomena

**1. Dirty Read**
Reading uncommitted data from another transaction.
```
T1: UPDATE user SET age=30
T2: READ age (sees 30)
T1: ROLLBACK (age back to original)
T2: Read stale data!
```

**2. Non-repeatable Read**
Same row read twice returns different values.
```
T1: READ age=30
T2: UPDATE age=35
T1: READ age=35 (changed!)
```

**3. Phantom Read**
Query returns different set of rows on repeat.
```
T1: SELECT * FROM users WHERE age > 25 (returns 5 rows)
T2: INSERT user WITH age=26
T1: SELECT * FROM users WHERE age > 25 (returns 6 rows)
```

### Isolation Levels

| Level | Dirty Read | Non-repeatable | Phantom | Performance |
|-------|-----------|----------------|---------|-------------|
| Read Uncommitted | Possible | Possible | Possible | Fastest |
| Read Committed | No | Possible | Possible | Good |
| Repeatable Read | No | No | Possible | Better |
| Serializable | No | No | No | Slowest |

## Eventual Consistency Patterns

### When to Accept Eventual Consistency
- Social media likes/followers
- Search indexes
- Analytics dashboards
- Recommendations

### Patterns for Handling Eventual Consistency

**1. Caching Pattern**
```
Client: Write to primary
Client: Read from cache (might be stale)
Background: Cache updates when replica catches up
```

**2. Event Sourcing**
```
Store all state changes as immutable events:
- UserCreated(id=1, name="John")
- UserEmailChanged(id=1, email="john@example.com")
- UserDeleted(id=1)

Rebuild state by replaying events
```

**3. CQRS (Command Query Responsibility Segregation)**
```
Writes: Normalized database (strong consistency)
Reads: Denormalized read model (eventually consistent)

Process:
Write Command -> Update DB -> Emit Event -> Update Read Model (async)
```

**4. Two-Phase Commit (2PC)**
For distributed transactions:
```
Phase 1 (Prepare): 
  Coordinator asks all participants: "Can you commit?"
  
Phase 2 (Commit/Abort):
  If all say yes: Coordinator broadcasts COMMIT
  If any say no: Coordinator broadcasts ABORT
```

**Limitations**: Blocking, coordination overhead, failure sensitivity

## Conflict Resolution

### Vector Clocks
Track causal relationships between events.

```
Node A: [2, 0, 0] - 2 events from A
Node B: [1, 3, 0] - 1 from A, 3 from B
Node C: [0, 0, 5] - 5 from C

Compare: [1,2,0] vs [2,1,0]
- First version: (1<2, 2>1) -> Concurrent (conflict)
- If [2,3,0] vs [2,3,1] -> Second is newer (causal dependency)
```

### Last-Write-Wins (LWW)
Keep version with latest timestamp. Simple but can lose data.

### Application-level Resolution
Merge strategies based on business logic:
```javascript
// Keep both versions (store conflict)
{
  doc_id: 123,
  conflicts: [version1, version2]
}

// Custom merge logic
const merged = {
  ...version1,
  title: version1.title, // Keep version1's title
  tags: [...new Set([...version1.tags, ...version2.tags])] // Merge tags
}
```

## Common Interview Questions

### Q1: Design a payment system (requires strong consistency)
```
Requirements:
- No lost transactions
- No double-charging
- Account balance always correct

Design:
- Single primary database (MySQL with InnoDB)
- Synchronous replication
- 2-phase commit for multi-account transfers
- Audit trail of all transactions
- Strict isolation level (Serializable)
```

### Q2: Design a social network (eventual consistency acceptable)
```
Requirements:
- Fast writes (likes, follows)
- Massive scale
- Some staleness acceptable

Design:
- Event-driven architecture
- NoSQL for writes (MongoDB/Cassandra)
- Cache layer (Redis) for reads
- Background jobs to update read models
- Replication with eventual consistency
```

### Q3: Why would you use eventual consistency?
- High availability requirement
- Geographic distribution
- Cost optimization
- Write-heavy workloads

### Q4: Handling concurrent updates
```
Scenario: Two users edit same document

Solutions:
1. Optimistic Locking: 
   version = 5
   UPDATE doc SET content=?, version=6 WHERE id=? AND version=5
   
2. Operational Transformation: 
   Track operations, merge concurrent edits intelligently
   
3. CRDTs (Conflict-free Replicated Data Types):
   Data structure resolves conflicts automatically
```

### Q5: Read-after-write consistency
After client writes, subsequent reads see that write.

**Implementation**:
- Read from primary for recent writes
- Use write tokens/timestamps
- Cache own writes locally

```javascript
// Client-side approach
writeTransaction(data) {
  db.write(data); // timestamp = now
  localCache.set(data); // read immediately from cache
}

read(id) {
  // Check if we just wrote this
  if (localCache.has(id)) return localCache.get(id);
  // Otherwise read from replica
  return db.read(id);
}
```
