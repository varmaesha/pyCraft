def kClosest(points: list[list[int]], k: int) -> list[list[int]]:
    # Sort points by their squared distance: x^2 + y^2
    points.sort(key=lambda p: p[0]**2 + p[1]**2)
    return points[:k]

print(kClosest( points = [[1,3],[-2,2]], k = 1))  # Output: [[-2, 2], [1, 3]]