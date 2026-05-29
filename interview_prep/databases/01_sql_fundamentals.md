# SQL Fundamentals

## What is SQL?
SQL (Structured Query Language) is a standard language for managing and querying relational databases. It allows you to create, read, update, and delete data in structured tables.

## Key Concepts

### 1. Database Schema
- **Database**: A collection of organized data
- **Table**: A structured collection of rows and columns
- **Row**: A single record
- **Column**: An attribute of the data
- **Primary Key**: Unique identifier for each row
- **Foreign Key**: Links to primary key in another table

### 2. Data Types
- INTEGER, FLOAT, DECIMAL
- VARCHAR, CHAR, TEXT
- DATE, TIME, TIMESTAMP
- BOOLEAN

### 3. Normalization
**Purpose**: Reduce redundancy and maintain data integrity

**Normal Forms**:
- **1NF**: Eliminate duplicate columns from same table
- **2NF**: Remove partial dependencies (all non-key attributes fully dependent on primary key)
- **3NF**: Remove transitive dependencies (non-key attributes not dependent on other non-key attributes)
- **BCNF**: Every determinant is a candidate key
- **4NF, 5NF**: Handle multi-valued and join dependencies

### 4. JOINS
- **INNER JOIN**: Returns matching records from both tables
- **LEFT JOIN**: All records from left table + matching from right
- **RIGHT JOIN**: All records from right table + matching from left
- **FULL OUTER JOIN**: All records from both tables
- **CROSS JOIN**: Cartesian product of both tables
- **SELF JOIN**: Join a table to itself

### 5. Aggregation Functions
- COUNT(), SUM(), AVG(), MIN(), MAX()
- GROUP BY, HAVING

### 6. Subqueries and CTEs
- **Subquery**: Query inside another query
- **CTE (Common Table Expression)**: WITH clause for readable queries

## Common Interview Questions

### Q1: What's the difference between DELETE and TRUNCATE?
```sql
DELETE FROM table WHERE condition;  -- Can be rolled back, slower
TRUNCATE TABLE table;              -- Faster, DDL operation
```

### Q2: Explain ACID properties
- **Atomicity**: Transaction completes fully or not at all
- **Consistency**: Data valid before and after transaction
- **Isolation**: Concurrent transactions don't interfere
- **Durability**: Committed data persists even after failure

### Q3: What is a VIEW?
Virtual table based on SELECT query. Can be used for security and simplifying complex queries.

### Q4: Indexes
- **Purpose**: Speed up data retrieval
- **Types**: Primary Index, Unique Index, Composite Index, Full-text Index
- **Trade-off**: Faster reads but slower writes and more storage

### Q5: What's the difference between HAVING and WHERE?
- **WHERE**: Filters rows before aggregation
- **HAVING**: Filters groups after aggregation

## Performance Tips
- Use indexes on frequently queried columns
- Avoid SELECT * - specify needed columns
- Use EXPLAIN to analyze query execution
- Denormalize when read performance is critical
- Use database-specific optimization techniques
