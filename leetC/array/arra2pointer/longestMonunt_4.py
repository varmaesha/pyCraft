"""
mount array
lent > 3
i exist 0<i<len(arr)-1
    a[0] < a[1] ... <a[i-1]<a[i]
    a[i] > a[i+1]...>a[len-1]

retunr len of longest subarray
else 0
o(n) =>n^2

if evenly distributed n^2
"""

def mount(arr):

    ret  = 0

    for i in range(1,len(arr)-1):
        if arr[i-1] < arr[i] > arr[i+1]:
            l = r = i

            while l >= 0 and arr[l] > arr[l-1]:
                l-=1

            while r < len(arr) -1 and arr[r] > arr[r+1]:
                r += 1

            ret = max(ret,r-l+1)
    return ret

print(mount([2,1,4,7,3,2,5]))