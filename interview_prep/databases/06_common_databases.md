# Common Databases

## Relational Databases

### MySQL
**Characteristics**:
- Open source, widely used
- Good for web applications
- ACID compliance (with InnoDB)
- Vertical scaling friendly

**Best for**: Web apps, OLTP systems

**Limitations**: 
- Limited horizontal scaling
- Not optimized for complex analytics
- Replication can lag

### PostgreSQL
**Characteristics**:
- Open source, advanced features
- Strong ACID guarantees
- JSON/JSONB support (semi-structured)
- Window functions, CTEs
- Full-text search

**Best for**: Complex queries, data integrity critical

**Advantages over MySQL**:
- Better query optimizer
- More SQL standards compliance
- Advanced data types

### SQL Server
**Characteristics**:
- Microsoft enterprise database
- Built-in analytics tools
- Strong security features
- Power BI integration

**Best for**: Enterprise, Windows environments

## NoSQL Databases

### MongoDB (Document)
```javascript
db.users.find({age: {$gt: 25}})
```

**Characteristics**:
- Flexible schema
- Good horizontal scaling
- ACID transactions (since 4.0)
- JSON-like BSON format

**Use cases**: Content management, user profiles, mobile apps

**Trade-offs**:
- Higher storage (denormalization)
- Eventual consistency by default
- No JOINs (requires client-side assembly)

### Redis (Key-Value)
```
SET user:123 '{"name":"John","age":25}'
GET user:123
```

**Characteristics**:
- In-memory, ultra-fast
- Multiple data structures (strings, lists, sets, sorted sets)
- Pub/Sub messaging
- Persistence options

**Use cases**: Caching, sessions, real-time counters, leaderboards

**Limitations**: 
- Entire dataset must fit in RAM
- Limited query capabilities
- Single-threaded (though cluster mode available)

### Cassandra (Column-Family)
**Characteristics**:
- Highly available and scalable
- Tunable consistency (eventual by default)
- Excellent for time-series data
- Linear scalability

**Use cases**: Time-series, analytics, high-write load

**Trade-offs**:
- Complex to operate
- Limited query capabilities
- Eventually consistent by default

### Elasticsearch (Search Engine)
**Characteristics**:
- Full-text search
- Near real-time indexing
- Distributed and scalable
- RESTful API

**Use cases**: Log analysis, search functionality, analytics

**Trade-offs**:
- High memory usage
- Not good for transactional data
- Index management overhead

### Neo4j (Graph)
```
MATCH (n:Person)-[:KNOWS]->(m:Person) 
WHERE n.name = 'John' 
RETURN m
```

**Characteristics**:
- Relationship traversal extremely fast
- ACID transactions
- Powerful query language (Cypher)

**Use cases**: Social networks, recommendations, knowledge graphs

**Trade-offs**:
- Overkill for non-graph data
- Smaller ecosystem vs SQL
- Scaling more complex

## When to Use What

| Use Case | Database |
|----------|----------|
| Standard business application | PostgreSQL, MySQL |
| High-speed caching | Redis |
| Time-series/analytics | Cassandra, ClickHouse |
| Document/flexible schema | MongoDB |
| Search/logging | Elasticsearch |
| Social networks/relationships | Neo4j |
| Real-time analytics | DuckDB, ClickHouse |

## Comparison Table

| Feature | SQL | MongoDB | Redis | Cassandra |
|---------|-----|---------|-------|-----------|
| ACID | Strong | Yes | Partial | Limited |
| Horizontal Scale | Difficult | Easy | Cluster | Easy |
| Query Complex | Yes | Limited | Limited | Limited |
| Write Throughput | Medium | High | Very High | Very High |
| Read Throughput | High | High | Very High | High |
| Consistency | Strong | Strong | Strong | Eventual |

## Common Interview Questions

### Q1: MySQL vs PostgreSQL?
```
MySQL: Simpler, faster for simple queries
PostgreSQL: Advanced features, better for complex systems
```

### Q2: When would you use NoSQL over SQL?
- Massive scale
- Flexible/evolving schema
- High write throughput
- Geographic distribution

### Q3: Redis as database vs cache?
```
Redis as Cache: Temporary data, loss acceptable
Redis as Database: Persistence enabled, but risky as primary
```

### Q4: Cassandra vs MongoDB?
```
Cassandra: Better for massive write volume
MongoDB: Better for flexible queries and transactions
```

### Q5: How to migrate from SQL to NoSQL?
1. Identify data access patterns
2. Design document structure
3. Plan for denormalization
4. Handle joins at application level
5. Test for performance
6. Plan rollback strategy
