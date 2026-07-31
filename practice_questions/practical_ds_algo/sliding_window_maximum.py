"""Sliding Window Maximum: moving-window peak detection.

Daily analogy: tracking the highest demand in the last hour as new sensor readings arrive.
"""
from collections import deque
from typing import Deque, List


def sliding_window_maximum_naive(nums: List[int], k: int) -> List[int]:
    """Base solution: compute max for each window."""
    return [max(nums[i:i + k]) for i in range(len(nums) - k + 1)]


def sliding_window_maximum(nums: List[int], k: int) -> List[int]:
    """Optimized solution: use a deque to track candidate indices.

    Time: O(n)
    Space: O(k)
    Technique: monotonic deque / sliding window
    Design system: streaming peak detection
    """
    if not nums or k == 0:
        return []

    window: Deque[int] = deque()
    result: List[int] = []

    for i, value in enumerate(nums):
        while window and window[0] <= i - k:
            window.popleft()
        while window and nums[window[-1]] < value:
            window.pop()
        window.append(i)
        if i >= k - 1:
            result.append(nums[window[0]])

    return result


if __name__ == "__main__":
    readings = [1, 3, -1, -3, 5, 3, 6, 7]
    print("Naive max values:", sliding_window_maximum_naive(readings, 3))
    print("Optimized max values:", sliding_window_maximum(readings, 3))
    print("Complexity: O(n) time, O(k) space")

PLAIN_COMPLEXITY_NOTE = """
Plain-language explanation of O(n * m log m):
- For n items each of length ~m, O(n * m log m) means you sort each item (≈ m log m) and do that for all n items → n * (m log m).
- Sorting costs m log m because sorting m elements takes about m log m comparisons/operations.
- Space O(n * m): storing a sorted key (length ~m) per item yields ~n * m storage.
- Example: n=1000, m=10 ⇒ cost ≈ 1000 * 10 * log2(10) ≈ 33,000 units; space ≈ 10,000 characters for keys.
- Use sort-key when m is small or implementation simplicity matters; use a frequency/count-key for ASCII lowercase to get O(n * m) time.
"""
