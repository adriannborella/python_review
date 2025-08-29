from typing import List


class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        # teorical_middle = (len(nums1) + len(nums2)) // 2

        # if len(nums1) > len(nums2):
        #     nums1, nums2 = nums2, nums1

        # index_1 = index_2 = 0
        # last_value = current_value = 0
        # current_index = -1

        # while current_index < teorical_middle:
        #     last_value = current_value
        #     current_index += 1

        #     if index_1 == len(nums1) or (
        #         index_2 != len(nums2) and nums1[index_1] > nums2[index_2]
        #     ):
        #         # 1 - 2 < 1
        #         current_value = nums2[index_2]
        #         index_2 += 1
        #     else:
        #         current_value = nums1[index_1]
        #         index_1 += 1

        # if (len(nums1) + len(nums2)) % 2 == 0:
        #     return (last_value + current_value) / 2
        # return current_value

        # Asegurar que nums1 es el más pequeño
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1

        m, n = len(nums1), len(nums2)
        left, right = 0, m

        while left <= right:
            partitionX = (left + right) // 2
            partitionY = (m + n + 1) // 2 - partitionX

            # Valores máximos a la izquierda
            maxLeftX = float("-inf") if partitionX == 0 else nums1[partitionX - 1]
            maxLeftY = float("-inf") if partitionY == 0 else nums2[partitionY - 1]

            # Valores mínimos a la derecha
            minRightX = float("inf") if partitionX == m else nums1[partitionX]
            minRightY = float("inf") if partitionY == n else nums2[partitionY]

            if maxLeftX <= minRightY and maxLeftY <= minRightX:
                # Partición correcta encontrada
                if (m + n) % 2 == 0:
                    return (max(maxLeftX, maxLeftY) + min(minRightX, minRightY)) / 2.0
                else:
                    return max(maxLeftX, maxLeftY)
            elif maxLeftX > minRightY:
                right = partitionX - 1
            else:
                left = partitionX + 1

        raise ValueError("Input arrays are not sorted")


sol = Solution()
assert sol.findMedianSortedArrays([1, 3], [2]) == 2
assert sol.findMedianSortedArrays([1, 3, 4, 5], [2]) == 3
assert sol.findMedianSortedArrays([1, 2], [3, 4]) == 2.5
assert sol.findMedianSortedArrays([1, 2], [3, 4]) == 2.5
assert sol.findMedianSortedArrays([2, 4], []) == 3
assert sol.findMedianSortedArrays([2, 4, 8], []) == 4
assert sol.findMedianSortedArrays([100001], [100000]) == (100000 + 100001) / 2
