"""
array n distinct nu be from [0,n]
return missing number
LENGTH OF LIST TO BE CONSIDERED TO BE NTH ELE
"""
"""
sorting in py is nlogn

difference of sum will be missing number
"""
"""
my_list = ['apple', 'banana', 'cherry', 'date']
for index, item in enumerate(my_list, start=1):
    print(index, item)
"""
def missingNum(num):
    num.sort()

    for i,v in enumerate(num):
        if(i != v):
            return v-1
        # edge case [0,1]
        if v == len(num)-1:
            return v + 1


"""
o(1)
range+1 because starts from o and ends len-1
"""

num = [3,0,1]
print(sum(range(len(num)+1)) - sum(num))

print(missingNum(num))