"""
postive array positive number target
min len of subarray >= target
o(n)

"""

def minDiff(nums,t):
    l = 0
    total = 0
    res = float('inf')

    for r in range(len(nums)):
        total += nums[r]

        while total >= t:
            res = min(res,r-l+1)

            total -= nums[l]
            l += 1

    if res == float('inf'):
        return 0
    else:
        return res
    
print(minDiff([2,3,1,2,4,3,8],7))




