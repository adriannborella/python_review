"""
LINKED LISTS COMPLETAS - Desde Implementación hasta Problemas Avanzados
Estructura fundamental que aparece en 60% de entrevistas técnicas
"""

class ListNode:
    """Basic building block - siempre define esto primero en entrevistas"""
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    
    def __str__(self):
        return f"ListNode({self.val})"
    
    def __repr__(self):
        return self.__str__()

class SinglyLinkedList:
    """
    Complete Singly Linked List implementation
    Debe poder implementar desde cero en <10 minutos
    """
    def __init__(self):
        self.head = None
        self.size = 0
    
    def append(self, val):
        """Add element at end - O(n)"""
        new_node = ListNode(val)
        
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        
        self.size += 1
    
    def prepend(self, val):
        """Add element at beginning - O(1)"""
        new_node = ListNode(val)
        new_node.next = self.head
        self.head = new_node
        self.size += 1
    
    def delete(self, val):
        """Delete first occurrence - O(n)"""
        if not self.head:
            return False
        
        if self.head.val == val:
            self.head = self.head.next
            self.size -= 1
            return True
        
        current = self.head
        while current.next:
            if current.next.val == val:
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next
        
        return False
    
    def find(self, val):
        """Search for value - O(n)"""
        current = self.head
        while current:
            if current.val == val:
                return current
            current = current.next
        return None
    
    def to_list(self):
        """Convert to Python list for testing"""
        result = []
        current = self.head
        while current:
            result.append(current.val)
            current = current.next
        return result
    
    def __len__(self):
        return self.size
    
    def __str__(self):
        return " -> ".join(map(str, self.to_list())) + " -> None"

class DoublyLinkedList:
    """
    Doubly Linked List - para when you need O(1) deletion at any position
    """
    class Node:
        def __init__(self, val=0, prev=None, next=None):
            self.val = val
            self.prev = prev
            self.next = next
    
    def __init__(self):
        # Dummy head and tail para easier edge case handling
        self.head = self.Node()
        self.tail = self.Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0
    
    def add_after(self, node, val):
        """Add new node after given node - O(1)"""
        new_node = self.Node(val)
        new_node.prev = node
        new_node.next = node.next
        node.next.prev = new_node
        node.next = new_node
        self.size += 1
        return new_node
    
    def remove_node(self, node):
        """Remove given node - O(1)"""
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1
        return node.val
    
    def append(self, val):
        """Add at end - O(1) thanks to tail pointer"""
        return self.add_after(self.tail.prev, val)
    
    def prepend(self, val):
        """Add at beginning - O(1)"""
        return self.add_after(self.head, val)

# LEETCODE PROBLEMS - ESSENTIAL PATTERNS

def reverse_linked_list(head):
    """
    LeetCode 206: Reverse Linked List (EASY)
    
    Must know both iterative and recursive solutions
    THE most common linked list question
    """
    # Iterative approach - preferred in interviews
    prev = None
    current = head
    
    while current:
        next_temp = current.next
        current.next = prev
        prev = current
        current = next_temp
    
    return prev

def reverse_linked_list_recursive(head):
    """Recursive approach - demonstrates recursion understanding"""
    if not head or not head.next:
        return head
    
    reversed_head = reverse_linked_list_recursive(head.next)
    head.next.next = head
    head.next = None
    
    return reversed_head

def has_cycle(head):
    """
    LeetCode 141: Linked List Cycle (EASY)
    
    Floyd's Cycle Detection - tortoise and hare
    """
    if not head:
        return False
    
    slow = fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
        if slow == fast:
            return True
    
    return False

def detect_cycle_start(head):
    """
    LeetCode 142: Linked List Cycle II (MEDIUM)
    
    Find WHERE the cycle starts - advanced Floyd's algorithm
    """
    if not head:
        return None
    
    # Phase 1: Detect if cycle exists
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    else:
        return None  # No cycle
    
    # Phase 2: Find cycle start
    # Mathematical proof: distance from head to cycle start = 
    # distance from meeting point to cycle start
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next
    
    return slow

def merge_two_sorted_lists(l1, l2):
    """
    LeetCode 21: Merge Two Sorted Lists (EASY)
    
    Fundamental for merge sort on linked lists
    """
    dummy = ListNode(0)
    current = dummy
    
    while l1 and l2:
        if l1.val <= l2.val:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next
    
    # Attach remaining nodes
    current.next = l1 or l2
    
    return dummy.next

def merge_k_sorted_lists(lists):
    """
    LeetCode 23: Merge k Sorted Lists (HARD)
    
    Multiple approaches - demonstrate algorithmic thinking
    """
    import heapq
    
    if not lists:
        return None
    
    # Approach 1: Min Heap - O(N log k) where N = total nodes
    heap = []
    
    # Initialize heap with first node from each list
    for i, head in enumerate(lists):
        if head:
            # Use index to break ties (heapq needs comparable elements)
            heapq.heappush(heap, (head.val, i, head))
    
    dummy = ListNode(0)
    current = dummy
    
    while heap:
        val, list_idx, node = heapq.heappop(heap)
        current.next = node
        current = current.next
        
        # Add next node from same list
        if node.next:
            heapq.heappush(heap, (node.next.val, list_idx, node.next))
    
    return dummy.next

def merge_k_sorted_lists_divide_conquer(lists):
    """
    Alternative: Divide and Conquer approach - O(N log k)
    More elegant, shows advanced thinking
    """
    if not lists:
        return None
    
    while len(lists) > 1:
        merged_lists = []
        
        # Merge lists pairwise
        for i in range(0, len(lists), 2):
            l1 = lists[i]
            l2 = lists[i + 1] if i + 1 < len(lists) else None
            merged_lists.append(merge_two_sorted_lists(l1, l2))
        
        lists = merged_lists
    
    return lists[0]

def remove_nth_from_end(head, n):
    """
    LeetCode 19: Remove Nth Node From End (MEDIUM)
    
    One-pass solution using two pointers
    """
    dummy = ListNode(0)
    dummy.next = head
    
    # Move first pointer n+1 steps ahead
    first = dummy
    for _ in range(n + 1):
        first = first.next
    
    # Move both pointers until first reaches end
    second = dummy
    while first:
        first = first.next
        second = second.next
    
    # Remove the nth node from end
    second.next = second.next.next
    
    return dummy.next

def reorder_list(head):
    """
    LeetCode 143: Reorder List (MEDIUM)
    
    L0 → L1 → … → Ln-1 → Ln becomes L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → …
    
    Combines multiple techniques: find middle, reverse, merge
    """
    if not head or not head.next:
        return
    
    # Step 1: Find middle of linked list
    slow = fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    
    # Step 2: Reverse second half
    second_half = slow.next
    slow.next = None
    second_half = reverse_linked_list(second_half)
    
    # Step 3: Merge two halves alternately
    first_half = head
    while second_half:
        temp1 = first_half.next
        temp2 = second_half.next
        
        first_half.next = second_half
        second_half.next = temp1
        
        first_half = temp1
        second_half = temp2

def add_two_numbers(l1, l2):
    """
    LeetCode 2: Add Two Numbers (MEDIUM)
    
    Numbers stored in reverse order: 342 + 465 = 807
    Represented as: [2,4,3] + [5,6,4] = [7,0,8]
    """
    dummy = ListNode(0)
    current = dummy
    carry = 0
    
    while l1 or l2 or carry:
        val1 = l1.val if l1 else 0
        val2 = l2.val if l2 else 0
        
        total = val1 + val2 + carry
        carry = total // 10
        current.next = ListNode(total % 10)
        
        current = current.next
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None
    
    return dummy.next

# UTILITY FUNCTIONS
def create_linked_list(values):
    """Helper function to create linked list from list"""
    if not values:
        return None
    
    head = ListNode(values[0])
    current = head
    
    for val in values[1:]:
        current.next = ListNode(val)
        current = current.next
    
    return head

def linked_list_to_list(head):
    """Helper function to convert linked list to Python list"""
    result = []
    current = head
    while current:
        result.append(current.val)
        current = current.next
    return result

# COMPREHENSIVE TESTING
def test_linked_lists():
    """Testing all linked list implementations and problems"""
    
    # Test basic linked list operations
    ll = SinglyLinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    ll.prepend(0)
    
    assert ll.to_list() == [0, 1, 2, 3]
    assert ll.delete(2) == True
    assert ll.to_list() == [0, 1, 3]
    
    print("✅ Basic Linked List operations tests passed")
    
    # Test reverse linked list
    head = create_linked_list([1, 2, 3, 4, 5])
    reversed_head = reverse_linked_list(head)
    assert linked_list_to_list(reversed_head) == [5, 4, 3, 2, 1]
    
    print("✅ Reverse Linked List tests passed")
    
    # Test cycle detection
    head = create_linked_list([3, 2, 0, -4])
    # Create cycle: tail -> node at index 1
    tail = head
    while tail.next:
        tail = tail.next
    tail.next = head.next  # Creates cycle
    
    assert has_cycle(head) == True
    
    print("✅ Cycle Detection tests passed")
    
    # Test merge two sorted lists
    l1 = create_linked_list([1, 2, 4])
    l2 = create_linked_list([1, 3, 4])
    merged = merge_two_sorted_lists(l1, l2)
    assert linked_list_to_list(merged) == [1, 1, 2, 3, 4, 4]
    
    print("✅ Merge Two Sorted Lists tests passed")
    
    # Test remove nth from end
    head = create_linked_list([1, 2, 3, 4, 5])
    result = remove_nth_from_end(head, 2)
    assert linked_list_to_list(result) == [1, 2, 3, 5]
    
    print("✅ Remove Nth From End tests passed")
    
    # Test add two numbers
    l1 = create_linked_list([2, 4, 3])  # 342
    l2 = create_linked_list([5, 6, 4])  # 465
    result = add_two_numbers(l1, l2)
    assert linked_list_to_list(result) == [7, 0, 8]  # 807
    
    print("✅ Add Two Numbers tests passed")

if __name__ == "__main__":
    test_linked_lists()
