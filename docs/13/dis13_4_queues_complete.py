"""
QUEUES - Implementación y Aplicaciones Avanzadas
FIFO (First In, First Out) - esencial para BFS, scheduling, etc.
"""

from collections import deque


class Queue:
    """
    Queue implementation using deque
    O(1) for all operations
    """

    def __init__(self):
        self.items = deque()

    def enqueue(self, item):
        """Add item to rear of queue"""
        self.items.append(item)

    def dequeue(self):
        """Remove and return item from front"""
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self.items.popleft()

    def front(self):
        """Return front item without removing"""
        if self.is_empty():
            raise IndexError("front from empty queue")
        return self.items[0]

    def is_empty(self):
        """Check if queue is empty"""
        return len(self.items) == 0

    def size(self):
        """Return number of items"""
        return len(self.items)

    def __str__(self):
        return str(list(self.items))


# LEETCODE PROBLEMS


class CircularQueue:
    """
    LeetCode 622: Design Circular Queue (MEDIUM)

    Fixed-size queue with efficient space usage
    All operations O(1)
    """

    def __init__(self, k):
        self.size = 0
        self.max_size = k
        self.data = [0] * k
        self.head = 0

    def enQueue(self, value):
        """Insert element into circular queue"""
        if self.isFull():
            return False

        tail = (self.head + self.size) % self.max_size
        self.data[tail] = value
        self.size += 1
        return True

    def deQueue(self):
        """Delete element from circular queue"""
        if self.isEmpty():
            return False

        self.head = (self.head + 1) % self.max_size
        self.size -= 1
        return True

    def Front(self):
        """Get front item"""
        if self.isEmpty():
            return -1
        return self.data[self.head]

    def Rear(self):
        """Get rear item"""
        if self.isEmpty():
            return -1
        tail = (self.head + self.size - 1) % self.max_size
        return self.data[tail]

    def isEmpty(self):
        return self.size == 0

    def isFull(self):
        return self.size == self.max_size


class QueueUsingStacks:
    """
    LeetCode 232: Implement Queue using Stacks (EASY)

    Demonstrates understanding of both data structures
    Amortized O(1) for all operations
    """

    def __init__(self):
        self.input_stack = []
        self.output_stack = []

    def push(self, x):
        """Add element to queue"""
        self.input_stack.append(x)

    def pop(self):
        """Remove element from queue"""
        self._move_if_needed()
        return self.output_stack.pop()

    def peek(self):
        """Get front element"""
        self._move_if_needed()
        return self.output_stack[-1]

    def empty(self):
        """Check if empty"""
        return not self.input_stack and not self.output_stack

    def _move_if_needed(self):
        """Move elements from input to output stack if needed"""
        if not self.output_stack:
            while self.input_stack:
                self.output_stack.append(self.input_stack.pop())


class MonotonicQueue:
    """
    Monotonic Deque for sliding window problems
    Maintains elements in decreasing order
    """

    def __init__(self):
        self.deque = deque()

    def push(self, val):
        """Add element, maintaining decreasing order"""
        while self.deque and self.deque[-1] < val:
            self.deque.pop()
        self.deque.append(val)

    def pop(self, val):
        """Remove element if it's the front"""
        if self.deque and self.deque[0] == val:
            self.deque.popleft()

    def max(self):
        """Get maximum element"""
        return self.deque[0] if self.deque else None


def sliding_window_maximum(nums, k):
    """
    LeetCode 239: Sliding Window Maximum (HARD)

    Use monotonic deque to track maximum in O(n) time
    """
    if not nums:
        return []

    dq = deque()  # Store indices
    result = []

    for i, num in enumerate(nums):
        # Remove elements outside current window
        while dq and dq[0] <= i - k:
            dq.popleft()

        # Remove elements smaller than current
        while dq and nums[dq[-1]] < num:
            dq.pop()

        dq.append(i)

        # Add to result if window is complete
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result


def walls_and_gates(rooms):
    """
    LeetCode 286: Walls and Gates (MEDIUM)

    Multi-source BFS using queue
    Fill empty rooms with distance to nearest gate
    """
    if not rooms or not rooms[0]:
        return

    m, n = len(rooms), len(rooms[0])
    queue = deque()

    # Find all gates and add to queue
    for i in range(m):
        for j in range(n):
            if rooms[i][j] == 0:  # Gate
                queue.append((i, j))

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # BFS from all gates simultaneously
    while queue:
        row, col = queue.popleft()

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            # Check bounds and if cell is empty room
            if (
                0 <= new_row < m
                and 0 <= new_col < n
                and rooms[new_row][new_col] == 2147483647
            ):  # INF (empty room)

                rooms[new_row][new_col] = rooms[row][col] + 1
                queue.append((new_row, new_col))


def open_the_lock(deadends, target):
    """
    LeetCode 752: Open the Lock (MEDIUM)

    BFS to find shortest path in state space
    """
    if "0000" in deadends:
        return -1

    queue = deque([("0000", 0)])  # (state, steps)
    visited = {"0000"}
    deadend_set = set(deadends)

    def get_neighbors(state):
        """Get all possible next states"""
        neighbors = []
        for i in range(4):
            digit = int(state[i])
            # Turn forward and backward
            for delta in [1, -1]:
                new_digit = (digit + delta) % 10
                new_state = state[:i] + str(new_digit) + state[i + 1 :]
                neighbors.append(new_state)
        return neighbors

    while queue:
        current_state, steps = queue.popleft()

        if current_state == target:
            return steps

        for next_state in get_neighbors(current_state):
            if next_state not in visited and next_state not in deadend_set:
                visited.add(next_state)
                queue.append((next_state, steps + 1))

    return -1


def perfect_squares(n):
    """
    LeetCode 279: Perfect Squares (MEDIUM)

    BFS approach: find minimum number of perfect squares that sum to n
    """
    if n <= 0:
        return 0

    # Generate perfect squares up to n
    perfect_squares = []
    i = 1
    while i * i <= n:
        perfect_squares.append(i * i)
        i += 1

    queue = deque([(n, 0)])  # (remaining, count)
    visited = {n}

    while queue:
        remaining, count = queue.popleft()

        for square in perfect_squares:
            if square == remaining:
                return count + 1
            elif square < remaining:
                new_remaining = remaining - square
                if new_remaining not in visited:
                    visited.add(new_remaining)
                    queue.append((new_remaining, count + 1))
            else:
                break  # No point checking larger squares

    return n  # Worst case: all 1s


def moving_average_from_data_stream(size):
    """
    LeetCode 346: Moving Average from Data Stream (EASY)

    Use queue to maintain sliding window
    """

    class MovingAverage:
        def __init__(self, size):
            self.size = size
            self.queue = deque()
            self.sum = 0

        def next(self, val):
            self.queue.append(val)
            self.sum += val

            # Remove old values if window exceeds size
            if len(self.queue) > self.size:
                self.sum -= self.queue.popleft()

            return self.sum / len(self.queue)

    return MovingAverage(size)


class HitCounter:
    """
    LeetCode 362: Design Hit Counter (MEDIUM)

    Track hits in the past 5 minutes using queue
    """

    def __init__(self):
        self.hits = deque()

    def hit(self, timestamp):
        """Record a hit at timestamp"""
        self.hits.append(timestamp)

    def getHits(self, timestamp):
        """Get hits in past 300 seconds"""
        # Remove hits older than 300 seconds
        while self.hits and self.hits[0] <= timestamp - 300:
            self.hits.popleft()

        return len(self.hits)


# COMPREHENSIVE TESTING
def test_queue_problems():
    """Testing all queue implementations and problems"""

    # Test basic queue
    queue = Queue()
    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)

    assert queue.dequeue() == 1
    assert queue.front() == 2
    assert queue.size() == 2
    assert not queue.is_empty()

    print("✅ Basic Queue tests passed")

    # Test circular queue
    cq = CircularQueue(3)
    assert cq.enQueue(1) == True
    assert cq.enQueue(2) == True
    assert cq.enQueue(3) == True
    assert cq.enQueue(4) == False  # Full
    assert cq.Rear() == 3
    assert cq.isFull() == True
    assert cq.deQueue() == True
    assert cq.enQueue(4) == True
    assert cq.Rear() == 4

    print("✅ Circular Queue tests passed")

    # Test queue using stacks
    queue_stack = QueueUsingStacks()
    queue_stack.push(1)
    queue_stack.push(2)
    assert queue_stack.peek() == 1
    assert queue_stack.pop() == 1
    assert not queue_stack.empty()

    print("✅ Queue Using Stacks tests passed")

    # Test sliding window maximum
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    expected = [3, 3, 5, 5, 6, 7]
    assert sliding_window_maximum(nums, k) == expected

    print("✅ Sliding Window Maximum tests passed")

    # Test open the lock
    deadends = ["0201", "0101", "0102", "1212", "2002"]
    target = "0202"
    assert open_the_lock(deadends, target) == 6

    print("✅ Open The Lock tests passed")

    # Test perfect squares
    assert perfect_squares(12) == 3  # 4 + 4 + 4
    assert perfect_squares(13) == 2  # 4 + 9

    print("✅ Perfect Squares tests passed")

    # Test moving average
    ma = moving_average_from_data_stream(3)
    assert ma.next(1) == 1.0
    assert ma.next(10) == 5.5  # (1+10)/2
    assert ma.next(3) == (1 + 10 + 3) / 3
    assert ma.next(5) == (10 + 3 + 5) / 3  # Window slides

    print("✅ Moving Average tests passed")

    # Test hit counter
    counter = HitCounter()
    counter.hit(1)
    counter.hit(2)
    counter.hit(3)
    assert counter.getHits(4) == 3
    counter.hit(300)
    assert counter.getHits(300) == 4
    assert counter.getHits(301) == 3  # Hit at timestamp 1 expires

    print("✅ Hit Counter tests passed")


if __name__ == "__main__":
    test_queue_problems()
