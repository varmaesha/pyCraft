"""Group Anagrams: practical string grouping.

Daily analogy: grouping scrambled letters into matching word piles.
"""
from collections import defaultdict
from typing import List


def group_anagrams_sort(strs: List[str]) -> List[List[str]]:
    """Base solution: use sorted string keys."""
    groups = defaultdict(list)
    for s in strs:
        groups[''.join(sorted(s))].append(s)
    return list(groups.values())


def group_anagrams_count(strs: List[str]) -> List[List[str]]:
    """Optimized solution: use frequency tuple keys.

    Time: O(n * m log m) in base, O(n * m) optimized
    Space: O(n * m)
    Technique: hashing with normalized keys
    Design system: classification/grouping
    """
    groups = defaultdict(list)
    for s in strs:
        count = [0] * 26
        for char in s:
            count[ord(char) - ord('a')] += 1
        groups[tuple(count)].append(s)
    return list(groups.values())


if __name__ == "__main__":
    words = ["eat", "tea", "tan", "ate", "nat", "bat"]
    print("Sort groups:", group_anagrams_sort(words))
    print("Count groups:", group_anagrams_count(words))
    print("Complexities:")
    print("  Sort key: O(n * m log m) time, O(n * m) space")
    print("  Count key: O(n * m) time, O(n * m) space")

PLAIN_COMPLEXITY_NOTE = """
Plain-language explanation of O(n * m log m):
- For n items each of length ~m, O(n * m log m) means you sort each item (≈ m log m) and do that for all n items → n * (m log m).
- Sorting costs m log m because sorting m elements takes about m log m comparisons/operations.
- Space O(n * m): storing a sorted key (length ~m) per item yields ~n * m storage.
- Example: n=1000, m=10 ⇒ cost ≈ 1000 * 10 * log2(10) ≈ 33,000 units; space ≈ 10,000 characters for keys.
- Use sort-key when m is small or implementation simplicity matters; use a frequency/count-key for ASCII lowercase to get O(n * m) time.
"""
