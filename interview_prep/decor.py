# Character frequency
def char_feq(s):    
    return {char: s.count(char) for char in set(s)}

res=char_feq("heeellooo")
print(sorted(res.items(), key=lambda x: (-x[1], x[0])))