"""
nums array k int, return true if
i !=j and nums[i] == nums [j] and abs(i-j) <=k
"""

"""
set solution

o(1)
"""
def contNearbyDuplicte(nums,k):
    seen = set()

    for i, num in enumerate(nums):
        if num in seen:
            return True
        seen.add(num)
        if len(seen) > k:
            seen.remove(nums[i-k])
    return False

"""
dict
"""
def contNearbyDup(nums,k):
    dic = {}
    for i, v in enumerate(nums):
        if v in dic and i-dic[v] <=k:
            return True
        dic[v] = i
    return False

print(contNearbyDup([1,2,3,1],3))
print(contNearbyDuplicte([1,2,3,4,1],3))