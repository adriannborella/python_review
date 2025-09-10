"""
PROBLEMAS CLÁSICOS CON HEAPS - DÍA 20
Problemas más frecuentes en entrevistas técnicas
"""

import heapq
from typing import List, Optional
from collections import defaultdict, Counter


class ListNode:
    """Definición de nodo para listas enlazadas"""
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# PROBLEMA 1: TOP K FREQUENT ELEMENTS
def top_k_frequent(nums: List[int], k: int) -> List[int]:
    """
    Encuentra los k elementos más frecuentes en un array
    
    Enfoque: Heap + Hash Map
    Complejidad: O(n log k)
    
    Ejemplo: nums = [1,1,1,2,2,3], k = 2
    Output: [1,2]
    """
    # Paso 1: Contar frecuencias
    freq_map = Counter(nums)
    
    # Paso 2: Usar min-heap de tamaño k
    # Mantenemos los k elementos MÁS frecuentes
    heap = []
    
    for num, freq in freq_map.items():
        if len(heap) < k:
            heapq.heappush(heap, (freq, num))
        elif freq > heap[0][0]:  # Más frecuente que el mínimo actual
            heapq.heapreplace(heap, (freq, num))
    
    # Extraer elementos del heap
    return [num for freq, num in heap]


# PROBLEMA 2: MERGE K SORTED LINKED LISTS
def merge_k_lists(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    """
    Merge k sorted linked lists y retorna una sola lista ordenada
    
    Enfoque: Min-heap con comparación de valores
    Complejidad: O(n log k) donde n = total de nodos
    
    TRUCO DE ENTREVISTA: heapq no puede comparar ListNode directamente,
    necesitamos usar tuplas con índices únicos
    """
    heap = []
    dummy = ListNode(0)
    current = dummy
    
    # Inicializar heap con primer nodo de cada lista
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))
    
    # Counter para manejar casos donde node.val es igual
    counter = len(lists)
    
    while heap:
        val, i, node = heapq.heappop(heap)
        current.next = ListNode(val)
        current = current.next
        
        # Agregar siguiente nodo de la misma lista
        if node.next:
            heapq.heappush(heap, (node.next.val, counter, node.next))
            counter += 1
    
    return dummy.next


# PROBLEMA 3: FIND MEDIAN FROM DATA STREAM
class MedianFinder:
    """
    Encuentra la mediana de un stream de datos
    
    Enfoque: Dos heaps (max-heap para mitad menor, min-heap para mitad mayor)
    Complejidad: addNum O(log n), findMedian O(1)
    
    CONCEPTO CLAVE: Balance entre dos heaps
    """
    def __init__(self):
        # Max-heap para la mitad menor (negamos valores)
        self.small = []  # max heap (valores negativos)
        # Min-heap para la mitad mayor  
        self.large = []  # min heap
    
    def addNum(self, num: int) -> None:
        # Siempre agregar a small primero (max-heap)
        heapq.heappush(self.small, -num)
        
        # Asegurar que max(small) <= min(large)
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        
        # Balance de tamaños: diferencia máxima de 1
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
            return (-self.small[0] + self.large[0]) / 2


# PROBLEMA 4: SLIDING WINDOW MAXIMUM
def max_sliding_window(nums: List[int], k: int) -> List[int]:
    """
    Encuentra el máximo en cada ventana deslizante de tamaño k
    
    Enfoque alternativo con heap: Lazy deletion
    Complejidad: O(n log k)
    
    Ejemplo: nums = [1,3,-1,-3,5,3,6,7], k = 3
    Output: [3,3,5,5,6,7]
    """
    if not nums or k == 0:
        return []
    
    result = []
    # Max-heap con (valor_negativo, índice)
    heap = []
    
    for i, num in enumerate(nums):
        # Agregar elemento actual
        heapq.heappush(heap, (-num, i))
        
        # Si tenemos ventana completa
        if i >= k - 1:
            # Lazy deletion: remover elementos fuera de ventana
            while heap and heap[0][1] <= i - k:
                heapq.heappop(heap)
            
            # El máximo actual
            result.append(-heap[0][0])
    
    return result


# PROBLEMA 5: K CLOSEST POINTS TO ORIGIN
def k_closest(points: List[List[int]], k: int) -> List[List[int]]:
    """
    Encuentra los k puntos más cercanos al origen
    
    Enfoque: Max-heap de tamaño k con distancias
    Complejidad: O(n log k)
    """
    heap = []
    
    for point in points:
        x, y = point
        distance = x*x + y*y  # No necesitamos sqrt para comparar
        
        if len(heap) < k:
            # Negamos para simular max-heap
            heapq.heappush(heap, (-distance, point))
        elif distance < -heap[0][0]:
            heapq.heapreplace(heap, (-distance, point))
    
    return [point for dist, point in heap]


# PROBLEMA 6: TASK SCHEDULER
def least_interval(tasks: List[str], n: int) -> int:
    """
    Calcula el tiempo mínimo para ejecutar todas las tareas con cooldown n
    
    Enfoque: Max-heap + Queue para cooldown
    Complejidad: O(m log m) donde m = unique tasks
    
    Ejemplo: tasks = ["A","A","A","B","B","B"], n = 2
    Output: 8 (A -> B -> idle -> A -> B -> idle -> A -> B)
    """
    # Contar frecuencias
    task_count = Counter(tasks)
    
    # Max-heap con frecuencias (valores negativos)
    heap = [-count for count in task_count.values()]
    heapq.heapify(heap)
    
    time = 0
    # Queue para manejar cooldown: (count, available_time)
    cooldown_queue = []
    
    while heap or cooldown_queue:
        time += 1
        
        # Mover tareas del cooldown de vuelta al heap
        if cooldown_queue and cooldown_queue[0][1] == time:
            heapq.heappush(heap, cooldown_queue.pop(0)[0])
        
        if heap:
            # Ejecutar tarea más frecuente
            count = heapq.heappop(heap)
            if count < -1:  # Aún quedan ejecuciones
                # Agregar a cooldown
                cooldown_queue.append((count + 1, time + n + 1))
    
    return time


# PROBLEMA 7: UGLY NUMBER II
def nth_ugly_number(n: int) -> int:
    """
    Encuentra el n-ésimo ugly number (solo factores 2, 3, 5)
    
    Enfoque: Min-heap para generar ugly numbers en orden
    Complejidad: O(n log n)
    
    Sequence: 1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, ...
    """
    heap = [1]
    seen = {1}
    
    for i in range(n):
        ugly = heapq.heappop(heap)
        
        # Generar siguientes ugly numbers
        for factor in [2, 3, 5]:
            new_ugly = ugly * factor
            if new_ugly not in seen:
                seen.add(new_ugly)
                heapq.heappush(heap, new_ugly)
    
    return ugly


# PROBLEMA 8: REORGANIZE STRING
def reorganize_string(s: str) -> str:
    """
    Reorganiza string para que no haya caracteres adyacentes iguales
    
    Enfoque: Max-heap con frecuencias + greedy approach
    Complejidad: O(n log k) donde k = unique characters
    """
    # Contar frecuencias
    count = Counter(s)
    
    # Verificar si es posible
    max_count = max(count.values())
    if max_count > (len(s) + 1) // 2:
        return ""
    
    # Max-heap con frecuencias
    heap = [(-freq, char) for char, freq in count.items()]
    heapq.heapify(heap)
    
    result = []
    prev_char = None
    prev_count = 0
    
    while heap:
        # Tomar el más frecuente disponible
        freq, char = heapq.heappop(heap)
        result.append(char)
        
        # Poner el anterior de vuelta si aún tiene count
        if prev_count < 0:
            heapq.heappush(heap, (prev_count, prev_char))
        
        # Actualizar para siguiente iteración
        prev_char = char
        prev_count = freq + 1  # Incrementar porque era negativo
    
    return ''.join(result)


# FUNCIONES DE TESTING
def test_heap_problems():
    """Prueba todos los problemas implementados"""
    
    print("=== TOP K FREQUENT ===")
    nums = [1, 1, 1, 2, 2, 3]
    k = 2
    result = top_k_frequent(nums, k)
    print(f"nums: {nums}, k: {k}")
    print(f"Top {k} frequent: {result}")
    
    print("\n=== MEDIAN FINDER ===")
    mf = MedianFinder()
    stream = [5, 15, 1, 3]
    for num in stream:
        mf.addNum(num)
        print(f"Added {num}, median: {mf.findMedian()}")
    
    print("\n=== SLIDING WINDOW MAXIMUM ===")
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    result = max_sliding_window(nums, k)
    print(f"nums: {nums}, k: {k}")
    print(f"Window maximums: {result}")
    
    print("\n=== K CLOSEST POINTS ===")
    points = [[1, 1], [1, 3], [3, 4], [2, 1], [-1, 1]]
    k = 3
    result = k_closest(points, k)
    print(f"Points: {points}, k: {k}")
    print(f"K closest: {result}")
    
    print("\n=== TASK SCHEDULER ===")
    tasks = ["A", "A", "A", "B", "B", "B"]
    n = 2
    result = least_interval(tasks, n)
    print(f"Tasks: {tasks}, cooldown: {n}")
    print(f"Minimum time: {result}")
    
    print("\n=== NTH UGLY NUMBER ===")
    n = 10
    result = nth_ugly_number(n)
    print(f"The {n}th ugly number: {result}")
    
    print("\n=== REORGANIZE STRING ===")
    s = "aab"
    result = reorganize_string(s)
    print(f"Original: '{s}', Reorganized: '{result}'")


# TIPS PARA ENTREVISTAS CON HEAPS
def heap_interview_tips():
    """
    TIPS CLAVE PARA ENTREVISTAS:
    
    1. CUÁNDO USAR HEAPS:
       - Top K problems
       - Median/percentile calculations
       - Priority-based scheduling
       - Merge operations
       - Stream processing
    
    2. TIPOS DE HEAP:
       - Min-heap: Para k-largest, median (right half)
       - Max-heap: Para k-smallest, median (left half)
    
    3. PYTHON HEAPQ TRICKS:
       - Solo min-heap: usar valores negativos para max-heap
       - Tuplas: (priority, counter, item) para evitar comparación de items
       - heapreplace() es más eficiente que pop() + push()
       - Lazy deletion: marcar como inválido en vez de buscar y remover
    
    4. PATRONES COMUNES:
       - Two heaps (median): balance automático
       - K-sized heap: mantener tamaño fijo
       - Frequency + heap: Counter + heap
       - Stream processing: heap + queue/deque
    
    5. COMPLEJIDADES TÍPICAS:
       - Insert/Extract: O(log n)
       - Build heap: O(n)
       - Top K from N elements: O(n log k)
    
    6. ERRORES COMUNES:
       - No manejar heaps vacíos
       - Comparar objetos no comparables
       - No balancear two-heap approach
       - Confundir min/max heap requirements
    """
    pass


if __name__ == "__main__":
    test_heap_problems()
    print("\n" + "="*50)
    heap_interview_tips()