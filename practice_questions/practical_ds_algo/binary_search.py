"""Binary Search: base vs optimized solutions.

Daily analogy: finding a name in a sorted phonebook vs scanning every contact.
"""
from typing import List, Optional


def linear_search(nums: List[int], target: int) -> Optional[int]:
    """Base solution: check each element until found."""
    for i, value in enumerate(nums):
        if value == target:
            return i
    return None


def binary_search(nums: List[int], target: int) -> Optional[int]:
    """Optimized solution: binary search in sorted data.

    Time: O(log n)
    Space: O(1)
    Technique: divide and conquer
    Design system: search optimization in ordered data
    """
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return None


if __name__ == "__main__":
    sample = [1, 3, 5, 7, 9, 11, 13]
    target = 7
    print("Linear search result:", linear_search(sample, target))
    print("Binary search result:", binary_search(sample, target))
    print("Complexities:")
    print("  Linear: O(n) time, O(1) space")
    print("  Binary: O(log n) time, O(1) space")

PLAIN_COMPLEXITY_NOTE = """
Plain-language explanation of O(n * m log m):
- For n items each of length ~m, O(n * m log m) means you sort each item (≈ m log m) and do that for all n items → n * (m log m).
- Sorting costs m log m because sorting m elements takes about m log m comparisons/operations.
- Space O(n * m): storing a sorted key (length ~m) per item yields ~n * m storage.
- Example: n=1000, m=10 ⇒ cost ≈ 1000 * 10 * log2(10) ≈ 33,000 units; space ≈ 10,000 characters for keys.
- Use sort-key when m is small or implementation simplicity matters; use a frequency/count-key for ASCII lowercase to get O(n * m) time.
"""
