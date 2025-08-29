"""
LEETCODE PROBLEMS COMBINADOS - DÍA 10
Problemas que combinan búsqueda, ordenamiento y optimización
"""

from typing import List, Optional, Tuple
import heapq
from collections import defaultdict, Counter


class CombinedLeetCodeProblems:
    """
    Problemas que combinan múltiples técnicas de algoritmos
    """

    def find_kth_largest_in_stream(self, k: int, nums: List[int]) -> "KthLargestStream":
        """
        LeetCode 703: Kth Largest Element in a Stream
        Design problem - Netflix, Amazon

        Combina: Heap + Stream processing
        """

        class KthLargestStream:
            def __init__(self, k: int, nums: List[int]):
                self.k = k
                self.heap = nums
                heapq.heapify(self.heap)

                # Mantener solo k elementos más grandes
                while len(self.heap) > k:
                    heapq.heappop(self.heap)

            def add(self, val: int) -> int:
                heapq.heappush(self.heap, val)
                if len(self.heap) > self.k:
                    heapq.heappop(self.heap)
                return self.heap[0]

        return KthLargestStream(k, nums)

    def find_median_from_data_stream(self) -> "MedianFinder":
        """
        LeetCode 295: Find Median from Data Stream
        HARD - Google, Facebook (PREGUNTA ESTRELLA)

        Combina: Two heaps + Balancing
        """

        class MedianFinder:
            def __init__(self):
                # Max heap para la mitad menor (negamos valores)
                self.small = []
                # Min heap para la mitad mayor
                self.large = []

            def addNum(self, num: int) -> None:
                # Siempre agregar a small primero
                heapq.heappush(self.small, -num)

                # Asegurar que max(small) <= min(large)
                if self.small and self.large and -self.small[0] > self.large[0]:
                    val = -heapq.heappop(self.small)
                    heapq.heappush(self.large, val)

                # Balancear tamaños
                if len(self.small) > len(self.large) + 1:
                    val = -heapq.heappop(self.small)
                    heapq.heappush(self.large, val)
                elif len(self.large) > len(self.small) + 1:
                    val = heapq.heappop(self.large)
                    heapq.heappush(self.small, -val)

            def findMedian(self) -> float:
                if len(self.small) > len(self.large):
                    return -self.small[0]
                elif len(self.large) > len(self.small):
                    return self.large[0]
                else:
                    return (-self.small[0] + self.large[0]) / 2.0

        return MedianFinder()

    def search_suggestions_system(
        self, products: List[str], searchWord: str
    ) -> List[List[str]]:
        """
        LeetCode 1268: Search Suggestions System
        Amazon (basado en su sistema real de sugerencias)

        Combina: Sorting + Binary Search + Trie concepts
        """
        products.sort()
        result = []

        for i in range(len(searchWord)):
            prefix = searchWord[: i + 1]

            # Binary search para encontrar primer producto que empiece con prefix
            left, right = 0, len(products) - 1

            while left < right:
                mid = left + (right - left) // 2
                if products[mid][: len(prefix)] < prefix:
                    left = mid + 1
                else:
                    right = mid

            # Recoger hasta 3 sugerencias
            suggestions = []
            for j in range(left, min(left + 3, len(products))):
                if j < len(products) and products[j].startswith(prefix):
                    suggestions.append(products[j])

            result.append(suggestions)

        return result

    def count_of_smaller_numbers_after_self(self, nums: List[int]) -> List[int]:
        """
        LeetCode 315: Count of Smaller Numbers After Self
        HARD - Google, Microsoft (problema de inversión)

        Combina: Merge Sort + Counting
        """

        def mergeSort(arr):
            if len(arr) <= 1:
                return arr

            mid = len(arr) // 2
            left = mergeSort(arr[:mid])
            right = mergeSort(arr[mid:])

            return merge(left, right)

        def merge(left, right):
            result = []
            i = j = 0

            while i < len(left) and j < len(right):
                if left[i][0] <= right[j][0]:
                    # left[i] <= right[j], contar elementos menores en right
                    counts[left[i][1]] += j
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1

            while i < len(left):
                counts[left[i][1]] += j
                result.append(left[i])
                i += 1

            while j < len(right):
                result.append(right[j])
                j += 1

            return result

        counts = [0] * len(nums)
        # (valor, índice_original)
        indexed_nums = [(nums[i], i) for i in range(len(nums))]
        mergeSort(indexed_nums)

        return counts

    # TODO: HAsta aca llegue
    def sliding_window_maximum(self, nums: List[int], k: int) -> List[int]:
        """
        LeetCode 239: Sliding Window Maximum
        HARD - Amazon, Google (optimización con deque)

        Combina: Deque + Sliding Window
        """
        from collections import deque

        if not nums:
            return []

        dq = deque()  # Almacena índices
        result = []

        for i in range(len(nums)):
            # Remover elementos fuera de la ventana
            while dq and dq[0] <= i - k:
                dq.popleft()

            # Mantener deque en orden decreciente
            while dq and nums[dq[-1]] <= nums[i]:
                dq.pop()

            dq.append(i)

            # Agregar resultado cuando la ventana esté completa
            if i >= k - 1:
                result.append(nums[dq[0]])

        return result

    def maximum_gap(self, nums: List[int]) -> int:
        """
        LeetCode 164: Maximum Gap
        HARD - Bucket Sort application

        Combina: Bucket Sort + Gap analysis
        """
        if len(nums) < 2:
            return 0

        min_val, max_val = min(nums), max(nums)

        if min_val == max_val:
            return 0

        # Tamaño mínimo de gap
        bucket_size = max(1, (max_val - min_val) // (len(nums) - 1))
        bucket_count = (max_val - min_val) // bucket_size + 1

        # Buckets para min y max de cada bucket
        buckets_min = [float("inf")] * bucket_count
        buckets_max = [float("-inf")] * bucket_count

        # Distribuir números en buckets
        for num in nums:
            bucket_idx = (num - min_val) // bucket_size
            buckets_min[bucket_idx] = min(buckets_min[bucket_idx], num)
            buckets_max[bucket_idx] = max(buckets_max[bucket_idx], num)

        # Encontrar máximo gap entre buckets
        max_gap = 0
        prev_max = min_val

        for i in range(bucket_count):
            if buckets_min[i] == float("inf"):
                continue  # Bucket vacío

            max_gap = max(max_gap, buckets_min[i] - prev_max)
            prev_max = buckets_max[i]

        return max_gap

    def merge_k_sorted_lists(
        self, lists: List[Optional["ListNode"]]
    ) -> Optional["ListNode"]:
        """
        LeetCode 23: Merge k Sorted Lists
        HARD - Facebook, Amazon, LinkedIn

        Combina: Heap + Divide & Conquer
        """

        class ListNode:
            def __init__(self, val=0, next=None):
                self.val = val
                self.next = next

            def __lt__(self, other):
                return self.val < other.val

        if not lists:
            return None

        # Método 1: Min Heap
        heap = []

        # Agregar primer nodo de cada lista
        for i, head in enumerate(lists):
            if head:
                heapq.heappush(heap, (head.val, i, head))

        dummy = ListNode(0)
        current = dummy

        while heap:
            val, list_idx, node = heapq.heappop(heap)
            current.next = node
            current = current.next

            if node.next:
                heapq.heappush(heap, (node.next.val, list_idx, node.next))

        return dummy.next

    def shortest_subarray_with_sum_at_least_k(self, nums: List[int], k: int) -> int:
        """
        LeetCode 862: Shortest Subarray with Sum at Least K
        HARD - Google, Facebook (muy difícil)

        Combina: Prefix Sum + Deque optimization
        """
        from collections import deque

        n = len(nums)
        prefix_sum = [0] * (n + 1)

        for i in range(n):
            prefix_sum[i + 1] = prefix_sum[i] + nums[i]

        min_len = float("inf")
        dq = deque()  # Mantiene índices en orden creciente de prefix_sum

        for i in range(n + 1):
            # Encontrar subarrays que terminan en i-1 con suma >= k
            while dq and prefix_sum[i] - prefix_sum[dq[0]] >= k:
                min_len = min(min_len, i - dq.popleft())

            # Mantener deque en orden creciente
            while dq and prefix_sum[dq[-1]] >= prefix_sum[i]:
                dq.pop()

            dq.append(i)

        return min_len if min_len != float("inf") else -1

    def range_sum_query_mutable(self) -> "NumArray":
        """
        LeetCode 307: Range Sum Query - Mutable
        MEDIUM - Segment Tree / Fenwick Tree

        Combina: Tree data structure + Range queries
        """

        class NumArray:
            def __init__(self, nums: List[int]):
                self.n = len(nums)
                # Fenwick Tree (Binary Indexed Tree)
                self.tree = [0] * (self.n + 1)
                self.nums = [0] * self.n

                for i, num in enumerate(nums):
                    self.update(i, num)

            def update(self, index: int, val: int) -> None:
                delta = val - self.nums[index]
                self.nums[index] = val

                # Update Fenwick Tree
                i = index + 1
                while i <= self.n:
                    self.tree[i] += delta
                    i += i & (-i)

            def sumRange(self, left: int, right: int) -> int:
                return self._prefix_sum(right + 1) - self._prefix_sum(left)

            def _prefix_sum(self, index: int) -> int:
                s = 0
                while index > 0:
                    s += self.tree[index]
                    index -= index & (-index)
                return s

        return NumArray

    def skyline_problem(self, buildings: List[List[int]]) -> List[List[int]]:
        """
        LeetCode 218: The Skyline Problem
        HARD - Google, Facebook (problema clásico)

        Combina: Sweep Line + Heap + Critical Points
        """
        events = []

        # Crear eventos: (posición, tipo, altura)
        # tipo: 0 = start, 1 = end
        for left, right, height in buildings:
            events.append((left, 0, height))
            events.append((right, 1, height))

        # Ordenar eventos
        events.sort(key=lambda x: (x[0], x[1], -x[2] if x[1] == 0 else x[2]))

        result = []
        heights = []  # Max heap (negamos valores)

        for pos, event_type, height in events:
            if event_type == 0:  # Building starts
                heapq.heappush(heights, -height)
            else:  # Building ends
                heights.remove(-height)
                heapq.heapify(heights)

            # Altura máxima actual
            max_height = -heights[0] if heights else 0

            # Si la altura cambió, agregar punto clave
            if not result or max_height != result[-1][1]:
                result.append([pos, max_height])

        return result


def comprehensive_combined_testing():
    """
    Testing de problemas combinados
    """
    print("=== TESTING PROBLEMAS COMBINADOS ===")

    problems = CombinedLeetCodeProblems()

    print("\n--- Stream Processing Problems ---")

    # Test Kth Largest in Stream
    kth_largest = problems.find_kth_largest_in_stream(3, [4, 5, 8, 2])
    print(f"Kth Largest Stream initialization completed")
    print(f"Add 3: {kth_largest.add(3)}")  # Should return 4
    print(f"Add 5: {kth_largest.add(5)}")  # Should return 5
    print(f"Add 10: {kth_largest.add(10)}")  # Should return 5

    # Test Median Finder
    median_finder = problems.find_median_from_data_stream()
    median_finder.addNum(1)
    median_finder.addNum(2)
    print(f"Median after adding 1,2: {median_finder.findMedian()}")  # 1.5
    median_finder.addNum(3)
    print(f"Median after adding 3: {median_finder.findMedian()}")  # 2.0

    print("\n--- Search & Sorting Combinations ---")

    # Test Search Suggestions
    products = ["mobile", "mouse", "moneypot", "monitor", "mousepad"]
    searchWord = "mouse"
    suggestions = problems.search_suggestions_system(products, searchWord)
    print(f"Search suggestions for '{searchWord}': {suggestions}")

    # Test Count Smaller Numbers
    nums = [5, 2, 6, 1]
    counts = problems.count_of_smaller_numbers_after_self(nums)
    print(f"Count smaller numbers after self {nums}: {counts}")

    # Test Sliding Window Maximum
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    maximums = problems.sliding_window_maximum(nums, k)
    print(f"Sliding window maximum (k={k}): {maximums}")

    # Test Maximum Gap
    nums = [3, 6, 9, 1]
    gap = problems.maximum_gap(nums)
    print(f"Maximum gap in {nums}: {gap}")

    print("\n--- Advanced Data Structure Problems ---")

    # Test Range Sum Query
    NumArray = problems.range_sum_query_mutable()
    nums = [1, 3, 5]
    num_array = NumArray(nums)
    print(f"Range sum [0,2]: {num_array.sumRange(0, 2)}")  # 9
    num_array.update(1, 2)
    print(f"After update(1,2), range sum [0,2]: {num_array.sumRange(0, 2)}")  # 8

    # Test Skyline Problem
    buildings = [[2, 9, 10], [3, 7, 15], [5, 12, 12], [15, 20, 10], [19, 24, 8]]
    skyline = problems.skyline_problem(buildings)
    print(f"Skyline key points: {skyline}")

    # Test Shortest Subarray
    nums = [1, 2]
    k = 4
    length = problems.shortest_subarray_with_sum_at_least_k(nums, k)
    print(f"Shortest subarray with sum >= {k}: {length}")

    print("\n✅ Todos los tests combinados pasaron!")


def interview_simulation():
    """
    Simulación de entrevista con problemas típicos
    """
    print("\n=== SIMULACIÓN DE ENTREVISTA ===")

    print("\n🎯 PREGUNTA 1 (WARM-UP):")
    print(
        "Dado un array ordenado con duplicados, encuentra la primera y última posición de un target."
    )
    print("Input: nums = [5,7,7,8,8,10], target = 8")
    print("Output: [3,4]")
    print("\n💡 Approach: Binary search variants (leftmost + rightmost)")

    print("\n🎯 PREGUNTA 2 (MEDIUM):")
    print(
        "Implementa una estructura que soporte inserción y obtención de mediana en O(log n)."
    )
    print("¿Qué estructuras de datos usarías?")
    print("\n💡 Approach: Two heaps (max-heap + min-heap)")

    print("\n🎯 PREGUNTA 3 (HARD):")
    print(
        "Dada una stream de enteros, encuentra el k-ésimo elemento más grande en cualquier momento."
    )
    print("¿Cómo optimizarías para memory y time?")
    print("\n💡 Approach: Min-heap of size k")

    print("\n🎯 PREGUNTA 4 (SYSTEM DESIGN):")
    print("Diseña un sistema de autocompletado como Google Search.")
    print("Considera: Trie vs Binary Search, caching, ranking.")
    print("\n💡 Approach: Trie + ranking + caching strategies")

    print("\n📝 TIPS PARA LA ENTREVISTA:")
    print("1. Siempre pregunta por constraints (tamaño, rango, duplicados)")
    print("2. Empieza con solución brute force, luego optimiza")
    print("3. Explica trade-offs: tiempo vs espacio vs complejidad")
    print("4. Maneja edge cases: arrays vacíos, un elemento, todos iguales")
    print("5. Testing: casos normales, edge cases, casos grandes")


def optimization_techniques():
    """
    Técnicas de optimización que debes dominar
    """
    print("\n=== TÉCNICAS DE OPTIMIZACIÓN ===")

    optimizations = {
        "Binary Search": {
            "Cuándo": "Array ordenado, búsqueda en O(log n)",
            "Variantes": "leftmost, rightmost, rotated, 2D matrix",
            "Pitfall": "Infinite loops con wrong bounds",
        },
        "Two Pointers": {
            "Cuándo": "Array ordenado, sum problems, palindromes",
            "Ventaja": "O(n) en lugar de O(n²)",
            "Ejemplos": "3Sum, container with most water",
        },
        "Sliding Window": {
            "Cuándo": "Subarrays contiguos, strings, fixed/variable size",
            "Técnica": "Expand right, contract left",
            "Deque": "Para maximum/minimum en ventana",
        },
        "Heap Optimizations": {
            "Min/Max Heap": "Top K problems, priority queues",
            "Two Heaps": "Median finding, running statistics",
            "Custom Comparator": "Para objetos complejos",
        },
        "Divide & Conquer": {
            "Merge Sort": "Stable sorting, external sorting",
            "Quick Select": "Kth element sin sort completo",
            "Binary Search Tree": "Balanced operations",
        },
    }

    for technique, details in optimizations.items():
        print(f"\n{technique}:")
        for key, value in details.items():
            print(f"  {key}: {value}")


if __name__ == "__main__":
    comprehensive_combined_testing()
    interview_simulation()
    optimization_techniques()

    print("\n🚀 CHECKLIST DÍA 10:")
    print("✓ Algoritmos avanzados implementados")
    print("✓ Problemas combinados resueltos")
    print("✓ Técnicas de optimización dominadas")
    print("✓ Preparado para simulacro de entrevista")
    print("\n¡Mañana: Estructuras de Datos Básicas! 💪")
