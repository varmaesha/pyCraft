"""
array handle num of queries
1. calculate sum of ele of nums bet left and right inclusive
numarray
- initialize obj with int array nums
- int sumtrange [left,right]returns sum of ele bethween indices

"""

class NumArrat(object):
    def __int__(self,nums):
        self.nums = nums
    def sumRange(self,left,right):
        return sum(self.nums[left:right+1])

#2
class NumArray(object):
    def __init__(self, nums):
        self.acc_num = [0]
        for num in nums:
            self.acc_num.append(self.acc_num[-1]+num)

    def sumRange(self,left,right):
        return self.acc_num[right+1] - self.acc_num[left]

["NumArray","sumRange","sumRange","sumRange"]
[[-2,0,3,-5,2,-1],[0,2],[2,5],[0,5]]