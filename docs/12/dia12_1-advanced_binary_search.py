"""
BINARY SEARCH AVANZADO - Para Entrevistas Senior
Key insight: Binary search no solo es para arrays ordenados!
También funciona para "search space" que tiene propiedades monótonas
"""

def find_peak_element(nums):
    """
    LeetCode 162: Find Peak Element (MEDIUM)
    Peak: nums[i] > nums[i-1] and nums[i] > nums[i+1]
    
    Key insight: Binary search en array NO ordenado
    Siempre podemos encontrar un peak siguiendo la slope ascendente
    """
    left, right = 0, len(nums) - 1
    
    while left < right:
        mid = left + (right - left) // 2
        
        if nums[mid] > nums[mid + 1]:
            # Peak está en la izquierda (incluyendo mid)
            right = mid
        else:
            # Peak está en la derecha
            left = mid + 1
    
    return left

def search_2d_matrix(matrix, target):
    """
    LeetCode 74: Search 2D Matrix (MEDIUM)
    Matrix ordenada row-wise y column-wise
    
    Approach: Treat as 1D sorted array
    """
    if not matrix or not matrix[0]:
        return False
    
    m, n = len(matrix), len(matrix[0])
    left, right = 0, m * n - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        mid_value = matrix[mid // n][mid % n]  # Convert 1D index to 2D
        
        if mid_value == target:
            return True
        elif mid_value < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return False

def search_2d_matrix_ii(matrix, target):
    """
    LeetCode 240: Search 2D Matrix II (MEDIUM)
    Más complejo: cada row Y column están ordenadas
    
    Approach: Start from top-right corner
    O(m + n) solution - más eficiente que binary search aquí
    """
    if not matrix or not matrix[0]:
        return False
    
    row, col = 0, len(matrix[0]) - 1
    
    while row < len(matrix) and col >= 0:
        if matrix[row][col] == target:
            return True
        elif matrix[row][col] > target:
            col -= 1  # Move left
        else:
            row += 1  # Move down
    
    return False

def find_first_bad_version(n, is_bad_version):
    """
    LeetCode 278: First Bad Version (EASY pero conceptually important)
    Classic application de binary search en problem domain
    
    API calls son expensive - minimize calls
    """
    left, right = 1, n
    
    while left < right:
        mid = left + (right - left) // 2
        
        if is_bad_version(mid):
            # First bad version is at mid or before
            right = mid
        else:
            # First bad version is after mid
            left = mid + 1
    
    return left

def sqrt_binary_search(x):
    """
    LeetCode 69: Sqrt(x) (EASY)
    Binary search en range de posibles respuestas
    
    Alternative to Newton's method
    """
    if x < 2:
        return x
    
    left, right = 2, x // 2
    
    while left <= right:
        mid = left + (right - left) // 2
        num = mid * mid
        
        if num == x:
            return mid
        elif num < x:
            left = mid + 1
        else:
            right = mid - 1
    
    return right  # Return floor of sqrt

def capacity_to_ship_packages(weights, days):
    """
    LeetCode 1011: Capacity To Ship Packages Within D Days (MEDIUM)
    
    Key insight: Binary search en range de capacidades posibles
    Minimum capacity = max(weights)
    Maximum capacity = sum(weights)
    """
    def can_ship_with_capacity(capacity):
        """Check if we can ship all packages with given capacity"""
        days_needed = 1
        current_load = 0
        
        for weight in weights:
            if current_load + weight > capacity:
                days_needed += 1
                current_load = weight
            else:
                current_load += weight
        
        return days_needed <= days
    
    left = max(weights)  # Minimum possible capacity
    right = sum(weights)  # Maximum possible capacity
    
    while left < right:
        mid = left + (right - left) // 2
        
        if can_ship_with_capacity(mid):
            right = mid  # Try smaller capacity
        else:
            left = mid + 1  # Need larger capacity
    
    return left

def kth_smallest_in_matrix(matrix, k):
    """
    LeetCode 378: Kth Smallest Element in Sorted Matrix (MEDIUM/HARD)
    
    Advanced: Binary search en VALUES, no en indices
    """
    n = len(matrix)
    left, right = matrix[0][0], matrix[n-1][n-1]
    
    def count_less_equal(mid):
        """Count elements <= mid in sorted matrix"""
        count = 0
        row, col = n - 1, 0  # Start from bottom-left
        
        while row >= 0 and col < n:
            if matrix[row][col] <= mid:
                count += row + 1  # All elements in this column up to row
                col += 1
            else:
                row -= 1
        
        return count
    
    while left < right:
        mid = left + (right - left) // 2
        
        if count_less_equal(mid) < k:
            left = mid + 1
        else:
            right = mid
    
    return left

# TESTS PARA BINARY SEARCH AVANZADO
def test_advanced_binary_search():
    """Testing de todos los casos avanzados"""
    
    # Test find peak
    assert find_peak_element([1,2,3,1]) in [2]  # Index 2 is a peak
    assert find_peak_element([1,2,1,3,5,6,4]) in [1, 5]  # Multiple peaks possible
    
    print("✅ Find Peak Element tests passed")
    
    # Test 2D matrix search
    matrix1 = [[1,4,7,11],[2,5,8,12],[3,6,9,16],[10,13,14,17]]
    assert search_2d_matrix_ii(matrix1, 5) == True
    assert search_2d_matrix_ii(matrix1, 20) == False
    
    matrix2 = [[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]]
    assert search_2d_matrix(matrix2, 5) == True
    assert search_2d_matrix(matrix2, 13) == True
    
    print("✅ 2D Matrix Search tests passed")
    
    # Test sqrt
    assert sqrt_binary_search(4) == 2
    assert sqrt_binary_search(8) == 2  # Floor of sqrt(8) = 2.828...
    assert sqrt_binary_search(1) == 1
    
    print("✅ Sqrt Binary Search tests passed")
    
    # Test shipping capacity
    assert capacity_to_ship_packages([1,2,3,4,5,6,7,8,9,10], 5) == 15
    assert capacity_to_ship_packages([3,2,2,4,1,4], 3) == 6
    
    print("✅ Ship Packages tests passed")
    
    # Test kth smallest in matrix
    matrix3 = [[1,5,9],[10,11,13],[12,13,15]]
    assert kth_smallest_in_matrix(matrix3, 8) == 13
    
    print("✅ Kth Smallest in Matrix tests passed")

if __name__ == "__main__":
    test_advanced_binary_search()
