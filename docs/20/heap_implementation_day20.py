"""
HEAP IMPLEMENTATION - DÍA 20
Implementación completa de Min-Heap y Max-Heap desde cero
Complejidades: Insert O(log n), Extract O(log n), Peek O(1)
"""

class MinHeap:
    """
    Implementación de Min-Heap (el elemento más pequeño está en la raíz)
    """
    def __init__(self):
        self.heap = []
    
    def parent(self, i):
        """Retorna el índice del padre"""
        return (i - 1) // 2
    
    def left_child(self, i):
        """Retorna el índice del hijo izquierdo"""
        return 2 * i + 1
    
    def right_child(self, i):
        """Retorna el índice del hijo derecho"""
        return 2 * i + 2
    
    def has_parent(self, i):
        """Verifica si el nodo tiene padre"""
        return self.parent(i) >= 0
    
    def has_left_child(self, i):
        """Verifica si el nodo tiene hijo izquierdo"""
        return self.left_child(i) < len(self.heap)
    
    def has_right_child(self, i):
        """Verifica si el nodo tiene hijo derecho"""
        return self.right_child(i) < len(self.heap)
    
    def swap(self, i, j):
        """Intercambia elementos en posiciones i y j"""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
    
    def peek(self):
        """Retorna el elemento mínimo sin eliminarlo - O(1)"""
        if not self.heap:
            raise IndexError("Heap is empty")
        return self.heap[0]
    
    def insert(self, value):
        """Inserta un nuevo elemento - O(log n)"""
        # Agregar al final
        self.heap.append(value)
        # Hacer heapify hacia arriba
        self._heapify_up(len(self.heap) - 1)
    
    def extract_min(self):
        """Extrae el elemento mínimo - O(log n)"""
        if not self.heap:
            raise IndexError("Heap is empty")
        
        if len(self.heap) == 1:
            return self.heap.pop()
        
        # Guardar el mínimo
        min_value = self.heap[0]
        # Mover el último elemento a la raíz
        self.heap[0] = self.heap.pop()
        # Hacer heapify hacia abajo
        self._heapify_down(0)
        
        return min_value
    
    def _heapify_up(self, index):
        """Mueve un elemento hacia arriba hasta mantener la propiedad del heap"""
        while (self.has_parent(index) and 
               self.heap[self.parent(index)] > self.heap[index]):
            self.swap(index, self.parent(index))
            index = self.parent(index)
    
    def _heapify_down(self, index):
        """Mueve un elemento hacia abajo hasta mantener la propiedad del heap"""
        while self.has_left_child(index):
            smaller_child_index = self.left_child(index)
            
            # Encontrar el hijo más pequeño
            if (self.has_right_child(index) and 
                self.heap[self.right_child(index)] < self.heap[smaller_child_index]):
                smaller_child_index = self.right_child(index)
            
            # Si el padre es menor que el hijo más pequeño, terminamos
            if self.heap[index] <= self.heap[smaller_child_index]:
                break
            
            self.swap(index, smaller_child_index)
            index = smaller_child_index
    
    def build_heap(self, arr):
        """Construye heap desde array - O(n)"""
        self.heap = arr.copy()
        # Comenzar desde el último nodo interno hacia atrás
        for i in range(len(arr) // 2 - 1, -1, -1):
            self._heapify_down(i)
    
    def is_empty(self):
        """Verifica si el heap está vacío"""
        return len(self.heap) == 0
    
    def size(self):
        """Retorna el tamaño del heap"""
        return len(self.heap)
    
    def __str__(self):
        """Representación string del heap"""
        return str(self.heap)


class MaxHeap:
    """
    Implementación de Max-Heap (el elemento más grande está en la raíz)
    Reutiliza MinHeap invirtiendo las comparaciones
    """
    def __init__(self):
        self.heap = []
    
    def parent(self, i):
        return (i - 1) // 2
    
    def left_child(self, i):
        return 2 * i + 1
    
    def right_child(self, i):
        return 2 * i + 2
    
    def has_parent(self, i):
        return self.parent(i) >= 0
    
    def has_left_child(self, i):
        return self.left_child(i) < len(self.heap)
    
    def has_right_child(self, i):
        return self.right_child(i) < len(self.heap)
    
    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
    
    def peek(self):
        """Retorna el elemento máximo sin eliminarlo - O(1)"""
        if not self.heap:
            raise IndexError("Heap is empty")
        return self.heap[0]
    
    def insert(self, value):
        """Inserta un nuevo elemento - O(log n)"""
        self.heap.append(value)
        self._heapify_up(len(self.heap) - 1)
    
    def extract_max(self):
        """Extrae el elemento máximo - O(log n)"""
        if not self.heap:
            raise IndexError("Heap is empty")
        
        if len(self.heap) == 1:
            return self.heap.pop()
        
        max_value = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        
        return max_value
    
    def _heapify_up(self, index):
        """Para Max-Heap: el padre debe ser >= que el hijo"""
        while (self.has_parent(index) and 
               self.heap[self.parent(index)] < self.heap[index]):
            self.swap(index, self.parent(index))
            index = self.parent(index)
    
    def _heapify_down(self, index):
        """Para Max-Heap: el padre debe ser >= que sus hijos"""
        while self.has_left_child(index):
            larger_child_index = self.left_child(index)
            
            if (self.has_right_child(index) and 
                self.heap[self.right_child(index)] > self.heap[larger_child_index]):
                larger_child_index = self.right_child(index)
            
            if self.heap[index] >= self.heap[larger_child_index]:
                break
            
            self.swap(index, larger_child_index)
            index = larger_child_index
    
    def build_heap(self, arr):
        """Construye heap desde array - O(n)"""
        self.heap = arr.copy()
        for i in range(len(arr) // 2 - 1, -1, -1):
            self._heapify_down(i)
    
    def is_empty(self):
        return len(self.heap) == 0
    
    def size(self):
        return len(self.heap)
    
    def __str__(self):
        return str(self.heap)


class PriorityQueue:
    """
    Priority Queue usando heap (puede ser min o max)
    Útil para problemas donde necesitamos prioridades
    """
    def __init__(self, is_max_heap=False):
        self.is_max = is_max_heap
        self.heap = []
    
    def push(self, item, priority):
        """Agregar elemento con prioridad"""
        if self.is_max:
            # Para max-heap, negamos la prioridad
            heapq.heappush(self.heap, (-priority, item))
        else:
            heapq.heappush(self.heap, (priority, item))
    
    def pop(self):
        """Extraer elemento con mayor/menor prioridad"""
        if not self.heap:
            raise IndexError("Priority queue is empty")
        
        if self.is_max:
            priority, item = heapq.heappop(self.heap)
            return item, -priority
        else:
            priority, item = heapq.heappop(self.heap)
            return item, priority
    
    def peek(self):
        """Ver elemento con mayor/menor prioridad sin extraerlo"""
        if not self.heap:
            raise IndexError("Priority queue is empty")
        
        if self.is_max:
            priority, item = self.heap[0]
            return item, -priority
        else:
            priority, item = self.heap[0]
            return item, priority
    
    def is_empty(self):
        return len(self.heap) == 0
    
    def size(self):
        return len(self.heap)


# TESTING Y EJEMPLOS DE USO
import heapq

def test_heap_implementations():
    """Testing completo de las implementaciones"""
    print("=== TESTING MIN HEAP ===")
    min_heap = MinHeap()
    
    # Test básico
    elements = [4, 10, 3, 5, 1, 6, 9, 2, 8, 7]
    print(f"Insertando elementos: {elements}")
    
    for elem in elements:
        min_heap.insert(elem)
        print(f"Después de insertar {elem}: {min_heap}")
    
    print("\nExtrayendo elementos en orden:")
    sorted_elements = []
    while not min_heap.is_empty():
        min_elem = min_heap.extract_min()
        sorted_elements.append(min_elem)
        print(f"Extraído: {min_elem}, Heap restante: {min_heap}")
    
    print(f"Elementos ordenados: {sorted_elements}")
    
    print("\n=== TESTING MAX HEAP ===")
    max_heap = MaxHeap()
    
    # Build heap from array
    arr = [4, 10, 3, 5, 1, 6, 9, 2, 8, 7]
    max_heap.build_heap(arr)
    print(f"Max heap construido desde {arr}: {max_heap}")
    
    print("Extrayendo los 3 elementos más grandes:")
    for i in range(3):
        if not max_heap.is_empty():
            max_elem = max_heap.extract_max()
            print(f"Extraído: {max_elem}")
    
    print("\n=== TESTING PRIORITY QUEUE ===")
    pq = PriorityQueue()
    
    # Simulando sistema de tareas con prioridades
    tasks = [
        ("Revisar email", 3),
        ("Llamar cliente", 1),  # Mayor prioridad (menor número)
        ("Escribir reporte", 5),
        ("Meeting", 2)
    ]
    
    print("Agregando tareas con prioridades:")
    for task, priority in tasks:
        pq.push(task, priority)
        print(f"  {task} (prioridad: {priority})")
    
    print("\nProcesando tareas por prioridad:")
    while not pq.is_empty():
        task, priority = pq.pop()
        print(f"  Procesando: {task} (prioridad: {priority})")


if __name__ == "__main__":
    test_heap_implementations()


# EJERCICIOS PARA PRACTICAR:

def heap_sort(arr):
    """
    Implementa heap sort usando nuestro MaxHeap
    Complejidad: O(n log n)
    """
    if not arr:
        return arr
    
    # Crear max heap
    max_heap = MaxHeap()
    max_heap.build_heap(arr)
    
    # Extraer elementos en orden descendente
    sorted_arr = []
    while not max_heap.is_empty():
        sorted_arr.append(max_heap.extract_max())
    
    # Para orden ascendente, revertir
    return sorted_arr[::-1]


def find_kth_largest(arr, k):
    """
    Encuentra el k-ésimo elemento más grande
    Usando min-heap de tamaño k - O(n log k)
    """
    if k > len(arr) or k <= 0:
        return None
    
    # Usar heapq (min-heap) de Python para eficiencia
    import heapq
    
    # Mantener heap de tamaño k con los k elementos más grandes
    heap = []
    
    for num in arr:
        if len(heap) < k:
            heapq.heappush(heap, num)
        elif num > heap[0]:  # num es mayor que el mínimo actual
            heapq.heapreplace(heap, num)  # Reemplaza y mantiene heap
    
    return heap[0]  # El mínimo del heap es el k-ésimo más grande


def merge_k_sorted_lists(lists):
    """
    PROBLEMA CLÁSICO: Merge K Sorted Lists
    Usando min-heap para eficiencia - O(n log k)
    """
    import heapq
    
    heap = []
    result = []
    
    # Inicializar heap con primer elemento de cada lista
    for i, lst in enumerate(lists):
        if lst:  # Si la lista no está vacía
            heapq.heappush(heap, (lst[0], i, 0))  # (valor, lista_id, índice)
    
    while heap:
        val, list_id, idx = heapq.heappop(heap)
        result.append(val)
        
        # Agregar siguiente elemento de la misma lista
        if idx + 1 < len(lists[list_id]):
            next_val = lists[list_id][idx + 1]
            heapq.heappush(heap, (next_val, list_id, idx + 1))
    
    return result


# EJEMPLOS DE TESTING ADICIONALES
def additional_examples():
    """Ejemplos adicionales para practicar"""
    
    print("=== HEAP SORT ===")
    arr = [64, 34, 25, 12, 22, 11, 90]
    print(f"Array original: {arr}")
    sorted_arr = heap_sort(arr)
    print(f"Array ordenado: {sorted_arr}")
    
    print("\n=== KTH LARGEST ===")
    nums = [3, 2, 1, 5, 6, 4]
    k = 2
    kth = find_kth_largest(nums, k)
    print(f"El {k}º elemento más grande de {nums} es: {kth}")
    
    print("\n=== MERGE K SORTED LISTS ===")
    lists = [
        [1, 4, 5],
        [1, 3, 4],
        [2, 6]
    ]
    merged = merge_k_sorted_lists(lists)
    print(f"Listas: {lists}")
    print(f"Merged: {merged}")


if __name__ == "__main__":
    test_heap_implementations()
    print("\n" + "="*50)
    additional_examples()
