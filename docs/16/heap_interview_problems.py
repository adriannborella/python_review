"""
PROBLEMAS CLÁSICOS DE ENTREVISTA - HEAPS
========================================

Estos son los problemas MÁS FRECUENTES que aparecen en entrevistas:
- Top K Problems (95% de probabilidad)
- Merge K Sorted Lists (85% probabilidad)
- Median from Stream (70% probabilidad)
- Meeting Rooms / Interval Problems (60% probabilidad)

Cada problema incluye múltiples enfoques y optimizaciones.
¡Domina estos patrones y tendrás una ventaja enorme!
"""

import heapq
from collections import defaultdict
import random

# ========================
# PROBLEMA 1: Kth Largest Element
# ========================
# Leetcode 215 - ¡EL MÁS COMÚN!


def find_kth_largest_v1(nums, k):
    """
    Approach 1: Sort - Simple pero no óptimo
    Complejidad: O(n log n) tiempo, O(1) espacio
    """
    nums.sort(reverse=True)
    return nums[k - 1]


def find_kth_largest_v2(nums, k):
    """
    Approach 2: Min-Heap de tamaño K - ÓPTIMO para K pequeño
    Complejidad: O(n log k) tiempo, O(k) espacio
    """
    # Mantener heap de los K elementos más grandes
    heap = []

    for num in nums:
        heapq.heappush(heap, num)

        # Mantener heap de tamaño K
        if len(heap) > k:
            heapq.heappop(heap)

    # La raíz es el K-ésimo más grande
    return heap[0]


def find_kth_largest_v3(nums, k):
    """
    Approach 3: Quickselect - ÓPTIMO para K grande
    Complejidad: O(n) promedio, O(n²) peor caso
    """

    def quickselect(left, right, k_smallest):
        if left == right:
            return nums[left]

        # Elegir pivot aleatorio
        pivot_index = random.randint(left, right)

        # Partition alrededor del pivot
        pivot_index = partition(left, right, pivot_index)

        if k_smallest == pivot_index:
            return nums[k_smallest]
        elif k_smallest < pivot_index:
            return quickselect(left, pivot_index - 1, k_smallest)
        else:
            return quickselect(pivot_index + 1, right, k_smallest)

    def partition(left, right, pivot_index):
        pivot = nums[pivot_index]
        # Mover pivot al final
        nums[pivot_index], nums[right] = nums[right], nums[pivot_index]

        store_index = left
        for i in range(left, right):
            if nums[i] < pivot:
                nums[store_index], nums[i] = nums[i], nums[store_index]
                store_index += 1

        # Mover pivot a su posición final
        nums[right], nums[store_index] = nums[store_index], nums[right]
        return store_index

    # Kth largest = (n-k)th smallest
    return quickselect(0, len(nums) - 1, len(nums) - k)


# ========================
# PROBLEMA 2: Top K Frequent Elements
# ========================
# Leetcode 347 - Muy común
from collections import Counter


def top_k_frequent(nums, k):
    """
    Top K elementos más frecuentes
    Complejidad: O(n log k) tiempo, O(n + k) espacio
    """
    # Contar frecuencias
    freq_map = {}
    for num in nums:
        freq_map[num] = freq_map.get(num, 0) + 1

    # Min-heap basado en frecuencia
    heap = []

    for num, freq in freq_map.items():
        heapq.heappush(heap, (freq, num))

        # Mantener heap de tamaño K
        if len(heap) > k:
            heapq.heappop(heap)

    # Extraer resultado
    result = []
    while heap:
        freq, num = heapq.heappop(heap)
        result.append(num)

    return result[::-1]  # Orden descendente por frecuencia


def top_k_frequent_bucket(nums, k):
    """
    Approach alternativo: Bucket Sort
    Complejidad: O(n) tiempo, O(n) espacio
    ¡Mejor para casos donde k es grande!
    """
    # Contar frecuencias
    freq_map = {}
    for num in nums:
        freq_map[num] = freq_map.get(num, 0) + 1

    # Bucket sort por frecuencia
    n = len(nums)
    buckets = [[] for _ in range(n + 1)]

    for num, freq in freq_map.items():
        buckets[freq].append(num)

    # Extraer top K desde frecuencia más alta
    result = []
    for freq in range(n, 0, -1):
        if buckets[freq]:
            result.extend(buckets[freq])
            if len(result) >= k:
                break

    return result[:k]


# ========================
# PROBLEMA 3: Merge K Sorted Lists
# ========================
# Leetcode 23 - Clásico de heaps


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        return f"ListNode({self.val})"

    # Para hacer comparables en el heap
    def __lt__(self, other):
        return self.val < other.val


def merge_k_lists(lists):
    """
    Merge K sorted linked lists
    Complejidad: O(n log k) donde n = total nodes, k = number of lists
    """
    if not lists:
        return None

    # Min-heap con el primer nodo de cada lista
    heap = []

    # Agregar primer nodo de cada lista no vacía
    for i, head in enumerate(lists):
        if head:
            heapq.heappush(heap, (head.val, i, head))

    # Dummy head para simplificar construcción
    dummy = ListNode(0)
    current = dummy

    while heap:
        val, list_index, node = heapq.heappop(heap)

        # Agregar nodo al resultado
        current.next = node
        current = current.next

        # Agregar siguiente nodo de la misma lista
        if node.next:
            heapq.heappush(heap, (node.next.val, list_index, node.next))

    return dummy.next


def merge_k_lists_divide_conquer(lists):
    """
    Approach alternativo: Divide and Conquer
    Complejidad: O(n log k) tiempo, O(log k) espacio
    """
    if not lists:
        return None

    def merge_two_lists(l1, l2):
        dummy = ListNode(0)
        current = dummy

        while l1 and l2:
            if l1.val <= l2.val:
                current.next = l1
                l1 = l1.next
            else:
                current.next = l2
                l2 = l2.next
            current = current.next

        # Agregar resto
        current.next = l1 if l1 else l2
        return dummy.next

    # Merge por pares hasta que quede uno
    while len(lists) > 1:
        merged_lists = []

        for i in range(0, len(lists), 2):
            l1 = lists[i]
            l2 = lists[i + 1] if i + 1 < len(lists) else None
            merged_lists.append(merge_two_lists(l1, l2))

        lists = merged_lists

    return lists[0]


# ========================
# PROBLEMA 4: Find Median from Data Stream
# ========================
# Leetcode 295 - Muy elegante con dos heaps


class MedianFinder:
    """
    Encontrar mediana en stream de datos
    Usa dos heaps: max-heap para mitad inferior, min-heap para superior
    """

    def __init__(self):
        # Mitad inferior (max-heap simulado con valores negativos)
        self.small = []  # max-heap
        # Mitad superior (min-heap)
        self.large = []  # min-heap

    def add_num(self, num):
        """
        Agregar número al stream
        Complejidad: O(log n)
        """
        # Siempre agregar a small primero (usando valores negativos)
        heapq.heappush(self.small, -num)

        # Asegurar que max de small <= min de large
        if self.small and self.large and -self.small[0] > self.large[0]:
            # Mover elemento de small a large
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)

        # Balancear tamaños (diferencia máxima = 1)
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        elif len(self.large) > len(self.small) + 1:
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def find_median(self):
        """
        Encontrar mediana actual
        Complejidad: O(1)
        """
        if len(self.small) > len(self.large):
            return -self.small[0]
        elif len(self.large) > len(self.small):
            return self.large[0]
        else:
            # Tamaños iguales - promedio de los dos medios
            return (-self.small[0] + self.large[0]) / 2


# ========================
# PROBLEMA 5: Meeting Rooms II
# ========================
# Leetcode 253 - Intervals con heap


def min_meeting_rooms(intervals):
    """
    Mínimo número de salas de reuniones necesarias
    Complejidad: O(n log n) tiempo, O(n) espacio
    """
    if not intervals:
        return 0

    # Ordenar por tiempo de inicio
    intervals.sort(key=lambda x: x[0])

    # Min-heap para track de end times de reuniones activas
    heap = []

    for start, end in intervals:
        # Si hay reunión que ya terminó, reusar su sala
        if heap and heap[0] <= start:
            heapq.heappop(heap)

        # Agregar end time de reunión actual
        heapq.heappush(heap, end)

    # Número de salas = número de reuniones concurrentes
    return len(heap)


# ========================
# PROBLEMA 6: Ugly Number II
# ========================
# Leetcode 264 - Heap para generación de secuencias


def nth_ugly_number(n):
    """
    El n-ésimo ugly number (solo factores 2, 3, 5)
    Complejidad: O(n log n) tiempo, O(n) espacio
    """
    heap = [1]
    seen = {1}

    for _ in range(n):
        ugly = heapq.heappop(heap)

        # Generar próximos ugly numbers
        for factor in [2, 3, 5]:
            new_ugly = ugly * factor
            if new_ugly not in seen:
                seen.add(new_ugly)
                heapq.heappush(heap, new_ugly)

    return ugly


# ========================
# TESTING FRAMEWORK
# ========================


def test_kth_largest():
    """Test Kth Largest Element"""
    print("=== TESTING KTH LARGEST ===\n")

    nums = [3, 2, 1, 5, 6, 4]
    k = 2

    print(f"Array: {nums}, K = {k}")
    print(f"Sort approach: {find_kth_largest_v1(nums[:], k)}")
    print(f"Min-heap approach: {find_kth_largest_v2(nums[:], k)}")
    print(f"Quickselect approach: {find_kth_largest_v3(nums[:], k)}")


def test_top_k_frequent():
    """Test Top K Frequent Elements"""
    print("\n=== TESTING TOP K FREQUENT ===\n")

    nums = [1, 1, 1, 2, 2, 3]
    k = 2

    print(f"Array: {nums}, K = {k}")
    print(f"Heap approach: {top_k_frequent(nums, k)}")
    print(f"Bucket approach: {top_k_frequent_bucket(nums, k)}")


def test_merge_k_lists():
    """Test Merge K Sorted Lists"""
    print("\n=== TESTING MERGE K LISTS ===\n")

    # Crear listas de prueba: [1,4,5], [1,3,4], [2,6]
    def create_list(values):
        if not values:
            return None
        head = ListNode(values[0])
        current = head
        for val in values[1:]:
            current.next = ListNode(val)
            current = current.next
        return head

    def list_to_array(head):
        result = []
        while head:
            result.append(head.val)
            head = head.next
        return result

    lists = [create_list([1, 4, 5]), create_list([1, 3, 4]), create_list([2, 6])]

    print("Input lists: [1,4,5], [1,3,4], [2,6]")

    # Test heap approach
    result1 = merge_k_lists(
        [create_list([1, 4, 5]), create_list([1, 3, 4]), create_list([2, 6])]
    )
    print(f"Heap approach: {list_to_array(result1)}")

    # Test divide & conquer
    result2 = merge_k_lists_divide_conquer(
        [create_list([1, 4, 5]), create_list([1, 3, 4]), create_list([2, 6])]
    )
    print(f"Divide & conquer: {list_to_array(result2)}")


def test_median_finder():
    """Test MedianFinder"""
    print("\n=== TESTING MEDIAN FINDER ===\n")

    mf = MedianFinder()
    operations = [
        ("add", 1),
        ("median", None),
        ("add", 2),
        ("median", None),
        ("add", 3),
        ("median", None),
        ("add", 4),
        ("median", None),
        ("add", 5),
        ("median", None),
    ]

    print("Operations and results:")
    for op, val in operations:
        if op == "add":
            mf.add_num(val)
            print(f"   Added {val}")
        else:
            median = mf.find_median()
            print(f"   Median: {median}")


def test_meeting_rooms():
    """Test Meeting Rooms II"""
    print("\n=== TESTING MEETING ROOMS ===\n")

    test_cases = [
        [[0, 30], [5, 10], [15, 20]],  # Expected: 2
        [[7, 10], [2, 4]],  # Expected: 1
        [[9, 10], [4, 9], [4, 17]],  # Expected: 2
        [[2, 11], [6, 16], [11, 16]],  # Expected: 2
    ]

    for i, intervals in enumerate(test_cases, 1):
        rooms = min_meeting_rooms(intervals)
        print(f"Test {i}: {intervals}")
        print(f"   Min rooms needed: {rooms}")


def test_ugly_numbers():
    """Test Ugly Numbers"""
    print("\n=== TESTING UGLY NUMBERS ===\n")

    test_values = [1, 2, 3, 4, 5, 6, 10, 15]

    print("First few ugly numbers:")
    for n in test_values:
        ugly = nth_ugly_number(n)
        print(f"   U({n}) = {ugly}")


def benchmark_heap_operations():
    """Benchmark diferentes operaciones de heap"""
    print("\n=== PERFORMANCE BENCHMARK ===\n")

    import time

    # Test con diferentes tamaños
    sizes = [1000, 10000, 100000]

    for size in sizes:
        print(f"Testing with {size:,} elements:")

        # Datos aleatorios
        data = [random.randint(1, size * 10) for _ in range(size)]

        # Test heapify
        start = time.time()
        heap_data = data[:]
        heapq.heapify(heap_data)
        heapify_time = time.time() - start

        # Test insert one by one
        start = time.time()
        insert_heap = []
        for val in data:
            heapq.heappush(insert_heap, val)
        insert_time = time.time() - start

        print(f"   Heapify: {heapify_time:.4f}s")
        print(f"   Insert one-by-one: {insert_time:.4f}s")
        print(f"   Heapify speedup: {insert_time/heapify_time:.1f}x faster")


# ========================
# PATRONES AVANZADOS
# ========================


def sliding_window_maximum(nums, k):
    """
    Sliding Window Maximum - Leetcode 239
    Combina deque + heap para solución óptima
    """
    from collections import deque

    if not nums or k == 0:
        return []

    # Deque para indices, heap para cleanup
    dq = deque()
    result = []

    for i in range(len(nums)):
        # Remover elementos fuera de ventana
        while dq and dq[0] <= i - k:
            dq.popleft()

        # Mantener deque en orden decreciente
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()

        dq.append(i)

        # Agregar resultado cuando ventana esté completa
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result


def k_closest_points_to_origin(points, k):
    """
    K Closest Points to Origin - Leetcode 973
    Usar max-heap de tamaño K para track de los más cercanos
    """
    import math

    def distance_squared(point):
        return point[0] ** 2 + point[1] ** 2

    # Max-heap de tamaño K (usar valores negativos)
    heap = []

    for point in points:
        dist_sq = distance_squared(point)

        if len(heap) < k:
            heapq.heappush(heap, (-dist_sq, point))
        elif dist_sq < -heap[0][0]:
            heapq.heappushpop(heap, (-dist_sq, point))

    return [point for _, point in heap]


def reorganize_string(s):
    """
    Reorganize String - Leetcode 767
    Usar heap para siempre elegir caracteres más frecuentes
    """
    # Contar frecuencias
    char_count = {}
    for char in s:
        char_count[char] = char_count.get(char, 0) + 1

    # Max-heap basado en frecuencia
    heap = []
    for char, count in char_count.items():
        heapq.heappush(heap, (-count, char))

    result = []
    prev_count, prev_char = 0, ""

    while heap:
        # Tomar carácter más frecuente
        count, char = heapq.heappop(heap)
        result.append(char)

        # Re-agregar carácter anterior si aún tiene usos
        if prev_count < 0:
            heapq.heappush(heap, (prev_count, prev_char))

        # Actualizar para próxima iteración
        prev_count, prev_char = count + 1, char

    # Verificar si fue posible reorganizar
    if len(result) != len(s):
        return ""

    return "".join(result)


# ========================
# TIPS PARA ENTREVISTAS
# ========================

"""
🎯 PATRONES GANADORES PARA HEAPS EN ENTREVISTAS:

1. TOP-K PROBLEMS:
   - Usar min-heap de tamaño K para Top-K largest
   - Usar max-heap de tamaño K para Top-K smallest
   - Siempre pregunta: ¿K es pequeño comparado con N?

2. MERGE PROBLEMS:
   - K sorted arrays/lists → heap con (value, source_index)
   - Sliding window maximum → deque + heap hybrid
   
3. STREAMING DATA:
   - Median → two heaps (max + min)
   - Running statistics → heaps para percentiles

4. SCHEDULING:
   - Meeting rooms → heap para track end times
   - Task scheduling → priority queue

5. OPTIMIZATION TRICKS:
   - heapify() es O(n), más rápido que K inserts O(k log k)
   - Para max-heap, usar valores negativos en min-heap
   - heappushpop() es más eficiente que push + pop separados

6. EDGE CASES CRÍTICOS:
   - Heap vacío (always check!)
   - K > len(array)
   - Todos elementos iguales
   - K = 1 o K = N

7. SPACE OPTIMIZATIONS:
   - Heap in-place para heap sort
   - Heap de tamaño K vs heap de tamaño N
   - Iterator patterns para memoria constante

8. WHEN NOT TO USE HEAPS:
   - Si necesitas búsqueda arbitraria → BST
   - Si necesitas orden total → sorting
   - Si K es muy grande → quickselect puede ser mejor
"""

if __name__ == "__main__":
    test_kth_largest()
    test_top_k_frequent()
    test_merge_k_lists()
    test_median_finder()
    test_meeting_rooms()
    test_ugly_numbers()
    benchmark_heap_operations()

    print("\n=== BONUS: ADVANCED PROBLEMS ===")

    # Test sliding window maximum
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    result = sliding_window_maximum(nums, k)
    print(f"\nSliding window max ({nums}, k={k}): {result}")

    # Test K closest points
    points = [[1, 1], [3, 3], [2, 2], [4, 4], [-1, -1]]
    k = 3
    closest = k_closest_points_to_origin(points, k)
    print(f"\n{k} closest points to origin: {closest}")

    # Test reorganize string
    s = "aab"
    reorganized = reorganize_string(s)
    print(f"\nReorganize '{s}': '{reorganized}'")
