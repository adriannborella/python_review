"""
HEAPS Y PRIORITY QUEUES - IMPLEMENTACIÓN COMPLETA
=================================================

Los heaps son árboles binarios COMPLETOS almacenados en arrays.
Esta implementación incluye TODAS las operaciones que pueden preguntarte:
- Insert, Extract, Peek
- Heapify (bottom-up construction)
- Heap Sort
- Priority Queue functionality

REPRESENTACIÓN EN ARRAY:
Para índice i:
- Parent: (i-1) // 2
- Left child: 2*i + 1  
- Right child: 2*i + 2

EJEMPLO MIN-HEAP:
      1
     / \
    3   6
   / \ / \
  5  9 8 15

Array: [1, 3, 6, 5, 9, 8, 15]
       0  1  2  3  4  5   6
"""

import heapq  # Para comparaciones con biblioteca estándar

class MinHeap:
    """
    Implementación completa de Min-Heap desde cero
    Todas las operaciones optimizadas para entrevistas
    """
    
    def __init__(self, initial_list=None):
        if initial_list:
            self.heap = initial_list[:]
            self.size = len(self.heap)
            self._heapify()
        else:
            self.heap = []
            self.size = 0
    
    def _parent(self, i):
        """Obtener índice del padre"""
        return (i - 1) // 2
    
    def _left_child(self, i):
        """Obtener índice del hijo izquierdo"""
        return 2 * i + 1
    
    def _right_child(self, i):
        """Obtener índice del hijo derecho"""
        return 2 * i + 2
    
    def _swap(self, i, j):
        """Intercambiar elementos en posiciones i y j"""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
    
    # ========================
    # OPERACIONES PRINCIPALES
    # ========================
    
    def peek(self):
        """
        Ver el mínimo sin extraerlo
        Complejidad: O(1)
        """
        if self.size == 0:
            raise IndexError("Heap is empty")
        return self.heap[0]
    
    def insert(self, value):
        """
        Insertar nuevo elemento
        Complejidad: O(log n)
        """
        # Agregar al final
        self.heap.append(value)
        self.size += 1
        
        # Bubble up para mantener heap property
        self._bubble_up(self.size - 1)
    
    def _bubble_up(self, index):
        """
        Mover elemento hacia arriba hasta posición correcta
        Usado después de insertar
        """
        while index > 0:
            parent_idx = self._parent(index)
            
            # Si heap property se mantiene, terminar
            if self.heap[index] >= self.heap[parent_idx]:
                break
            
            # Intercambiar con padre y continuar
            self._swap(index, parent_idx)
            index = parent_idx
    
    def extract_min(self):
        """
        Extraer y retornar el mínimo elemento
        Complejidad: O(log n)
        """
        if self.size == 0:
            raise IndexError("Heap is empty")
        
        # El mínimo está en la raíz
        min_val = self.heap[0]
        
        # Mover último elemento a la raíz
        self.heap[0] = self.heap[self.size - 1]
        self.heap.pop()
        self.size -= 1
        
        # Bubble down para restaurar heap property
        if self.size > 0:
            self._bubble_down(0)
        
        return min_val
    
    def _bubble_down(self, index):
        """
        Mover elemento hacia abajo hasta posición correcta
        Usado después de extract_min
        """
        while True:
            smallest = index
            left = self._left_child(index)
            right = self._right_child(index)
            
            # Encontrar el más pequeño entre padre e hijos
            if (left < self.size and 
                self.heap[left] < self.heap[smallest]):
                smallest = left
            
            if (right < self.size and 
                self.heap[right] < self.heap[smallest]):
                smallest = right
            
            # Si heap property se mantiene, terminar
            if smallest == index:
                break
            
            # Intercambiar y continuar
            self._swap(index, smallest)
            index = smallest
    
    def _heapify(self):
        """
        Convertir array arbitrario en heap válido
        Complejidad: O(n) - ¡Más eficiente que insertar uno por uno!
        """
        # Comenzar desde el último padre y hacer bubble_down
        start = self._parent(self.size - 1)
        for i in range(start, -1, -1):
            self._bubble_down(i)
    
    # ========================
    # OPERACIONES AVANZADAS
    # ========================
    
    def replace(self, value):
        """
        Extraer min y insertar nuevo valor en una operación
        Más eficiente que extract + insert por separado
        """
        if self.size == 0:
            raise IndexError("Heap is empty")
        
        old_min = self.heap[0]
        self.heap[0] = value
        self._bubble_down(0)
        return old_min
    
    def delete(self, index):
        """
        Eliminar elemento en índice específico
        Complejidad: O(log n)
        """
        if index >= self.size:
            raise IndexError("Index out of bounds")
        
        # Reemplazar con último elemento
        self.heap[index] = self.heap[self.size - 1]
        self.heap.pop()
        self.size -= 1
        
        if self.size > 0 and index < self.size:
            # Puede necesitar bubble up o down
            parent_idx = self._parent(index)
            if (index > 0 and 
                self.heap[index] < self.heap[parent_idx]):
                self._bubble_up(index)
            else:
                self._bubble_down(index)
    
    def heap_sort(self):
        """
        Ordenar usando heap sort
        Complejidad: O(n log n)
        """
        original_size = self.size
        result = []
        
        while self.size > 0:
            result.append(self.extract_min())
        
        # Restaurar heap original
        self.heap = result[:]
        self.size = original_size
        self._heapify()
        
        return result
    
    # ========================
    # UTILIDADES
    # ========================
    
    def is_empty(self):
        return self.size == 0
    
    def __len__(self):
        return self.size
    
    def __str__(self):
        return f"MinHeap({self.heap[:self.size]})"
    
    def display_tree(self):
        """Mostrar heap como árbol (para debug)"""
        if self.size == 0:
            print("Empty heap")
            return
        
        def display_recursive(index, level=0):
            if index >= self.size:
                return
            
            # Mostrar hijo derecho
            right = self._right_child(index)
            if right < self.size:
                display_recursive(right, level + 1)
            
            # Mostrar nodo actual
            print("  " * level + f"├── {self.heap[index]}")
            
            # Mostrar hijo izquierdo
            left = self._left_child(index)
            if left < self.size:
                display_recursive(left, level + 1)
        
        print("Heap as tree:")
        display_recursive(0)

class MaxHeap:
    """
    Max-Heap implementado usando Min-Heap con valores negados
    Trick común en entrevistas cuando solo tienes min-heap disponible
    """
    
    def __init__(self, initial_list=None):
        # Negar todos los valores para simular max-heap
        if initial_list:
            negated = [-x for x in initial_list]
            self.min_heap = MinHeap(negated)
        else:
            self.min_heap = MinHeap()
    
    def insert(self, value):
        self.min_heap.insert(-value)
    
    def extract_max(self):
        return -self.min_heap.extract_min()
    
    def peek(self):
        return -self.min_heap.peek()
    
    def is_empty(self):
        return self.min_heap.is_empty()
    
    def __len__(self):
        return len(self.min_heap)
    
    def __str__(self):
        # Mostrar valores originales (no negados)
        original_values = [-x for x in self.min_heap.heap[:self.min_heap.size]]
        return f"MaxHeap({original_values})"

class PriorityQueue:
    """
    Priority Queue usando Min-Heap
    Elementos con menor prioridad salen primero
    """
    
    def __init__(self):
        self.heap = MinHeap()
        self.entry_count = 0  # Para handle ties
    
    def push(self, item, priority):
        """Agregar item con prioridad dada"""
        # Usar entry_count para mantener orden FIFO en ties
        entry = (priority, self.entry_count, item)
        self.heap.insert(entry)
        self.entry_count += 1
    
    def pop(self):
        """Extraer item con mayor prioridad (menor número)"""
        if self.heap.is_empty():
            raise IndexError("Priority queue is empty")
        
        priority, _, item = self.heap.extract_min()
        return item
    
    def peek(self):
        """Ver próximo item sin extraerlo"""
        if self.heap.is_empty():
            raise IndexError("Priority queue is empty")
        
        priority, _, item = self.heap.peek()
        return item
    
    def is_empty(self):
        return self.heap.is_empty()
    
    def __len__(self):
        return len(self.heap)

# ========================
# TESTING COMPREHENSIVO
# ========================

def test_min_heap():
    """Test completo de Min-Heap"""
    print("=== TESTING MIN-HEAP ===\n")
    
    # Test construcción vacía
    heap = MinHeap()
    print("1. EMPTY HEAP:")
    print(f"   Empty: {heap.is_empty()}")
    print(f"   Size: {len(heap)}")
    
    # Test inserción
    print("\n2. INSERTIONS:")
    values = [15, 10, 20, 8, 25, 5, 7]
    for val in values:
        heap.insert(val)
        print(f"   Inserted {val}: {heap}")
    
    print(f"   Tree structure:")
    heap.display_tree()
    
    # Test peek
    print(f"\n3. PEEK:")
    print(f"   Minimum: {heap.peek()}")
    
    # Test extractions
    print(f"\n4. EXTRACTIONS:")
    extracted = []
    while not heap.is_empty():
        min_val = heap.extract_min()
        extracted.append(min_val)
        print(f"   Extracted {min_val}, remaining: {heap}")
    
    print(f"   All extracted (should be sorted): {extracted}")
    
    # Test heapify
    print(f"\n5. HEAPIFY:")
    unsorted = [20, 15, 8, 10, 5, 7, 6, 2, 9, 1]
    heap2 = MinHeap(unsorted)
    print(f"   Original: {unsorted}")
    print(f"   Heapified: {heap2}")
    print(f"   Sorted: {heap2.heap_sort()}")

def test_max_heap():
    """Test de Max-Heap"""
    print("\n=== TESTING MAX-HEAP ===\n")
    
    max_heap = MaxHeap([1, 3, 6, 5, 2, 4])
    print(f"Initial max-heap: {max_heap}")
    print(f"Max element: {max_heap.peek()}")
    
    max_heap.insert(10)
    print(f"After inserting 10: {max_heap}")
    
    print("Extracting all elements:")
    while not max_heap.is_empty():
        max_val = max_heap.extract_max()
        print(f"   Extracted {max_val}")

def test_priority_queue():
    """Test de Priority Queue"""
    print("\n=== TESTING PRIORITY QUEUE ===\n")
    
    pq = PriorityQueue()
    
    # Agregar tareas con diferentes prioridades
    tasks = [
        ("Send email", 3),
        ("Fix critical bug", 1),  # Máxima prioridad
        ("Update documentation", 5),
        ("Code review", 2),
        ("Meeting prep", 4)
    ]
    
    print("Adding tasks:")
    for task, priority in tasks:
        pq.push(task, priority)
        print(f"   Added: {task} (priority {priority})")
    
    print(f"\nProcessing tasks in priority order:")
    while not pq.is_empty():
        task = pq.pop()
        print(f"   Processing: {task}")

def benchmark_vs_builtin():
    """Comparar con heapq de Python"""
    import time
    import random
    
    print("\n=== PERFORMANCE COMPARISON ===\n")
    
    # Generar datos de prueba
    data = [random.randint(1, 10000) for _ in range(1000)]
    
    # Test nuestra implementación
    start = time.time()
    our_heap = MinHeap(data[:])
    for _ in range(100):
        our_heap.extract_min()
        our_heap.insert(random.randint(1, 10000))
    our_time = time.time() - start
    
    # Test heapq builtin
    start = time.time()
    builtin_heap = data[:]
    heapq.heapify(builtin_heap)
    for _ in range(100):
        heapq.heappop(builtin_heap)
        heapq.heappush(builtin_heap, random.randint(1, 10000))
    builtin_time = time.time() - start
    
    print(f"Our implementation: {our_time:.4f}s")
    print(f"Built-in heapq: {builtin_time:.4f}s")
    print(f"Ratio: {our_time/builtin_time:.2f}x")

if __name__ == "__main__":
    test_min_heap()
    test_max_heap()
    test_priority_queue()
    benchmark_vs_builtin()
