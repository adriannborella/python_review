from typing import List


class Solution:
    def insert(
        self, intervals: List[List[int]], newInterval: List[int]
    ) -> List[List[int]]:
        """
        LeetCode 57: Insert Interval
        Given sorted intervals, insert new interval and merge

        More complex: need to handle insertion position
        """
        result = []
        i = 0
        n = len(intervals)

        # agrega los intervalos menores al inicio del nuevo intervalo
        while i < n and intervals[i][1] < newInterval[0]:
            result.append(intervals[i])
            i += 1

        # Realizo un merge de los intervalos
        while i < n and intervals[i][0] <= newInterval[1]:
            newInterval[0] = min(newInterval[0], intervals[i][0])
            newInterval[1] = max(newInterval[1], intervals[i][1])

        result.append(newInterval)

        # Add intervalos restantes
        while i < n:
            result.append(intervals[i])
            i += 1

        return result


sol = Solution()
# assert sol.insert([[1, 3], [6, 9]], [4, 5]) == [[1, 3], [4, 5], [6, 9]], "Test case 1"
# assert sol.insert([[1, 3], [6, 9]], [2, 5]) == [[1, 5], [6, 9]], "Test case 2"
# assert sol.insert([[2, 5], [6, 9]], [1, 3]) == [[1, 5], [6, 9]], "Test case 3"
assert sol.insert([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]) == [
    [1, 2],
    [3, 10],
    [12, 16],
], "Test case 4"
