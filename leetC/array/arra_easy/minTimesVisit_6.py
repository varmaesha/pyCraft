"""
p[i] = x,y
from list of points calculate min dist bet 1st and last pt
can move only one x or y
or move diagonally
O(n)=>time
"""

"""
for one cord to another
min amount of dist =  max of diff bet x and y cords
add to res and update cords
"""

points = [[1,1],[3,4],[-1,0]]

def minTime(points):
    res = 0
    x1,y1 = points.pop()
    while points:
        x2,y2 = points.pop()
        res += max(abs(y2-y1),abs(x2-x1))
        x1,y1 = x2,y2
    return res

print(minTime(points))




