# Practice Questions: Simple, Medium, Hard

This folder contains three example problems with both base and optimized Python solutions, complexity analysis, and related questions.

## Problems included

1. `easy_two_sum.py`
   - Problem: Two Sum
   - Base solution: brute-force pair search
   - Optimized solution: hash table one-pass lookup
   - Technique: hash-based lookup, complement search
   - Design system: data structure design pattern

2. `medium_longest_substring.py`
   - Problem: Longest Substring Without Repeating Characters
   - Base solution: nested loops with substring scanning
   - Optimized solution: sliding window with hash map
   - Technique: sliding window, dynamic window resizing
   - Design system: streaming/windowing pattern

3. `hard_lru_cache.py`
   - Problem: Design LRU Cache
   - Base solution: naive list-based eviction
   - Optimized solution: hash map + doubly linked list / ordered dictionary
   - Technique: cache eviction, constant-time lookup and update
   - Design system: cache system design, eviction policy

## How to use

Run each Python file to see the sample inputs and outputs. Each file contains:
- a base implementation for clarity
- an optimized implementation for production-style use
- complexity analysis in comments and docstrings
- a real-world analogy for the problem

## Related concepts

- `Two Sum`: pair sum, complement search, sorted array two-pointer variant
- `Longest Substring Without Repeating Characters`: sliding window, unique-window, minimum-window substring
- `LRU Cache`: caching, eviction, system design for memory-limited fast retrieval

## Related follow-up questions

See `related_questions.md` for question prompts that are natural extensions of these problems.
