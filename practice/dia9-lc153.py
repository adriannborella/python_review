from typing import List


class Solution:
    def findMin(self, nums: List[int]) -> int:
        """
        LeetCode 153: Find Minimum in Rotated Sorted Array
        Microsoft, Amazon - Variante común

        Tiempo: O(log n), Espacio: O(1)
        """
        left, right = 0, len(nums) - 1
        while left < right:
            print(f"searching in {nums[left:right + 1]}")
            ci = left + (right - left) // 2

            if nums[ci] > nums[right]:
                # minimo esta en la derecha
                left = ci + 1
            else:
                # Minimo esta a la izquida o es mid
                right = ci

        print(f"Result: Index:{left} Value:{nums[left]}")
        return nums[left]


sol = Solution()
assert sol.findMin([3, 4, 5, 1, 2]) == 1
assert sol.findMin([4, 5, 6, 7, 0, 1, 2]) == 0
assert sol.findMin([11, 13, 15, 17]) == 11
assert sol.findMin([5, 1, 2, 3, 4]) == 1
