# Advanced SQL Topics

## Window Functions
Allow performing calculations across a set of table rows.

```sql
SELECT 
    employee_id,
    salary,
    ROW_NUMBER() OVER (ORDER BY salary DESC) as rank,
    AVG(salary) OVER (PARTITION BY department) as dept_avg
FROM employees;
```

**Common Window Functions**:
- ROW_NUMBER(), RANK(), DENSE_RANK()
- LAG(), LEAD() - Access previous/next rows
- FIRST_VALUE(), LAST_VALUE()
- SUM(), AVG(), COUNT() as window functions

## Transactions and Locking

### Transaction Levels
- **Read Uncommitted**: Dirty reads possible (no locks)
- **Read Committed**: Dirty reads prevented but phantom reads possible
- **Repeatable Read**: Phantom reads possible
- **Serializable**: Highest isolation, full serialization

### Locking Mechanisms
- **Row-level Lock**: Lock individual rows
- **Table-level Lock**: Lock entire table
- **Deadlock**: When two transactions wait for each other

## Query Optimization

### Execution Plan Analysis
```sql
EXPLAIN SELECT * FROM orders WHERE customer_id = 5;
```

### Optimization Strategies
1. **Index Strategy**
   - Add indexes on WHERE, JOIN, ORDER BY columns
   - Avoid over-indexing (slows writes)
   - Consider composite indexes for multi-column queries

2. **Query Rewriting**
   - Avoid functions on indexed columns
   - Use UNION ALL instead of UNION (if duplicates acceptable)
   - Avoid OR conditions - use IN or UNION instead

3. **Partitioning**
   - Range partitioning by date/number
   - List partitioning by discrete values
   - Hash partitioning for load distribution

## Common Interview Questions

### Q1: How to find duplicate records?
```sql
SELECT column, COUNT(*) 
FROM table 
GROUP BY column 
HAVING COUNT(*) > 1;
```

### Q2: Find Nth highest salary
```sql
SELECT salary FROM employees 
ORDER BY salary DESC 
LIMIT 1 OFFSET N-1;

-- Using window function
SELECT salary FROM (
    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) as rank
    FROM employees
) WHERE rank = N;
```

### Q3: Update with JOIN
```sql
UPDATE orders o
SET o.status = 'shipped'
FROM customers c
WHERE o.customer_id = c.id AND c.premium = true;
```

### Q4: How to handle NULL values?
```sql
COALESCE(column1, column2, default_value)
ISNULL(column, default_value)  -- SQL Server
IFNULL(column, default_value)  -- MySQL
```

### Q5: Recursive Queries (CTEs)
```sql
WITH RECURSIVE numbers AS (
    SELECT 1 as n
    UNION ALL
    SELECT n + 1 FROM numbers WHERE n < 10
)
SELECT * FROM numbers;
```
