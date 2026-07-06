# SQL and Data Processing Interview Prep

This file is for SQL, pandas, and data-related interview questions that often come up with Python roles.

---

## 1. What is the difference between SQL and NoSQL?

**Answer**:
- SQL databases use tables with fixed schemas.
- NoSQL databases are more flexible and are often used for unstructured or rapidly changing data.
- Use SQL when consistency and relationships matter.
- Use NoSQL when scale and flexibility matter more.

**Real-life example**:
- SQL for banking systems
- NoSQL for product catalog or event logging

---

## 2. What is a primary key?

**Answer**:
A primary key uniquely identifies each row in a table.

```sql
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(100)
);
```

**Why it matters**:
- It ensures uniqueness.
- It helps join tables reliably.

---

## 3. What is a foreign key?

**Answer**:
A foreign key links one table to another.

```sql
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**Real-life example**:
- Each order belongs to one user.

---

## 4. What is the difference between INNER JOIN and LEFT JOIN?

**Answer**:
- `INNER JOIN` returns only matching rows.
- `LEFT JOIN` returns all rows from the left table and matching rows from the right table.

```sql
SELECT u.name, o.order_id
FROM users u
INNER JOIN orders o ON u.id = o.user_id;
```

**Real-life example**:
- Use `LEFT JOIN` when you want every user, even those with no orders.

---

## 5. What is GROUP BY used for?

**Answer**:
`GROUP BY` groups rows with the same value in one or more columns.

```sql
SELECT department, COUNT(*) AS total_employees
FROM employees
GROUP BY department;
```

**Real-life example**:
- Count how many employees work in each department.

---

## 6. What is the difference between WHERE and HAVING?

**Answer**:
- `WHERE` filters rows before grouping.
- `HAVING` filters after grouping.

```sql
SELECT department, COUNT(*) AS cnt
FROM employees
WHERE salary > 50000
GROUP BY department
HAVING COUNT(*) > 2;
```

---

## 7. Second highest salary

```sql
SELECT MAX(salary) AS second_highest_salary
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);
```

**Simple explanation**:
- First find the highest salary.
- Then find the highest salary that is still lower than that.

---

## 8. Find duplicate rows

```sql
SELECT name, COUNT(*)
FROM users
GROUP BY name
HAVING COUNT(*) > 1;
```

**Real-life example**:
- Detect duplicate customer names or email entries.

---

## 9. What is normalization?

**Answer**:
Normalization is the process of organizing data to reduce duplication and improve consistency.

**Example**:
- Instead of storing customer address in every order row, keep it in a separate table.

---

## 10. What is indexing?

**Answer**:
An index helps the database find rows faster.

**Example**:
```sql
CREATE INDEX idx_users_email ON users(email);
```

**Important note**:
- Indexes speed up reads.
- They can slow down writes slightly.

---

## 11. What is a transaction?

**Answer**:
A transaction is a group of database operations that should succeed or fail together.

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

**Real-life example**:
- Money transfer between bank accounts.

---

## 12. What is the difference between DELETE and TRUNCATE?

**Answer**:
- `DELETE` removes rows one by one and can be rolled back.
- `TRUNCATE` removes all rows faster but is more destructive.

---

## 13. What is a view?

**Answer**:
A view is a virtual table based on a query.

```sql
CREATE VIEW active_users AS
SELECT * FROM users WHERE active = 1;
```

**Use case**:
- Hide complexity from users.
- Provide a simple interface for reporting.

---

## 14. pandas basics you should know

### Create a dataframe
```python
import pandas as pd

df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35]
})
```

### View first rows
```python
print(df.head())
```

### Filter rows
```python
print(df[df['age'] > 28])
```

### Group by
```python
print(df.groupby('age').size())
```

### Fill missing values
```python
df['age'] = df['age'].fillna(0)
```

### Drop duplicates
```python
df = df.drop_duplicates()
```

---

## 15. Difference between merge, join, and concat in pandas

### Merge
```python
import pandas as pd

customers = pd.DataFrame({
    'customer_id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie']
})

orders = pd.DataFrame({
    'customer_id': [1, 2, 4],
    'amount': [100, 200, 300]
})

merged = pd.merge(customers, orders, on='customer_id', how='left')
print(merged)
```

**Simple answer**:
- `merge` combines on a common key.
- `join` is similar but is more like a database join.
- `concat` stacks dataframes on top of each other or side by side.

---

## 16. What is the difference between `apply`, `map`, and vectorized operations?

**Answer**:
- `apply` is flexible but slower for large data.
- `map` is useful for simple transformations.
- Vectorized operations are fastest because pandas uses optimized C code.

```python
import pandas as pd

s = pd.Series([1, 2, 3])
print(s * 2)  # vectorized
```

---

## 17. Common SQL + pandas interview questions

- How do you find duplicates?
- How do you handle missing values?
- How do you join two tables/dataframes?
- How do you aggregate a column by category?
- How do you find the top 3 salaries?

---

## 18. A good interview answer structure for SQL/data questions

Use this structure:
1. Say what the concept means in simple words.
2. Give a small example.
3. Give a real-world use case.
4. Mention trade-offs if needed.

**Example**:
> A join combines two tables based on a common column. In a real business app, you might join customers and orders to see which customer bought what.

---

## 19. Final practice checklist

- Practice `SELECT`, `WHERE`, `GROUP BY`, `HAVING`, `JOIN`
- Practice basic SQL questions like second highest salary and duplicates
- Practice pandas operations like filtering, grouping, merging, and filling missing values
- Be able to explain why one approach is better than another in a real production case
