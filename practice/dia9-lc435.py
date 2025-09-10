from typing import List


class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda x: x[1])

        intersections = 0
        last_end = intervals[0][1]

        for start, end in intervals[1:]:
            if start < last_end:
                intersections += 1
            else:
                last_end = end

        return intersections


sol = Solution()
assert sol.eraseOverlapIntervals([[1, 2], [2, 3], [3, 4], [1, 3]]) == 1, "Test case 1"
assert sol.eraseOverlapIntervals([[1, 2], [1, 2], [1, 2]]) == 2, "Test case 2"
assert sol.eraseOverlapIntervals([[1, 2], [2, 3]]) == 0, "Test case 3"
assert (
    sol.eraseOverlapIntervals([[1, 100], [11, 22], [1, 11], [2, 12]]) == 2
), "Test case 4"
