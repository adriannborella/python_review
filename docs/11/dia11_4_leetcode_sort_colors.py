"""
LeetCode 75: Sort Colors (MEDIUM)
También conocido como "Dutch National Flag Problem"

Given: [2,0,2,1,1,0]
Output: [0,0,1,1,2,2]

Challenge: One-pass algorithm using O(1) extra space
NO usar sort() built-in!
"""

def sort_colors(nums):
    """
    Dutch Flag Algorithm - Three-way partitioning
    
    Approach: Mantener tres punteros
    - low: boundary para 0s
    - mid: current element
    - high: boundary para 2s
    
    Time: O(n) - single pass
    Space: O(1)
    """
    low = mid = 0
    high = len(nums) - 1
    
    while mid <= high:
        if nums[mid] == 0:
            # Swap current with low boundary
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            # 1 is in correct position, just move forward
            mid += 1
        else:  # nums[mid] == 2
            # Swap current with high boundary
            nums[high], nums[mid] = nums[mid], nums[high]
            high -= 1
            # Don't increment mid, need to check swapped element

def sort_colors_counting(nums):
    """
    Alternative: Counting Sort approach
    Less elegant pero también válido en entrevistas
    """
    # Count occurrences
    count = [0, 0, 0]
    for num in nums:
        count[num] += 1
    
    # Reconstruct array
    idx = 0
    for color in range(3):
        for _ in range(count[color]):
            nums[idx] = color
            idx += 1

def partition_around_value(nums, pivot):
    """
    Generalización del Dutch Flag Problem
    Particiona array around un valor específico
    
    Useful para: Quick Select, Kth Largest Element
    """
    smaller = equal = 0
    larger = len(nums) - 1
    
    while equal <= larger:
        if nums[equal] < pivot:
            nums[smaller], nums[equal] = nums[equal], nums[smaller]
            smaller += 1
            equal += 1
        elif nums[equal] == pivot:
            equal += 1
        else:
            nums[larger], nums[equal] = nums[equal], nums[larger]
            larger -= 1

def sort_colors_k_colors(nums, k):
    """
    Extensión: Sort K colors (0, 1, 2, ..., k-1)
    Demuestra ability to generalize solutions
    """
    # Counting sort approach for k colors
    count = [0] * k
    
    # Count each color
    for num in nums:
        count[num] += 1
    
    # Reconstruct
    idx = 0
    for color in range(k):
        for _ in range(count[color]):
            nums[idx] = color
            idx += 1

# FOLLOW-UP QUESTIONS que pueden preguntar:

def sort_colors_follow_ups():
    """
    Preguntas típicas de follow-up en entrevistas:
    
    1. "¿Qué pasa si tenemos k colores instead de 3?"
       - Counting sort O(n + k)
       - Radix sort para k muy grande
    
    2. "¿Cómo optimizarías para arrays muy grandes?"
       - External sorting si no cabe en memoria
       - Parallel sorting para múltiples cores
    
    3. "¿Qué si los números no son 0,1,2 sino valores arbitrary?"
       - Counting sort si range es pequeño
       - Comparison-based sorting otherwise
    """
    pass

def test_sort_colors():
    """Testing comprehensivo con edge cases"""
    
    # Test básico
    nums1 = [2,0,2,1,1,0]
    sort_colors(nums1)
    assert nums1 == [0,0,1,1,2,2]
    
    # Edge cases
    nums2 = [2,0,1]
    sort_colors(nums2)
    assert nums2 == [0,1,2]
    
    nums3 = [0]
    sort_colors(nums3)
    assert nums3 == [0]
    
    nums4 = [1]
    sort_colors(nums4)
    assert nums4 == [1]
    
    # All same color
    nums5 = [1,1,1,1]
    sort_colors(nums5)
    assert nums5 == [1,1,1,1]
    
    # Already sorted
    nums6 = [0,0,1,1,2,2]
    sort_colors(nums6)
    assert nums6 == [0,0,1,1,2,2]
    
    # Reverse sorted
    nums7 = [2,2,1,1,0,0]
    sort_colors(nums7)
    assert nums7 == [0,0,1,1,2,2]
    
    print("✅ Sort Colors tests passed")
    
    # Test counting approach
    nums8 = [2,0,2,1,1,0]
    sort_colors_counting(nums8)
    assert nums8 == [0,0,1,1,2,2]
    
    print("✅ Counting sort approach passed")
    
    # Test generalized partition
    nums9 = [1,3,2,3,1,3,2,1,2]
    partition_around_value(nums9, 2)
    # After partitioning around 2: [1,1,1,2,2,2,3,3,3]
    # Verifiamos que está correctamente particionado
    pivot_idx = nums9.index(2)
    for i in range(pivot_idx):
        assert nums9[i] < 2
    
    print("✅ Generalized partition passed")

if __name__ == "__main__":
    test_sort_colors()
