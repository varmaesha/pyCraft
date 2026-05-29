# NoSQL Fundamentals

## What is NoSQL?
Non-relational databases designed for distributed, unstructured, or semi-structured data. Prioritizes scalability and flexibility over strict consistency.

## Types of NoSQL Databases

### 1. Document Databases
**Examples**: MongoDB, CouchDB, Firebase
- Store data as JSON/BSON documents
- Flexible schema (schemaless)
- Hierarchical data support
- Use case: User profiles, content management

```javascript
// MongoDB example
db.users.insertOne({
    _id: 1,
    name: "John",
    email: "john@example.com",
    address: {
        city: "NYC",
        zip: "10001"
    },
    tags: ["developer", "python"]
});
```

### 2. Key-Value Stores
**Examples**: Redis, Memcached, DynamoDB
- Simple key-value pairs
- Ultra-fast retrieval
- In-memory storage
- Use case: Caching, sessions, real-time data

```
SET user:123:name "John"
GET user:123:name
```

### 3. Column-Family Stores
**Examples**: HBase, Cassandra
- Data organized by columns instead of rows
- Excellent for time-series data
- Highly scalable and available
- Use case: Analytics, time-series data

### 4. Search Engines
**Examples**: Elasticsearch, Solr
- Full-text search capabilities
- Indexing and aggregation
- Real-time analytics
- Use case: Search functionality, logging

### 5. Graph Databases
**Examples**: Neo4j, ArangoDB
- Nodes, edges, and properties
- Relationship traversal
- Use case: Social networks, recommendation engines

```
CREATE (john:Person {name: "John"})
CREATE (jane:Person {name: "Jane"})
CREATE (john)-[:KNOWS]->(jane)
```

## CAP Theorem
In a distributed system, you can guarantee only 2 of 3:

- **Consistency**: All nodes see same data at same time
- **Availability**: System always responsive
- **Partition Tolerance**: System continues despite network partitions

**NoSQL Trade-offs**:
- MongoDB: CP (consistency + partition tolerance)
- Cassandra: AP (availability + partition tolerance)
- Redis: CP (consistency + partition tolerance)

## Common Interview Questions

### Q1: SQL vs NoSQL
| Factor | SQL | NoSQL |
|--------|-----|-------|
| Schema | Fixed | Flexible |
| Scalability | Vertical | Horizontal |
| ACID | Strong | Eventual consistency |
| Joins | Native support | Limited |
| Data Structure | Structured | Unstructured/Semi-structured |

### Q2: When to use NoSQL?
- Massive scale requirements
- High velocity/high volume data
- Flexible schema requirements
- Geographic distribution needed
- Real-time data processing

### Q3: Document vs Relational
**Document DB**:
- Nested data naturally represented
- Fewer queries needed
- Schema evolution easier

**Relational DB**:
- Data normalization prevents redundancy
- ACID guarantees
- Complex queries easier

### Q4: Sharding vs Replication
- **Sharding**: Data split across multiple servers (horizontal scaling)
- **Replication**: Same data copied across multiple servers (availability)

### Q5: Eventual Consistency
Data eventually becomes consistent across all nodes after some time. Acceptable for:
- Social media likes/comments
- Analytics data
- Recommendations

Not acceptable for:
- Financial transactions
- Inventory management
- Critical medical data
