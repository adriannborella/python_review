"""
KMP Algorithm Explanation for str_str_robust
haystack = "mississippi"
needle = "issip"
Expected result: 4

The KMP (Knuth-Morris-Pratt) algorithm efficiently finds pattern occurrences by using a
preprocessing step that creates an LPS (Longest Proper Prefix which is also Suffix) array.
This allows us to skip redundant comparisons when a mismatch occurs.
"""


def str_str_robust_with_explanation(haystack, needle):
    """
    KMP Algorithm with detailed step-by-step explanation
    """
    print(f"Searching for '{needle}' in '{haystack}'")
    print("=" * 50)

    def build_lps_array(pattern):
        """
        Build LPS array for the pattern
        For pattern "issip":

        i s s i p
        0 1 2 3 4  (indices)
        0 0 0 1 0  (LPS values)

        Explanation:
        - i[0]: no proper prefix, LPS = 0
        - s[1]: "i" != "s", LPS = 0
        - s[2]: "is" != "s", LPS = 0
        - i[3]: "iss" has prefix "i" == suffix "i", LPS = 1
        - p[4]: "issi" has no matching prefix/suffix, LPS = 0
        """
        print(f"\nBuilding LPS array for pattern '{pattern}':")
        lps = [0] * len(pattern)
        length = 0
        i = 1

        print(f"Initial: LPS = {lps}")

        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                print(
                    f"Match at i={i}: '{pattern[i]}' == '{pattern[length-1]}', LPS[{i}] = {length}"
                )
                i += 1
            else:
                if length != 0:
                    print(
                        f"Mismatch at i={i}: '{pattern[i]}' != '{pattern[length]}', backtrack length from {length} to {lps[length-1]}"
                    )
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    print(f"No match at i={i}: '{pattern[i]}', LPS[{i}] = 0")
                    i += 1

        print(f"Final LPS array: {lps}")
        return lps

    # Build LPS array
    lps = build_lps_array(needle)

    print(f"\nStarting KMP search:")
    print(f"Haystack: {haystack}")
    print(f"Needle:   {needle}")
    print(f"LPS:      {lps}")
    print()

    # KMP search with detailed tracing
    index_haystack = 0  # Index for haystack
    Index_needle = 0  # Index for needle
    step = 1

    while index_haystack < len(haystack):
        print(
            f"Step {step}: Comparing haystack[{index_haystack}]='{haystack[index_haystack]}' with needle[{Index_needle}]='{needle[Index_needle]}'"
        )

        if haystack[index_haystack] == needle[Index_needle]:
            print(f"         ✓ Match! Advance both pointers")
            index_haystack += 1
            Index_needle += 1

        if Index_needle == len(needle):
            result = index_haystack - Index_needle
            print(f"         🎉 Pattern found! Starting at index {result}")
            return result
        elif (
            index_haystack < len(haystack)
            and haystack[index_haystack] != needle[Index_needle]
        ):
            if Index_needle != 0:
                old_j = Index_needle
                Index_needle = lps[Index_needle - 1]
                print(
                    f"         ✗ Mismatch! Use LPS to skip: j = lps[{old_j-1}] = {Index_needle}"
                )
                print(
                    f"           Now comparing haystack[{index_haystack}]='{haystack[index_haystack]}' with needle[{Index_needle}]='{needle[Index_needle] if Index_needle < len(needle) else 'END'}'"
                )
            else:
                print(f"         ✗ Mismatch at start, advance haystack pointer")
                index_haystack += 1

        step += 1
        if step > 20:  # Safety break
            break

    print(f"Pattern not found")
    return -1


# Test with the example
print("KMP Algorithm Step-by-Step Explanation")
print("=" * 50)
result = str_str_robust_with_explanation("mississippi", "issip")
print(f"\nFinal Result: {result}")

print("\n" + "=" * 50)
print("Why KMP is efficient:")
print("=" * 50)
print(
    """
1. Without KMP (naive approach):
   When we find a mismatch, we go back to the beginning of the pattern
   and advance the haystack by 1, leading to O(m*n) time complexity.

2. With KMP:
   When we find a mismatch, we use the LPS array to determine how far
   we can skip in the pattern without missing any potential matches.
   This gives us O(m+n) time complexity.

For "mississippi" searching for "issip":
- The LPS array [0,0,0,1,0] tells us that when we mismatch at position 4,
  we can restart the pattern from position 0 (since LPS[3] = 1 but the next char doesn't match)
- This avoids redundant comparisons and makes the algorithm efficient.
"""
)
