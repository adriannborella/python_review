from typing import List


class Solution:
    def findClosestElements(self, arr: List[int], k: int, x: int) -> List[int]:
        """
        LeetCode 658: Find K Closest Elements
        LinkedIn, Uber - Combina binary search + two pointers

        Tiempo: O(log n + k), Espacio: O(1)
        """
        # Buscar numero o posicion donde deberia estar y desde ahi calcular los k elementos cercas
        left = 0
        rigth = len(arr) - k
        while left < rigth:
            mid = left + (rigth - left) // 2

            if x - arr[mid] > arr[mid + k] - x:
                left = mid + 1
            else:
                rigth = mid

        print(f"Result: Start:{left} end:{left + k} {arr[left : left + k]}")
        return arr[left : left + k]


sol = Solution()
# assert sol.findClosestElements([1, 2, 3, 4, 5], 4, 3) == [1, 2, 3, 4]
# assert sol.findClosestElements([1, 1, 2, 3, 4, 5], 4, -1) == [1, 1, 2, 3]
# assert sol.findClosestElements([1, 1, 2, 3, 4, 5], 2, 5) == [4, 5]
assert sol.findClosestElements([1, 1, 1, 10, 10, 10], 1, 9) == [10]
