"""House Robber: dynamic programming for sequential choices.

Daily analogy: choosing which houses to visit to avoid neighbors and still maximize rewards.
"""
from typing import List


def house_robber_recursive(nums: List[int]) -> int:
    """Base solution: recursion with memoization."""
    memo = {}

    def rob(i: int) -> int:
        if i < 0:
            return 0
        if i in memo:
            return memo[i]
        memo[i] = max(rob(i - 1), rob(i - 2) + nums[i])
        return memo[i]

    return rob(len(nums) - 1)


def house_robber_dp(nums: List[int]) -> int:
    """Optimized solution: iterative DP with constant space.

    Time: O(n)
    Space: O(1)
    Technique: dynamic programming
    Design system: sequential decision making
    """
    prev, curr = 0, 0
    for value in nums:
        prev, curr = curr, max(curr, prev + value)
    return curr


if __name__ == "__main__":
    houses = [2, 7, 9, 3, 1]
    print("Recursive rob result:", house_robber_recursive(houses))
    print("DP rob result:", house_robber_dp(houses))
    print("Complexity: O(n) time, O(1) optimized space")

PLAIN_COMPLEXITY_NOTE = """
Plain-language explanation of O(n * m log m):
- For n items each of length ~m, O(n * m log m) means you sort each item (≈ m log m) and do that for all n items → n * (m log m).
- Sorting costs m log m because sorting m elements takes about m log m comparisons/operations.
- Space O(n * m): storing a sorted key (length ~m) per item yields ~n * m storage.
- Example: n=1000, m=10 ⇒ cost ≈ 1000 * 10 * log2(10) ≈ 33,000 units; space ≈ 10,000 characters for keys.
- Use sort-key when m is small or implementation simplicity matters; use a frequency/count-key for ASCII lowercase to get O(n * m) time.
"""
