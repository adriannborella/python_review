from typing import List


class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        """
        LeetCode 240: Search 2D Matrix II
        Google, Facebook - Técnica de eliminación

        Tiempo: O(m + n), Espacio: O(1)
        """
        # Buscar primero la maxima fila a buscar
        if not matrix or not matrix[0]:
            return False

        # Empezar desde esquina superior derecha
        row = 0
        col = len(matrix[0]) - 1

        while row < len(matrix) and col >= 0:
            if matrix[row][col] == target:
                return True
            else:
                if matrix[row][col] > target:
                    col -= 1  # Eliminar columna
                else:
                    row += 1  # Eliminar fila

        return False


sol = Solution()
matrix = [
    [1, 4, 7, 11, 15],
    [2, 5, 8, 12, 19],
    [3, 6, 9, 16, 22],
    [10, 13, 14, 17, 24],
    [18, 21, 23, 26, 30],
]
assert sol.searchMatrix(matrix, 5)
# assert sol.searchMatrix(matrix, 30)
# assert sol.searchMatrix(matrix, 1)
# assert sol.searchMatrix(matrix, 20) == False
