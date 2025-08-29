from typing import List

# LeetCode 240
# LeetCode 4
# LeetCode 295
# LeetCode 35
import heapq


class KthLargest:
    """
    LeetCode 703: Kth Largest Element in a Stream
    Design problem - Netflix, Amazon

    Combina: Heap + Stream processing
    """

    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.heap = nums
        heapq.heapify(self.heap)

        # Mantener solo k elementos más grandes
        while len(self.heap) > k:
            heapq.heappop(self.heap)

    def add(self, val: int) -> int:
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        return self.heap[0]


# Your KthLargest object will be instantiated and called as such:
# obj = KthLargest(k, nums)
# param_1 = obj.add(val)
# 1 - 1810

# kthLargest = KthLargest(3, [4, 5, 8, 2])  # [8, 5, 4]
# assert kthLargest.add(3) == 4, "Test case 1"  # [8, 5, 4]
# assert kthLargest.add(5) == 5, "Test case 2"  # [8, 5, 5]
# assert kthLargest.add(10) == 5, "Test case 3"  # [10, 8, 5]
# assert kthLargest.add(9) == 8, "Test case 4"  # [10, 9, 8]
# assert kthLargest.add(4) == 8, "Test case 5"  # [10, 9, 8]

# kthLargest = KthLargest(3, [])  # []
# assert kthLargest.add(-3) == -3, "Test case 1"  # [-3]
# assert kthLargest.add(-2) == -2, "Test case 2"  # [-3,-2]
# assert kthLargest.add(-4) == -2, "Test case 3"  # [-4, -3, -2]
# assert kthLargest.add(0) == 0, "Test case 4"  # [-3,-2,0]
# assert kthLargest.add(4) == 4, "Test case 5"  # [-2, 0, 4]


class MedianFinder:

    def __init__(self):
        self.values = []

    def search_insert_position(self, target):
        """
        LeetCode 35: Search Insert Position
        Encuentra dónde insertar target para mantener orden
        """
        left, right = 0, len(self.values)

        while left < right:
            mid = left + (right - left) // 2

            if self.values[mid] < target:
                left = mid + 1
            else:
                right = mid

        return left

    def addNum(self, num: int) -> None:
        # search the position and split the array and merge it
        if len(self.values) == 0:
            self.values.append(num)
            return

        l = self.search_insert_position(num)
        self.values = self.values[:l] + [num] + self.values[l:]

    def findMedian(self) -> float:
        m_i = len(self.values) // 2
        if len(self.values) % 2 == 0:
            return (self.values[m_i - 1] + self.values[m_i]) / 2
        else:
            return self.values[m_i]


# medianFinder = MedianFinder()
# medianFinder.addNum(1)
# medianFinder.addNum(2)
# assert medianFinder.findMedian() == 1.5  # (i.e., (1 + 2) / 2)
# medianFinder.addNum(3)
# assert medianFinder.findMedian() == 2.0
medianFinder = MedianFinder()
medianFinder.addNum(6)
assert medianFinder.findMedian() == 6, f"Test case 1: {medianFinder.values}"
medianFinder.addNum(10)
assert medianFinder.findMedian() == 8, f"Test case 2: {medianFinder.values}"
medianFinder.addNum(2)
assert medianFinder.findMedian() == 6, f"Test case 3: {medianFinder.values}"
medianFinder.addNum(6)
assert medianFinder.findMedian() == 6, f"Test case 4: {medianFinder.values}"
medianFinder.addNum(5)
assert medianFinder.findMedian() == 6, f"Test case 5: {medianFinder.values}"
medianFinder.addNum(0)
assert medianFinder.findMedian() == 5.5, f"Test case 6: {medianFinder.values}"
medianFinder.addNum(6)
assert medianFinder.findMedian() == 6, f"Test case 7: {medianFinder.values}"
medianFinder.addNum(3)
assert medianFinder.findMedian() == 5.5, f"Test case 8: {medianFinder.values}"
medianFinder.addNum(1)
assert medianFinder.findMedian() == 5, f"Test case 9: {medianFinder.values}"
medianFinder.addNum(0)
assert medianFinder.findMedian() == 4, f"Test case 10: {medianFinder.values}"
medianFinder.addNum(0)
assert medianFinder.findMedian() == 3, f"Test case 11: {medianFinder.values}"

# Your MedianFinder object will be instantiated and called as such:
# obj = MedianFinder()
# obj.addNum(num)
# param_2 = obj.findMedian()
