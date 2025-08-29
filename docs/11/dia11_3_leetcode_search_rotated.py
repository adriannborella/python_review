"""
LeetCode 33: Search in Rotated Sorted Array (MEDIUM)
Problema MUY COMÚN en entrevistas de FAANG

Given: [4,5,6,7,0,1,2], target = 0
Output: 4

Challenge: O(log n) time complexity
"""

def search_rotated_array(nums, target):
    """
    Approach: Modified Binary Search
    Key insight: En cualquier punto, al menos una mitad está ordenada
    
    Time: O(log n)
    Space: O(1)
    """
    if not nums:
        return -1
    
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        # Found target
        if nums[mid] == target:
            return mid
        
        # Determinar cuál mitad está ordenada
        if nums[left] <= nums[mid]:  # Left half is sorted
            # Check if target is in left half
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:  # Right half is sorted
            # Check if target is in right half
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    
    return -1

def find_minimum_rotated(nums):
    """
    LeetCode 153: Find Minimum in Rotated Sorted Array
    Extensión natural del problema anterior
    """
    left, right = 0, len(nums) - 1
    
    while left < right:
        mid = left + (right - left) // 2
        
        if nums[mid] > nums[right]:
            # Minimum is in right half
            left = mid + 1
        else:
            # Minimum is in left half (including mid)
            right = mid
    
    return nums[left]

def search_range(nums, target):
    """
    LeetCode 34: Find First and Last Position of Element
    Combina binary search variations que implementamos antes
    """
    def find_first(nums, target):
        left, right = 0, len(nums)
        while left < right:
            mid = left + (right - left) // 2
            if nums[mid] < target:
                left = mid + 1
            else:
                right = mid
        return left
    
    def find_last(nums, target):
        left, right = 0, len(nums)
        while left < right:
            mid = left + (right - left) // 2
            if nums[mid] <= target:
                left = mid + 1
            else:
                right = mid
        return left - 1
    
    first = find_first(nums, target)
    if first == len(nums) or nums[first] != target:
        return [-1, -1]
    
    last = find_last(nums, target)
    return [first, last]

# TESTS COMPREHENSIVOS
def test_rotated_search():
    # Test cases del problema original
    assert search_rotated_array([4,5,6,7,0,1,2], 0) == 4
    assert search_rotated_array([4,5,6,7,0,1,2], 3) == -1
    assert search_rotated_array([1], 0) == -1
    
    # Edge cases
    assert search_rotated_array([1], 1) == 0
    assert search_rotated_array([1,3], 3) == 1
    
    # No rotation
    assert search_rotated_array([1,2,3,4,5], 3) == 2
    
    print("✅ Search Rotated Array tests passed")
    
    # Test minimum finding
    assert find_minimum_rotated([3,4,5,1,2]) == 1
    assert find_minimum_rotated([4,5,6,7,0,1,2]) == 0
    assert find_minimum_rotated([1]) == 1
    
    print("✅ Find Minimum tests passed")
    
    # Test range finding
    assert search_range([5,7,7,8,8,10], 8) == [3, 4]
    assert search_range([5,7,7,8,8,10], 6) == [-1, -1]
    assert search_range([], 0) == [-1, -1]
    
    print("✅ Search Range tests passed")

if __name__ == "__main__":
    test_rotated_search()
