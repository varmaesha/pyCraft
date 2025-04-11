"""
nxn 2d matrix
1 land 0 water
connect 1s are one iland find how many
"""
"""
use itrative bfs
dfs left subtre first then right subtree
bfs is level order traversal
"""

from collections import deque

def nubIsla(grid):

    if not grid:
        return 0

    def bfs(r,c):

        q = deque()
        visit.add((r,c))
        q.append((r,c))

        while q:

            row, col = q.popleft()
            directions = [(0,1),(0,-1),(1,0),(-1,0)]

            for dr, dc in directions:
                r, c = row+dr, col+dc

                if (r in range(rows) and c in range(cols) and grid[r][c] == 1 and (r,c) not in visit):
                    q.append((r,c))
                    visit.add((r,c))
    count = 0
    rows = len(grid)
    cols = len(grid[0])
    visit = set()

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and (r,c) not in visit:
                bfs(r,c)
                count += 1
    return count

grid = [[1,1,0,0,0],
        [1,1,0,0,0],
        [0,0,1,0,0],
        [0,0,0,1,1]]

print(nubIsla(grid))
