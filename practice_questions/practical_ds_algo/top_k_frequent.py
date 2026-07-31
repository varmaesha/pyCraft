"""Top K Frequent Elements: base vs optimized solutions.

Daily analogy: finding the top k most-used apps or most-ordered menu items.
"""
from collections import Counter
from heapq import nlargest
from typing import List


def top_k_frequent_sort(nums: List[int], k: int) -> List[int]:
    """Base solution: count then sort frequencies."""
    freq = Counter(nums)
    return [num for num, _ in sorted(freq.items(), key=lambda item: item[1], reverse=True)[:k]]


def top_k_frequent_heap(nums: List[int], k: int) -> List[int]:
    """Optimized solution: use a heap on frequency counts.

    Time: O(n + k log n)
    Space: O(n)
    Technique: frequency counting + heap selection
    Design system: trending item detection
    """
    freq = Counter(nums)
    return nlargest(k, freq.keys(), key=freq.get)


if __name__ == "__main__":
    items = [1, 1, 1, 2, 2, 3, 4, 4, 5]
    print("Top 2 frequent sorted:", top_k_frequent_sort(items, 2))
    print("Top 2 frequent heap:", top_k_frequent_heap(items, 2))
    print("Complexities:")
    print("  Sort: O(n log n) time, O(n) space")
    print("  Heap: O(n + k log n) time, O(n) space")

PLAIN_COMPLEXITY_NOTE = """
Plain-language explanation of O(n * m log m):
- For n items each of length ~m, O(n * m log m) means you sort each item (≈ m log m) and do that for all n items → n * (m log m).
- Sorting costs m log m because sorting m elements takes about m log m comparisons/operations.
- Space O(n * m): storing a sorted key (length ~m) per item yields ~n * m storage.
- Example: n=1000, m=10 ⇒ cost ≈ 1000 * 10 * log2(10) ≈ 33,000 units; space ≈ 10,000 characters for keys.
- Use sort-key when m is small or implementation simplicity matters; use a frequency/count-key for ASCII lowercase to get O(n * m) time.
"""
