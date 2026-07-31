from copy import deepcopy
a = [1,2,3,{'a':1}]
b=a.copy()
c=deepcopy(a)
c[3]['a']=2
d=a
print(a)
print(b)
print(c)
print(d)