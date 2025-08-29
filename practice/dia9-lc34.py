from typing import List


def searchRange(nums: List[int], target: int) -> List[int]:
    l, r = 0, len(nums)

    while l < r:
        m = l + (r - l) // 2

        if nums[m] < target:
            l = m + 1
        else:
            r = m

    start = l if l < len(nums) and nums[l] == target else -1

    l, r = 0, len(nums)
    while l < r:
        m = l + (r - l) // 2

        if nums[m] <= target:
            l = m + 1
        else:
            r = m

    last = l - 1 if l > 0 and nums[l - 1] == target else -1

    return [start, last]


assert searchRange([5, 7, 7, 8, 8, 10], 8) == [3, 4]
assert searchRange([5, 7, 7, 8, 8, 10], 6) == [-1, -1]
assert searchRange([], 6) == [-1, -1]
assert searchRange([5, 7, 7, 8, 8, 10], 5) == [0, 0]
