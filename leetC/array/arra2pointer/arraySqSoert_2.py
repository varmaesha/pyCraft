"""
array in non dec order return sq in non-dec order

# sqare and sort
nlogn

# split n merge
has num check for -ve(no need to sort)

find 1st positive number get the index and value
ervers upto the index for rest of the list


"""
from collections import deque


def sortedSquares(nums):

    # edge case
    if not nums:
        return nums
    
    # find first positive index
    m = 0
    for i, n in enumerate(nums):
        if n >=0:
            m = i
            break

    # slipt in 2 arrays
    # A +ve B -ve revers as psotive
    A,B = nums[m:],[n*-1 for n in reversed(nums[:m])]
    def merge(A,B):

        a =b =0
        ret = []

        while a < len(A) and b < len(B):

            if A[a] < B[b]:
                ret.append(A[a])
                a+=1

            else:
                ret.append(B[b])
                b+=1

        if a < len(A):
            ret.extend(A[a:])
        else:
            ret.extend(B[b:])

        print(ret,nums)
        return [n**2 for n in ret]
    print(merge(A,B))
"""
deque
absoulte sqaures
using 2 ptintes to travrs from right to left pointer cmpare and cadd sqared

"""
def sort(nums):
    
    l_p, r_p = 0, len(nums)-1
    ans = deque()
    while l_p <= r_p:
        l_v,r_v = abs(nums[l_p]), abs(nums[r_p])
        if l_v > r_v:
            l_p-=1
            ans.appendleft(l_v*l_v)
        else:
            ans.appendleft(r_v*r_v)
            r_p-=1

    return list(ans)
nums = [-4,-2,0,1,3,10]
# print(sort(nums))
print(sortedSquares(nums))