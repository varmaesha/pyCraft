"""Merge Intervals: combine overlapping calendar blocks.

Daily analogy: consolidating meetings in a calendar so free time is easy to see.
"""
from typing import List


def merge_intervals_bruteforce(intervals: List[List[int]]) -> List[List[int]]:
    """Base solution: compare every interval to merge overlaps."""
    if not intervals:
        return []
    intervals = sorted(intervals, key=lambda x: x[0])
    merged = []
    for interval in intervals:
        if not merged or merged[-1][1] < interval[0]:
            merged.append(interval[:])
        else:
            merged[-1][1] = max(merged[-1][1], interval[1])
    return merged


def merge_intervals_sorted(intervals: List[List[int]]) -> List[List[int]]:
    """Optimized solution: sort then scan once.

    Time: O(n log n) due to sorting
    Space: O(n)
    Technique: greedy interval processing
    Design system: scheduling and reservation optimization
    """
    if not intervals:
        return []
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0][:]]
    for start, end in intervals[1:]:
        last_end = merged[-1][1]
        if start <= last_end:
            merged[-1][1] = max(last_end, end)
        else:
            merged.append([start, end])
    return merged


if __name__ == "__main__":
    meetings = [[1, 3], [2, 6], [8, 10], [15, 18]]
    print("Merged intervals:", merge_intervals_sorted(meetings))
    print("Complexity: O(n log n) time, O(n) space")

PLAIN_COMPLEXITY_NOTE = """
Plain-language explanation of O(n * m log m):
- For n items each of length ~m, O(n * m log m) means you sort each item (≈ m log m) and do that for all n items → n * (m log m).
- Sorting costs m log m because sorting m elements takes about m log m comparisons/operations.
- Space O(n * m): storing a sorted key (length ~m) per item yields ~n * m storage.
- Example: n=1000, m=10 ⇒ cost ≈ 1000 * 10 * log2(10) ≈ 33,000 units; space ≈ 10,000 characters for keys.
- Use sort-key when m is small or implementation simplicity matters; use a frequency/count-key for ASCII lowercase to get O(n * m) time.
"""
