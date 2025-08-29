"""
LEETCODE HARD PROBLEMS - Sorting & Searching
Para demostrar mastery en entrevistas senior/staff level
"""

def median_of_two_sorted_arrays(nums1, nums2):
    """
    LeetCode 4: Median of Two Sorted Arrays (HARD)
    THE MOST ASKED HARD PROBLEM en FAANG interviews
    
    Challenge: O(log(min(m,n))) time complexity
    Key insight: Binary search en partitions, no en elements
    """
    # Ensure nums1 is the smaller array
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    
    m, n = len(nums1), len(nums2)
    left, right = 0, m
    
    while left <= right:
        partition_x = (left + right) // 2
        partition_y = (m + n + 1) // 2 - partition_x
        
        # Handle edge cases
        max_left_x = float('-inf') if partition_x == 0 else nums1[partition_x - 1]
        min_right_x = float('inf') if partition_x == m else nums1[partition_x]
        
        max_left_y = float('-inf') if partition_y == 0 else nums2[partition_y - 1]
        min_right_y = float('inf') if partition_y == n else nums2[partition_y]
        
        if max_left_x <= min_right_y and max_left_y <= min_right_x:
            # Found correct partition
            if (m + n) % 2 == 0:
                return (max(max_left_x, max_left_y) + min(min_right_x, min_right_y)) / 2
            else:
                return max(max_left_x, max_left_y)
        elif max_left_x > min_right_y:
            # Too far right in nums1
            right = partition_x - 1
        else:
            # Too far left in nums1
            left = partition_x + 1
    
    return -1  # Should never reach here

def smallest_range_covering_k_lists(nums):
    """
    LeetCode 632: Smallest Range Covering Elements from K Lists (HARD)
    
    Advanced: Merge K sorted lists concept + sliding window
    """
    import heapq
    
    # Min heap: (value, list_index, element_index)
    heap = []
    max_val = float('-inf')
    
    # Initialize heap with first element from each list
    for i in range(len(nums)):
        if nums[i]:
            heapq.heappush(heap, (nums[i][0], i, 0))
            max_val = max(max_val, nums[i][0])
    
    range_start, range_end = 0, float('inf')
    
    while len(heap) == len(nums):
        min_val, list_idx, elem_idx = heapq.heappop(heap)
        
        # Update range if current is smaller
        if max_val - min_val < range_end - range_start:
            range_start, range_end = min_val, max_val
        
        # Add next element from same list
        if elem_idx + 1 < len(nums[list_idx]):
            next_val = nums[list_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))
            max_val = max(max_val, next_val)
    
    return [range_start, range_end]

def reverse_pairs(nums):
    """
    LeetCode 493: Reverse Pairs (HARD)
    
    Count important reverse pairs: i < j and nums[i] > 2 * nums[j]
    
    Advanced: Modified merge sort with counting
    O(n log n) solution
    """
    def merge_sort_and_count(left, right):
        if left >= right:
            return 0
        
        mid = (left + right) // 2
        count = merge_sort_and_count(left, mid) + merge_sort_and_count(mid + 1, right)
        
        # Count reverse pairs across partitions
        j = mid + 1
        for i in range(left, mid + 1):
            while j <= right and nums[i] > 2 * nums[j]:
                j += 1
            count += j - (mid + 1)
        
        # Merge sorted arrays
        temp = []
        i, j = left, mid + 1
        
        while i <= mid and j <= right:
            if nums[i] <= nums[j]:
                temp.append(nums[i])
                i += 1
            else:
                temp.append(nums[j])
                j += 1
        
        while i <= mid:
            temp.append(nums[i])
            i += 1
        
        while j <= right:
            temp.append(nums[j])
            j += 1
        
        # Copy back
        for i in range(len(temp)):
            nums[left + i] = temp[i]
        
        return count
    
    return merge_sort_and_count(0, len(nums) - 1)

def count_smaller_after_self(nums):
    """
    LeetCode 315: Count of Smaller Numbers After Self (HARD)
    
    For each element, count how many smaller elements are to its right
    
    Advanced: Modified merge sort with index tracking
    """
    def merge_sort_with_count(enum_arr):
        half = len(enum_arr) // 2
        if half:
            left = merge_sort_with_count(enum_arr[:half])
            right = merge_sort_with_count(enum_arr[half:])
            
            i = j = 0
            # Count elements in right half smaller than left half
            for k in range(len(enum_arr)):
                if j == len(right) or (i < len(left) and left[i][1] <= right[j][1]):
                    enum_arr[k] = left[i]
                    counts[left[i][0]] += j  # j elements from right are smaller
                    i += 1
                else:
                    enum_arr[k] = right[j]
                    j += 1
        
        return enum_arr
    
    counts = [0] * len(nums)
    enum_arr = [(i, v) for i, v in enumerate(nums)]
    merge_sort_with_count(enum_arr)
    return counts

def split_array_largest_sum(nums, m):
    """
    LeetCode 410: Split Array Largest Sum (HARD)
    
    Binary search en answer space + greedy validation
    Classic "minimize the maximum" pattern
    """
    def can_split(max_sum):
        """Check if array can be split into m subarrays with max_sum limit"""
        splits = 1
        current_sum = 0
        
        for num in nums:
            if current_sum + num > max_sum:
                splits += 1
                current_sum = num
                if splits > m:
                    return False
            else:
                current_sum += num
        
        return True
    
    left = max(nums)  # Minimum possible answer
    right = sum(nums)  # Maximum possible answer
    
    while left < right:
        mid = left + (right - left) // 2
        
        if can_split(mid):
            right = mid
        else:
            left = mid + 1
    
    return left

def find_k_pairs_smallest_sums(nums1, nums2, k):
    """
    LeetCode 373: Find K Pairs with Smallest Sums (MEDIUM/HARD)
    
    Advanced heap usage + optimization
    """
    import heapq
    
    if not nums1 or not nums2:
        return []
    
    heap = []
    result = []
    visited = set()
    
    # Start with smallest pair
    heapq.heappush(heap, (nums1[0] + nums2[0], 0, 0))
    visited.add((0, 0))
    
    while heap and len(result) < k:
        sum_val, i, j = heapq.heappop(heap)
        result.append([nums1[i], nums2[j]])
        
        # Add adjacent pairs
        if i + 1 < len(nums1) and (i + 1, j) not in visited:
            heapq.heappush(heap, (nums1[i + 1] + nums2[j], i + 1, j))
            visited.add((i + 1, j))
        
        if j + 1 < len(nums2) and (i, j + 1) not in visited:
            heapq.heappush(heap, (nums1[i] + nums2[j + 1], i, j + 1))
            visited.add((i, j + 1))
    
    return result

def count_range_sum(nums, lower, upper):
    """
    LeetCode 327: Count of Range Sum (HARD)
    
    Count number of range sums in [lower, upper]
    
    Advanced: Merge sort + prefix sum
    """
    def merge_sort_and_count(prefix_sums, left, right):
        if left >= right:
            return 0
        
        mid = (left + right) // 2
        count = (merge_sort_and_count(prefix_sums, left, mid) + 
                merge_sort_and_count(prefix_sums, mid + 1, right))
        
        # Count range sums
        j = k = mid + 1
        for i in range(left, mid + 1):
            while j <= right and prefix_sums[j] - prefix_sums[i] < lower:
                j += 1
            while k <= right and prefix_sums[k] - prefix_sums[i] <= upper:
                k += 1
            count += k - j
        
        # Merge
        temp = []
        i, j = left, mid + 1
        
        while i <= mid and j <= right:
            if prefix_sums[i] <= prefix_sums[j]:
                temp.append(prefix_sums[i])
                i += 1
            else:
                temp.append(prefix_sums[j])
                j += 1
        
        while i <= mid:
            temp.append(prefix_sums[i])
            i += 1
        
        while j <= right:
            temp.append(prefix_sums[j])
            j += 1
        
        for i in range(len(temp)):
            prefix_sums[left + i] = temp[i]
        
        return count
    
    # Build prefix sums
    prefix_sums = [0]
    for num in nums:
        prefix_sums.append(prefix_sums[-1] + num)
    
    return merge_sort_and_count(prefix_sums, 0, len(prefix_sums) - 1)

# COMPREHENSIVE TESTING PARA HARD PROBLEMS
def test_hard_problems():
    """Testing all hard problems"""
    
    # Test median of two sorted arrays
    assert median_of_two_sorted_arrays([1, 3], [2]) == 2.0
    assert median_of_two_sorted_arrays([1, 2], [3, 4]) == 2.5
    assert median_of_two_sorted_arrays([0, 0], [0, 0]) == 0.0
    assert median_of_two_sorted_arrays([], [1]) == 1.0
    
    print("✅ Median of Two Sorted Arrays tests passed")
    
    # Test smallest range
    nums = [[4,10,15,24,26],[0,9,12,20],[5,18,22,30]]
    result = smallest_range_covering_k_lists(nums)
    assert result == [20, 24]  # Range [20,24] covers all lists
    
    print("✅ Smallest Range Covering tests passed")
    
    # Test reverse pairs
    assert reverse_pairs([1,3,2,3,1]) == 2
    assert reverse_pairs([2,4,3,5,1]) == 3
    
    print("✅ Reverse Pairs tests passed")
    
    # Test count smaller after self
    assert count_smaller_after_self([5,2,6,1]) == [2,1,1,0]
    assert count_smaller_after_self([-1]) == [0]
    assert count_smaller_after_self([-1,-1]) == [0,0]
    
    print("✅ Count Smaller After Self tests passed")
    
    # Test split array
    assert split_array_largest_sum([7,2,5,10,8], 2) == 18
    assert split_array_largest_sum([1,2,3,4,5], 2) == 9
    
    print("✅ Split Array Largest Sum tests passed")
    
    # Test k pairs with smallest sums
    result = find_k_pairs_smallest_sums([1,7,11], [2,4,6], 3)
    expected = [[1,2],[1,4],[1,6]]
    assert result == expected
    
    print("✅ Find K Pairs tests passed")
    
    # Test count range sum
    assert count_range_sum([-2,5,-1], -2, 2) == 3
    assert count_range_sum([0], 0, 0) == 1
    
    print("✅ Count Range Sum tests passed")

if __name__ == "__main__":
    test_hard_problems()
