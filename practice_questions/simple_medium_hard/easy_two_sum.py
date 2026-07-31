"""Two Sum: base vs optimized solutions.

Daily analogy: finding two purchases that exactly match a budget, or two items whose prices sum to a gift card amount.
"""

from typing import List, Optional, Tuple


def two_sum_bruteforce(nums: List[int], target: int) -> Optional[Tuple[int, int]]:
    """Base solution: check every pair."""
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return i, j
    return None


def two_sum_hash(nums: List[int], target: int) -> Optional[Tuple[int, int]]:
    """Optimized solution: hash table lookup.

    Time: O(n)
    Space: O(n)
    Technique: hash-based complement search
    Design pattern: data structure design (lookup table)
    """
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return seen[complement], i
        seen[num] = i
    return None


if __name__ == "__main__":
    sample = [2, 7, 11, 15]
    target = 9
    print("Base brute-force result:", two_sum_bruteforce(sample, target))
    print("Optimized hash result:", two_sum_hash(sample, target))
    print("Complexities:")
    print("  Brute force: O(n^2) time, O(1) space")
    print("  Hash map: O(n) time, O(n) space")

PLAIN_COMPLEXITY_NOTE = """
Plain-language explanation of O(n * m log m):
- For n items each of length ~m, O(n * m log m) means you sort each item (≈ m log m) and do that for all n items → n * (m log m).
- Sorting costs m log m because sorting m elements takes about m log m comparisons/operations.
- Space O(n * m): storing a sorted key (length ~m) per item yields ~n * m storage.
- Example: n=1000, m=10 ⇒ cost ≈ 1000 * 10 * log2(10) ≈ 33,000 units; space ≈ 10,000 characters for keys.
- Use sort-key when m is small or implementation simplicity matters; use a frequency/count-key for ASCII lowercase to get O(n * m) time.
"""
