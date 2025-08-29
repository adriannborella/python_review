"""
LEETCODE MEDIUM - SEARCHING & SORTING
Día 9 - Problemas frecuentes en entrevistas
"""

def find_first_and_last_position(nums, target):
    """
    LeetCode 34: Find First and Last Position of Element in Sorted Array
    PREGUNTA MUY FRECUENTE - Amazon, Google, Microsoft
    
    Tiempo: O(log n), Espacio: O(1)
    """
    def find_leftmost(nums, target):
        left, right = 0, len(nums)
        while left < right:
            mid = left + (right - left) // 2
            if nums[mid] < target:
                left = mid + 1
            else:
                right = mid
        return left
    
    def find_rightmost(nums, target):
        left, right = 0, len(nums)
        while left < right:
            mid = left + (right - left) // 2
            if nums[mid] <= target:
                left = mid + 1
            else:
                right = mid
        return left - 1
    
    if not nums:
        return [-1, -1]
    
    left_pos = find_leftmost(nums, target)
    if left_pos >= len(nums) or nums[left_pos] != target:
        return [-1, -1]
    
    right_pos = find_rightmost(nums, target)
    return [left_pos, right_pos]

def search_in_rotated_sorted_array_ii(nums, target):
    """
    LeetCode 81: Search in Rotated Sorted Array II (con duplicados)
    Más complejo que la versión I - Meta, Apple
    
    Tiempo: O(log n) average, O(n) worst case
    """
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if nums[mid] == target:
            return True
        
        # Casos con duplicados: no podemos determinar qué lado está ordenado
        if nums[left] == nums[mid] == nums[right]:
            left += 1
            right -= 1
        elif nums[left] <= nums[mid]:  # Izquierda ordenada
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:  # Derecha ordenada
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    
    return False

def find_minimum_in_rotated_sorted_array(nums):
    """
    LeetCode 153: Find Minimum in Rotated Sorted Array
    Microsoft, Amazon - Variante común
    
    Tiempo: O(log n), Espacio: O(1)
    """
    left, right = 0, len(nums) - 1
    
    while left < right:
        mid = left + (right - left) // 2
        
        if nums[mid] > nums[right]:
            # Mínimo está en la derecha
            left = mid + 1
        else:
            # Mínimo está en la izquierda (o es mid)
            right = mid
    
    return nums[left]

def search_2d_matrix_ii(matrix, target):
    """
    LeetCode 240: Search 2D Matrix II
    Google, Facebook - Técnica de eliminación
    
    Tiempo: O(m + n), Espacio: O(1)
    """
    if not matrix or not matrix[0]:
        return False
    
    # Empezar desde esquina superior derecha
    row, col = 0, len(matrix[0]) - 1
    
    while row < len(matrix) and col >= 0:
        if matrix[row][col] == target:
            return True
        elif matrix[row][col] > target:
            col -= 1  # Eliminar columna
        else:
            row += 1  # Eliminar fila
    
    return False

def find_k_closest_elements(arr, k, x):
    """
    LeetCode 658: Find K Closest Elements
    LinkedIn, Uber - Combina binary search + two pointers
    
    Tiempo: O(log n + k), Espacio: O(1)
    """
    # Binary search para encontrar posición de inserción
    left, right = 0, len(arr) - k
    
    while left < right:
        mid = left + (right - left) // 2
        
        # Comparar distancias a los extremos de la ventana
        if x - arr[mid] > arr[mid + k] - x:
            left = mid + 1
        else:
            right = mid
    
    return arr[left:left + k]

def sort_colors(nums):
    """
    LeetCode 75: Sort Colors (Dutch National Flag)
    Apple, Google - Algoritmo de partición avanzado
    
    Tiempo: O(n), Espacio: O(1)
    """
    # Three pointers approach
    low = current = 0
    high = len(nums) - 1
    
    while current <= high:
        if nums[current] == 0:
            nums[low], nums[current] = nums[current], nums[low]
            low += 1
            current += 1
        elif nums[current] == 1:
            current += 1
        else:  # nums[current] == 2
            nums[current], nums[high] = nums[high], nums[current]
            high -= 1
            # No incrementar current porque necesitamos revisar el elemento swapped

def kth_largest_element(nums, k):
    """
    LeetCode 215: Kth Largest Element (QuickSelect)
    Amazon, Facebook - Optimización de QuickSort
    
    Tiempo: O(n) average, O(n²) worst case
    """
    import random
    
    def quickselect(left, right, k_smallest):
        if left == right:
            return nums[left]
        
        # Pivot aleatorio
        random_index = random.randint(left, right)
        nums[random_index], nums[right] = nums[right], nums[random_index]
        
        # Partición
        pivot_index = partition_for_quickselect(left, right)
        
        if k_smallest == pivot_index:
            return nums[k_smallest]
        elif k_smallest < pivot_index:
            return quickselect(left, pivot_index - 1, k_smallest)
        else:
            return quickselect(pivot_index + 1, right, k_smallest)
    
    def partition_for_quickselect(left, right):
        pivot = nums[right]
        i = left
        
        for j in range(left, right):
            if nums[j] <= pivot:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
        
        nums[i], nums[right] = nums[right], nums[i]
        return i
    
    return quickselect(0, len(nums) - 1, len(nums) - k)

def merge_intervals(intervals):
    """
    LeetCode 56: Merge Intervals
    Microsoft, Google - Sorting + Merging
    
    Tiempo: O(n log n), Espacio: O(1)
    """
    if not intervals:
        return []
    
    # Ordenar por inicio del intervalo
    intervals.sort(key=lambda x: x[0])
    
    merged = [intervals[0]]
    
    for current in intervals[1:]:
        last_merged = merged[-1]
        
        if current[0] <= last_merged[1]:  # Overlap
            last_merged[1] = max(last_merged[1], current[1])
        else:
            merged.append(current)
    
    return merged

def top_k_frequent_elements(nums, k):
    """
    LeetCode 347: Top K Frequent Elements
    Facebook, Amazon - Heap + Hash Map
    
    Tiempo: O(n log k), Espacio: O(n)
    """
    from collections import Counter
    import heapq
    
    # Contar frecuencias
    count = Counter(nums)
    
    # Min heap para mantener los k más frecuentes
    heap = []
    
    for num, freq in count.items():
        heapq.heappush(heap, (freq, num))
        if len(heap) > k:
            heapq.heappop(heap)
    
    return [num for freq, num in heap]

# TESTING DE TODOS LOS ALGORITMOS

def test_leetcode_problems():
    """Test comprehensivo de todos los problemas"""
    
    print("=== TESTING LEETCODE MEDIUM PROBLEMS ===")
    
    # Test 34: First and Last Position
    nums = [5,7,7,8,8,10]
    result = find_first_and_last_position(nums, 8)
    print(f"First and Last Position of 8 in {nums}: {result}")
    assert result == [3, 4]
    
    # Test 81: Search in Rotated Array II
    nums = [2,5,6,0,0,1,2]
    result = search_in_rotated_sorted_array_ii(nums, 0)
    print(f"Search 0 in rotated array with duplicates: {result}")
    assert result == True
    
    # Test 153: Find Minimum
    nums = [3,4,5,1,2]
    result = find_minimum_in_rotated_sorted_array(nums)
    print(f"Minimum in {nums}: {result}")
    assert result == 1
    
    # Test 240: Search 2D Matrix II
    matrix = [
        [1,4,7,11,15],
        [2,5,8,12,19],
        [3,6,9,16,22],
        [10,13,14,17,24],
        [18,21,23,26,30]
    ]
    result = search_2d_matrix_ii(matrix, 5)
    print(f"Search 5 in 2D matrix: {result}")
    assert result == True
    
    # Test 658: K Closest Elements
    arr = [1,2,3,4,5]
    result = find_k_closest_elements(arr, 4, 3)
    print(f"4 closest elements to 3 in {arr}: {result}")
    assert result == [1,2,3,4]
    
    # Test 75: Sort Colors
    nums = [2,0,2,1,1,0]
    sort_colors(nums)
    print(f"Sort colors: {nums}")
    assert nums == [0,0,1,1,2,2]
    
    # Test 215: Kth Largest
    nums = [3,2,1,5,6,4]
    result = kth_largest_element(nums, 2)
    print(f"2nd largest in [3,2,1,5,6,4]: {result}")
    assert result == 5
    
    # Test 56: Merge Intervals
    intervals = [[1,3],[2,6],[8,10],[15,18]]
    result = merge_intervals(intervals)
    print(f"Merge intervals {intervals}: {result}")
    assert result == [[1,6],[8,10],[15,18]]
    
    # Test 347: Top K Frequent
    nums = [1,1,1,2,2,3]
    result = top_k_frequent_elements(nums, 2)
    print(f"Top 2 frequent in {nums}: {sorted(result)}")
    assert sorted(result) == [1,2]
    
    print("\n✅ Todos los tests de LeetCode pasaron!")

# ANÁLISIS DE COMPLEJIDAD PARA ENTREVISTAS

def complexity_analysis():
    """
    Análisis que debes dominar para explicar en entrevistas
    """
    print("\n=== ANÁLISIS DE COMPLEJIDAD ===")
    
    algorithms = {
        "Binary Search Básico": {
            "tiempo": "O(log n)",
            "espacio": "O(1)",
            "cuándo_usar": "Array ordenado, búsqueda exacta"
        },
        "Binary Search Leftmost/Rightmost": {
            "tiempo": "O(log n)", 
            "espacio": "O(1)",
            "cuándo_usar": "Arrays con duplicados, rangos"
        },
        "Search Rotated Array": {
            "tiempo": "O(log n)",
            "espacio": "O(1)", 
            "cuándo_usar": "Array rotado sin duplicados"
        },
        "Merge Sort": {
            "tiempo": "O(n log n)",
            "espacio": "O(n)",
            "cuándo_usar": "Estabilidad requerida, datos grandes"
        },
        "Quick Sort": {
            "tiempo": "O(n log n) avg, O(n²) worst",
            "espacio": "O(log n) avg, O(n) worst",
            "cuándo_usar": "In-place sorting, promedio más rápido"
        },
        "QuickSelect": {
            "tiempo": "O(n) avg, O(n²) worst", 
            "espacio": "O(1)",
            "cuándo_usar": "K-th element, mejor que sorting completo"
        }
    }
    
    for alg, props in algorithms.items():
        print(f"\n{alg}:")
        print(f"  Tiempo: {props['tiempo']}")
        print(f"  Espacio: {props['espacio']}")
        print(f"  Cuándo usar: {props['cuándo_usar']}")

if __name__ == "__main__":
    test_leetcode_problems()
    complexity_analysis()
    
    print("\n🎯 PUNTOS CLAVE PARA ENTREVISTAS:")
    print("1. Siempre verifica casos edge (array vacío, un elemento)")
    print("2. Explica por qué mid = left + (right - left) // 2")
    print("3. Diferencia entre left <= right vs left < right")
    print("4. Conoce cuándo usar cada variante de binary search")
    print("5. Practica explicar trade-offs tiempo vs espacio")
    print("6. Domina la implementación in-place vs out-of-place")