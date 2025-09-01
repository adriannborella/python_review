"""
BINARY SEARCH - Implementaciones Completas para Entrevistas
Día 9 - Preparación Entrevistas Python
"""


def binary_search_basic(arr, target):
    """
    Binary Search Básico
    Tiempo: O(log n), Espacio: O(1)
    """
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = left + (right - left) // 2  # Evita overflow

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


def binary_search_leftmost(arr, target):
    """
    Encuentra la primera ocurrencia del target
    Crucial para problemas con duplicados
    """
    left, right = 0, len(arr)

    while left < right:
        mid = left + (right - left) // 2

        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid

    return left if left < len(arr) and arr[left] == target else -1


def binary_search_rightmost(arr, target):
    """
    Encuentra la última ocurrencia del target
    """
    left, right = 0, len(arr)

    while left < right:
        mid = left + (right - left) // 2

        if arr[mid] <= target:
            left = mid + 1
        else:
            right = mid

    return left - 1 if left > 0 and arr[left - 1] == target else -1


def search_insert_position(arr, target):
    """
    LeetCode 35: Search Insert Position
    Encuentra dónde insertar target para mantener orden
    """
    left, right = 0, len(arr)

    while left < right:
        mid = left + (right - left) // 2

        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid

    return left


def search_rotated_array(arr, target):
    """
    LeetCode 33: Search in Rotated Sorted Array
    PREGUNTA FRECUENTE EN ENTREVISTAS!
    """
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if arr[mid] == target:
            return mid

        # Determinar qué mitad está ordenada
        if arr[left] <= arr[mid]:  # Mitad izquierda ordenada
            if arr[left] <= target < arr[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:  # Mitad derecha ordenada
            if arr[mid] < target <= arr[right]:
                left = mid + 1
            else:
                right = mid - 1

    return -1


def find_peak_element(arr):
    """
    LeetCode 162: Find Peak Element
    Aplicación avanzada de binary search
    """
    left, right = 0, len(arr) - 1

    while left < right:
        mid = left + (right - left) // 2

        if arr[mid] > arr[mid + 1]:
            right = mid
        else:
            left = mid + 1

    return left


def search_2d_matrix(matrix, target):
    """
    LeetCode 74: Search 2D Matrix
    Binary search en matriz ordenada
    """
    if not matrix or not matrix[0]:
        return False

    rows, cols = len(matrix), len(matrix[0])
    left, right = 0, rows * cols - 1

    while left <= right:
        mid = left + (right - left) // 2
        mid_value = matrix[mid // cols][mid % cols]

        if mid_value == target:
            return True
        elif mid_value < target:
            left = mid + 1
        else:
            right = mid - 1

    return False


# ALGORITMOS DE ORDENAMIENTO - Implementaciones Optimizadas


# https://www.youtube.com/shorts/y2AghjB4Wxs
def bubble_sort(arr):
    """
    Bubble Sort con optimización early termination
    Mejor caso: O(n), Peor caso: O(n²)
    """
    n = len(arr)

    for i in range(n):
        swapped = False

        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        if not swapped:  # Array ya ordenado
            break

    return arr


# https://www.youtube.com/shorts/QFrgq60Y6mw
def merge_sort(arr):
    """
    Merge Sort - Divide y vencerás
    Tiempo: O(n log n), Espacio: O(n)
    ESTABLE y predecible
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)


def merge(left, right):
    """Helper para merge sort"""
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:  # <= mantiene estabilidad
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


# https://www.youtube.com/shorts/j0Dp9H5ogno
# https://www.youtube.com/shorts/gptBZml12lU
def quick_sort(arr):
    """
    Quick Sort - In-place implementation
    Mejor/Promedio: O(n log n), Peor: O(n²)
    """

    def quick_sort_helper(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)
            quick_sort_helper(arr, low, pi - 1)
            quick_sort_helper(arr, pi + 1, high)

    quick_sort_helper(arr, 0, len(arr) - 1)
    return arr


def partition(arr, low, high):
    """
    Partición Lomuto para Quick Sort
    Más fácil de recordar en entrevistas
    """
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quick_sort_random_pivot(arr):
    """
    Quick Sort con pivot aleatorio
    Reduce probabilidad de O(n²)
    """
    import random

    def partition_random(arr, low, high):
        random_index = random.randint(low, high)
        arr[random_index], arr[high] = arr[high], arr[random_index]
        return partition(arr, low, high)

    def quick_sort_helper(arr, low, high):
        if low < high:
            pi = partition_random(arr, low, high)
            quick_sort_helper(arr, low, pi - 1)
            quick_sort_helper(arr, pi + 1, high)

    quick_sort_helper(arr, 0, len(arr) - 1)
    return arr


# TESTS Y EJEMPLOS DE USO


def test_all_algorithms():
    """Tests comprehensivos para todos los algoritmos"""

    # Test data
    test_cases = [
        [],
        [1],
        [3, 1, 4, 1, 5, 9, 2, 6],
        [1, 1, 1, 1],
        [5, 4, 3, 2, 1],
        list(range(1000, 0, -1)),  # Peor caso para quick sort
    ]

    print("=== TESTING BINARY SEARCH ===")
    sorted_arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(f"Array: {sorted_arr}")
    print(f"Search 5: {binary_search_basic(sorted_arr, 5)}")
    print(f"Search 10: {binary_search_basic(sorted_arr, 10)}")

    # Test con duplicados
    duplicates = [1, 2, 2, 2, 3, 4, 5]
    print(f"\nArray con duplicados: {duplicates}")
    print(f"Leftmost 2: {binary_search_leftmost(duplicates, 2)}")
    print(f"Rightmost 2: {binary_search_rightmost(duplicates, 2)}")

    # Test rotated array
    rotated = [4, 5, 6, 7, 0, 1, 2]
    print(f"\nRotated array: {rotated}")
    print(f"Search 0: {search_rotated_array(rotated, 0)}")
    print(f"Search 3: {search_rotated_array(rotated, 3)}")

    print("\n=== TESTING SORTING ALGORITHMS ===")
    for i, arr in enumerate(test_cases[:4]):  # Skip large array for display
        original = arr.copy()

        bubble_result = bubble_sort(arr.copy())
        merge_result = merge_sort(arr.copy())
        quick_result = quick_sort(arr.copy())

        print(f"\nTest Case {i+1}: {original}")
        print(f"Bubble Sort: {bubble_result}")
        print(f"Merge Sort:  {merge_result}")
        print(f"Quick Sort:  {quick_result}")

        # Verificar que todos dan el mismo resultado
        assert bubble_result == merge_result == quick_result


if __name__ == "__main__":
    test_all_algorithms()
    print("\n✅ Todos los tests pasaron!")

    # Benchmark rápido
    import time

    large_arr = list(range(10000, 0, -1))

    start = time.time()
    merge_sort(large_arr.copy())
    merge_time = time.time() - start

    start = time.time()
    quick_sort_random_pivot(large_arr.copy())
    quick_time = time.time() - start

    print(f"\n⚡ Performance (10k elementos):")
    print(f"Merge Sort: {merge_time:.4f}s")
    print(f"Quick Sort: {quick_time:.4f}s")
