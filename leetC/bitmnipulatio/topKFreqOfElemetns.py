from collections import Counter

def topKFrequent(nums: list[int], k: int) -> list[int]:
    count = Counter(nums)
    # Buckets array where index is the frequency
    buckets = [[] for _ in range(len(nums) + 1)]
    
    for num, freq in count.items():
        buckets[freq].append(num)
        
    result = []
    # Gather items from highest frequency bucket down to lowest
    for i in range(len(buckets) - 1, 0, -1):
        for num in buckets[i]:
            result.append(num)
            if len(result) == k:
                return result


import heapq
from collections import Counter

def topKFrequent(nums: list[int], k: int) -> list[int]:
    # Step 1: Count element frequencies
    count = Counter(nums)
    
    # Step 2: Use min-heap to keep track of top k elements
    # heapq.nlargest can also be used, but this shows manual heap logic
    heap = []
    for num, freq in count.items():
        heapq.heappush(heap, (freq, num))
        if len(heap) > k:
            heapq.heappop(heap)
            
    return [num for freq, num in heap]


import random
from collections import Counter

def topKFrequent(nums: list[int], k: int) -> list[int]:
    count = Counter(nums)
    unique_elements = list(count.keys())
    
    def quick_select(left, right, target):
        if left >= right:
            return
        
        pivot_idx = random.randint(left, right)
        pivot = unique_elements[pivot_idx]
        unique_elements[pivot_idx], unique_elements[right] = unique_elements[right], unique_elements[pivot_idx]
        
        fill_idx = left
        for i in range(left, right):
            if count[unique_elements[i]] >= count[pivot]:
                unique_elements[i], unique_elements[fill_idx] = unique_elements[fill_idx], unique_elements[i]
                fill_idx += 1
                
        unique_elements[fill_idx], unique_elements[right] = unique_elements[right], unique_elements[fill_idx]
        
        if fill_idx == target:
            return
        elif fill_idx > target:
            quick_select(left, fill_idx - 1, target)
        else:
            quick_select(fill_idx + 1, right, target)
            
    # QuickSelect to find the kth elements partition index
    quick_select(0, len(unique_elements) - 1, k - 1)
    return unique_elements[:k]
