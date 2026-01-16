"""
list onf num 1 to n
return missing number where n is len of list

o(n)
"""

nums = [4,3,2,7,8,2,3,1]
# def mising(nums):
#     ret = []
#     for i in range(1,len(nums)+1):
#         if i not in nums:
#             ret.append(i)

#     return ret
# print(mising(nums))

"""
const space sol
o(1) space
"""
def findMisng(nums):
    for i in range(len(nums)):
        temp = abs(nums[i]) - 1
        if nums[temp] > 0:
            nums[temp] *= -1

    res = []
    for i,n in enumerate(nums):
        if n > 0:
            res.append(i+1)

    return res

print(findMisng(nums))

