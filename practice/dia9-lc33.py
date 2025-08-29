def search_insert_position(nums, target):
    """
    LeetCode 33: Search in Rotated Sorted Array
    PREGUNTA FRECUENTE EN ENTREVISTAS!
    """
    left, right = 0, len(nums) - 1

    while left <= right:
        search_index = left + (right - left) // 2

        print(f"Variables left:{left}, right:{right}, search_index:{search_index}")
        if nums[search_index] == target:
            print(f"Fount at {search_index}")
            return search_index

        # Ver que mitad esta ordenada
        print(
            f"Compara {nums[left:search_index + 1]} {nums[left]} <= {nums[search_index]}"
        )
        if nums[left] <= nums[search_index]:  # left side is ordered
            print(f"SI - Is target in {nums[left:search_index]}")
            if nums[left] <= target < nums[search_index]:
                right = search_index - 1
            else:
                left = search_index + 1
        else:
            print(f"NO - Is target in {nums[search_index: right]}")
            if nums[search_index] < target <= nums[right]:
                left = search_index + 1
            else:
                right = search_index - 1
    print("Not found")
    return -1


assert search_insert_position([4, 5, 6, 7, 0, 1, 2], 0) == 4
# assert search_insert_position([4, 5, 6, 7, 0, 1, 2], 5) == 1
# assert search_insert_position([4, 5, 6, 7, 0, 1, 2], 3) == -1
# assert search_insert_position([1], 0) == -1
# assert search_insert_position([5, 1, 3], 0) == -1
