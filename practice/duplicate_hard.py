from typing import List
from data import data_test


def containsNearbyAlmostDuplicate(
    nums: List[int], indexDiff: int, valueDiff: int
) -> bool:
    to = -(indexDiff) if indexDiff - len(nums) > 0 else -1
    for i, number in enumerate(nums[:to]):
        if any(abs(number - i) <= valueDiff for i in nums[i + 1 : i + indexDiff + 1]):
            return True

    return False


# def containsNearbyAlmostDuplicate(self, nums: List[int], indexDiff: int, valueDiff: int) -> bool:
#         to = -(indexDiff) if indexDiff - len(nums) > 0 else -1
#         for i, number in enumerate(nums[:to]):
#             for y, next_number in enumerate(nums[i+1: i + indexDiff + 1]):
#                 if abs(number - next_number) <= valueDiff:
#                     return True


#         return False

# assert containsNearbyAlmostDuplicate([1, 2, 3, 1], 3, 6) == True, "Test case 1 failed"

# assert (
#     containsNearbyAlmostDuplicate([1, 5, 9, 1, 5, 9], 2, 3) == False
# ), "Test case 2 failed"

# assert (
#     containsNearbyAlmostDuplicate([8, 7, 15, 1, 6, 1, 9, 15], 1, 3) == True
# ), "Test case 3 failed"

# assert containsNearbyAlmostDuplicate([-2, 3], 2, 5) == True, "Test case 4 failed"


assert containsNearbyAlmostDuplicate(data_test, 10000, 0) == False, "Test case 5 failed"
