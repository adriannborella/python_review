import heapq


class MedianFinder:
    def __init__(self):
        # Max heap para la mitad menor (negamos valores)
        self.small = []
        # Min heap para la mitad mayor
        self.large = []

    def addNum(self, num: int) -> None:
        # Siempre agregar a small primero
        heapq.heappush(self.small, -num)

        # Asegurar que max(small) <= min(large)
        if self.small and self.large and -self.small[0] > self.large[0]:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)

        # Balancear tamaños
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        elif len(self.large) > len(self.small) + 1:
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return -self.small[0]
        elif len(self.large) > len(self.small):
            return self.large[0]
        else:
            return (-self.small[0] + self.large[0]) / 2.0


test = MedianFinder()

test.addNum(1)
test.addNum(2)
assert test.findMedian() == 1.5
test.addNum(3)
assert test.findMedian() == 2
