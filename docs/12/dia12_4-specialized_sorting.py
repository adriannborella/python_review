"""
NON-COMPARISON BASED SORTING ALGORITHMS
Para casos específicos donde podemos hacer mejor que O(n log n)

Key insight: Cuando conocemos el range de datos, podemos usar linear sorting
"""

def counting_sort(arr, max_val=None):
    """
    Counting Sort: O(n + k) donde k es el range de valores
    
    Perfect para:
    - Small range of integers (k << n log n)
    - Cuando necesitas stable sorting
    - Como subroutine para radix sort
    
    Limitations:
    - Solo funciona con integers
    - Requiere conocer el range
    - Space complexity O(k)
    """
    if not arr:
        return []
    
    if max_val is None:
        max_val = max(arr)
    
    min_val = min(arr)
    range_val = max_val - min_val + 1
    
    # Count occurrences
    count = [0] * range_val
    for num in arr:
        count[num - min_val] += 1
    
    # Calculate cumulative counts (for stable sorting)
    for i in range(1, range_val):
        count[i] += count[i - 1]
    
    # Build result array
    result = [0] * len(arr)
    for i in range(len(arr) - 1, -1, -1):  # Traverse backwards for stability
        result[count[arr[i] - min_val] - 1] = arr[i]
        count[arr[i] - min_val] -= 1
    
    return result

def counting_sort_for_radix(arr, exp):
    """
    Modified counting sort para radix sort
    Sort by digit at position exp (1, 10, 100, etc.)
    """
    n = len(arr)
    output = [0] * n
    count = [0] * 10  # Digits 0-9
    
    # Count occurrences of each digit
    for i in range(n):
        index = arr[i] // exp
        count[index % 10] += 1
    
    # Calculate cumulative counts
    for i in range(1, 10):
        count[i] += count[i - 1]
    
    # Build output array
    i = n - 1
    while i >= 0:
        index = arr[i] // exp
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1
    
    # Copy output array to arr
    for i in range(n):
        arr[i] = output[i]

def radix_sort(arr):
    """
    Radix Sort: O(d * (n + k)) donde d = número de digits, k = base (10)
    
    For integers: O(n log(max_value))
    Often better than O(n log n) comparison sorts para large datasets
    
    Applications:
    - Sorting large integers
    - String sorting (with modification)
    - Suffix array construction
    """
    if not arr:
        return []
    
    arr = arr.copy()  # Don't modify original
    
    # Find maximum number to know number of digits
    max_num = max(arr)
    
    # Do counting sort for every digit
    exp = 1
    while max_num // exp > 0:
        counting_sort_for_radix(arr, exp)
        exp *= 10
    
    return arr

def bucket_sort(arr, num_buckets=10):
    """
    Bucket Sort: O(n + k) average case, O(n²) worst case
    
    Best para:
    - Uniformly distributed floating point numbers in range [0, 1)
    - When input is distributed across range
    
    Algorithm:
    1. Distribute elements into buckets
    2. Sort individual buckets
    3. Concatenate buckets
    """
    if not arr:
        return []
    
    # Normalize to [0, 1) range
    max_val = max(arr)
    min_val = min(arr)
    range_val = max_val - min_val
    
    if range_val == 0:
        return arr  # All elements are same
    
    # Create buckets
    buckets = [[] for _ in range(num_buckets)]
    
    # Distribute elements into buckets
    for num in arr:
        # Normalize and find bucket index
        normalized = (num - min_val) / range_val
        bucket_idx = min(int(normalized * num_buckets), num_buckets - 1)
        buckets[bucket_idx].append(num)
    
    # Sort individual buckets and concatenate
    result = []
    for bucket in buckets:
        if bucket:
            bucket.sort()  # Use comparison sort for small buckets
            result.extend(bucket)
    
    return result

def sort_colors_radix(nums):
    """
    LeetCode 75: Sort Colors using Radix Sort approach
    Overkill para 3 colors, pero demuestra versatility
    """
    if not nums:
        return
    
    # Since we only have 3 colors (0, 1, 2), direct counting is better
    count = [0, 0, 0]
    
    for num in nums:
        count[num] += 1
    
    idx = 0
    for color in range(3):
        for _ in range(count[color]):
            nums[idx] = color
            idx += 1

def sort_array_by_parity(arr):
    """
    LeetCode 905: Sort Array By Parity
    Using counting sort concept
    """
    evens = []
    odds = []
    
    for num in arr:
        if num % 2 == 0:
            evens.append(num)
        else:
            odds.append(num)
    
    return evens + odds

def relative_sort_array(arr1, arr2):
    """
    LeetCode 1122: Relative Sort Array
    Perfect application de counting sort
    """
    # Count elements in arr1
    count = {}
    for num in arr1:
        count[num] = count.get(num, 0) + 1
    
    result = []
    
    # Add elements in order of arr2
    for num in arr2:
        if num in count:
            result.extend([num] * count[num])
            del count[num]
    
    # Add remaining elements in sorted order
    remaining = []
    for num in count:
        remaining.extend([num] * count[num])
    remaining.sort()
    
    return result + remaining

def maximum_gap(nums):
    """
    LeetCode 164: Maximum Gap (HARD)
    Must solve in O(n) time and O(n) space
    
    Key insight: Use radix sort, then find max gap
    """
    if len(nums) < 2:
        return 0
    
    # Radix sort
    sorted_nums = radix_sort(nums)
    
    # Find maximum gap
    max_gap = 0
    for i in range(1, len(sorted_nums)):
        gap = sorted_nums[i] - sorted_nums[i - 1]
        max_gap = max(max_gap, gap)
    
    return max_gap

def maximum_gap_bucket_sort(nums):
    """
    Alternative solution using bucket sort approach
    More elegant para este specific problem
    """
    if len(nums) < 2:
        return 0
    
    n = len(nums)
    min_val = min(nums)
    max_val = max(nums)
    
    if min_val == max_val:
        return 0
    
    # Bucket size: ceiling division
    bucket_size = max(1, (max_val - min_val) // (n - 1))
    bucket_count = (max_val - min_val) // bucket_size + 1
    
    # Each bucket stores [min_in_bucket, max_in_bucket]
    buckets = [[float('inf'), float('-inf')] for _ in range(bucket_count)]
    
    # Place numbers in buckets
    for num in nums:
        bucket_idx = (num - min_val) // bucket_size
        buckets[bucket_idx][0] = min(buckets[bucket_idx][0], num)
        buckets[bucket_idx][1] = max(buckets[bucket_idx][1], num)
    
    # Find maximum gap between buckets
    max_gap = 0
    prev_max = min_val
    
    for min_in_bucket, max_in_bucket in buckets:
        if min_in_bucket == float('inf'):
            continue  # Empty bucket
        
        max_gap = max(max_gap, min_in_bucket - prev_max)
        prev_max = max_in_bucket
    
    return max_gap

# PERFORMANCE COMPARISON
def compare_sorting_algorithms():
    """
    Performance comparison para different scenarios
    
    Para interviewer questions sobre cuándo usar cada algoritmo
    """
    import time
    import random
    
    # Generate test data
    small_range = [random.randint(0, 100) for _ in range(10000)]
    large_range = [random.randint(0, 1000000) for _ in range(10000)]
    
    print("🔥 Sorting Algorithm Performance Comparison")
    print("=" * 50)
    
    # Test counting sort on small range
    start = time.time()
    counting_sort(small_range.copy())
    counting_time = time.time() - start
    print(f"Counting Sort (small range): {counting_time:.4f}s")
    
    # Test radix sort
    start = time.time()
    radix_sort(large_range.copy())
    radix_time = time.time() - start
    print(f"Radix Sort (large range): {radix_time:.4f}s")
    
    # Compare with Python's built-in sort
    start = time.time()
    sorted(large_range)
    builtin_time = time.time() - start
    print(f"Python built-in sort: {builtin_time:.4f}s")
    
    print(f"\nRadix vs Built-in ratio: {radix_time / builtin_time:.2f}")

def test_specialized_sorting():
    """Comprehensive testing"""
    
    # Test counting sort
    arr1 = [4, 2, 2, 8, 3, 3, 1]
    result1 = counting_sort(arr1)
    assert result1 == [1, 2, 2, 3, 3, 4, 8]
    
    # Test with negative numbers
    arr2 = [4, -1, 2, -3, 0]
    result2 = counting_sort(arr2)
    assert result2 == [-3, -1, 0, 2, 4]
    
    print("✅ Counting Sort tests passed")
    
    # Test radix sort
    arr3 = [170, 45, 75, 90, 2, 802, 24, 66]
    result3 = radix_sort(arr3)
    assert result3 == [2, 24, 45, 66, 75, 90, 170, 802]
    
    print("✅ Radix Sort tests passed")
    
    # Test bucket sort
    arr4 = [0.897, 0.565, 0.656, 0.1234, 0.665, 0.3434]
    result4 = bucket_sort(arr4)
    assert result4 == sorted(arr4)
    
    print("✅ Bucket Sort tests passed")
    
    # Test maximum gap
    nums1 = [3, 6, 9, 1]
    assert maximum_gap(nums1) == 3
    assert maximum_gap_bucket_sort(nums1) == 3
    
    nums2 = [10]
    assert maximum_gap(nums2) == 0
    
    print("✅ Maximum Gap tests passed")
    
    # Test relative sort
    arr1 = [2,3,1,3,2,4,6,7,9,2,19]
    arr2 = [2,1,4,3,9,6]
    expected = [2,2,2,1,4,3,3,9,6,7,19]
    assert relative_sort_array(arr1, arr2) == expected
    
    print("✅ Relative Sort tests passed")

if __name__ == "__main__":
    test_specialized_sorting()
    # compare_sorting_algorithms()  # Uncomment para performance analysis