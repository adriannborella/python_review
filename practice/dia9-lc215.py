from typing import List


class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        """
        LeetCode 215: Kth Largest Element (QuickSelect)
        Amazon, Facebook - Optimización de QuickSort

        Tiempo: O(n) average, O(n²) worst case
        """
        nums.sort()
        print(f"{nums}, {nums[-(k)]}")
        return nums[-k]


sol = Solution()
assert sol.findKthLargest([3, 2, 1, 5, 6, 4], 2) == 5
assert sol.findKthLargest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
