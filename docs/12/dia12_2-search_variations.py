"""
SEARCH VARIATIONS - Más allá de Binary Search
Para demostrar conocimiento algorítmico profundo en entrevistas senior
"""

def ternary_search_max(arr, left, right):
    """
    Ternary Search: Para encontrar máximo en función unimodal
    
    Divide search space en 3 partes instead of 2
    Útil para optimization problems
    
    Time: O(log₃ n) ≈ O(log n)
    Space: O(1)
    """
    if left == right:
        return left
    
    # Divide into three parts
    mid1 = left + (right - left) // 3
    mid2 = right - (right - left) // 3
    
    if arr[mid1] < arr[mid2]:
        # Maximum is in right 2/3
        return ternary_search_max(arr, mid1 + 1, right)
    else:
        # Maximum is in left 2/3
        return ternary_search_max(arr, left, mid2 - 1)

def ternary_search_continuous(func, left, right, epsilon=1e-9):
    """
    Ternary Search para funciones continuas
    Encuentra máximo de función unimodal en range continuo
    
    Useful para: optimization problems, mathematical functions
    """
    while right - left > epsilon:
        mid1 = left + (right - left) / 3
        mid2 = right - (right - left) / 3
        
        if func(mid1) < func(mid2):
            left = mid1
        else:
            right = mid2
    
    return (left + right) / 2

def exponential_search(arr, target):
    """
    Exponential Search: Para unbounded/infinite arrays
    
    Phase 1: Find range where target might exist - O(log n)
    Phase 2: Binary search in that range - O(log n)
    
    Total: O(log n)
    Better than binary search when target is close to beginning
    """
    if arr[0] == target:
        return 0
    
    # Find range for binary search by doubling
    i = 1
    while i < len(arr) and arr[i] <= target:
        i *= 2
    
    # Binary search in found range
    return binary_search_range(arr, target, i // 2, min(i, len(arr) - 1))

def binary_search_range(arr, target, left, right):
    """Helper for exponential search"""
    while left <= right:
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

def interpolation_search(arr, target):
    """
    Interpolation Search: Better than binary for uniformly distributed data
    
    Instead of always going to middle, estimate position based on value
    Average case: O(log log n)
    Worst case: O(n) - when data is not uniformly distributed
    """
    left, right = 0, len(arr) - 1
    
    while left <= right and arr[left] <= target <= arr[right]:
        # If only one element
        if left == right:
            return left if arr[left] == target else -1
        
        # Estimate position using linear interpolation
        pos = left + ((target - arr[left]) * (right - left)) // (arr[right] - arr[left])
        
        if arr[pos] == target:
            return pos
        elif arr[pos] < target:
            left = pos + 1
        else:
            right = pos - 1
    
    return -1

def find_rotation_point(arr):
    """
    Find pivot point in rotated sorted array
    Useful para: understanding array rotations
    """
    left, right = 0, len(arr) - 1
    
    # Array is not rotated
    if arr[left] <= arr[right]:
        return 0
    
    while left <= right:
        mid = left + (right - left) // 2
        
        # Found rotation point
        if mid > 0 and arr[mid] < arr[mid - 1]:
            return mid
        
        if arr[mid] >= arr[left]:
            # Rotation point is in right half
            left = mid + 1
        else:
            # Rotation point is in left half
            right = mid - 1
    
    return 0

def jump_search(arr, target):
    """
    Jump Search: Block-based search algorithm
    
    Jump √n elements at a time, then linear search in block
    Time: O(√n)
    Space: O(1)
    
    Better than linear search, simpler than binary search
    """
    import math
    
    n = len(arr)
    step = int(math.sqrt(n))
    prev = 0
    
    # Find block where element is present
    while prev < n and arr[min(step, n) - 1] < target:
        prev = step
        step += int(math.sqrt(n))
        
        if prev >= n:
            return -1
    
    # Linear search in identified block
    while prev < n and arr[prev] < target:
        prev += 1
    
    if prev < n and arr[prev] == target:
        return prev
    
    return -1

# COMPARISON DE ALGORITMOS DE BÚSQUEDA
def search_algorithms_comparison():
    """
    Comparación de algoritmos de búsqueda para interview discussions
    
    Binary Search: O(log n) - General purpose, works on any sorted data
    Ternary Search: O(log₃ n) - For unimodal functions, optimization
    Exponential Search: O(log n) - For unbounded arrays, target near start
    Interpolation Search: O(log log n) avg - Uniformly distributed data
    Jump Search: O(√n) - Simple implementation, good for small datasets
    
    Trade-offs discussion:
    - Binary: Most versatile, always O(log n)
    - Ternary: Slightly more comparisons per iteration than binary
    - Exponential: Great when you don't know array size
    - Interpolation: Amazing on uniform data, terrible on skewed data
    - Jump: Simple to implement, doesn't require random access
    """
    pass

def test_search_variations():
    """Comprehensive testing de todas las variaciones"""
    
    # Test ternary search
    # Unimodal array: increases then decreases
    unimodal = [1, 3, 8, 12, 15, 17, 16, 10, 6, 2]
    max_idx = ternary_search_max(unimodal, 0, len(unimodal) - 1)
    assert unimodal[max_idx] == 17  # Maximum value
    
    print("✅ Ternary Search tests passed")
    
    # Test ternary search continuous
    def quadratic(x):
        return -(x - 3) ** 2 + 9  # Max at x=3, value=9
    
    max_x = ternary_search_continuous(quadratic, 0, 6)
    assert abs(max_x - 3.0) < 1e-6
    
    print("✅ Continuous Ternary Search tests passed")
    
    # Test exponential search
    arr = list(range(1, 1001))  # [1, 2, 3, ..., 1000]
    assert exponential_search(arr, 500) == 499  # 0-indexed
    assert exponential_search(arr, 1) == 0
    assert exponential_search(arr, 1001) == -1
    
    print("✅ Exponential Search tests passed")
    
    # Test interpolation search
    uniform_arr = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    assert interpolation_search(uniform_arr, 50) == 4
    assert interpolation_search(uniform_arr, 25) == -1
    
    print("✅ Interpolation Search tests passed")
    
    # Test rotation point
    rotated1 = [4, 5, 6, 7, 0, 1, 2]
    assert find_rotation_point(rotated1) == 4  # Index of 0
    
    rotated2 = [1, 2, 3, 4, 5]  # Not rotated
    assert find_rotation_point(rotated2) == 0
    
    print("✅ Rotation Point tests passed")
    
    # Test jump search
    search_arr = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]
    assert jump_search(search_arr, 55) == 10
    assert jump_search(search_arr, 999) == -1
    
    print("✅ Jump Search tests passed")

if __name__ == "__main__":
    test_search_variations()
