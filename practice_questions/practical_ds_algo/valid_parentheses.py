"""Valid Parentheses: base vs optimized solutions.

Daily analogy: making sure nested boxes are closed in the right order.
"""

def is_valid_bruteforce(s: str) -> bool:
    """Base solution: remove matching pairs until no more remain."""
    pairs = ["()", "[]", "{}"]
    while any(pair in s for pair in pairs):
        for pair in pairs:
            s = s.replace(pair, "")
    return not s


def is_valid_stack(s: str) -> bool:
    """Optimized solution: use a stack to track opening brackets.

    Time: O(n)
    Space: O(n)
    Technique: stack for nested structure validation
    Design system: parser-like input validation
    """
    stack = []
    matching = {')': '(', ']': '[', '}': '{'}
    for char in s:
        if char in matching.values():
            stack.append(char)
        elif char in matching:
            if not stack or stack.pop() != matching[char]:
                return False
        else:
            return False
    return not stack


if __name__ == "__main__":
    sample = "([{}])"
    print("Bruteforce valid:", is_valid_bruteforce(sample))
    print("Stack valid:", is_valid_stack(sample))
    print("Complexities:")
    print("  Bruteforce: O(n^2) time, O(n) space")
    print("  Stack: O(n) time, O(n) space")

PLAIN_COMPLEXITY_NOTE = """
Plain-language explanation of O(n * m log m):
- For n items each of length ~m, O(n * m log m) means you sort each item (≈ m log m) and do that for all n items → n * (m log m).
- Sorting costs m log m because sorting m elements takes about m log m comparisons/operations.
- Space O(n * m): storing a sorted key (length ~m) per item yields ~n * m storage.
- Example: n=1000, m=10 ⇒ cost ≈ 1000 * 10 * log2(10) ≈ 33,000 units; space ≈ 10,000 characters for keys.
- Use sort-key when m is small or implementation simplicity matters; use a frequency/count-key for ASCII lowercase to get O(n * m) time.
"""
