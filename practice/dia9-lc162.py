from typing import List


def find_peak_element(nums: List[int]) -> int:
    """
    LeetCode 162: Find Peak Element
    Aplicación avanzada de binary search
    """
    if len(nums) == 1:
        return 0

    # for index in range(0, len(nums) - 1):  # on the worst scenario this in O(n)
    #     if nums[min(0, index - 1)] <= nums[index] > nums[index + 1]:
    #         return index

    # return len(nums) - 1

    l = 0
    r = len(nums) - 1
    while l < r:
        si = (l + r) // 2
        if nums[si] > nums[si + 1]:
            r = si
        else:
            l = si + 1

    return l

    arr = nums
    left, right = 0, len(arr) - 1

    while left < right:
        mid = left + (right - left) // 2

        if arr[mid] > arr[mid + 1]:
            right = mid
        else:
            left = mid + 1

    return left


assert find_peak_element([1, 2, 3, 1]) == 2, "test case 1"
# assert find_peak_element([1, 2, 1, 3, 5, 6, 4]) in [1, 5], "test case 2"  #
# assert find_peak_element([1]) == 0, "test case 3"  #
# assert find_peak_element([1, 2]) == 1, "test case 4"  #
# assert find_peak_element([2, 1]) == 0, f"test case 5: {find_peak_element([2, 1])}"  #
# assert (
#     find_peak_element([3, 2, 1]) == 0
# ), f"test case 6: {find_peak_element([3,2,1])}"  #
