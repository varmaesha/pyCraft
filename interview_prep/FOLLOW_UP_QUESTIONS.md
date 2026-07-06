# Follow-Up Interview Questions - Intermediate Level

This version is written to feel more practical and human. Each follow-up question now includes a simple answer you can actually say out loud in an interview.

## Extra Simple Questions You Should Be Able to Answer

### 1. What is a function?
**Answer**: A function is a reusable block of code that performs one job. It helps avoid repetition and makes code easier to test.

### 2. What is the difference between `print()` and `return`?
**Answer**: `print()` shows output to the screen, while `return` sends a value back from a function so it can be used elsewhere.

### 3. What is a list?
**Answer**: A list is an ordered, mutable collection. You can add, remove, or change items after creation.

### 4. What is a tuple?
**Answer**: A tuple is also ordered, but it is immutable. Once created, its contents cannot be changed.

### 5. What is a dictionary?
**Answer**: A dictionary stores data as key-value pairs. It is great when you want fast lookup by a meaningful key like an ID or name.

### 6. What is `self` in a class?
**Answer**: `self` refers to the current instance of the object so the class can access its own attributes and methods.

### 7. What is an exception?
**Answer**: An exception is an error that happens while the program is running. Python lets you catch it and respond gracefully.

### 8. What is the difference between a set and a list?
**Answer**: A list keeps order and allows duplicates. A set stores unique values and does not preserve order.

### 9. Why do we use `with open(...)`?
**Answer**: It ensures the file is properly closed after use, even if an error happens.

### 10. What is the difference between `==` and `is`?
**Answer**: `==` checks whether values are equal. `is` checks whether two variables point to the exact same object in memory.

---

## Python Fundamentals & Advanced Concepts

### 1. Explain *args and **kwargs in Python
**Level**: Intermediate  
**Sample Answer**: 
- `*args` allows function to accept variable number of positional arguments (stored as tuple)
- `**kwargs` allows variable number of keyword arguments (stored as dictionary)
- Use when you don't know number of arguments upfront
```python
def func(*args, **kwargs):
    print(args)      # (1, 2, 3)
    print(kwargs)    # {'name': 'John', 'age': 30}

func(1, 2, 3, name='John', age=30)
```
**Follow-up Q**: What's the difference between `*args` and `*iterable` unpacking?

**Answer**: `*args` collects extra positional arguments into a tuple, while `*iterable` is used to unpack the contents of an existing iterable into separate arguments. In simple words, `*args` is for accepting unknown inputs, while unpacking is for passing existing values into a function or container.

---

### 2. What's the difference between Mutable and Immutable objects?
**Level**: Intermediate  
**Sample Answer**:
- **Mutable**: Can be changed after creation (list, dict, set)
- **Immutable**: Cannot be changed after creation (int, str, tuple)
- Immutable objects are hashable and can be dictionary keys
- Mutable objects are not hashable
```python
# Mutable
lst = [1, 2, 3]
lst[0] = 99  # ✓ Works

# Immutable
tpl = (1, 2, 3)
tpl[0] = 99  # ✗ TypeError
```
**Follow-up Q**: Why would you prefer immutable objects in multi-threaded code?

**Answer**: Immutable objects are safer in concurrent code because they cannot be changed unexpectedly by another thread. That reduces bugs related to shared state and makes your code easier to reason about.

---

### 3. Explain Method Resolution Order (MRO) in Python
**Level**: Intermediate  
**Sample Answer**:
- Determines order in which methods are looked up in hierarchy of classes
- Python uses C3 linearization algorithm
- Use `ClassName.__mro__` or `ClassName.mro()` to check
```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass

print(D.mro())
# [D, B, C, A, object]
```
**Follow-up Q**: What happens with diamond problem in multiple inheritance?

**Answer**: The diamond problem appears when two parent classes inherit from the same base class. Python resolves it using MRO so the method lookup order stays consistent and predictable.

---

### 3.5. Explain Multiple Inheritance and Diamond Problem
**Level**: Intermediate  
**Sample Answer**:
- **Multiple Inheritance**: Class inherits from multiple parent classes
- **Diamond Problem**: Ambiguity when inheriting from classes with common ancestor
```python
class A:
    def show(self):
        print("A")

class B(A):
    def show(self):
        print("B")

class C(A):
    def show(self):
        print("C")

class D(B, C):  # Diamond shape!
    pass

d = D()
d.show()  # Which show() gets called? B or C?
# Answer: B (follows MRO: [D, B, C, A, object])
```
**Solution**: Python uses C3 linearization algorithm to determine correct method call order through MRO
**Follow-up Q**: What would happen if you changed `class D(C, B)` instead of `class D(B, C)`?

**Answer**: The MRO would change, so the method resolution order would be different. In other words, Python would look for the method in `C` before `B`, which can change which implementation gets called.

---

### 3.6. How does super() function work with MRO?
**Level**: Intermediate-Hard  
**Sample Answer**:
- `super()` calls next method in MRO chain without explicitly naming parent class
- Enables proper cooperation with multiple inheritance
```python
class A:
    def __init__(self):
        print("A init")

class B(A):
    def __init__(self):
        super().__init__()
        print("B init")

class C(A):
    def __init__(self):
        super().__init__()
        print("C init")

class D(B, C):
    def __init__(self):
        super().__init__()
        print("D init")

d = D()
# Output:
# A init
# C init
# B init
# D init
```
**Why super() is better than direct parent call**: Works with MRO, handles multiple inheritance correctly  
**Follow-up Q**: Why does `super().__init__()` print in that specific order?

**Answer**: Because `super()` does not call the immediate parent in a rigid way; it follows the MRO chain. That is why the output goes through the chain in a carefully defined order, which is especially important in multiple inheritance.

---

### 4. Difference between Shallow Copy and Deep Copy
**Level**: Intermediate  
**Sample Answer**:
- **Shallow Copy**: Copies object but references to nested objects remain same
- **Deep Copy**: Creates completely independent copy with new nested objects
```python
import copy
original = [[1, 2], [3, 4]]
shallow = copy.copy(original)
deep = copy.deepcopy(original)

shallow[0][0] = 99  # Changes original too!
deep[0][0] = 99     # Doesn't affect original
```
**Follow-up Q**: When would using shallow copy cause bugs?

**Answer**: It causes bugs when the object contains nested objects and you change one of them. Since shallow copy shares nested references, the change may accidentally affect the original object too.

---

### 5. Explain Iterators vs Iterables
**Level**: Intermediate  
**Sample Answer**:
- **Iterable**: Object with `__iter__()` method that returns iterator (list, string, dict)
- **Iterator**: Object with `__iter__()` and `__next__()` methods, maintains state
```python
my_list = [1, 2, 3]  # Iterable
iterator = iter(my_list)  # Get iterator
print(next(iterator))  # 1
print(next(iterator))  # 2
```
**Follow-up Q**: How is `for` loop different from using `iter()` and `next()`?

**Answer**: A `for` loop hides the iterator mechanics and automatically calls `next()` until it reaches the end. Using `iter()` and `next()` gives you more control, but it is more manual.

---

### 6. What are Generators and why use them?
**Level**: Intermediate  
**Sample Answer**:
- Functions using `yield` instead of `return`
- Lazy evaluation - generate values on-demand
- Memory efficient for large datasets
```python
def gen_numbers(n):
    for i in range(n):
        yield i * i

gen = gen_numbers(5)
print(next(gen))  # 0
print(next(gen))  # 1
```
**Benefits**: Memory efficient, pipeable, faster startup  
**Follow-up Q**: What's difference between generator and generator expression?

**Answer**: A generator function uses `yield` and can contain logic, while a generator expression is a short one-line version for simple lazy generation. Both are lazy, but generator expressions are more compact.

---

### 7. Explain Decorators in Python
**Level**: Intermediate  
**Sample Answer**:
- Function/class that wraps another function/class and modifies its behavior
- Uses higher-order functions concept
```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before function call")
        result = func(*args, **kwargs)
        print("After function call")
        return result
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()
```
**Common Use Cases**: logging, caching, authentication, validation  
**Follow-up Q**: How do you create a decorator that accepts arguments?

**Answer**: You create an outer function that takes the decorator parameters, then return a regular decorator inside it. A common pattern is `def decorator_factory(arg): def decorator(func): ... return decorator`.

---

### 8. What are Type Annotations and their benefits?
**Level**: Intermediate  
**Sample Answer**:
- Hints about expected types of variables/parameters (not enforced at runtime)
- Improves code readability and enables IDE assistance
```python
def add(x: int, y: int) -> int:
    return x + y

def process_data(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}
```
**Benefits**: Better IDE support, documentation, catches bugs  
**Follow-up Q**: What's difference between type hints and actual type checking?

**Answer**: Type hints are instructions for humans and tools; they do not enforce types at runtime. Actual type checking is done by tools like `mypy` or IDE analyzers, which can catch type mismatches earlier.

---

### 9. Difference between Stateless and Stateful
**Level**: Intermediate  
**Sample Answer**:
- **Stateless**: Function/service doesn't depend on previous interactions
- **Stateful**: Function/service depends on previous state
```python
# Stateless
def calculate_total(price, tax_rate):
    return price * (1 + tax_rate)

# Stateful
class ShoppingCart:
    def __init__(self):
        self.items = []
    
    def add_item(self, item):
        self.items.append(item)  # Depends on current state
```
**Follow-up Q**: Why are microservices preferred to be stateless?

**Answer**: Stateless services are easier to scale, restart, and deploy because they do not depend on previous requests or local in-memory state. If a service crashes, it can recover without losing important context.

---

### 10. Explain Context Managers in Python
**Level**: Intermediate  
**Sample Answer**:
- Protocol for managing resources (acquire/release)
- Uses `with` statement with `__enter__()` and `__exit__()` methods
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

with FileManager('test.txt', 'r') as f:
    content = f.read()  # Automatically closes
```
**Follow-up Q**: How is context manager better than try-finally?

**Answer**: It makes resource handling cleaner and easier to read. You do not have to repeat cleanup code manually, and it clearly shows the scope of the resource.

---

### 10.5. Explain Method Overriding with MRO
**Level**: Intermediate  
**Sample Answer**:
- Replacing parent class method with child class implementation
- MRO determines which method gets called
```python
class Animal:
    def speak(self):
        return "Generic sound"

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

class Husky(Dog):
    # Doesn't override, inherits from Dog
    pass

h = Husky()
print(h.speak())  # "Woof!" (follows MRO: Husky → Dog → Animal)
```
**Key Point**: Method lookup follows MRO order, first match is used  
**Follow-up Q**: How do you call parent's overridden method?

**Answer**: You can call it using `super()` or by explicitly naming the parent class, such as `ParentClass.method(self)`. `super()` is usually preferred because it respects MRO.

---

### 10.6. What is Abstract Base Class (ABC) and MRO?
**Level**: Intermediate-Hard  
**Sample Answer**:
- ABC enforces that subclasses implement specific methods
- Works with MRO to ensure proper inheritance structure
```python
from abc import ABC, abstractmethod

class DatabaseInterface(ABC):
    @abstractmethod
    def connect(self):
        pass
    
    @abstractmethod
    def query(self, sql):
        pass

class MySQLDB(DatabaseInterface):
    def connect(self):
        print("Connecting to MySQL")
    
    def query(self, sql):
        print(f"Executing: {sql}")

# db = DatabaseInterface()  # ✗ Cannot instantiate abstract class
db = MySQLDB()  # ✓ Works
```
**Why use ABC**: Enforce contract, prevent incomplete implementations  
**Follow-up Q**: What happens if subclass doesn't implement abstract method?

**Answer**: The subclass remains abstract and cannot be instantiated. That is the whole point of an ABC: it forces the subclass to provide the required behavior.

---

### 10.7. Explain C3 Linearization Algorithm
**Level**: Hard  
**Sample Answer**:
- Algorithm Python uses to determine MRO with multiple inheritance
- Ensures parent appears before grandparent, preserves order
```python
# C3 Linearization ensures consistency
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass

# MRO: [D, B, C, A, object]
# NOT [D, B, A, C, A, object] - would have A twice!

# Invalid case - would violate C3
# class E(C, B): pass  # ✗ Error if B also inherits from A
```
**Rules**:
1. Parent appears before grandparent
2. Order of parents preserved
3. No duplicates in MRO
4. Result is consistent with all parent MROs

**Follow-up Q**: Why is C3 better than simple breadth-first or depth-first search?

**Answer**: C3 produces a consistent and deterministic method resolution order. It avoids ambiguity and prevents duplicate parents from appearing in the wrong order, which simple search strategies can fail to do correctly.

---

## HTTP & REST API Concepts

### 11. Difference between PUT and PATCH
**Level**: Intermediate  
**Sample Answer**:
- **PUT**: Replace entire resource (idempotent)
- **PATCH**: Partial update of resource
```
PUT /users/1
{ "name": "John", "age": 30, "email": "john@example.com" }  # Full replacement

PATCH /users/1
{ "age": 31 }  # Only updates age
```
**Follow-up Q**: When should you use PUT vs PATCH?

---

### 12. Explain SOLID Principles with Examples
**Level**: Intermediate  
**Sample Answer**:
- **S - Single Responsibility**: Class should have one reason to change
  ```python
  # ✓ Good
  class UserValidator:
      def validate_email(self, email): pass
  
  # ✗ Bad
  class User:
      def validate_email(self, email): pass
      def send_email(self, to): pass
      def save_to_db(self): pass
  ```
- **O - Open/Closed**: Open for extension, closed for modification
  ```python
  # ✓ Good - extend without modifying
  class PaymentProcessor:
      def process(self, payment_method):
          return payment_method.pay()
  ```
- **L - Liskov Substitution**: Subtypes must be substitutable for base type
- **I - Interface Segregation**: Specific interfaces, not fat/bloated ones
- **D - Dependency Inversion**: Depend on abstractions, not concrete implementations

**Follow-up Q**: Which SOLID principle is most commonly violated?

---

## Coding Problems

### Problem 1: Character Frequency Counter
**Difficulty**: Easy-Medium  
**Problem**: Given a string, return characters and their frequencies in order of appearance
```
Input: "aabbbccde"
Output: {'a': 2, 'b': 3, 'c': 2, 'd': 1, 'e': 1}
```
**Solution**:
```python
def count_frequency(s):
    freq = {}
    for char in s:
        freq[char] = freq.get(char, 0) + 1
    return freq

# Or using Counter
from collections import Counter
def count_frequency(s):
    return dict(Counter(s))
```
**Follow-up Q**: How would you handle Unicode characters? What about case sensitivity?

---

### Problem 2: Remove Duplicates from List (maintain order)
**Difficulty**: Easy-Medium  
**Problem**: Remove duplicates but maintain original order
```
Input: [1, 2, 2, 3, 1, 4]
Output: [1, 2, 3, 4]
```
**Solution**:
```python
def remove_duplicates(lst):
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

# Or using dict (Python 3.7+ maintains insertion order)
def remove_duplicates(lst):
    return list(dict.fromkeys(lst))
```
**Follow-up Q**: What's the time and space complexity? Can you do it without extra space?

---

### Problem 3: Two Sum Problem
**Difficulty**: Medium  
**Problem**: Given array of numbers and a target, find two indices that sum to target
```
Input: [2, 7, 11, 15], target = 9
Output: [0, 1]  (2 + 7 = 9)
```
**Solution**:
```python
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
```
**Follow-up Q**: Can you do it with sorted array without hash map?

---

### Problem 4: Reverse a String (with constraints)
**Difficulty**: Medium  
**Problem**: Reverse only alphanumeric characters, keep special chars in place
```
Input: "a-bC-dEf-ghIj"
Output: "j-Ih-gfE-dCba"
```
**Solution**:
```python
def reverse_alphanumeric(s):
    chars = list(s)
    left, right = 0, len(chars) - 1
    
    while left < right:
        if not chars[left].isalnum():
            left += 1
        elif not chars[right].isalnum():
            right -= 1
        else:
            chars[left], chars[right] = chars[right], chars[left]
            left += 1
            right -= 1
    
    return ''.join(chars)
```
**Follow-up Q**: What's the time complexity? Can you do it in-place?

---

### Problem 5: First Non-Repeating Character
**Difficulty**: Medium  
**Problem**: Find first character that appears only once
```
Input: "leetcode"
Output: 'l'

Input: "loveleetcode"
Output: 'e'
```
**Solution**:
```python
def first_unique_char(s):
    from collections import Counter
    count = Counter(s)
    for char in s:
        if count[char] == 1:
            return char
    return ''
```
**Follow-up Q**: What if you need to find it with single pass?

---

### Problem 6: Flatten Nested List
**Difficulty**: Medium-Hard  
**Problem**: Flatten a nested list with mixed integers and lists
```
Input: [1, [2, [3, 4]], 5]
Output: [1, 2, 3, 4, 5]
```
**Solution (Recursive)**:
```python
def flatten(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result
```
**Solution (Generator)**:
```python
def flatten(lst):
    for item in lst:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item

result = list(flatten([1, [2, [3, 4]], 5]))
```
**Follow-up Q**: How would you handle circular references?

---

### Problem 7: Word Break
**Difficulty**: Medium-Hard  
**Problem**: Check if string can be segmented into dictionary words
```
Input: s = "leetcode", dict = ["leet", "code"]
Output: True

Input: s = "applepenapple", dict = ["apple", "pen"]
Output: True
```
**Solution (DP)**:
```python
def word_break(s, word_dict):
    dp = [False] * (len(s) + 1)
    dp[0] = True
    
    for i in range(1, len(s) + 1):
        for word in word_dict:
            if i >= len(word) and dp[i - len(word)]:
                if s[i - len(word):i] == word:
                    dp[i] = True
                    break
    
    return dp[len(s)]
```
**Follow-up Q**: Can you optimize with Trie? What's time complexity?

---

### Problem 8: LRU Cache
**Difficulty**: Hard  
**Problem**: Implement LRU (Least Recently Used) Cache with O(1) operations
```
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
print(cache.get(1))  # Returns 1
cache.put(3, 3)      # Evicts key 2
print(cache.get(2))  # Returns -1 (not found)
```
**Solution**:
```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity
    
    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
```
**Follow-up Q**: Can you implement without OrderedDict using Doubly Linked List?

---

## System Design & Architecture

### 13. Explain API Versioning Strategies
**Level**: Intermediate  
**Sample Answer**:
- **URL-based**: `/api/v1/users`, `/api/v2/users`
- **Query parameter**: `/api/users?version=1`
- **Header-based**: `Accept: application/vnd.myapi.v1+json`
- **Content negotiation**: Used by REST

**Pros/Cons of each approach**  
**Follow-up Q**: How do you deprecate old API versions?

---

### 14. What is Idempotency in APIs?
**Level**: Intermediate  
**Sample Answer**:
- An operation that produces same result when called multiple times
- Safe to retry without side effects
```
GET /users/1       # Idempotent
POST /users        # NOT idempotent (creates each time)
PUT /users/1       # Idempotent (replaces completely)
DELETE /users/1    # Idempotent
```
**Why it matters**: Distributed systems, network retries  
**Follow-up Q**: How do you implement idempotent POST requests?

---

### 15. Explain Caching Strategies
**Level**: Intermediate  
**Sample Answer**:
- **Cache-Aside**: Check cache, miss → fetch from DB, store in cache
- **Write-Through**: Write to both cache and DB simultaneously
- **Write-Behind**: Write to cache, asynchronously to DB
- **TTL (Time To Live)**: Automatic expiration

**When to use each strategy** and tradeoffs  
**Follow-up Q**: What's cache invalidation problem?

---

### 16. What is Rate Limiting and Throttling?
**Level**: Intermediate  
**Sample Answer**:
- **Rate Limiting**: Restrict number of requests per time unit
- **Throttling**: Controlled slowing of requests

**Algorithms**:
- Token Bucket
- Leaky Bucket
- Sliding Window
- Fixed Window

**Follow-up Q**: How would you implement distributed rate limiting?

---

### 17. Explain Microservices vs Monolithic Architecture
**Level**: Intermediate  
**Sample Answer**:
| Aspect | Monolithic | Microservices |
|--------|-----------|---------------|
| Deployment | Single unit | Independent services |
| Scaling | Entire app | Individual services |
| Tech Stack | Unified | Diverse per service |
| Communication | In-process | Network (HTTP/gRPC) |
| Testing | Simpler | Complex |
| Data Management | Single DB | Distributed DB |

**When to use each**  
**Follow-up Q**: What are challenges of microservices?

---

### 18. REST vs GraphQL
**Level**: Intermediate  
**Sample Answer**:
| Aspect | REST | GraphQL |
|--------|------|---------|
| Query | Fixed endpoints | Flexible queries |
| Over-fetching | Yes | No |
| Under-fetching | Possible | No |
| Versioning | URL-based | Not needed |
| Caching | HTTP cache friendly | Complex |
| Learning Curve | Easy | Steeper |

**Use Cases**: REST for simple APIs, GraphQL for complex queries  
**Follow-up Q**: How do you implement pagination in GraphQL?

---

### 19. Explain HTTP Status Codes
**Level**: Intermediate  
**Sample Answer**:
- **2xx**: Success (200 OK, 201 Created, 204 No Content)
- **3xx**: Redirection (301 Moved, 304 Not Modified)
- **4xx**: Client error (400 Bad Request, 401 Unauthorized, 404 Not Found)
- **5xx**: Server error (500 Internal Server, 503 Service Unavailable)

**Common codes and when to use**  
**Follow-up Q**: When should you use 201 vs 200 for POST?

---

### 20. Explain Webhooks
**Level**: Intermediate  
**Sample Answer**:
- User-defined HTTP callbacks triggered by events
- Push notifications instead of polling
```
Event: Order placed
Webhook: POST https://yourapp.com/webhooks/order
Payload: { orderId: 123, status: "completed" }
```
**Best Practices**:
- Idempotent handler (handle retries)
- Verify webhook signature
- Implement exponential backoff
- Timeout handling

**Follow-up Q**: How do you secure webhook communications?

---

## Tips for Interview Success

### Before the Interview
- ✓ Review SOLID principles and common design patterns
- ✓ Practice coding problems on paper/whiteboard
- ✓ Understand your project implementations deeply
- ✓ Prepare 2-3 questions for the interviewer

### During the Interview
- ✓ Listen carefully, clarify requirements
- ✓ Think out loud, show your reasoning
- ✓ Start with simple solution, then optimize
- ✓ Discuss time/space complexity
- ✓ Ask for feedback

### Common Mistakes to Avoid
- ✗ Jump to code without understanding problem
- ✗ Ignore edge cases
- ✗ Over-engineer simple problems
- ✗ Panic when stuck - explain your approach
- ✗ Forget to test your code

---

## Quick Complexity Reference

| Operation | Time | Space |
|-----------|------|-------|
| Array access | O(1) | - |
| Array search (unsorted) | O(n) | - |
| Array search (sorted) | O(log n) | - |
| Array insert/delete | O(n) | - |
| Hash lookup | O(1) avg | O(n) |
| Hash insert/delete | O(1) avg | O(n) |
| Merge sort | O(n log n) | O(n) |
| Quick sort | O(n log n) avg | O(log n) |
| BFS/DFS | O(V + E) | O(V) |

---

## Resource Links

- [Python Official Docs](https://docs.python.org/)
- [LeetCode](https://leetcode.com/)
- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [Python Design Patterns](https://refactoring.guru/design-patterns)
