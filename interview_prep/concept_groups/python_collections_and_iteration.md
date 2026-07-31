# Python Collections And Iteration

This file combines content from the following source files in `interview_prep/segragate/`:
- PYTHON_LOOPS_MAP_LAMBDA_SORTING.md
- ADVANCED_PYTHON_INTERVIEW_GUIDE.md
- PYTHON_INTERVIEW_QUESTION_BANK.md
- FOLLOW_UP_QUESTIONS.md

---

## Source: PYTHON_LOOPS_MAP_LAMBDA_SORTING.md

# Python Basics to Advanced: Loops, Map, Lambda, Sorting

## Core Python Basics Interview Questions

### 1. What are the different loop constructs in Python?
**Level**: Beginner-Intermediate

**Answer:**
- **for loop**: Iterate over sequence (list, string, dict, etc.)
- **while loop**: Repeat until condition is False
- **for-else & while-else**: Executes else block if loop completes without break
- **break & continue**: Control loop flow

```python
# for loop
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

# for-else (else executes if no break)
for i in range(5):
    if i == 10:
        break
else:
    print("Loop completed normally")  # This prints

# while loop
count = 0
while count < 3:
    print(count)
    count += 1

# Nested loops
for i in range(3):
    for j in range(2):
        print(f"i={i}, j={j}")

# Loop with enumerate (get index and value)
fruits = ['apple', 'banana', 'cherry']
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")
```

**Follow-up Q**: What's the difference between for-else and break statement?

---

### 2. What are List Comprehensions vs Generator Expressions?
**Level**: Intermediate

**Answer:**
- **List Comprehension**: Creates entire list in memory at once
- **Generator Expression**: Creates items lazily, one at a time

```python
# List Comprehension - creates entire list
squares = [x**2 for x in range(5)]
# Result: [0, 1, 4, 9, 16]

# With condition
evens = [x for x in range(10) if x % 2 == 0]
# Result: [0, 2, 4, 6, 8]

# Nested list comprehension
matrix = [[i*j for j in range(3)] for i in range(3)]
# Result: [[0, 0, 0], [0, 1, 2], [0, 2, 4]]

# Generator Expression - lazy evaluation
squares_gen = (x**2 for x in range(5))
print(next(squares_gen))  # 0 (only generates when asked)

# Memory comparison
import sys
list_comp = [x**2 for x in range(1000)]
gen_expr = (x**2 for x in range(1000))
print(sys.getsizeof(list_comp))  # Large
print(sys.getsizeof(gen_expr))   # Small (just generator object)

# Dictionary comprehension
square_dict = {x: x**2 for x in range(5)}
# Result: {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# Set comprehension
unique_squares = {x**2 for x in [1, 2, 2, 3, 3, 4]}
# Result: {1, 4, 9, 16}
```

**Follow-up Q**: When should you use list comprehension vs generator expression?

---

### 3. Explain Map, Filter, and Reduce Functions
**Level**: Intermediate

**Answer:**
- **map()**: Apply function to each item, return new list
- **filter()**: Keep items where function returns True
- **reduce()**: Accumulate single value from sequence

```python
# MAP - apply function to each element
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, numbers))
# Result: [1, 4, 9, 16, 25]

# vs list comprehension (preferred)
squared = [x**2 for x in numbers]

# Map with multiple iterables
a = [1, 2, 3]
b = [4, 5, 6]
sums = list(map(lambda x, y: x + y, a, b))
# Result: [5, 7, 9]

# FILTER - keep items where condition is True
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = list(filter(lambda x: x % 2 == 0, numbers))
# Result: [2, 4, 6, 8, 10]

# vs list comprehension (preferred)
evens = [x for x in numbers if x % 2 == 0]

# REDUCE - accumulate single value
from functools import reduce
numbers = [1, 2, 3, 4, 5]
product = reduce(lambda x, y: x * y, numbers)
# Result: 120 (1*2*3*4*5)

# With initial value
total = reduce(lambda x, y: x + y, numbers, 100)
# Result: 115 (100 + 1 + 2 + 3 + 4 + 5)

# Chaining map and filter
numbers = [1, 2, 3, 4, 5, 6]
result = list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, numbers)))
# Result: [4, 16, 36] (squares of evens)

# vs comprehension (more readable)
result = [x**2 for x in numbers if x % 2 == 0]
```

**Key Points:**
- map/filter return iterators (not lists) in Python 3
- List comprehensions are more readable and Pythonic
- Use reduce for accumulation operations

**Follow-up Q**: Why are list comprehensions preferred over map/filter?

---

### 4. What are Lambda Functions and When to Use Them?
**Level**: Intermediate

**Answer:**
- Anonymous function defined with `lambda` keyword
- Useful for short, simple functions
- Often used with map, filter, sorted

```python
# Basic lambda
square = lambda x: x**2
print(square(5))  # 25

# Lambda in map/filter (as seen above)
numbers = [1, 2, 3, 4, 5]
evens = list(filter(lambda x: x % 2 == 0, numbers))

# Lambda with multiple parameters
add = lambda x, y: x + y
print(add(3, 5))  # 8

# Lambda in sorted (key parameter)
students = [
    {'name': 'Alice', 'age': 25},
    {'name': 'Bob', 'age': 23},
    {'name': 'Charlie', 'age': 24}
]
sorted_students = sorted(students, key=lambda s: s['age'])
# Result: [{'name': 'Bob', 'age': 23}, {'name': 'Charlie', 'age': 24}, {'name': 'Alice', 'age': 25}]

# Lambda with conditional (ternary operator)
max_of_two = lambda x, y: x if x > y else y
print(max_of_two(10, 20))  # 20

# Lambda with default arguments
power = lambda x, n=2: x ** n
print(power(3))    # 9
print(power(3, 3)) # 27

# When NOT to use lambda
# Bad: Too complex
# bad_lambda = lambda x: x if x % 2 == 0 and x > 10 and x < 100 else None

# Better: Use regular function
def check_even_in_range(x):
    if x % 2 == 0 and 10 < x < 100:
        return x
    return None
```

**When to Use:**
- Simple one-line operations
- Passing to higher-order functions (map, filter, sorted)
- Quick sorting keys

**When NOT to Use:**
- Complex logic (use def instead)
- When you need documentation/comments
- Multi-line functions

**Follow-up Q**: What's the difference between lambda and regular functions?

---

### 5. Sorting: Different Approaches and When to Use Them
**Level**: Intermediate

**Answer:**
- **sorted()**: Returns new sorted list
- **list.sort()**: Sorts list in-place, modifies original
- **key parameter**: Custom sort criterion
- **reverse parameter**: Sort in descending order

```python
# Basic sorting
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
sorted_asc = sorted(numbers)
# Result: [1, 1, 2, 3, 4, 5, 6, 9]

sorted_desc = sorted(numbers, reverse=True)
# Result: [9, 6, 5, 4, 3, 2, 1, 1]

# Sorting strings
words = ['python', 'java', 'cpp', 'c']
sorted_words = sorted(words)
# Result: ['c', 'cpp', 'java', 'python']

# Case-insensitive string sorting
words = ['Python', 'JAVA', 'cpp', 'C']
sorted_insensitive = sorted(words, key=str.lower)
# Result: ['C', 'cpp', 'JAVA', 'Python']

# Sorting objects (dictionaries)
students = [
    {'name': 'Alice', 'score': 85},
    {'name': 'Bob', 'score': 92},
    {'name': 'Charlie', 'score': 78}
]

# Sort by score
by_score = sorted(students, key=lambda s: s['score'])
# Sort by score descending
by_score_desc = sorted(students, key=lambda s: s['score'], reverse=True)

# Sort by name length
by_name_len = sorted(students, key=lambda s: len(s['name']))

# Multi-key sorting (sort by score desc, then name asc)
# Use tuple - first element is primary, second is secondary
multi_sorted = sorted(students, key=lambda s: (-s['score'], s['name']))

# Sorting with custom comparison
# Old way (Python 2) - using cmp parameter
# New way (Python 3) - using key parameter only

# In-place sorting (modifies original list)
numbers = [3, 1, 4, 1, 5, 9]
numbers.sort()  # numbers is now [1, 1, 3, 4, 5, 9]

# Stable sorting - preserves order of equal elements
data = [(1, 'a'), (2, 'b'), (1, 'c'), (2, 'd')]
by_first = sorted(data, key=lambda x: x[0])
# Result: [(1, 'a'), (1, 'c'), (2, 'b'), (2, 'd')]
# Notice (1, 'a') comes before (1, 'c') because of original order

# Sorting with operator module (efficient)
from operator import itemgetter, attrgetter
students_tuple = [
    ('Alice', 85),
    ('Bob', 92),
    ('Charlie', 78)
]
by_score = sorted(students_tuple, key=itemgetter(1))

class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

students_obj = [Student('Alice', 85), Student('Bob', 92)]
by_name = sorted(students_obj, key=attrgetter('name'))
```

**Time Complexity:**
- `sorted()`: O(n log n) - uses Timsort algorithm
- `list.sort()`: O(n log n) - same as sorted, but in-place

**Follow-up Q**: When should you use sorted() vs list.sort()?

---

### 6. What are Advanced Loop Techniques?
**Level**: Intermediate-Advanced

**Answer:**

```python
# ZIP - combine multiple iterables
names = ['Alice', 'Bob', 'Charlie']
scores = [85, 92, 78]
ages = [20, 21, 19]

for name, score in zip(names, scores):
    print(f"{name}: {score}")

# Zip with unequal lengths (stops at shortest)
result = list(zip(names, scores))
# Result: [('Alice', 85), ('Bob', 92), ('Charlie', 78)]

# Multiple unpack
for name, score, age in zip(names, scores, ages):
    print(f"{name}: {score}, age {age}")

# Zip with fill value for unequal lengths
from itertools import zip_longest
a = [1, 2, 3]
b = ['a', 'b']
result = list(zip_longest(a, b, fillvalue='N/A'))
# Result: [(1, 'a'), (2, 'b'), (3, 'N/A')]

# ENUMERATE - get index and value
fruits = ['apple', 'banana', 'cherry']
for index, fruit in enumerate(fruits, start=1):
    print(f"{index}. {fruit}")
# Output: 1. apple, 2. banana, 3. cherry

# RANGE - create sequence of numbers
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

for i in range(2, 8, 2):
    print(i)  # 2, 4, 6

# REVERSED - reverse iteration
numbers = [1, 2, 3, 4, 5]
for num in reversed(numbers):
    print(num)  # 5, 4, 3, 2, 1

# ITERTOOLS - advanced iteration
from itertools import combinations, permutations, product
items = ['a', 'b', 'c']

# Combinations (order doesn't matter)
combs = list(combinations(items, 2))
# Result: [('a', 'b'), ('a', 'c'), ('b', 'c')]

# Permutations (order matters)
perms = list(permutations(items, 2))
# Result: [('a', 'b'), ('a', 'c'), ('b', 'a'), ('b', 'c'), ('c', 'a'), ('c', 'b')]

# Cartesian product
result = list(product([1, 2], ['a', 'b']))
# Result: [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]

# CHAIN - flatten multiple iterables
from itertools import chain
list1 = [1, 2, 3]
list2 = [4, 5, 6]
result = list(chain(list1, list2))
# Result: [1, 2, 3, 4, 5, 6]
```

**Follow-up Q**: When should you use zip vs zip_longest?

---

## Practical Programs Combining Loops, Map, Lambda, Sorting

### Program 1: Student Grade Management System
**Difficulty**: Easy-Intermediate

```python
students = [
    {'name': 'Alice', 'grade': 85, 'subject': 'Math'},
    {'name': 'Bob', 'grade': 92, 'subject': 'Math'},
    {'name': 'Charlie', 'grade': 78, 'subject': 'Math'},
    {'name': 'Alice', 'grade': 90, 'subject': 'Science'},
    {'name': 'Bob', 'grade': 88, 'subject': 'Science'},
]

# 1. Sort by grade descending
top_performers = sorted(students, key=lambda s: s['grade'], reverse=True)
print("Top performers:", top_performers[:3])

# 2. Get students above 80
above_80 = list(filter(lambda s: s['grade'] >= 80, students))
print("Above 80:", above_80)

# 3. Map to get only names and grades
results = list(map(lambda s: f"{s['name']}: {s['grade']}", students))
print("Results:", results)

# 4. Group by subject (using dict)
subjects = {}
for student in students:
    subject = student['subject']
    if subject not in subjects:
        subjects[subject] = []
    subjects[subject].append(student)

# 5. Average grade per student using reduce
from functools import reduce
unique_names = set(s['name'] for s in students)
averages = {
    name: sum(s['grade'] for s in students if s['name'] == name) / 
          len([s for s in students if s['name'] == name])
    for name in unique_names
}
print("Averages:", averages)

# 6. Calculate overall statistics
total_grades = reduce(lambda acc, s: acc + s['grade'], students, 0)
avg_grade = total_grades / len(students)
print(f"Class average: {avg_grade:.2f}")
```

---

### Program 2: E-commerce Product Filtering and Sorting
**Difficulty**: Intermediate

```python
products = [
    {'id': 1, 'name': 'Laptop', 'price': 1200, 'rating': 4.5, 'stock': 5},
    {'id': 2, 'name': 'Mouse', 'price': 25, 'rating': 4.8, 'stock': 50},
    {'id': 3, 'name': 'Keyboard', 'price': 75, 'rating': 4.2, 'stock': 30},
    {'id': 4, 'name': 'Monitor', 'price': 300, 'rating': 4.6, 'stock': 0},
    {'id': 5, 'name': 'Headphones', 'price': 100, 'rating': 4.4, 'stock': 15},
]

# 1. Filter products in stock and under $500
affordable = list(filter(
    lambda p: p['price'] < 500 and p['stock'] > 0, 
    products
))

# 2. Sort by rating descending, then price ascending
best_rated = sorted(
    affordable,
    key=lambda p: (-p['rating'], p['price'])
)

# 3. Apply discount to high-rated items (rating > 4.5)
def apply_discount(product):
    discount = 0.1 if product['rating'] > 4.5 else 0
    return {
        **product,
        'original_price': product['price'],
        'discounted_price': product['price'] * (1 - discount),
        'discount': f"{discount*100}%"
    }

discounted = list(map(apply_discount, best_rated))

# 4. Calculate total inventory value
from functools import reduce
total_value = reduce(
    lambda acc, p: acc + (p['price'] * p['stock']),
    products,
    0
)
print(f"Total inventory value: ${total_value}")

# 5. Get products sorted by value in stock
by_value = sorted(
    [p for p in products if p['stock'] > 0],
    key=lambda p: p['price'] * p['stock'],
    reverse=True
)
```

---

### Program 3: Data Processing Pipeline
**Difficulty**: Intermediate

```python
# Raw data
raw_data = [
    "  alice  , 25, 85000  ",
    "bob, 30, 95000",
    "CHARLIE, 28, 75000",
    "diana , 26,  88000 ",
]

# Process employees through pipeline
from functools import reduce

# Step 1: Clean and parse data
def parse_employee(line):
    name, age, salary = line.split(',')
    return {
        'name': name.strip().lower(),
        'age': int(age.strip()),
        'salary': int(salary.strip())
    }

employees = list(map(parse_employee, raw_data))

# Step 2: Filter valid employees (age > 25, salary > 70000)
valid = list(filter(
    lambda e: e['age'] > 25 and e['salary'] > 70000,
    employees
))

# Step 3: Sort by salary descending
by_salary = sorted(valid, key=lambda e: e['salary'], reverse=True)

# Step 4: Add title based on salary
def add_title(employee):
    if employee['salary'] > 90000:
        title = 'Senior'
    elif employee['salary'] > 80000:
        title = 'Mid-level'
    else:
        title = 'Junior'
    return {**employee, 'title': title}

titled = list(map(add_title, by_salary))

# Step 5: Calculate statistics using reduce
stats = {
    'total_employees': len(titled),
    'avg_salary': reduce(
        lambda acc, e: acc + e['salary'], 
        titled, 
        0
    ) / len(titled),
    'total_payroll': reduce(
        lambda acc, e: acc + e['salary'],
        titled,
        0
    )
}

print("Employees:", titled)
print("Statistics:", stats)
```

---

### Program 4: String Transformation Pipeline
**Difficulty**: Intermediate

```python
# Transform text through multiple operations
text = "hello world from python programming"

# 1. Split, uppercase, and filter words longer than 4 chars
words = text.split()
long_words = list(filter(lambda w: len(w) > 4, words))
uppercase = list(map(str.upper, long_words))
print("Uppercase long words:", uppercase)

# 2. Create word statistics
word_stats = list(map(
    lambda w: {'word': w, 'length': len(w), 'vowels': sum(1 for c in w if c in 'aeiou')},
    words
))
print("Word stats:", word_stats)

# 3. Sort by vowel count descending
by_vowels = sorted(word_stats, key=lambda w: w['vowels'], reverse=True)
print("Sorted by vowels:", by_vowels)

# 4. Filter and transform
processed = list(map(
    lambda w: f"{w['word']} ({w['length']} chars)",
    filter(lambda w: w['vowels'] > 1, word_stats)
))
print("Processed:", processed)

# 5. Join back
result = " | ".join(processed)
print("Final:", result)
```

---

### Program 5: Complex Nested Data Processing
**Difficulty**: Hard

```python
# Processing nested student grades data
school_data = {
    'class_A': [
        {'name': 'Alice', 'scores': [85, 90, 88]},
        {'name': 'Bob', 'scores': [78, 82, 80]},
    ],
    'class_B': [
        {'name': 'Charlie', 'scores': [92, 95, 90]},
        {'name': 'Diana', 'scores': [88, 87, 89]},
    ]
}

# Flatten and process
from functools import reduce

# 1. Flatten nested structure
all_students = reduce(
    lambda acc, students: acc + students,
    school_data.values(),
    []
)

# 2. Add average score
def add_average(student):
    avg = sum(student['scores']) / len(student['scores'])
    return {**student, 'average': round(avg, 2)}

with_averages = list(map(add_average, all_students))

# 3. Sort by average descending
top_students = sorted(with_averages, key=lambda s: s['average'], reverse=True)

# 4. Grade assignment (A: >90, B: >80, C: >=70)
def assign_grade(student):
    grade = 'A' if student['average'] > 90 else 'B' if student['average'] > 80 else 'C'
    return {**student, 'grade': grade}

graded = list(map(assign_grade, top_students))

# 5. Group by grade
grades_dict = {}
for student in graded:
    grade = student['grade']
    if grade not in grades_dict:
        grades_dict[grade] = []
    grades_dict[grade].append(student['name'])

print("Students by grade:")
for grade in sorted(grades_dict.keys(), reverse=True):
    print(f"Grade {grade}: {', '.join(grades_dict[grade])}")

# 6. Calculate statistics per class
class_stats = {
    cls: {
        'avg_score': round(sum(s['average'] for s in students) / len(students), 2),
        'top_student': max(students, key=lambda s: s['average'])['name'],
        'count': len(students)
    }
    for cls, students in school_data.items()
}
print("\nClass Statistics:", class_stats)
```

---

### Program 6: Data Aggregation and Reporting
**Difficulty**: Hard

```python
# Sales data processing
sales_data = [
    {'date': '2024-01-01', 'product': 'Laptop', 'quantity': 2, 'price': 1200},
    {'date': '2024-01-01', 'product': 'Mouse', 'quantity': 5, 'price': 25},
    {'date': '2024-01-02', 'product': 'Keyboard', 'quantity': 3, 'price': 75},
    {'date': '2024-01-02', 'product': 'Laptop', 'quantity': 1, 'price': 1200},
    {'date': '2024-01-03', 'product': 'Monitor', 'quantity': 2, 'price': 300},
]

from functools import reduce

# 1. Add total amount to each transaction
def add_total(transaction):
    return {
        **transaction,
        'total': transaction['quantity'] * transaction['price']
    }

with_totals = list(map(add_total, sales_data))

# 2. Find top 3 transactions by value
top_3 = sorted(with_totals, key=lambda t: t['total'], reverse=True)[:3]
print("Top 3 transactions:", top_3)

# 3. Group by date
by_date = {}
for transaction in with_totals:
    date = transaction['date']
    if date not in by_date:
        by_date[date] = []
    by_date[date].append(transaction)

# 4. Daily sales summary
daily_summary = {
    date: {
        'total_sales': sum(t['total'] for t in transactions),
        'total_quantity': sum(t['quantity'] for t in transactions),
        'avg_transaction': round(sum(t['total'] for t in transactions) / len(transactions), 2)
    }
    for date, transactions in by_date.items()
}

# 5. Product analysis
by_product = {}
for transaction in with_totals:
    product = transaction['product']
    if product not in by_product:
        by_product[product] = []
    by_product[product].append(transaction)

product_summary = {
    product: {
        'total_sold': sum(t['quantity'] for t in transactions),
        'total_revenue': sum(t['total'] for t in transactions),
        'transactions': len(transactions)
    }
    for product, transactions in by_product.items()
}

# Sort products by revenue
sorted_products = sorted(
    product_summary.items(),
    key=lambda x: x[1]['total_revenue'],
    reverse=True
)

print("\nDaily Summary:", daily_summary)
print("\nProduct Summary (sorted by revenue):")
for product, stats in sorted_products:
    print(f"  {product}: ${stats['total_revenue']} ({stats['total_sold']} units)")
```

---

## Interview Tips for These Topics

### What Interviewers Look For:
1. **Understand when to use each approach**
   - List comprehension vs map/filter
   - for loop vs while loop
   
2. **Write clean, readable code**
   - Prefer comprehensions over complex map/filter chains
   - Use meaningful variable names
   
3. **Optimize for readability first**
   - Lambda should be simple one-liners
   - Complex logic → regular function
   
4. **Know the performance implications**
   - Generator expressions save memory
   - sorted() is O(n log n)
   - Dictionary operations are O(1) average

### Common Mistakes to Avoid:
- ❌ Using lambda for complex operations
- ❌ Chaining too many map/filter calls
- ❌ Forgetting list() to materialize iterators
- ❌ Not considering time complexity of nested loops

### Practice Tips:
1. Write solutions with loops first, then with comprehensions
2. Convert nested loops to nested comprehensions
3. Practice combining map/filter/reduce
4. Time your solutions on large datasets

---

## Quick Reference

| Concept | Use Case | Example |
|---------|----------|---------|
| **for loop** | Iterate over sequence | `for item in items:` |
| **while loop** | Repeat until condition false | `while count < 10:` |
| **List comprehension** | Create filtered/transformed list | `[x*2 for x in range(5)]` |
| **Generator expression** | Memory-efficient iteration | `(x*2 for x in range(5))` |
| **map()** | Apply function to all items | `map(lambda x: x*2, nums)` |
| **filter()** | Keep items where condition true | `filter(lambda x: x > 5, nums)` |
| **reduce()** | Accumulate to single value | `reduce(lambda a,b: a+b, nums)` |
| **lambda** | Short anonymous function | `lambda x: x > 5` |
| **sorted()** | Return new sorted list | `sorted(items, key=...)` |
| **zip()** | Combine iterables | `zip(names, ages)` |
| **enumerate()** | Index and value | `enumerate(items)` |


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

## Source: FOLLOW_UP_QUESTIONS.md

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


---

