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
