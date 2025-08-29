from typing import List
from collections import Counter


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        """
        LeetCode 347: Top K Frequent Elements
        Facebook, Amazon - Heap + Hash Map

        Tiempo: O(n log k), Espacio: O(n)
        """
        cnt = Counter(nums)
        return [x[0] for x in cnt.most_common(k)]


sol = Solution()
assert sol.topKFrequent([1, 1, 1, 2, 2, 3], 2) == [1, 2]
