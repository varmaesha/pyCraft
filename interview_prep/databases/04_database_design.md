# Database Design Principles

## Requirements Analysis
1. **Identify entities** and their attributes
2. **Define relationships** between entities
3. **Determine cardinality** (1:1, 1:N, N:N)
4. **Specify constraints** and business rules
5. **Plan for scale** and performance

## Entity-Relationship Model (ER)

### Entity Types
- **Strong Entity**: Can exist independently (has primary key)
- **Weak Entity**: Depends on another entity (partial key + foreign key)

### Relationships
- **One-to-One (1:1)**: Each entity relates to exactly one other
- **One-to-Many (1:N)**: One entity relates to many others
- **Many-to-Many (N:N)**: Multiple entities relate to multiple others

### N:N Resolution
N:N relationships cannot be directly modeled in relational databases. Use junction/bridge table:

```
Students ---|< Enrollment >|--- Courses
                 |
          (student_id, course_id)
```

## Denormalization Trade-offs

### When to Denormalize
1. **Read-heavy workloads**: Reduce JOIN operations
2. **Reporting queries**: Pre-aggregated data
3. **Historical data**: Snapshot columns
4. **Cache optimization**: Duplicate frequently accessed data

### Denormalization Example
```sql
-- Normalized
CREATE TABLE orders (order_id, customer_id, total);
CREATE TABLE customers (customer_id, name, email);

-- Denormalized (customer data copied)
CREATE TABLE orders (
    order_id, 
    customer_id, 
    customer_name,  -- Denormalized
    customer_email, -- Denormalized
    total
);
```

## Indexing Strategy

### Index Types
- **Primary Index**: On primary key (unique, not null)
- **Unique Index**: Ensures uniqueness on column(s)
- **Composite Index**: Multiple columns
- **Full-text Index**: Text searching
- **Spatial Index**: Geographic data

### Index Selection Rules
1. Index columns in WHERE clause
2. Index columns in JOIN conditions
3. Index columns in ORDER BY/GROUP BY
4. Don't over-index (impacts INSERT/UPDATE performance)
5. Monitor and maintain indexes regularly

### Composite Index Order Matters
```sql
-- Index on (department, salary)
-- Efficient for: WHERE department = 'Sales' AND salary > 50000
-- Not efficient for: WHERE salary > 50000 (leading column not used)
```

## Common Interview Questions

### Q1: Design a Twitter-like system (users, tweets, followers)

```sql
-- Users
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    email VARCHAR(100),
    created_at TIMESTAMP
);

-- Tweets
CREATE TABLE tweets (
    tweet_id INT PRIMARY KEY,
    user_id INT FOREIGN KEY,
    content TEXT,
    created_at TIMESTAMP,
    INDEX (user_id, created_at)
);

-- Followers
CREATE TABLE followers (
    follower_id INT,
    following_id INT,
    created_at TIMESTAMP,
    PRIMARY KEY (follower_id, following_id),
    FOREIGN KEY (follower_id) REFERENCES users(user_id),
    FOREIGN KEY (following_id) REFERENCES users(user_id)
);

-- Feed query
SELECT t.* FROM tweets t
JOIN followers f ON t.user_id = f.following_id
WHERE f.follower_id = ?
ORDER BY t.created_at DESC
LIMIT 20;
```

### Q2: Handle One-to-Many relationships
```sql
-- Correct approach
CREATE TABLE departments (dept_id INT PRIMARY KEY);
CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    dept_id INT FOREIGN KEY REFERENCES departments(dept_id)
);
```

### Q3: Design schema for comments on comments (nested)
```sql
CREATE TABLE comments (
    comment_id INT PRIMARY KEY,
    post_id INT,
    parent_comment_id INT,  -- NULL for top-level, references comment_id for replies
    user_id INT,
    content TEXT,
    created_at TIMESTAMP,
    FOREIGN KEY (parent_comment_id) REFERENCES comments(comment_id)
);
```

### Q4: Soft deletes vs Hard deletes
```sql
-- Soft delete (keep data for audit trails)
CREATE TABLE records (
    record_id INT PRIMARY KEY,
    deleted_at TIMESTAMP NULL,
    -- Query: SELECT * FROM records WHERE deleted_at IS NULL;
);

-- Hard delete (permanent removal)
DELETE FROM records WHERE record_id = ?;
```

### Q5: How to store hierarchical data?
**Options**:
1. **Adjacency List**: parent_id column
2. **Nested Sets**: left, right boundary values
3. **Path Enumeration**: Full path as string
4. **Closure Table**: Separate table tracking all ancestor-descendant pairs

**Choose based on**:
- How often you query vs update hierarchy
- Depth of hierarchy
- Performance requirements
