from typing import List


class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.

        LeetCode 75: Sort Colors (Dutch National Flag)
        Apple, Google - Algoritmo de partición avanzado

        Tiempo: O(n), Espacio: O(1)

        """

        # 0 1 2
        low = current = 0
        high = len(nums) - 1

        while current <= high:
            if nums[current] == 0:
                nums[low], nums[current] = nums[current], nums[low]
                low += 1
                current += 1
            else:
                if nums[current] == 1:
                    current += 1
                else:  # nums[current] == 2
                    nums[current], nums[high] = nums[high], nums[current]
                    high -= 1
                    # No incrementar current porque necesitamos revisar el elemento swapped


sol = Solution()
assert sol.sortColors([2, 0, 2, 1, 1, 0]) == [0, 0, 1, 1, 2, 2]
assert sol.sortColors([2, 0, 1]) == [0, 1, 2]
