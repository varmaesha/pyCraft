"""
perm =  order or arranging
cobimation = selection of data order does not matter
"""
"""
gien a atring, return listn of all case tranforamtions

tranform every letter individually yo be lower or upper case to crete string

"""
# itreative
# time and space 2^n
s = "a1b2"
def get_per(s):
    output = ['']
    for c in s:
        temp = []
        if c.isalpha():
            for o in output:
                temp.append(o + c.lower())
                temp.append(o + c.upper())
        else:
            for o in output:
                temp.append(o + c)
        output = temp
    return output

print(get_per(s))


# recursive
# worst case space 2^n

def lettPerm(s):
    res = []
    
    def backTracking(sub='',i=0):
        if len(sub) == len(s):
            res.append(sub)
            return
        if s[i].isalpha():
            backTracking(sub + s[i].swapcase(), i+1)
        backTracking(sub + s[i], i +1)
    backTracking()
    return res
print(lettPerm(s))