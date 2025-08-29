"""
ARRAYS AVANZADOS - Manipulaciones y Optimizaciones
Para entrevistas senior: no solo usar arrays, sino optimizar y implementar desde cero
"""

class DynamicArray:
    """
    Dynamic Array implementation desde cero
    Similar a Python's list o C++ vector
    
    Key concepts: Amortized O(1) append, resizing strategy
    """
    def __init__(self, initial_capacity=4):
        self.capacity = initial_capacity
        self.size = 0
        self.data = [None] * self.capacity
    
    def __len__(self):
        return self.size
    
    def __getitem__(self, index):
        if not (0 <= index < self.size):
            raise IndexError("Index out of range")
        return self.data[index]
    
    def __setitem__(self, index, value):
        if not (0 <= index < self.size):
            raise IndexError("Index out of range")
        self.data[index] = value
    
    def _resize(self):
        """Double the capacity when needed - Amortized O(1)"""
        old_capacity = self.capacity
        self.capacity *= 2
        new_data = [None] * self.capacity
        
        for i in range(self.size):
            new_data[i] = self.data[i]
        
        self.data = new_data
        print(f"Resized from {old_capacity} to {self.capacity}")
    
    def append(self, value):
        """Amortized O(1) - occasionally O(n) for resize"""
        if self.size >= self.capacity:
            self._resize()
        
        self.data[self.size] = value
        self.size += 1
    
    def pop(self, index=-1):
        """Remove and return element at index"""
        if self.size == 0:
            raise IndexError("Pop from empty array")
        
        if index == -1:
            index = self.size - 1
        
        if not (0 <= index < self.size):
            raise IndexError("Index out of range")
        
        value = self.data[index]
        
        # Shift elements left
        for i in range(index, self.size - 1):
            self.data[i] = self.data[i + 1]
        
        self.size -= 1
        self.data[self.size] = None  # Clear reference
        
        # Shrink if too empty (optional optimization)
        if self.size <= self.capacity // 4 and self.capacity > 4:
            self._shrink()
        
        return value
    
    def _shrink(self):
        """Shrink capacity to save memory"""
        self.capacity //= 2
        new_data = [None] * self.capacity
        for i in range(self.size):
            new_data[i] = self.data[i]
        self.data = new_data
    
    def insert(self, index, value):
        """Insert value at index - O(n) due to shifting"""
        if not (0 <= index <= self.size):
            raise IndexError("Index out of range")
        
        if self.size >= self.capacity:
            self._resize()
        
        # Shift elements right
        for i in range(self.size, index, -1):
            self.data[i] = self.data[i - 1]
        
        self.data[index] = value
        self.size += 1
    
    def __str__(self):
        return str([self.data[i] for i in range(self.size)])

def two_sum(nums, target):
    """
    LeetCode 1: Two Sum (EASY pero fundamental)
    
    Multiple approaches para demonstrate array mastery
    """
    # Approach 1: Hash Map - O(n) time, O(n) space
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

def three_sum(nums):
    """
    LeetCode 15: 3Sum (MEDIUM)
    
    Two pointers technique - classic array manipulation
    """
    nums.sort()
    result = []
    n = len(nums)
    
    for i in range(n - 2):
        # Skip duplicates for first element
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        left, right = i + 1, n - 1
        
        while left < right:
            current_sum = nums[i] + nums[left] + nums[right]
            
            if current_sum < 0:
                left += 1
            elif current_sum > 0:
                right -= 1
            else:
                result.append([nums[i], nums[left], nums[right]])
                
                # Skip duplicates
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
    
    return result

def container_with_most_water(height):
    """
    LeetCode 11: Container With Most Water (MEDIUM)
    
    Two pointers optimization - greedy approach
    """
    left, right = 0, len(height) - 1
    max_area = 0
    
    while left < right:
        # Area limited by shorter line
        width = right - left
        area = min(height[left], height[right]) * width
        max_area = max(max_area, area)
        
        # Move pointer of shorter line (greedy choice)
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return max_area

def trapping_rain_water(height):
    """
    LeetCode 42: Trapping Rain Water (HARD)
    
    Multiple approaches - demonstrate algorithmic thinking
    """
    if not height:
        return 0
    
    # Approach 1: Two pointers - O(n) time, O(1) space
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    water = 0
    
    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                water += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                water += right_max - height[right]
            right -= 1
    
    return water

def max_subarray_sum(nums):
    """
    LeetCode 53: Maximum Subarray (MEDIUM)
    
    Kadane's Algorithm - classic DP on arrays
    """
    if not nums:
        return 0
    
    max_sum = current_sum = nums[0]
    
    for i in range(1, len(nums)):
        # Either extend current subarray or start new one
        current_sum = max(nums[i], current_sum + nums[i])
        max_sum = max(max_sum, current_sum)
    
    return max_sum

def product_except_self(nums):
    """
    LeetCode 238: Product of Array Except Self (MEDIUM)
    
    Constraint: No division allowed, O(1) extra space
    Clever use of result array para left/right products
    """
    n = len(nums)
    result = [1] * n
    
    # Left products
    for i in range(1, n):
        result[i] = result[i - 1] * nums[i - 1]
    
    # Right products (using single variable)
    right_product = 1
    for i in range(n - 1, -1, -1):
        result[i] *= right_product
        right_product *= nums[i]
    
    return result

def rotate_array(nums, k):
    """
    LeetCode 189: Rotate Array (MEDIUM)
    
    Multiple approaches - in-place rotation
    """
    n = len(nums)
    k = k % n  # Handle k > n
    
    # Approach: Reverse technique - O(n) time, O(1) space
    def reverse(arr, start, end):
        while start < end:
            arr[start], arr[end] = arr[end], arr[start]
            start += 1
            end -= 1
    
    # Reverse entire array
    reverse(nums, 0, n - 1)
    # Reverse first k elements
    reverse(nums, 0, k - 1)
    # Reverse remaining elements
    reverse(nums, k, n - 1)

# COMPREHENSIVE TESTING
def test_advanced_arrays():
    """Testing all array implementations and algorithms"""
    
    # Test Dynamic Array
    arr = DynamicArray()
    for i in range(10):
        arr.append(i)
    
    assert len(arr) == 10
    assert arr[5] == 5
    assert arr.pop() == 9
    assert len(arr) == 9
    
    arr.insert(0, -1)
    assert arr[0] == -1
    assert len(arr) == 10
    
    print("✅ Dynamic Array implementation tests passed")
    
    # Test Two Sum
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    assert two_sum([3, 2, 4], 6) == [1, 2]
    
    print("✅ Two Sum tests passed")
    
    # Test Three Sum
    result = three_sum([-1, 0, 1, 2, -1, -4])
    expected = [[-1, -1, 2], [-1, 0, 1]]
    assert result == expected
    
    print("✅ Three Sum tests passed")
    
    # Test Container With Most Water
    assert container_with_most_water([1,8,6,2,5,4,8,3,7]) == 49
    
    print("✅ Container With Most Water tests passed")
    
    # Test Trapping Rain Water
    assert trapping_rain_water([0,1,0,2,1,0,1,3,2,1,2,1]) == 6
    assert trapping_rain_water([4,2,0,3,2,5]) == 9
    
    print("✅ Trapping Rain Water tests passed")
    
    # Test Maximum Subarray
    assert max_subarray_sum([-2,1,-3,4,-1,2,1,-5,4]) == 6
    assert max_subarray_sum([1]) == 1
    assert max_subarray_sum([5,4,-1,7,8]) == 23
    
    print("✅ Maximum Subarray tests passed")
    
    # Test Product Except Self
    assert product_except_self([1,2,3,4]) == [24,12,8,6]
    assert product_except_self([-1,1,0,-3,3]) == [0,0,9,0,0]
    
    print("✅ Product Except Self tests passed")
    
    # Test Rotate Array
    nums = [1,2,3,4,5,6,7]
    rotate_array(nums, 3)
    assert nums == [5,6,7,1,2,3,4]
    
    print("✅ Rotate Array tests passed")

if __name__ == "__main__":
    test_advanced_arrays()
