""" Contains Duplicate
 Loop through nested for each element
 n^2
 Set => not allow duplicate
 O(n)
"""
"""
Once a set is created, you cannot change its items, but you can remove items and add new items.
returns bool
"""

thisset = {"apple", "banana", "cherry"}
print("thisset",thisset)

def checkIfDuplicatePresent(num):
    if len(set(num)) == len(num):
        return False
    else:
        return True

num=[1,2,3,1]
print(checkIfDuplicatePresent(num))
num=[12,3,4]
print(checkIfDuplicatePresent(num))