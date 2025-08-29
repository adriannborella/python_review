from typing import List


def searchMatrix(matrix: List[List[int]], target: int) -> bool:
    """
    LeetCode 74: Search 2D Matrix
    Binary search en matriz ordenada
    """
    index = 0

    l = 0
    r = len(matrix)
    while l < r:
        si = (l + r) // 2
        if matrix[si][0] <= target <= matrix[si][-1]:
            index = si
            break

        if matrix[si][-1] > target:
            r = si
        else:
            l = si + 1

    l = 0
    r = len(matrix[index]) - 1
    while l <= r:
        si = (l + r) // 2
        if matrix[index][si] == target:
            return True

        if matrix[index][si] > target:
            r = si - 1
        else:
            l = si + 1

    return False

    if not matrix or not matrix[0]:
        return False

    rows, cols = len(matrix), len(matrix[0])
    left, right = 0, rows * cols - 1

    while left <= right:
        mid = left + (right - left) // 2
        mid_value = matrix[mid // cols][mid % cols]

        if mid_value == target:
            return True
        elif mid_value < target:
            left = mid + 1
        else:
            right = mid - 1

    return False


assert searchMatrix(
    [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 3
), "Test case 1"
assert (
    searchMatrix([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 13) == False
), "Test case 2"
assert searchMatrix([[1]], 2) == False, "Test case 3"
