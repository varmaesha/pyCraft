"""LRU Cache: base vs optimized solutions.

Daily analogy: remembering the most recently used open documents or web pages while removing the least recently used ones when space is limited.
"""

from collections import OrderedDict


class LRUCacheNaive:
    """Naive implementation using a list and a dictionary.

    Time:
      get: O(n)
      put: O(n)
    Space: O(capacity)
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.order = []

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.order.remove(key)
        self.order.append(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            lru = self.order.pop(0)
            del self.cache[lru]
        self.cache[key] = value
        self.order.append(key)


class LRUCacheOptimized:
    """Optimized implementation using OrderedDict.

    Time:
      get: O(1)
      put: O(1)
    Space: O(capacity)
    Technique: hash map + ordered linked data structure
    Design pattern: cache eviction policy, system design for fast retrieval
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


if __name__ == "__main__":
    print("LRU Cache Naive vs Optimized")
    naive = LRUCacheNaive(2)
    naive.put(1, 1)
    naive.put(2, 2)
    print("Naive get(1):", naive.get(1))
    naive.put(3, 3)
    print("Naive get(2) after eviction:", naive.get(2))

    optimized = LRUCacheOptimized(2)
    optimized.put(1, 1)
    optimized.put(2, 2)
    print("Optimized get(1):", optimized.get(1))
    optimized.put(3, 3)
    print("Optimized get(2) after eviction:", optimized.get(2))

PLAIN_COMPLEXITY_NOTE = """
Plain-language explanation of O(n * m log m):
- For n items each of length ~m, O(n * m log m) means you sort each item (≈ m log m) and do that for all n items → n * (m log m).
- Sorting costs m log m because sorting m elements takes about m log m comparisons/operations.
- Space O(n * m): storing a sorted key (length ~m) per item yields ~n * m storage.
- Example: n=1000, m=10 ⇒ cost ≈ 1000 * 10 * log2(10) ≈ 33,000 units; space ≈ 10,000 characters for keys.
- Use sort-key when m is small or implementation simplicity matters; use a frequency/count-key for ASCII lowercase to get O(n * m) time.
"""
