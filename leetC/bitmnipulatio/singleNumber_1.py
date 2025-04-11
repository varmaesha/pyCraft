"""
single number

one lelmet appreas twice

liner runtime complezity
 and const extra space
 
"""

"""
brute forece=>n^2
srot nlogn
hashmap n space
bitmanipulation xor => same values give 0 n^0 = n
"""

def bitMan(nums):
    xor = 0
    for i in nums:
        xor^=i
    return xor

print(bitMan([2,3,4,3,2,4,1]))

