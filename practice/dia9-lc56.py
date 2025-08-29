from typing import List


class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        """
        LeetCode 56: Merge Intervals
        Microsoft, Google - Sorting + Merging

        Tiempo: O(n log n), Espacio: O(1)
        """
        intervals.sort(key=lambda x: x[0])

        result = [intervals[0]]

        for current in intervals[1:]:
            last_merged = result[-1]

            if current[0] <= last_merged[1]:
                last_merged[1] = max(current[1], last_merged[1])
            else:
                result.append(current)
        return result


sol = Solution()
# assert sol.merge([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
# assert sol.merge([[1, 4], [4, 5]]) == [[1, 5]]
assert sol.merge([[1, 4], [2, 3]]) == [[1, 4]]
