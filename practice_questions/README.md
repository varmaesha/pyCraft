# Practice Questions Collection

This folder is designed to help you understand data structures and algorithms through practical examples.

## Subfolders

- `simple_medium_hard/`: a small set of easy, medium, and hard examples with base and optimized code.
- `practical_ds_algo/`: a larger set of practical DS/Algo programs with real-world analogies.

## Usage

Run any Python file directly to see sample behavior and complexity notes. Use the examples as templates for interview practice or real-world problem solving.

## Suggested workflow

1. Start with easy problems in `simple_medium_hard/`.
2. Move to practical patterns in `practical_ds_algo/`.
3. Modify the sample inputs to try edge cases.
4. Add your own real-life variants based on tasks like scheduling, caching, searching, and streaming analytics.

## Plain-language complexity note (example)

Plain-language explanation of O(n * m log m):

- For n items each of length ~m, O(n * m log m) means you sort each item (≈ m log m) and do that for all n items → n * (m log m).
- Sorting costs m log m because sorting m elements takes about m log m comparisons/operations.
- Space O(n * m): storing a sorted key (length ~m) per item yields ~n * m storage.
- Example: n=1000, m=10 ⇒ cost ≈ 1000 * 10 * log2(10) ≈ 33,000 units; space ≈ 10,000 characters for keys.
- Use sort-key when m is small or implementation simplicity matters; use a frequency/count-key for ASCII lowercase to get O(n * m) time.

This note is suitable to add to any example file that uses a sort-based normalization key.
