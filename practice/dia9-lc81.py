from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> bool:
        """
        LeetCode 81: Search in Rotated Sorted Array II (con duplicados)
        Más complejo que la versión I - Meta, Apple

        Tiempo: O(log n) average, O(n) worst case
        """
        left, rigth = 0, len(nums) - 1

        while left <= rigth:
            si = left + (rigth - left) // 2

            if nums[si] == target:
                print(f"Found it at {si}")
                return True

            if nums[left] == nums[si] == nums[right]:
                left += 1
                right -= 1
            else:
                # if nums[left] <= nums[si]:  # Izquierda ordenada
                #     if nums[left] <= target < nums[si]:
                #         right = si - 1
                #     else:
                #         left = si + 1
                # else:  # Derecha ordenada
                #     if nums[si] < target <= nums[right]:
                #         left = si + 1
                #     else:
                #         right = si - 1
                if nums[rigth] < nums[si]:
                    if nums[si] >= target > nums[rigth]:
                        left = si + 1
                    else:
                        rigth = si - 1
                else:
                    if nums[left] > target >= nums[si]:
                        rigth = si - 1
                    else:
                        left = si + 1

        print(f"Not found {target} in {nums}")
        return False


sol = Solution()

# assert sol.search([2, 5, 6, 0, 0, 1, 2], 0) == True
# assert sol.search([2, 5, 6, 0, 0, 1, 2], 3) == False
assert sol.search([1, 0, 1, 1, 1], 0) == True
assert sol.search([1, 0, 1, 1, 1], 1) == True
assert sol.search([1, 0, 1, 1, 1], 2) == False
