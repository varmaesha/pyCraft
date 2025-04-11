"""
list , count of each element smaller that current
sort instead of nested loops
spcae is cheap
nlogn
"""
nums = [8,1,2,2,3]

def lessMe(nums):
    nums.sort()
    d ={}
    for i, num in enumerate(nums):
        if num not in d:
            d[num] = i
    ret = []
    for i in nums:
        ret.append(d[i])
    return ret

print(lessMe(nums))