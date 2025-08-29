from typing import List


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        start_pos = result = 0
        seen = {}

        for current_pos, letter in enumerate(s):
            if letter in seen and seen[letter] >= start_pos:
                start_pos = seen[letter] + 1

            seen[letter] = current_pos
            result = max(result, current_pos - start_pos + 1)

        print(f"result: {result}")
        return result


sol = Solution()
assert sol.lengthOfLongestSubstring("abcabcbb") == 3
assert sol.lengthOfLongestSubstring("bbbb") == 1
assert sol.lengthOfLongestSubstring("pwwkew") == 3
assert sol.lengthOfLongestSubstring(" ") == 1
assert sol.lengthOfLongestSubstring("dvdf") == 3
assert sol.lengthOfLongestSubstring("tmmzuxt") == 5
assert sol.lengthOfLongestSubstring("ohvhjdml") == 6
assert sol.lengthOfLongestSubstring("bbtablud") == 6
