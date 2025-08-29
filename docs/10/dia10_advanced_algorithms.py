"""
ALGORITMOS AVANZADOS - DÍA 10
Implementaciones optimizadas y técnicas avanzadas para entrevistas
"""

import time
import random
from typing import List, Optional, Tuple
from collections import deque


class AdvancedSearchAlgorithms:
    """
    Implementaciones avanzadas de algoritmos de búsqueda
    Con optimizaciones y casos edge manejados
    """

    @staticmethod
    def exponential_search(arr: List[int], target: int) -> int:
        """
        Exponential Search - Para arrays infinitos o muy grandes
        Tiempo: O(log n), mejor que binary search cuando target está cerca del inicio

        Usado en: Google, Microsoft para sistemas de archivos grandes
        """
        if not arr:
            return -1

        # Caso especial: primer elemento
        if arr[0] == target:
            return 0

        # Encontrar rango donde puede estar target
        bound = 1
        while bound < len(arr) and arr[bound] < target:
            bound *= 2

        # Binary search en el rango encontrado
        left = bound // 2
        right = min(bound, len(arr) - 1)

        while left <= right:
            mid = left + (right - left) // 2

            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        return -1

    @staticmethod
    def interpolation_search(arr: List[int], target: int) -> int:
        """
        Interpolation Search - Para datos uniformemente distribuidos
        Tiempo: O(log log n) para distribución uniforme, O(n) worst case

        Útil cuando: Los datos están uniformemente distribuidos
        """
        if not arr:
            return -1

        left, right = 0, len(arr) - 1

        while left <= right and target >= arr[left] and target <= arr[right]:
            # Evitar división por cero
            if arr[right] == arr[left]:
                if arr[left] == target:
                    return left
                break

            # Interpolación lineal para estimar posición
            pos = left + ((target - arr[left]) * (right - left)) // (
                arr[right] - arr[left]
            )

            # Asegurar que pos esté en rango válido
            pos = max(left, min(pos, right))

            if arr[pos] == target:
                return pos
            elif arr[pos] < target:
                left = pos + 1
            else:
                right = pos - 1

        return -1

    @staticmethod
    def ternary_search_peak(arr: List[int]) -> int:
        """
        Ternary Search para encontrar el pico en array unimodal
        Tiempo: O(log n), Espacio: O(1)

        Pregunta frecuente: "Encuentra el máximo en mountain array"
        """
        left, right = 0, len(arr) - 1

        while left < right:
            mid1 = left + (right - left) // 3
            mid2 = right - (right - left) // 3

            if arr[mid1] < arr[mid2]:
                left = mid1 + 1
            else:
                right = mid2 - 1

        return left


class OptimizedSortingAlgorithms:
    """
    Algoritmos de ordenamiento con optimizaciones para entrevistas
    """

    @staticmethod
    def tim_sort_merge(arr: List[int]) -> List[int]:
        """
        Implementación simplificada de TimSort (Python's default sort)
        Híbrido entre Merge Sort e Insertion Sort
        """
        MIN_MERGE = 32

        def insertion_sort(arr, left, right):
            """Insertion sort para arrays pequeños"""
            for i in range(left + 1, right + 1):
                key = arr[i]
                j = i - 1
                while j >= left and arr[j] > key:
                    arr[j + 1] = arr[j]
                    j -= 1
                arr[j + 1] = key

        def merge(arr, left, mid, right):
            """Merge optimizado"""
            left_part = arr[left : mid + 1]
            right_part = arr[mid + 1 : right + 1]

            i = j = 0
            k = left

            while i < len(left_part) and j < len(right_part):
                if left_part[i] <= right_part[j]:
                    arr[k] = left_part[i]
                    i += 1
                else:
                    arr[k] = right_part[j]
                    j += 1
                k += 1

            while i < len(left_part):
                arr[k] = left_part[i]
                i += 1
                k += 1

            while j < len(right_part):
                arr[k] = right_part[j]
                j += 1
                k += 1

        n = len(arr)

        # Usar insertion sort para runs pequeños
        for start in range(0, n, MIN_MERGE):
            end = min(start + MIN_MERGE - 1, n - 1)
            insertion_sort(arr, start, end)

        # Merge runs
        size = MIN_MERGE
        while size < n:
            for start in range(0, n, size * 2):
                mid = min(start + size - 1, n - 1)
                end = min(start + size * 2 - 1, n - 1)

                if mid < end:
                    merge(arr, start, mid, end)

            size *= 2

        return arr

    @staticmethod
    def three_way_quicksort(arr: List[int]) -> List[int]:
        """
        3-Way QuickSort - Óptimo para arrays con muchos duplicados
        Tiempo: O(n log n), mejor para duplicados

        Usado en: Arrays con pocos valores únicos
        """

        def three_way_partition(arr, low, high):
            """Particiona en 3 partes: <pivot, =pivot, >pivot"""
            if high <= low:
                return low, high

            pivot = arr[low]
            lt = low  # arr[low..lt-1] < pivot
            gt = high  # arr[gt+1..high] > pivot
            i = low + 1  # arr[lt..i-1] == pivot

            while i <= gt:
                if arr[i] < pivot:
                    arr[lt], arr[i] = arr[i], arr[lt]
                    lt += 1
                    i += 1
                elif arr[i] > pivot:
                    arr[i], arr[gt] = arr[gt], arr[i]
                    gt -= 1
                else:
                    i += 1

            return lt, gt

        def quicksort_3way(arr, low, high):
            if high <= low:
                return

            lt, gt = three_way_partition(arr, low, high)
            quicksort_3way(arr, low, lt - 1)
            quicksort_3way(arr, gt + 1, high)

        if len(arr) <= 1:
            return arr

        quicksort_3way(arr, 0, len(arr) - 1)
        return arr

    @staticmethod
    def counting_sort_optimized(arr: List[int]) -> List[int]:
        """
        Counting Sort optimizado - Para rangos limitados
        Tiempo: O(n + k), Espacio: O(k)

        Cuándo usar: Rango de valores conocido y pequeño
        """
        if not arr:
            return arr

        min_val, max_val = min(arr), max(arr)
        range_size = max_val - min_val + 1

        # Optimización: Si el rango es muy grande, usar otro algoritmo
        if range_size > len(arr) * 2:
            return sorted(arr)  # Fallback

        count = [0] * range_size

        # Contar ocurrencias
        for num in arr:
            count[num - min_val] += 1

        # Reconstruir array
        result = []
        for i, freq in enumerate(count):
            result.extend([i + min_val] * freq)

        return result

    @staticmethod
    def radix_sort_lsd(arr: List[int]) -> List[int]:
        """
        Radix Sort LSD (Least Significant Digit)
        Tiempo: O(d * (n + b)), donde d=dígitos, b=base

        Excelente para: Enteros grandes, IDs, sorting estable
        """
        if not arr or all(x == 0 for x in arr):
            return arr

        # Manejar negativos convirtiéndolos
        max_val = max(abs(x) for x in arr)

        def counting_sort_by_digit(arr, exp):
            """Counting sort por dígito específico"""
            n = len(arr)
            output = [0] * n
            count = [0] * 10

            # Contar ocurrencias del dígito
            for num in arr:
                index = abs(num) // exp % 10
                count[index] += 1

            # Hacer count acumulativo
            for i in range(1, 10):
                count[i] += count[i - 1]

            # Construir array resultado
            for i in range(n - 1, -1, -1):
                index = abs(arr[i]) // exp % 10
                output[count[index] - 1] = arr[i]
                count[index] -= 1

            return output

        # Aplicar counting sort por cada dígito
        exp = 1
        while max_val // exp > 0:
            arr = counting_sort_by_digit(arr, exp)
            exp *= 10

        return arr


class AdvancedSearchProblems:
    """
    Problemas avanzados que combinan múltiples técnicas
    """

    @staticmethod
    def median_of_two_sorted_arrays(nums1: List[int], nums2: List[int]) -> float:
        """
        LeetCode 4: Median of Two Sorted Arrays
        HARD - Google, Microsoft, Amazon (MUY FRECUENTE)

        Tiempo: O(log(min(m,n))), Espacio: O(1)


        """
        # Asegurar que nums1 es el más pequeño
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1

        m, n = len(nums1), len(nums2)
        left, right = 0, m

        while left <= right:
            partitionX = (left + right) // 2
            partitionY = (m + n + 1) // 2 - partitionX

            # Valores máximos a la izquierda
            maxLeftX = float("-inf") if partitionX == 0 else nums1[partitionX - 1]
            maxLeftY = float("-inf") if partitionY == 0 else nums2[partitionY - 1]

            # Valores mínimos a la derecha
            minRightX = float("inf") if partitionX == m else nums1[partitionX]
            minRightY = float("inf") if partitionY == n else nums2[partitionY]

            if maxLeftX <= minRightY and maxLeftY <= minRightX:
                # Partición correcta encontrada
                if (m + n) % 2 == 0:
                    return (max(maxLeftX, maxLeftY) + min(minRightX, minRightY)) / 2.0
                else:
                    return max(maxLeftX, maxLeftY)
            elif maxLeftX > minRightY:
                right = partitionX - 1
            else:
                left = partitionX + 1

        raise ValueError("Input arrays are not sorted")

    @staticmethod
    def search_range_in_2d_matrix(
        matrix: List[List[int]], target: int
    ) -> List[Tuple[int, int]]:
        """
        Encontrar todas las posiciones de target en matriz ordenada
        Extensión de LeetCode 240

        Tiempo: O(m + n), Espacio: O(k) donde k = número de ocurrencias
        """
        if not matrix or not matrix[0]:
            return []

        positions = []
        rows, cols = len(matrix), len(matrix[0])

        # Empezar desde esquina superior derecha
        row, col = 0, cols - 1

        while row < rows and col >= 0:
            if matrix[row][col] == target:
                positions.append((row, col))

                # Buscar más ocurrencias en la fila
                temp_col = col - 1
                while temp_col >= 0 and matrix[row][temp_col] == target:
                    positions.append((row, temp_col))
                    temp_col -= 1

                # Buscar más ocurrencias en la columna
                temp_row = row + 1
                while temp_row < rows and matrix[temp_row][col] == target:
                    positions.append((temp_row, col))
                    temp_row += 1

                row += 1
            elif matrix[row][col] > target:
                col -= 1
            else:
                row += 1

        return positions


def comprehensive_testing():
    """
    Testing comprehensivo de todos los algoritmos avanzados
    """
    print("=== TESTING ALGORITMOS AVANZADOS ===")

    # Test data
    test_arrays = [
        [],
        [1],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        [1, 3, 3, 3, 5, 7, 9, 11],
        [5, 5, 5, 5, 5],
        list(range(1000)),
    ]

    search_algo = AdvancedSearchAlgorithms()
    sort_algo = OptimizedSortingAlgorithms()
    problems = AdvancedSearchProblems()

    print("\n--- Advanced Search Algorithms ---")

    # Test Exponential Search
    arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    result = search_algo.exponential_search(arr, 7)
    print(f"Exponential Search for 7 in {arr[:5]}...{arr[-3:]}: index {result}")
    assert result == 6

    # Test Interpolation Search
    arr = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
    result = search_algo.interpolation_search(arr, 64)
    print(f"Interpolation Search for 64: index {result}")
    assert result == 6

    # Test Ternary Search Peak
    mountain = [1, 3, 8, 12, 4, 2]
    peak_idx = search_algo.ternary_search_peak(mountain)
    print(f"Peak in {mountain}: index {peak_idx} (value: {mountain[peak_idx]})")
    assert peak_idx == 3

    print("\n--- Optimized Sorting Algorithms ---")

    # Test TimSort-like
    arr = [3, 7, 1, 9, 4, 2, 8, 6, 5]
    sorted_arr = sort_algo.tim_sort_merge(arr.copy())
    print(f"TimSort: {arr} → {sorted_arr}")
    assert sorted_arr == sorted(arr)

    # Test 3-Way QuickSort (good for duplicates)
    arr = [3, 1, 3, 2, 3, 1, 2, 3, 1]
    sorted_arr = sort_algo.three_way_quicksort(arr.copy())
    print(f"3-Way QuickSort: {arr} → {sorted_arr}")
    assert sorted_arr == sorted(arr)

    # Test Counting Sort
    arr = [4, 2, 2, 8, 3, 3, 1]
    sorted_arr = sort_algo.counting_sort_optimized(arr)
    print(f"Counting Sort: {arr} → {sorted_arr}")
    assert sorted_arr == sorted(arr)

    # Test Radix Sort
    arr = [170, 45, 75, 90, 2, 802, 24, 66]
    sorted_arr = sort_algo.radix_sort_lsd(arr.copy())
    print(f"Radix Sort: {arr} → {sorted_arr}")
    assert sorted_arr == sorted(arr)

    print("\n--- Advanced Problems ---")

    # Test Median of Two Sorted Arrays
    nums1, nums2 = [1, 3], [2]
    median = problems.median_of_two_sorted_arrays(nums1, nums2)
    print(f"Median of {nums1} and {nums2}: {median}")
    assert median == 2.0

    nums1, nums2 = [1, 2], [3, 4]
    median = problems.median_of_two_sorted_arrays(nums1, nums2)
    print(f"Median of {nums1} and {nums2}: {median}")
    assert median == 2.5

    # Test 2D Matrix Search with Multiple Results
    matrix = [[1, 4, 7, 11], [2, 5, 8, 12], [3, 6, 9, 16]]
    positions = problems.search_range_in_2d_matrix(matrix, 6)
    print(f"Positions of 6 in matrix: {positions}")

    print("\n✅ Todos los tests avanzados pasaron!")


def performance_comparison():
    """
    Comparación de performance entre algoritmos
    """
    print("\n=== PERFORMANCE COMPARISON ===")

    # Generar datos de prueba
    sizes = [1000, 10000]

    for size in sizes:
        print(f"\nArray size: {size}")

        # Array aleatorio
        random_data = [random.randint(1, size) for _ in range(size)]

        # Array con muchos duplicados
        duplicate_data = [random.randint(1, 10) for _ in range(size)]

        # Test sorting algorithms
        algorithms = [
            ("Python sorted", lambda arr: sorted(arr)),
            ("TimSort-like", OptimizedSortingAlgorithms.tim_sort_merge),
            ("3-Way QuickSort", OptimizedSortingAlgorithms.three_way_quicksort),
            ("Radix Sort", OptimizedSortingAlgorithms.radix_sort_lsd),
        ]

        print("  Random data:")
        for name, algo in algorithms:
            data_copy = random_data.copy()
            start_time = time.time()
            algo(data_copy)
            elapsed = time.time() - start_time
            print(f"    {name}: {elapsed:.4f}s")

        print("  Data with many duplicates:")
        for name, algo in algorithms[:3]:  # Skip radix for duplicates test
            data_copy = duplicate_data.copy()
            start_time = time.time()
            algo(data_copy)
            elapsed = time.time() - start_time
            print(f"    {name}: {elapsed:.4f}s")


if __name__ == "__main__":
    comprehensive_testing()
    performance_comparison()

    print("\n🎯 PUNTOS CLAVE PARA ENTREVISTAS:")
    print("1. Exponential Search: Mejor cuando target está cerca del inicio")
    print("2. Interpolation Search: Excelente para datos uniformes")
    print("3. 3-Way QuickSort: Óptimo para arrays con muchos duplicados")
    print("4. TimSort: Híbrido que maneja runs ordenadas eficientemente")
    print("5. Median of Two Arrays: Requiere binary search en espacio de particiones")
    print("6. Siempre considera el tipo de datos antes de elegir algoritmo")
