def find_peak_element(nums):
    """
    Encuentra un pico en O(log n) tiempo.
    Un pico es un elemento mayor que sus vecinos.
    """

    def binary_search(left, right):
        if left == right:
            return left

        mid = (left + right) // 2

        # Si mid es menor que mid+1, el pico está a la derecha
        if nums[mid] < nums[mid + 1]:
            return binary_search(mid + 1, right)
        # Si no, el pico está a la izquierda (incluyendo mid)
        else:
            return binary_search(left, mid)

    return binary_search(0, len(nums) - 1)


# Test
nums = [1, 2, 1, 3, 5, 6, 4]
peak_idx = find_peak_element(nums)
print(f"Peak at index {peak_idx}, value: {nums[peak_idx]}")
