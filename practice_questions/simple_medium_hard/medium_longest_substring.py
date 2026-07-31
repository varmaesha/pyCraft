"""Longest Substring Without Repeating Characters: base vs optimized solutions.

Daily analogy: finding the longest time interval during the day when no task repeats. 
"""

from typing import Dict, List


def longest_unique_substring_bruteforce(s: str) -> int:
    """Base solution: check every substring and validate uniqueness."""
    def is_unique(sub: str) -> bool:
        return len(set(sub)) == len(sub)

    max_len = 0
    n = len(s)
    for i in range(n):
        for j in range(i + 1, n + 1):
            if is_unique(s[i:j]):
                max_len = max(max_len, j - i)
    return max_len


def longest_unique_substring_sliding_window(s: str) -> int:
    """Optimized solution: sliding window with hash map.

    Time: O(n)
    Space: O(min(n, charset_size))
    Technique: sliding window, two-pointer window expansion/contraction
    Design pattern: streaming window / greedy window maintenance
    """
    char_index: Dict[str, int] = {}
    left = 0
    max_len = 0

    for right, char in enumerate(s):
        if char in char_index and char_index[char] >= left:
            left = char_index[char] + 1
        char_index[char] = right
        max_len = max(max_len, right - left + 1)

    return max_len


if __name__ == "__main__":
    sample = "abcabcbb"
    print("Base brute-force result:", longest_unique_substring_bruteforce(sample))
    print("Optimized sliding-window result:", longest_unique_substring_sliding_window(sample))
    print("Complexities:")
    print("  Brute force: O(n^3) time in worst-case due to substring uniqueness checks, O(n) space for sets")
    print("  Sliding window: O(n) time, O(min(n, charset)) space")

PLAIN_COMPLEXITY_NOTE = """
Plain-language explanation of O(n * m log m):
- For n items each of length ~m, O(n * m log m) means you sort each item (≈ m log m) and do that for all n items → n * (m log m).
- Sorting costs m log m because sorting m elements takes about m log m comparisons/operations.
- Space O(n * m): storing a sorted key (length ~m) per item yields ~n * m storage.
- Example: n=1000, m=10 ⇒ cost ≈ 1000 * 10 * log2(10) ≈ 33,000 units; space ≈ 10,000 characters for keys.
- Use sort-key when m is small or implementation simplicity matters; use a frequency/count-key for ASCII lowercase to get O(n * m) time.
"""
