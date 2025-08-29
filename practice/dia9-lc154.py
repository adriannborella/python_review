from typing import List


class Solution:
    def findMin(self, nums: List[int]) -> int:
        """
        LeetCode 153: Find Minimum in Rotated Sorted Array
        Microsoft, Amazon - Variante común

        Tiempo: O(log n), Espacio: O(1)
        """
        left = 0
        rigth = len(nums) - 1

        while left < rigth:
            mid = left + (rigth - left) // 2

            if nums[left] == nums[mid] == nums[rigth]:
                rigth -= 1
            else:
                if nums[mid] > nums[rigth]:
                    left = mid + 1
                else:
                    rigth = mid

        print(f"result: {nums[left]}")
        return nums[left]


sol = Solution()
# assert sol.findMin([1, 3, 5]) == 1
# assert sol.findMin([2, 2, 2, 0, 1]) == 0
# assert sol.findMin([4, 5, 6, 7, 0, 1, 4]) == 0
# assert sol.findMin([5, 1, 2, 3, 4, 4, 4, 4, 4]) == 1
assert sol.findMin([2, 2, 2, 0, 2, 2]) == 0
