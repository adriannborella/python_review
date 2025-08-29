"""
QUICK SELECT ALGORITHM
Para encontrar Kth largest/smallest element sin ordenar todo el array

Key insight: Modificación de QuickSort que solo procesa una partición
Average: O(n), Worst: O(n²), pero mucho más rápido que sorting O(n log n)
"""

import random

def quickselect(nums, k):
    """
    Find Kth largest element (1-indexed)
    
    LeetCode 215: Kth Largest Element in Array (MEDIUM)
    Extremely common en entrevistas FAANG
    """
    def partition(left, right, pivot_index):
        """Lomuto partition - move pivot to end, then partition"""
        pivot_value = nums[pivot_index]
        # Move pivot to end
        nums[pivot_index], nums[right] = nums[right], nums[pivot_index]
        
        store_index = left
        for i in range(left, right):
            if nums[i] < pivot_value:
                nums[store_index], nums[i] = nums[i], nums[store_index]
                store_index += 1
        
        # Move pivot to final place
        nums[right], nums[store_index] = nums[store_index], nums[right]
        return store_index
    
    def quickselect_helper(left, right, k_smallest):
        """
        Returns kth smallest element in nums[left:right+1]
        """
        if left == right:
            return nums[left]
        
        # Random pivot para evitar worst case O(n²)
        pivot_index = random.randint(left, right)
        pivot_index = partition(left, right, pivot_index)
        
        if k_smallest == pivot_index:
            return nums[k_smallest]
        elif k_smallest < pivot_index:
            return quickselect_helper(left, pivot_index - 1, k_smallest)
        else:
            return quickselect_helper(pivot_index + 1, right, k_smallest)
    
    # Convert to 0-indexed: kth largest = (n-k)th smallest
    return quickselect_helper(0, len(nums) - 1, len(nums) - k)

def quickselect_iterative(nums, k):
    """
    Iterative version - avoids recursion stack overflow
    Often preferred in interviews para large datasets
    """
    def partition(left, right, pivot_index):
        pivot_value = nums[pivot_index]
        nums[pivot_index], nums[right] = nums[right], nums[pivot_index]
        
        store_index = left
        for i in range(left, right):
            if nums[i] < pivot_value:
                nums[store_index], nums[i] = nums[i], nums[store_index]
                store_index += 1
        
        nums[right], nums[store_index] = nums[store_index], nums[right]
        return store_index
    
    left, right = 0, len(nums) - 1
    k_smallest = len(nums) - k  # Convert to smallest
    
    while left <= right:
        pivot_index = random.randint(left, right)
        pivot_index = partition(left, right, pivot_index)
        
        if k_smallest == pivot_index:
            return nums[k_smallest]
        elif k_smallest < pivot_index:
            right = pivot_index - 1
        else:
            left = pivot_index + 1
    
    return -1  # Should never reach here

def find_kth_smallest(nums, k):
    """
    Find Kth smallest element (1-indexed)
    Complementary function para completeness
    """
    def partition(left, right, pivot_index):
        pivot_value = nums[pivot_index]
        nums[pivot_index], nums[right] = nums[right], nums[pivot_index]
        
        store_index = left
        for i in range(left, right):
            if nums[i] < pivot_value:
                nums[store_index], nums[i] = nums[i], nums[store_index]
                store_index += 1
        
        nums[right], nums[store_index] = nums[store_index], nums[right]
        return store_index
    
    def select(left, right, k_smallest):
        if left == right:
            return nums[left]
        
        pivot_index = random.randint(left, right)
        pivot_index = partition(left, right, pivot_index)
        
        if k_smallest == pivot_index:
            return nums[k_smallest]
        elif k_smallest < pivot_index:
            return select(left, pivot_index - 1, k_smallest)
        else:
            return select(pivot_index + 1, right, k_smallest)
    
    return select(0, len(nums) - 1, k - 1)  # Convert to 0-indexed

def top_k_frequent(nums, k):
    """
    LeetCode 347: Top K Frequent Elements (MEDIUM)
    Application de quickselect en frequency counting
    """
    from collections import Counter
    
    # Count frequencies
    count = Counter(nums)
    unique = list(count.keys())
    
    def partition(left, right, pivot_index):
        pivot_frequency = count[unique[pivot_index]]
        unique[pivot_index], unique[right] = unique[right], unique[pivot_index]
        
        store_index = left
        for i in range(left, right):
            if count[unique[i]] < pivot_frequency:
                unique[store_index], unique[i] = unique[i], unique[store_index]
                store_index += 1
        
        unique[right], unique[store_index] = unique[store_index], unique[right]
        return store_index
    
    def quickselect_freq(left, right, k_smallest):
        if left == right:
            return
        
        pivot_index = random.randint(left, right)
        pivot_index = partition(left, right, pivot_index)
        
        if k_smallest == pivot_index:
            return
        elif k_smallest < pivot_index:
            quickselect_freq(left, pivot_index - 1, k_smallest)
        else:
            quickselect_freq(pivot_index + 1, right, k_smallest)
    
    n = len(unique)
    quickselect_freq(0, n - 1, n - k)
    return unique[n - k:]

def wiggle_sort_ii(nums):
    """
    LeetCode 324: Wiggle Sort II (MEDIUM/HARD)
    Advanced application: nums[0] < nums[1] > nums[2] < nums[3]...
    
    Uses quickselect to find median, then three-way partitioning
    """
    def find_median():
        """Find median using quickselect"""
        temp = nums[:]
        n = len(temp)
        
        def partition(left, right, pivot_idx):
            pivot = temp[pivot_idx]
            temp[pivot_idx], temp[right] = temp[right], temp[pivot_idx]
            
            store_idx = left
            for i in range(left, right):
                if temp[i] < pivot:
                    temp[store_idx], temp[i] = temp[i], temp[store_idx]
                    store_idx += 1
            
            temp[right], temp[store_idx] = temp[store_idx], temp[right]
            return store_idx
        
        def select(left, right, k):
            if left == right:
                return temp[left]
            
            pivot_idx = random.randint(left, right)
            pivot_idx = partition(left, right, pivot_idx)
            
            if k == pivot_idx:
                return temp[k]
            elif k < pivot_idx:
                return select(left, pivot_idx - 1, k)
            else:
                return select(pivot_idx + 1, right, k)
        
        return select(0, n - 1, (n - 1) // 2)
    
    n = len(nums)
    median = find_median()
    
    # Virtual indexing para three-way partitioning
    # Maps indices: 0->1, 1->3, 2->5, 3->0, 4->2, 5->4
    def new_index(i):
        return (1 + 2 * i) % (n | 1)
    
    # Three-way partitioning with virtual indexing
    i = j = 0
    k = n - 1
    
    while j <= k:
        if nums[new_index(j)] > median:
            nums[new_index(i)], nums[new_index(j)] = nums[new_index(j)], nums[new_index(i)]
            i += 1
            j += 1
        elif nums[new_index(j)] < median:
            nums[new_index(j)], nums[new_index(k)] = nums[new_index(k)], nums[new_index(j)]
            k -= 1
        else:
            j += 1

# COMPREHENSIVE TESTING
def test_quickselect():
    """Testing todas las variaciones de quickselect"""
    
    # Test básico kth largest
    nums1 = [3,2,1,5,6,4]
    assert quickselect(nums1.copy(), 2) == 5  # 2nd largest
    assert quickselect_iterative(nums1.copy(), 2) == 5
    
    nums2 = [3,2,3,1,2,4,5,5,6]
    assert quickselect(nums2.copy(), 4) == 4  # 4th largest
    
    print("✅ Quickselect Kth Largest tests passed")
    
    # Test kth smallest
    nums3 = [7,10,4,3,20,15]
    assert find_kth_smallest(nums3.copy(), 3) == 7  # 3rd smallest
    
    print("✅ Quickselect Kth Smallest tests passed")
    
    # Test top k frequent
    nums4 = [1,1,1,2,2,3]
    result = top_k_frequent(nums4, 2)
    assert set(result) == {1, 2}  # Order might vary
    
    nums5 = [1]
    assert top_k_frequent(nums5, 1) == [1]
    
    print("✅ Top K Frequent tests passed")
    
    # Test wiggle sort
    nums6 = [1,5,1,1,6,4]
    wiggle_sort_ii(nums6)
    
    # Verify wiggle property
    for i in range(1, len(nums6)):
        if i % 2 == 1:  # Odd indices should be peaks
            assert nums6[i] >= nums6[i-1]
            if i + 1 < len(nums6):
                assert nums6[i] >= nums6[i+1]
    
    print("✅ Wiggle Sort II tests passed")

if __name__ == "__main__":
    test_quickselect()
