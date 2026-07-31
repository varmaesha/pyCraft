import heapq

def kClosest(points: list[list[int]], k: int) -> list[list[int]]:
    max_heap = []
    
    for x, y in points:
        dist = -(x**2 + y**2) # Negative for max-heap behavior
        if len(max_heap) < k:
            heapq.heappush(max_heap, (dist, [x, y]))
        else:
            # Push new element and pop the furthest one
            heapq.heappushpop(max_heap, (dist, [x, y]))
            
    return [point for dist, point in max_heap]



import random

def kClosest(points: list[list[int]], k: int) -> list[list[int]]:
    def get_dist(p):
        return p[0]**2 + p[1]**2

    def quick_select(left: int, right: int, target: int):
        if left >= right:
            return
        
        pivot_idx = random.randint(left, right)
        points[pivot_idx], points[right] = points[right], points[pivot_idx]
        pivot_dist = get_dist(points[right])
        
        fill_idx = left
        for i in range(left, right):
            if get_dist(points[i]) <= pivot_dist:
                points[i], points[fill_idx] = points[fill_idx], points[i]
                fill_idx += 1
                
        points[fill_idx], points[right] = points[right], points[fill_idx]
        
        if fill_idx == target:
            return
        elif fill_idx > target:
            quick_select(left, fill_idx - 1, target)
        else:
            quick_select(fill_idx + 1, right, target)

    quick_select(0, len(points) - 1, k)
    return points[:k]
