"""
return tirplest index should nt=ot be same. duplicate numberrs can be used only if in the lsit

sum equalt to target = 0
"""
"""
3 nested for => n^3, prblem duloacate

sorting fixes this

if loop starts with -ve only then start because if not then no pount

"""

"""
inde nect and last
check sum if not 0 move left < 0 if greater then 0 move right

greedy
"""

def sume3(nums):
    triplet = []

    nums.sort()

    for ind,val in enumerate(nums):

        #  skip for values if next num is same as prev
        if (ind > 0) & (val == nums[ind-1]):
            continue

        left = ind+1
        right = len(nums)-1

        while left < right:
            currentSum = nums[ind] + nums[left] + nums[right]

            # if its more positive make it less positive
            if currentSum > 0:
                right -= 1

            # if its more negative move towards 0 
            elif currentSum < 0:
                left += 1

            else:
                triplet.append([val,nums[left],nums[right]]
                )
                left+=1

                while (left < right) & (nums[left]== nums[left-1]):
                    left += 1

    return triplet

print(sume3([-1,-4,0,-1,1,2]))