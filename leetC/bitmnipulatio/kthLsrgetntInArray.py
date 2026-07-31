import heapq

def findKthLargest(nums: list[int], k: int) -> int:
    # Initialize a min-heap with the first k elements
    heap = nums[:k]
    heapq.heapify(heap)
    
    # Process the remaining elements
    for num in nums[k:]:
        if num > heap[0]:
            heapq.heappushpop(heap, num)
            
    return heap[0]

print(findKthLargest([3,2,1,5,6,4], 2))  # Output: 5

import random

def findKthLargest(nums: list[int], k: int) -> int:
    def quick_select(left: int, right: int, target_idx: int) -> int:
        if left == right:
            return nums[left]
        
        # Pick a random pivot to avoid O(N^2) worst-case
        pivot_idx = random.randint(left, right)
        nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]
        
        # Partition step
        pivot = nums[right]
        fill_idx = left
        for i in range(left, right):
            if nums[i] > pivot:  # Sort in descending fashion
                nums[i], nums[fill_idx] = nums[fill_idx], nums[i]
                fill_idx += 1
        nums[fill_idx], nums[right] = nums[right], nums[fill_idx]
        
        # Binary search-like navigation
        if fill_idx == target_idx:
            return nums[fill_idx]
        elif fill_idx > target_idx:
            return quick_select(left, fill_idx - 1, target_idx)
        else:
            return quick_select(fill_idx + 1, right, target_idx)

    # For descending sort partitioning, kth largest maps directly to index k - 1
    return quick_select(0, len(nums) - 1, k - 1)
