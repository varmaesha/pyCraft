# Practical DS & Algo Examples

This folder contains practical, daily-life analogies for common data structures and algorithm patterns.

## Included examples

- `binary_search.py`: ordered search in a sorted list
- `merge_intervals.py`: calendar meeting merge
- `valid_parentheses.py`: stack-based nested validation
- `top_k_frequent.py`: trending item extraction
- `anagram_groups.py`: string grouping via hash normalization
- `house_robber.py`: sequential decision dynamic programming
- `connected_components.py`: graph traversal for island counting
- `sliding_window_maximum.py`: moving-window peak detection

## How to use

Each file includes:
- a base/naive implementation for understanding
- an optimized implementation for practical use
- complexity comments and concept notes
- a simple `__main__` example that can be run directly

## Related follow-up ideas

- binary search trees and balanced search structures
- interval scheduling and room allocation
- parser validation and expression evaluation
- frequent-item caching and heavy-hitter detection
- string deduplication and message normalization
- DP for inventory optimization and scheduling
- graph clustering and connected network discovery
- stream analytics with sliding windows

## Plain-language complexity note (example)

Plain-language explanation of O(n * m log m):

- For n items each of length ~m, O(n * m log m) means you sort each item (≈ m log m) and do that for all n items → n * (m log m).
- Sorting costs m log m because sorting m elements takes about m log m comparisons/operations.
- Space O(n * m): storing a sorted key (length ~m) per item yields ~n * m storage.
- Example: n=1000, m=10 ⇒ cost ≈ 1000 * 10 * log2(10) ≈ 33,000 units; space ≈ 10,000 characters for keys.
- Use sort-key when m is small or implementation simplicity matters; use a frequency/count-key for ASCII lowercase to get O(n * m) time.

You can copy this note into any example file where `O(n * m log m)` appears.
