# Database Scaling and Performance

## Scaling Strategies

### Vertical Scaling
- Add more resources to single server (CPU, RAM, Storage)
- **Pros**: Simple, no application changes needed
- **Cons**: Hardware limits, single point of failure
- **Use case**: When data fits on one machine

### Horizontal Scaling
- Distribute data across multiple servers
- **Pros**: Unlimited scalability, high availability
- **Cons**: Complex, requires replication/sharding
- **Use case**: Big data, high traffic systems

## Replication

### Master-Slave (Primary-Replica)
```
Master (Write)
    |
    v
Slave (Read-only copies)
```

**Advantages**:
- Increases read throughput
- High availability (failover to slave)
- Load balancing for reads

**Disadvantages**:
- Replication lag (eventual consistency)
- Slave cannot handle writes
- Extra storage requirements

### Master-Master (Multi-Master)
Both servers can handle reads and writes, synchronized between them.

**Advantages**: No single point of failure

**Disadvantages**: Conflict resolution, higher complexity

## Sharding

### What is Sharding?
Horizontal partitioning: Split data across multiple databases based on shard key.

```
Shard 1: Users 1-1000
Shard 2: Users 1001-2000
Shard 3: Users 2001-3000
```

### Sharding Strategies

#### 1. Range-based
Shard by range of values (e.g., user_id ranges)
- **Pros**: Simple, easy to implement
- **Cons**: Hot shards if data non-uniform

#### 2. Hash-based
Shard by hash of shard key
- **Pros**: Uniform distribution
- **Cons**: Rebalancing difficult when adding shards

#### 3. Directory-based
Maintain lookup table for shard locations
- **Pros**: Flexible, supports range/hash schemes
- **Cons**: Extra lookup, single point of failure

#### 4. Geographic/Location-based
Shard by geographic region
- **Pros**: Low latency for users
- **Cons**: Uneven distribution possible

### Sharding Challenges
- **Cross-shard queries**: Slower, require aggregation
- **Rebalancing**: Complex when growing shards
- **Distributed transactions**: ACID compliance difficult
- **Joins across shards**: Nearly impossible

## Caching Strategies

### Query Result Caching
Store query results in fast cache (Redis, Memcached)

```python
# Pseudo-code
result = cache.get('user_123')
if result is None:
    result = database.query('SELECT * FROM users WHERE id = 123')
    cache.set('user_123', result, expire=3600)
return result
```

### Cache Invalidation Patterns

**1. TTL-based (Time To Live)**
Cache expires after set time.

**2. Event-based**
Invalidate on data changes.

**3. LRU (Least Recently Used)**
Remove least used items when cache full.

**4. Write-through**
Update cache and database together.

**5. Write-behind (Write-back)**
Update cache immediately, database asynchronously.

## Connection Pooling

### Why Connection Pooling?
Database connections are expensive. Maintain a pool of reusable connections.

```
Connection Pool (size: min=10, max=100)
   ├── Connection 1 (idle)
   ├── Connection 2 (in use)
   ├── Connection 3 (idle)
   └── ...
```

**Benefits**:
- Reduced connection overhead
- Better resource utilization
- Prevents connection exhaustion

## Common Interview Questions

### Q1: Design a highly available database system
```
- Multi-region replication (for disaster recovery)
- Read replicas in each region (for local reads)
- Database sharding by user_id (for scalability)
- Caching layer (Redis) for hot data
- Connection pooling (min=10, max=100)
- Monitoring and auto-failover
```

### Q2: How to handle database failover?
1. Detect primary failure (heartbeat timeout)
2. Promote replica to primary
3. Redirect write traffic to new primary
4. Update DNS records
5. Demote failed primary to replica when recovered

### Q3: Handling hot shards
- **Problem**: Some shards get more traffic than others
- **Solutions**:
  - Use secondary index on hot data
  - Add caching layer
  - Split hot shard further
  - Upgrade shard server resources

### Q4: Cross-shard transactions
```
Scenario: Transfer money from shard1 to shard2

Challenges:
- Need 2-phase commit (complex)
- Potential deadlocks
- Partial failures hard to handle

Solutions:
- Design schema to avoid cross-shard transactions
- Use eventual consistency with compensation
- Accept potential inconsistencies for some operations
```

### Q5: When would you shard?
- Data > single server capacity
- QPS exceeds single server throughput
- Need geographic distribution
- Cost optimization (use more small servers)

**When NOT to shard**:
- Data easily fits on one server
- Queries mostly require cross-shard joins
- Team inexperienced with distributed systems
