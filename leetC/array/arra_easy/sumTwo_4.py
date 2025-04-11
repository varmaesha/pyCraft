"""
list of number, rernt numbers whoes sum is target
loop nested => n^2

O(n)
taget - current = sol

hash map
"""

def checkSum(nums,target):
    hash_map = {}
    for i, v in enumerate(nums):
        if target-v in hash_map:
            return i, hash_map[target-v]
        
        else:
            hash_map[v] = i

def check2(nums,target):
    hash_map = {}
    for ind, val in enumerate(nums):
        diff = target - val

        if diff in hash_map:
            return[ind, hash_map[diff]]
        hash_map[val] = ind

nums=[2,9,11,7]
target =9
print(checkSum(nums,target))
print(check2(nums,target))