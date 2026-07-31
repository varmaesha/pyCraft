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
