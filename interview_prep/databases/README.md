# Database Interview Topics

This folder contains comprehensive coverage of SQL, NoSQL, and database design topics commonly asked in technical interviews.

## Topics Covered

### 1. **SQL Fundamentals** (`01_sql_fundamentals.md`)
- Database schema and data types
- Normalization and normal forms
- JOIN types and operations
- Aggregation and subqueries
- ACID properties and basic optimization

### 2. **Advanced SQL** (`02_advanced_sql.md`)
- Window functions
- Transactions and isolation levels
- Query optimization and execution plans
- Common SQL interview problems
- Recursive queries and CTEs

### 3. **NoSQL Fundamentals** (`03_nosql_fundamentals.md`)
- Types of NoSQL databases (document, key-value, column-family, graph, search)
- CAP theorem and trade-offs
- SQL vs NoSQL comparison
- When to use NoSQL
- Sharding and replication basics

### 4. **Database Design** (`04_database_design.md`)
- Requirements analysis and ER modeling
- Entity relationships (1:1, 1:N, N:N)
- Normalization vs denormalization
- Indexing strategies
- System design examples

### 5. **Scaling and Performance** (`05_scaling_and_performance.md`)
- Vertical vs horizontal scaling
- Replication (master-slave, master-master)
- Sharding strategies and challenges
- Caching patterns and invalidation
- Connection pooling

### 6. **Common Databases** (`06_common_databases.md`)
- Relational: MySQL, PostgreSQL, SQL Server
- Key-Value: Redis
- Document: MongoDB
- Column-Family: Cassandra
- Search: Elasticsearch
- Graph: Neo4j
- When to use each database

### 7. **Data Consistency Patterns** (`07_data_consistency_patterns.md`)
- ACID properties deep dive
- Isolation levels and anomalies
- Eventual consistency patterns
- Event sourcing and CQRS
- Conflict resolution strategies
- Distributed transactions

## Quick Reference

### Key Concepts
- **Normalization**: Eliminate data redundancy (1NF → 3NF → BCNF)
- **Denormalization**: Optimize for read performance by duplicating data
- **Sharding**: Horizontal partitioning of data across servers
- **Replication**: Copying data to multiple servers for availability
- **CAP Theorem**: Can only guarantee 2 of 3 (Consistency, Availability, Partition tolerance)
- **ACID**: Atomicity, Consistency, Isolation, Durability
- **Eventual Consistency**: Data becomes consistent eventually, not immediately

### Database Selection Matrix
```
| Requirement                    | Use              |
|--------------------------------|------------------|
| Complex queries & transactions | PostgreSQL       |
| High write throughput          | Cassandra        |
| Fast caching/sessions          | Redis            |
| Flexible schema                | MongoDB          |
| Full-text search               | Elasticsearch    |
| Relationships/graph data       | Neo4j            |
| Time-series analytics          | ClickHouse       |
```

## Interview Question Categories

### Design Questions
- Design Twitter/Instagram/Facebook (user follower relationships)
- Design payment system (strong consistency required)
- Design recommendation engine (relationships matter)
- Design hotel booking system (inventory management)

### Theory Questions
- Explain ACID properties
- What's CAP theorem?
- SQL vs NoSQL trade-offs
- When to denormalize?
- How does indexing work?

### Optimization Questions
- Optimize slow query
- Design indexes for query pattern
- Handle hot shards
- Cache invalidation strategies

### Scaling Questions
- How to scale read-heavy workload?
- Design highly available system
- Handle cross-shard transactions
- Failover strategy

## Tips for Interview

1. **Understand Trade-offs**: Every choice (SQL vs NoSQL, normalization vs denormalization) has pros and cons
2. **Ask Clarifying Questions**: Understand requirements before designing
3. **Start Simple**: Build design incrementally, address bottlenecks
4. **Think About Scale**: Consider QPS, data volume, growth trajectory
5. **Discuss Alternatives**: Show you know multiple approaches
6. **Performance Matters**: Know basic optimization techniques
7. **Know Your Databases**: Be familiar with common databases' strengths/weaknesses

## Common Mistakes to Avoid

❌ Choosing SQL for everything (some problems need NoSQL)
❌ Ignoring indexing in design
❌ Over-normalizing (excessive joins hurt performance)
❌ Not considering replication/sharding early
❌ Assuming strong consistency is always needed
❌ Ignoring CAP theorem constraints
❌ Not testing with realistic data volumes

## Resources to Deep Dive

- Study existing large-scale systems (YouTube, Netflix architecture)
- Practice writing SQL queries
- Understand transaction isolation levels in depth
- Learn about distributed systems challenges
- Experiment with multiple database types
