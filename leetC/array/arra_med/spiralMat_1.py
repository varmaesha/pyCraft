"""
mxn matrix
return matrix in spiral order
"""
"""
add all elements of first non-empty row
pop elements

append last element of all lists

reverse append last non-empty list

reverse append first element of all lists

step one again

"""

matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
def spiral(matrix):
    ret = []

    while matrix:

        # add first row
        ret += matrix.pop(0)

        # add last element of all lists
        if matrix and matrix[0]:
            for row in matrix:
                ret.append(row.pop())

        # reverse add last row
        if matrix:
            ret += (matrix.pop()[::-1])
        
        # append first element in reverse order from all lists
        if matrix and matrix[0]:
            for row in matrix[::-1]:
                ret.append(row.pop(0))

    return ret

print(spiral(matrix))