"""
STACKS - Implementación y Aplicaciones Avanzadas
LIFO (Last In, First Out) - fundamental para muchos algoritmos
"""

class Stack:
    """
    Stack implementation using dynamic array
    All operations O(1) amortized
    """
    def __init__(self):
        self.items = []
    
    def push(self, item):
        """Add item to top of stack"""
        self.items.append(item)
    
    def pop(self):
        """Remove and return top item"""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self.items.pop()
    
    def peek(self):
        """Return top item without removing"""
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self.items[-1]
    
    def is_empty(self):
        """Check if stack is empty"""
        return len(self.items) == 0
    
    def size(self):
        """Return number of items"""
        return len(self.items)
    
    def __str__(self):
        return str(self.items)

class StackWithLinkedList:
    """
    Stack implementation using linked list
    True O(1) for all operations (no amortization)
    """
    class Node:
        def __init__(self, data):
            self.data = data
            self.next = None
    
    def __init__(self):
        self.head = None
        self.size = 0
    
    def push(self, data):
        """Add to front of linked list"""
        new_node = self.Node(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1
    
    def pop(self):
        """Remove from front of linked list"""
        if self.head is None:
            raise IndexError("pop from empty stack")
        
        data = self.head.data
        self.head = self.head.next
        self.size -= 1
        return data
    
    def peek(self):
        if self.head is None:
            raise IndexError("peek from empty stack")
        return self.head.data
    
    def is_empty(self):
        return self.head is None

def valid_parentheses(s):
    """
    LeetCode 20: Valid Parentheses (EASY)
    
    THE classic stack problem - must solve in <5 minutes
    """
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:
            # Closing bracket
            top_element = stack.pop() if stack else '#'
            if mapping[char] != top_element:
                return False
        else:
            # Opening bracket
            stack.append(char)
    
    return not stack

def min_stack():
    """
    LeetCode 155: Min Stack (MEDIUM)
    
    Design stack that supports push, pop, top, and getMin in O(1)
    Key insight: Use auxiliary stack to track minimums
    """
    class MinStack:
        def __init__(self):
            self.stack = []
            self.min_stack = []
        
        def push(self, val):
            self.stack.append(val)
            # Push to min_stack if it's empty or val <= current min
            if not self.min_stack or val <= self.min_stack[-1]:
                self.min_stack.append(val)
        
        def pop(self):
            if not self.stack:
                return
            
            val = self.stack.pop()
            # Pop from min_stack if popped value was the minimum
            if self.min_stack and val == self.min_stack[-1]:
                self.min_stack.pop()
            return val
        
        def top(self):
            return self.stack[-1] if self.stack else None
        
        def getMin(self):
            return self.min_stack[-1] if self.min_stack else None
    
    return MinStack()

def daily_temperatures(temperatures):
    """
    LeetCode 739: Daily Temperatures (MEDIUM)
    
    Monotonic Stack pattern - extremely important
    For each day, find how many days until warmer temperature
    """
    n = len(temperatures)
    result = [0] * n
    stack = []  # Stack of indices
    
    for i, temp in enumerate(temperatures):
        # Process all days that are cooler than current day
        while stack and temperatures[stack[-1]] < temp:
            prev_day = stack.pop()
            result[prev_day] = i - prev_day
        
        stack.append(i)
    
    return result

def largest_rectangle_histogram(heights):
    """
    LeetCode 84: Largest Rectangle in Histogram (HARD)
    
    Advanced monotonic stack - challenging but important
    Find largest rectangular area in histogram
    """
    stack = []
    max_area = 0
    
    for i, height in enumerate(heights):
        # Process bars that are taller than current
        while stack and heights[stack[-1]] > height:
            h = heights[stack.pop()]
            # Width: current index - previous index - 1
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, h * width)
        
        stack.append(i)
    
    # Process remaining bars
    while stack:
        h = heights[stack.pop()]
        width = len(heights) if not stack else len(heights) - stack[-1] - 1
        max_area = max(max_area, h * width)
    
    return max_area

def evaluate_reverse_polish_notation(tokens):
    """
    LeetCode 150: Evaluate Reverse Polish Notation (MEDIUM)
    
    Classic stack application for expression evaluation
    """
    stack = []
    operators = {'+', '-', '*', '/'}
    
    for token in tokens:
        if token in operators:
            # Pop two operands (note the order!)
            b = stack.pop()
            a = stack.pop()
            
            if token == '+':
                result = a + b
            elif token == '-':
                result = a - b
            elif token == '*':
                result = a * b
            elif token == '/':
                # Integer division towards zero
                result = int(a / b)
            
            stack.append(result)
        else:
            # Operand
            stack.append(int(token))
    
    return stack[0]

def simplify_path(path):
    """
    LeetCode 71: Simplify Path (MEDIUM)
    
    Unix-style path simplification using stack
    """
    stack = []
    components = path.split('/')
    
    for component in components:
        if component == '' or component == '.':
            # Skip empty and current directory
            continue
        elif component == '..':
            # Parent directory - pop if stack not empty
            if stack:
                stack.pop()
        else:
            # Valid directory name
            stack.append(component)
    
    return '/' + '/'.join(stack)

def next_greater_element(nums1, nums2):
    """
    LeetCode 496: Next Greater Element I (EASY)
    
    Monotonic stack to find next greater element
    """
    # Build next greater mapping for nums2
    next_greater = {}
    stack = []
    
    for num in nums2:
        while stack and stack[-1] < num:
            next_greater[stack.pop()] = num
        stack.append(num)
    
    # Build result for nums1
    return [next_greater.get(num, -1) for num in nums1]

def remove_duplicate_letters(s):
    """
    LeetCode 316: Remove Duplicate Letters (HARD)
    
    Advanced: Monotonic stack + greedy + character counting
    Result should be lexicographically smallest
    """
    from collections import Counter
    
    count = Counter(s)
    stack = []
    in_stack = set()
    
    for char in s:
        count[char] -= 1  # We've seen this character
        
        if char in in_stack:
            continue  # Already in result
        
        # Remove characters that are:
        # 1. Larger than current character (lexicographically)
        # 2. Will appear later in the string
        while (stack and 
               stack[-1] > char and 
               count[stack[-1]] > 0):
            removed = stack.pop()
            in_stack.remove(removed)
        
        stack.append(char)
        in_stack.add(char)
    
    return ''.join(stack)

class StackUsingQueues:
    """
    LeetCode 225: Implement Stack using Queues (EASY)
    
    Demonstrates understanding of both data structures
    """
    def __init__(self):
        from collections import deque
        self.queue = deque()
    
    def push(self, x):
        """Push element to top of stack"""
        self.queue.append(x)
        # Rotate queue to make last element first
        for _ in range(len(self.queue) - 1):
            self.queue.append(self.queue.popleft())
    
    def pop(self):
        """Remove top element"""
        return self.queue.popleft()
    
    def top(self):
        """Get top element"""
        return self.queue[0]
    
    def empty(self):
        """Check if empty"""
        return len(self.queue) == 0

# COMPREHENSIVE TESTING
def test_stack_problems():
    """Testing all stack implementations and problems"""
    
    # Test basic stack
    stack = Stack()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    
    assert stack.pop() == 3
    assert stack.peek() == 2
    assert stack.size() == 2
    assert not stack.is_empty()
    
    print("✅ Basic Stack tests passed")
    
    # Test valid parentheses
    assert valid_parentheses("()") == True
    assert valid_parentheses("()[]{}") == True
    assert valid_parentheses("(]") == False
    assert valid_parentheses("([)]") == False
    assert valid_parentheses("{[]}") == True
    
    print("✅ Valid Parentheses tests passed")
    
    # Test min stack
    min_st = min_stack()
    min_st.push(-2)
    min_st.push(0)
    min_st.push(-3)
    assert min_st.getMin() == -3
    min_st.pop()
    assert min_st.top() == 0
    assert min_st.getMin() == -2
    
    print("✅ Min Stack tests passed")
    
    # Test daily temperatures
    temps = [73,74,75,71,69,72,76,73]
    expected = [1,1,4,2,1,1,0,0]
    assert daily_temperatures(temps) == expected
    
    print("✅ Daily Temperatures tests passed")
    
    # Test largest rectangle
    heights = [2,1,5,6,2,3]
    assert largest_rectangle_histogram(heights) == 10
    
    heights2 = [2,4]
    assert largest_rectangle_histogram(heights2) == 4
    
    print("✅ Largest Rectangle tests passed")
    
    # Test RPN evaluation
    tokens = ["2","1","+","3","*"]
    assert evaluate_reverse_polish_notation(tokens) == 9  # ((2+1)*3)
    
    tokens2 = ["4","13","5","/","+"]
    assert evaluate_reverse_polish_notation(tokens2) == 6  # (4+(13/5))
    
    print("✅ RPN Evaluation tests passed")
    
    # Test path simplification
    assert simplify_path("/home/") == "/home"
    assert simplify_path("/../") == "/"
    assert simplify_path("/home//foo/") == "/home/foo"
    assert simplify_path("/a/./b/../../c/") == "/c"
    
    print("✅ Path Simplification tests passed")
    
    # Test next greater element
    nums1 = [4,1,2]
    nums2 = [1,3,4,2]
    expected = [-1,3,-1]  # For 4: no greater, For 1: 3, For 2: no greater
    assert next_greater_element(nums1, nums2) == expected
    
    print("✅ Next Greater Element tests passed")
    
    # Test remove duplicate letters
    assert remove_duplicate_letters("bcabc") == "abc"
    assert remove_duplicate_letters("cbacdcbc") == "acdb"
    
    print("✅ Remove Duplicate Letters tests passed")

if __name__ == "__main__":
    test_stack_problems()