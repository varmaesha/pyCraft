# Python Oop Design And Patterns

This file combines content from the following source files in `interview_prep/segragate/`:
- ADVANCED_PYTHON_INTERVIEW_GUIDE.md
- PYTHON_INTERVIEW_QUESTION_BANK.md
- TOP_40_QUESTIONS.md

---

## Source: ADVANCED_PYTHON_INTERVIEW_GUIDE.md

# Advanced Python Interview Guide

This guide is meant to complement the existing interview prep notes with practical, interview-style answers and real-world examples.

---

## 1. Which is faster: list or tuple?

**Short answer:**
- `list` is more flexible but usually a bit slower and uses more memory.
- `tuple` is slightly faster for iteration and uses less memory because it is immutable.

**How to say it in an interview:**
> I would choose a list when I need to change the data often. I would choose a tuple when I want something safer and lighter, especially for values that should not change.

**Simple memory trick:**
- Think of a list as a backpack you can keep adding to.
- Think of a tuple as a fixed box that you are not supposed to change.

**Example**
```python
import sys

l = [1, 2, 3, 4, 5]
t = (1, 2, 3, 4, 5)

print(sys.getsizeof(l))  # larger
print(sys.getsizeof(t))  # smaller
```

**Real-world use case**:
- Use `list` when you need to add/remove items often.
- Use `tuple` for constant data such as coordinates, config values, return values from functions.

**Interview-style answer**:
> A tuple is faster and lighter because it is immutable, while a list supports mutation and therefore needs extra overhead.

---

## 2. Common list functions you should know

```python
nums = [3, 1, 2, 2, 4]

nums.append(5)          # add at end
nums.insert(1, 99)      # insert at index
nums.remove(2)          # remove first matching value
nums.pop()              # remove last element
nums.sort()             # sort in place
nums.reverse()          # reverse in place
nums.count(2)           # count occurrences
nums.index(4)           # find index
```

**Important notes**:
- `append` is efficient.
- `insert` and `remove` can be slower for large lists.
- `list` methods mutate the original list unless you create a copy.

**Real-life explanation**:
- If you are building a shopping cart, you will keep appending items and removing them when needed.
- That is why lists are so common in day-to-day Python code.

**Real-world use case**:
- A shopping cart list uses `append`, `remove`, and `pop` frequently.

---

## 3. What makes a dictionary key valid?

Dictionary keys must be hashable.

**Hashable examples**:
- `int`
- `str`
- `tuple`
- `frozenset`

**Not hashable**:
- `list`
- `dict`
- `set`

```python
valid_dict = {
    "name": "Alice",
    1: "one",
    (1, 2): "pair"
}

# This will fail
# invalid_dict = {[1, 2]: "x"}
```

**Interview answer**:
> A dictionary key needs a stable hash value so Python can quickly find the value. Mutable objects like lists and sets are not hashable because their contents can change. In simple terms, dictionaries need a key that will not suddenly become different.

**Real-world use case**:
- A user profile cache may use user ID as a key.
- A `dict` of product IDs to prices is common in e-commerce systems.

---

## 4. What happens when two lists are compared with `==` and `is`?

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)  # True -> same contents
print(a is b)  # False -> different objects
print(a is c)  # True -> same object
```

**Key difference**:
- `==` checks values.
- `is` checks identity (same object in memory).

**Interview-style answer**:
> `==` asks, “Do these two objects contain the same data?” while `is` asks, “Are these the exact same object?”

**Human version**:
- `==` means “same contents”
- `is` means “same identity”

A very common mistake is thinking that two equal lists are the same object. They may have the same values, but they are still different objects in memory.

---

## 5. Decorator in a simpler way

A decorator wraps a function and changes or extends its behavior.

```python
def log_call(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_call
def add(a, b):
    return a + b

print(add(2, 3))
```

**Simpler memory trick**:
- Decorator = “wrapper around a function”
- Real-world analogy: a security check before entering a room

**Very simple explanation**:
> A decorator is like putting a small layer around a function so that before or after it runs, you can do extra work such as logging, validation, or authentication.

**Use cases**:
- logging
- authentication
- caching
- performance timing

---

## 6. List vs generator: memory usage

```python
nums_list = [i * i for i in range(10_000_000)]
nums_gen = (i * i for i in range(10_000_000))
```

**Key difference**:
- A list stores all values in memory.
- A generator produces one value at a time.

**Memory idea**:
- `list` -> `O(n)` memory
- `generator` -> `O(1)` memory (mostly)

**Human explanation**:
- A list is like loading an entire box of books into your room.
- A generator is like taking one book out at a time when you need it.

That is why generators are so helpful when working with huge files or endless streams of data.

**Real-world use case**:
- Use a generator for large files or streaming data.
- Use a list when you need random access and repeated iteration.

---

## 7. Context managers: a way you will not forget

A context manager ensures that resources are properly opened and closed.

```python
with open("sample.txt", "w") as f:
    f.write("Hello")
```

**Memory trick**:
- “Open it, use it, close it automatically”
- The `with` statement calls `__enter__()` and `__exit__()` behind the scenes.

**Very human version**:
> A context manager is just a clean way to say, “Use this resource while I am inside this block, and make sure it is cleaned up when I am done.”

This is one of those ideas that becomes very natural once you use it with files, database connections, and locks.

**Custom example**:
```python
class FileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

with FileManager("sample.txt", "r") as f:
    print(f.read())
```

**Use cases**:
- file handling
- database connections
- locks
- temporary resources

---

## 8. Multithreading vs multiprocessing

### Multithreading
- Good for I/O-bound work
- Threads share memory
- Useful when waiting on network, file I/O, database calls

### Multiprocessing
- Good for CPU-bound work
- Separate processes with their own memory
- Useful for heavy calculations, image processing, data transformation

**Real-life examples**:
- I/O task: downloading 100 images from the internet
- CPU task: resizing thousands of images or training a model

```python
import threading
import time


def download_task():
    time.sleep(2)
    print("Downloaded")

threads = [threading.Thread(target=download_task) for _ in range(3)]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

**Interview answer**:
> Use multithreading when the program is waiting on external resources. Use multiprocessing when the program is doing heavy CPU work.

**Simple real-world analogy**:
- Multithreading is like having multiple workers waiting at a desk while the printer is slow.
- Multiprocessing is like having multiple people each doing a heavy calculation in their own room.

---

## 9. GIL and FastAPI

The Global Interpreter Lock (GIL) is a mechanism in CPython that allows only one thread to execute Python bytecode at a time.

### Why it matters
- It limits true parallel CPU execution for Python threads.
- It does not block I/O-bound applications as much.

### In FastAPI
- FastAPI is great for I/O-heavy apps because async code can handle many requests efficiently.
- For CPU-heavy tasks, use multiprocessing or background workers rather than threads.

**Simple example**:
```python
from fastapi import FastAPI
import asyncio

app = FastAPI()

@app.get("/slow")
async def slow_endpoint():
    await asyncio.sleep(2)
    return {"message": "done"}
```

**Interview answer**:
> In FastAPI, the async model is excellent for network and database I/O. For CPU-heavy tasks, the GIL becomes a bottleneck, so multiprocessing is often the better choice.

**Simple explanation**:
- If your app is mostly waiting on the database or network, async and FastAPI are a great fit.
- If your app is doing a lot of math or image processing, Python threads alone will not give you true parallel CPU speed.

---

## 10. Class method vs static method

```python
class Student:
    school = "ABC School"

    def __init__(self, name):
        self.name = name

    @classmethod
    def from_string(cls, data):
        name = data.split("-")[0]
        return cls(name)

    @staticmethod
    def is_valid_name(name):
        return name.isalpha()

s = Student.from_string("Alice-10")
print(s.name)
print(Student.is_valid_name("Alice"))
```

**Difference**:
- `@classmethod` gets access to the class (`cls`)
- `@staticmethod` does not get `self` or `cls`

**Very simple way to remember it**:
- Use `@classmethod` when you want to work with the class itself.
- Use `@staticmethod` when you want a helper that does not need object state.

**Real-world use case**:
- `classmethod` for factory methods
- `staticmethod` for utility logic that does not depend on object state

---

## 11. Try, except, else, finally

```python
def divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Cannot divide by zero")
    else:
        print("Division succeeded")
        return result
    finally:
        print("This always runs")

print(divide(10, 2))
print(divide(10, 0))
```

**Remember**:
- `try` contains risky code
- `except` handles the error
- `else` runs if no exception happened
- `finally` always runs

**Human version**:
> Think of it like this: “Try the risky thing, handle the problem if it happens, and still do the cleanup at the end.”

**Real-world use case**:
- Closing a DB connection even if a query fails

---

## 12. Regex for email validation

```python
import re

pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

emails = ["abc@example.com", "john.doe@company.co.in", "bad-email"]
for email in emails:
    print(bool(re.fullmatch(pattern, email)))
```

**Interview note**:
- Use `fullmatch` when you want the entire string to match.
- Real-world validation is often stricter than this simple regex.

**Simple explanation**:
- Regex is basically a pattern for matching text.
- In interviews, you do not need to be a regex master; you just need to show that you understand the idea and can write a basic pattern.

---

## 13. Lock vs RLock

```python
import threading

lock = threading.Lock()
# lock = threading.RLock()

counter = 0


def increment():
    global counter
    with lock:
        with lock:
            counter += 1
```

**Difference**:
- `Lock` can only be acquired once by one thread at a time.
- `RLock` allows the same thread to acquire it multiple times.

**Simple memory trick**:
- `Lock` is a normal door lock.
- `RLock` is a lock that the same person can use again while still inside.

**Real-world use case**:
- Use `Lock` for simple shared-resource protection.
- Use `RLock` when nested functions both need the same lock.

---

## 14. FastAPI `Depends` and what you should know

`Depends` is used for dependency injection in FastAPI.

```python
from fastapi import FastAPI, Depends

app = FastAPI()

def get_db():
    db = "database-connection"
    try:
        yield db
    finally:
        print("close db")

@app.get("/users")
def get_users(db=Depends(get_db)):
    return {"db": db}
```

### Important FastAPI concepts
- `Depends` for shared logic like auth or DB sessions
- Pydantic models for request/response validation
- `Query`, `Path`, `Body` for parameter handling
- `HTTPException` for custom errors
- `BackgroundTasks` for non-blocking follow-up work
- Middleware and exception handlers
- Async endpoints for I/O-bound work

**Real-world use case**:
- Authentication token verification
- Database session creation per request
- Shared service logic across multiple routes

**How to explain it comfortably in an interview**:
> `Depends` lets me inject reusable logic into my FastAPI routes. For example, I can create a dependency that opens a database session for a request and closes it automatically when the request is done.

---

## 15. Python data processing interview questions

### Difference between `merge`, `join`, and `concat`
```python
import pandas as pd

customers = pd.DataFrame({
    "customer_id": [1, 2, 3],
    "name": ["Alice", "Bob", "Charlie"]
})

orders = pd.DataFrame({
    "customer_id": [1, 2, 4],
    "amount": [100, 200, 300]
})

merged = pd.merge(customers, orders, on="customer_id", how="left")
print(merged)
```

**Common interview questions**:
- What is the difference between `merge` and `concat`?
- How do you handle missing values?
- What does `groupby` do?
- How do you remove duplicates?
- What is the difference between `apply`, `map`, and `vectorized` operations?

**Example answers**:
- `merge` combines on keys.
- `concat` stacks dataframes.
- `groupby` aggregates data by a column.
- `fillna` fills missing values.

**Human way to explain it**:
> In a real data project, I might merge customer and order data to understand which customer placed which order, or group sales data by month to generate a report.

**Real-world use case**:
- Joining customer data with transaction data for analytics.

---

## 16. Basic SQL questions that are often asked

### Second highest salary
```sql
SELECT MAX(salary) AS second_highest_salary
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);
```

### Alternative using window function
```sql
SELECT salary
FROM (
    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
    FROM employees
) t
WHERE rnk = 2;
```

### Find duplicates
```sql
SELECT name, COUNT(*)
FROM users
GROUP BY name
HAVING COUNT(*) > 1;
```

### Find employees earning more than average
```sql
SELECT *
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);
```

### Join example
```sql
SELECT u.name, o.amount
FROM users u
JOIN orders o ON u.id = o.user_id;
```

**Interview tip**:
- Be ready to explain `INNER JOIN`, `LEFT JOIN`, `GROUP BY`, `HAVING`, and `ORDER BY`.

**Simple explanation**:
- `JOIN` connects tables.
- `GROUP BY` summarizes data.
- `ORDER BY` sorts the results.
- `HAVING` filters after grouping.

---

## 17. Extra topics that are frequently asked

### 1. Shallow copy vs deep copy
```python
import copy

original = [[1, 2], [3, 4]]
shallow = copy.copy(original)
deep = copy.deepcopy(original)
```

### 2. Lambda, map, filter
```python
nums = [1, 2, 3, 4]
print(list(map(lambda x: x * 2, nums)))
print(list(filter(lambda x: x % 2 == 0, nums)))
```

### 3. List comprehension
```python
squares = [x * x for x in range(5)]
```

### 4. `*args` and `**kwargs`
```python
def demo(*args, **kwargs):
    print(args)
    print(kwargs)
```

### 5. `enumerate` and `zip`
```python
for i, value in enumerate([10, 20, 30]):
    print(i, value)
```

---

## 18. How to answer in an interview

A strong interview answer usually follows this structure:
1. Explain the concept clearly in one line.
2. Give a small code example.
3. Mention a real-world use case.
4. Mention complexity if relevant.

**A good interview sentence**:
> I would explain it like this: “This concept helps with X, it works like Y in code, and it is useful in real applications because Z.”

**Example**:
> A generator is lazy and does not store all values in memory. It is useful when reading large files or processing streams one item at a time.

---

## 19. Final checklist before the interview

- Know the difference between mutable and immutable objects
- Understand `list`, `tuple`, `set`, `dict`
- Be comfortable with decorators, generators, and comprehensions
- Practice exception handling and regex
- Know basic SQL joins and aggregations
- Understand FastAPI basics such as `Depends`, models, and async endpoints
- Practice one or two pandas problems such as merge, groupby, and missing value handling

---

## 20. Bonus real-world interview examples

- “Why would you choose a tuple over a list in a function return?”
- “Why is a generator better than a list for processing a huge CSV file?”
- “When would you use multiprocessing instead of threading?”
- “How would you prevent race conditions in a multi-threaded app?”
- “How would you design a rate-limited API in FastAPI?”
- “How would you join sales and customer tables in pandas?”

This should give you a solid mix of basic and advanced Python concepts, plus practical interview-style answers.


---

## Source: PYTHON_INTERVIEW_QUESTION_BANK.md

# Python Interview Question Bank

This file contains more common Python interview questions with short, practical answers.

---

## 1. What is the difference between a module and a package?
**Answer**:
- A module is a single Python file.
- A package is a folder containing modules and an `__init__.py` file.

---

## 2. What is `__init__`?
**Answer**:
It is the constructor method of a class. It runs when a new object is created.

```python
class Person:
    def __init__(self, name):
        self.name = name
```

---

## 3. What is `self`?
**Answer**:
`self` points to the current instance of the class so methods can access its attributes.

---

## 4. What is the difference between `append` and `extend`?
**Answer**:
- `append` adds one item to the end of a list.
- `extend` adds multiple items.

```python
lst = [1, 2]
lst.append([3, 4])
print(lst)          # [1, 2, [3, 4]]

lst = [1, 2]
lst.extend([3, 4])
print(lst)          # [1, 2, 3, 4]
```

---

## 5. What is a set?
**Answer**:
A set is an unordered collection of unique items.

```python
s = {1, 2, 2, 3}
print(s)  # {1, 2, 3}
```

---

## 6. What is the difference between `range` and `xrange`?
**Answer**:
In Python 3, `range` is the standard version and returns a range object. In Python 2, `xrange` was more memory efficient.

---

## 7. What is the difference between `list`, `tuple`, `set`, and `dict`?
**Answer**:
- `list`: ordered, mutable
- `tuple`: ordered, immutable
- `set`: unordered, unique values
- `dict`: key-value pairs

---

## 8. What is a lambda function?
**Answer**:
A lambda is a short anonymous function.

```python
square = lambda x: x * x
print(square(5))
```

---

## 9. What is the difference between `map`, `filter`, and `reduce`?
**Answer**:
- `map` transforms items.
- `filter` selects items.
- `reduce` combines items into one value.

---

## 10. What is a comprehension?
**Answer**:
A compact way to create lists, sets, or dictionaries.

```python
squares = [x * x for x in range(5)]
```

---

## 11. What is monkey patching?
**Answer**:
It means changing an attribute or method at runtime.

---

## 12. What is `__name__ == "__main__"`?
**Answer**:
It checks whether a Python file is being run directly or imported as a module.

---

## 13. What is the difference between local and global variables?
**Answer**:
- Local variables are defined inside a function.
- Global variables are defined outside functions and can be used throughout the file.

---

## 14. What is recursion?
**Answer**:
Recursion is when a function calls itself to solve a smaller version of the same problem.

---

## 15. What are `__iter__` and `__next__`?
**Answer**:
These methods make an object iterable and allow it to be consumed by `next()`.

---

## 16. What is `None`?
**Answer**:
`None` represents the absence of a value.

---

## 17. What is the difference between `deepcopy` and `copy`?
**Answer**:
- `copy` creates a shallow copy.
- `deepcopy` creates a fully independent copy.

---

## 18. What is a frozen set?
**Answer**:
A `frozenset` is an immutable version of a set.

---

## 19. What is the difference between `pass`, `continue`, and `break`?
**Answer**:
- `pass` does nothing.
- `continue` skips the current iteration.
- `break` stops the loop completely.

---

## 20. What is method overloading?
**Answer**:
Python does not support traditional method overloading like Java, but you can simulate it using default arguments or `*args`.


---

## Source: TOP_40_QUESTIONS.md

# Top 40 Interview Questions & Answers

## OOP & Design

### 1. What is the difference between classes and objects?
**Answer:** A class is a blueprint or template for creating objects. An object is an instance of a class with actual values. Multiple objects can be created from one class.

### 2. Explain the four pillars of OOP
**Answer:** 
- **Encapsulation**: Bundling data and methods, hiding internal details
- **Abstraction**: Showing only essential features, hiding complexity
- **Inheritance**: Deriving new classes from existing ones (IS-A)
- **Polymorphism**: Same interface, different implementations

### 3. What's the difference between composition and inheritance?
**Answer:** 
- **Inheritance (IS-A)**: Class extends another class, tightly coupled
- **Composition (HAS-A)**: Class contains instances of other classes, loosely coupled
- **Rule**: Prefer composition over inheritance for flexibility

### 4. What are SOLID principles?
**Answer:** 
- **S**: Single Responsibility - one reason to change
- **O**: Open/Closed - open for extension, closed for modification
- **L**: Liskov Substitution - subtypes interchangeable
- **I**: Interface Segregation - specific interfaces
- **D**: Dependency Inversion - depend on abstractions

### 5. What's a design pattern?
**Answer:** Reusable solution to common design problem. Provides template for writing better, maintainable code.

---

## Design Patterns

### 6. When would you use Singleton pattern?
**Answer:** When you need exactly one instance of a class:
- Database connections
- Logger
- Configuration manager
- Thread pools
- **Caution**: Makes testing difficult, hides dependencies

### 7. Difference between Factory and Builder patterns?
**Answer:** 
- **Factory**: One-step object creation, good for simple objects
- **Builder**: Step-by-step construction, good for complex objects with many options

### 8. When to use Strategy pattern?
**Answer:** When you have multiple algorithms for same task and want to:
- Select algorithm at runtime
- Switch algorithms easily
- Avoid if-else chains
**Example**: Payment methods (Credit Card, PayPal, Crypto)

### 9. What is Observer pattern?
**Answer:** One-to-many relationship where observers watch a subject. When subject changes, all observers are notified automatically.
**Example**: Stock price updates, button click handlers

### 10. How does Decorator pattern differ from Inheritance?
**Answer:** 
- **Inheritance**: Fixed at compile-time, creates class hierarchy
- **Decorator**: Runtime composition, adds behavior dynamically without modifying class

---

## Concurrency

### 11. What's a race condition?
**Answer:** When multiple threads access shared resource without synchronization, leading to unpredictable results because of non-deterministic execution order.

### 12. How do you prevent race conditions?
**Answer:** 
- Use **Locks/Mutex**: Ensure only one thread at a time
- **Atomic operations**: Indivisible operations
- **Immutable objects**: Cannot be modified
- **Thread pools**: Controlled threading

### 13. What causes deadlock?
**Answer:** Circular wait for resources:
- Thread A waits for lock held by Thread B
- Thread B waits for lock held by Thread A
- **Prevention**: Always acquire locks in same order

### 14. What's the difference between Lock and RLock?
**Answer:** 
- **Lock**: Single acquisition per thread
- **RLock** (Reentrant): Same thread can acquire multiple times

### 15. When should you use synchronized methods?
**Answer:** When multiple threads access shared mutable state. Keep synchronized blocks small for performance.

---

## System Design

### 16. What do you consider when designing a system?
**Answer:** 
1. **Requirements**: Functional and non-functional
2. **Components**: Identify major pieces
3. **Trade-offs**: Consistency vs Availability, latency vs throughput
4. **Scalability**: Handle growth
5. **Reliability**: Handle failures
6. **Maintainability**: Easy to change

### 17. How would you design an ATM?
**Answer:** 
1. **Components**: Card reader, PIN verification, account manager, cash manager
2. **State Machine**: IDLE → CARD_INSERTED → AUTHENTICATED → TRANSACTION
3. **Security**: PIN encryption, failed attempt limits
4. **Transactions**: Withdraw, deposit, balance check
5. **Patterns**: Singleton, Factory, State

### 18. How would you design a Parking Lot?
**Answer:** 
1. **Entities**: ParkingLot, Level, Spot, Vehicle, Ticket
2. **Spot Types**: Motorcycle, Compact, Regular, Large
3. **Features**: Availability tracking, fee calculation, spot search algorithm
4. **State**: Available, Occupied, Reserved
5. **Patterns**: Singleton, Factory, Strategy

### 19. How would you design a Library Management System?
**Answer:** 
1. **Entities**: Book, BookCopy, Member, Borrowing, reservation
2. **Features**: Search, borrow, return, track due dates, fine calculation
3. **Patterns**: Repository, Observer (notify of due dates), Strategy (fine calculation)

### 20. What are the pillars of a good system design?
**Answer**: **RASCAL**
- **Reliability**: Fault tolerance
- **Availability**: Uptime
- **Scalability**: Handle growth
- **Consistency**: Data correctness
- **Availability**: Access anytime
- **Latency**: Low response time

---

## Advanced Concepts

### 21. What's the difference between abstraction and encapsulation?
**Answer:** 
- **Abstraction**: WHAT - showing only essential features
- **Encapsulation**: HOW - hiding internal details and providing controlled access

### 22. Explain Liskov Substitution Principle
**Answer:** Derived classes should be substitutable for base classes without breaking functionality. If Penguin extends Bird but can't fly, it violates LSP.

### 23. What's idempotency and why is it important?
**Answer:** Operation producing same result regardless of how many times it's called. Important in:
- Payment systems (charge user only once)
- Distributed systems (retry-able operations)
- APIs (safe retries without side effects)

### 24. How do you handle concurrent updates to same resource?
**Answer:** Options:
- **Pessimistic Locking**: Lock before updating
- **Optimistic Locking**: Detect conflicts, retry if needed
- **MVCC**: Multiple versions, timestamp-based

### 25. What's shallow copy vs deep copy?
**Answer:** 
- **Shallow**: Copies object references, nested objects shared
- **Deep**: Copies recursively, complete independence
- **Use Deep Copy**: When you need complete independence (undo/redo, snapshots)

---

## Code & Implementation

### 26. How would you implement thread-safe Singleton?
**Answer:** Using double-checked locking:
```python
class Singleton:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
```

### 27. How would you enforce immutability in Python?
**Answer:** 
- Use `@dataclass(frozen=True)`
- Override `__setattr__` to prevent modifications
- Use Tuple instead of List
- Use `namedtuple`

### 28. How to handle exceptions in distributed systems?
**Answer:** 
- **Timeout**: Fail fast
- **Retry**: Exponential backoff
- **Circuit Breaker**: Fail gracefully
- **Fallback**: Use cached/default value
- **Bulkhead**: Isolate failures

### 29. What's the most important design consideration?
**Answer:** **Separation of Concerns** - each component should have single responsibility, making code modular, testable, and maintainable.

### 30. How do you make code more testable?
**Answer:** 
- Dependency Injection
- Single Responsibility
- Loose Coupling
- Avoid Singletons
- Mock/Stub external dependencies

---

## Real-World Scenarios

### 31. Design an e-commerce checkout system
**Answer:** 
1. **Cart**: Items, quantities, prices
2. **Validation**: Check inventory, validate user
3. **Payment**: Strategy pattern for multiple methods
4. **Order**: Create order record
5. **Notification**: Observer pattern for order updates
6. **Consistency**: Database transactions, idempotency

### 32. How would you design a cache system?
**Answer:** 
- **Eviction Policy**: LRU, LFU, FIFO
- **Size Limit**: Max entries, max memory
- **Concurrency**: Thread-safe access
- **Invalidation**: TTL, manual invalidation
- **Patterns**: Singleton for cache instance

### 33. Design a notification system handling millions of users
**Answer:** 
- **Async Processing**: Queue notifications
- **Batching**: Group notifications
- **Channels**: Email, SMS, Push
- **Retry Logic**: Handle failures
- **Observer Pattern**: Decouple senders from notification handlers

### 34. How to handle rate limiting?
**Answer:** 
- **Token Bucket**: Allow burst traffic
- **Leaky Bucket**: Smooth traffic
- **Sliding Window**: Track recent requests
- **Distributed**: Use Redis for multi-server setup

### 35. Design a recommendation system
**Answer:** 
- **Data Collection**: User behavior tracking
- **Algorithms**: Collaborative filtering, content-based
- **Strategy Pattern**: Switch between algorithms
- **Performance**: Cache popular recommendations
- **A/B Testing**: Compare algorithm effectiveness

---

## Mistakes to Avoid

### 36. What's over-engineering?
**Answer:** Using complex solutions for simple problems. Use patterns only when needed, not for everything.

### 37. What's premature optimization?
**Answer:** Optimizing code before profiling. Focus on correctness first, optimize bottlenecks later.

### 38. What's wrong with tight coupling?
**Answer:** 
- Hard to test (can't mock)
- Hard to extend (must modify existing code)
- Ripple effects (change cascades)
- **Solution**: Depend on abstractions, use DI

### 39. Why avoid long inheritance chains?
**Answer:** 
- Fragile base class problem
- Hard to understand
- Difficult to modify
- **Solution**: Prefer composition

### 40. When is a design pattern unnecessary?
**Answer:** When the problem is too simple. Adding pattern introduces complexity without benefit. **Key**: Simplicity first, patterns when needed.

---

## Interview Tips

1. **Listen carefully** to requirements before jumping to solution
2. **Ask clarifications** about non-functional requirements
3. **Think out loud** so interviewer can follow your reasoning
4. **Draw diagrams** to visualize components and relationships
5. **Discuss trade-offs** - nothing is perfect
6. **Be ready to pivot** if interviewer suggests different approach
7. **Code quality matters** - clean, readable, maintainable code
8. **Test your code** - explain edge cases and error handling


---

