def search_insert_position(arr, target):
    """
    LeetCode 35: Search Insert Position
    Encuentra dónde insertar target para mantener orden
    """
    l, r = 0, len(arr)

    while l < r:
        m = l + (r - l) // 2

        if arr[m] == target:
            return m
        else:
            if arr[m] < target:
                l = m + 1
            else:
                r = m

    return l


# assert search_insert_position([1, 3, 5, 6], 5) == 2
# assert search_insert_position([1, 3, 5, 6], 2) == 1
# assert search_insert_position([1, 3, 5, 6], 7) == 4
# assert search_insert_position([], 7) == 0
# assert search_insert_position([1], 7) == 1
# assert search_insert_position([8], 7) == 0
assert search_insert_position([1, 3], 2) == 1
