"""
ALGORITMOS DE ORDENAMIENTO - Implementaciones para Entrevistas
Como senior, debes conocer complejidades y trade-offs de cada uno
"""

def bubble_sort(arr):
    """
    Bubble Sort: O(n²) tiempo, O(1) espacio
    Raramente usado en producción, pero bueno para explicar conceptos básicos
    """
    n = len(arr)
    arr = arr.copy()  # No modificar el array original
    
    for i in range(n):
        swapped = False
        # Optimización: elementos ya ordenados no necesitan revisarse
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        
        # Si no hubo swaps, ya está ordenado
        if not swapped:
            break
    
    return arr

def merge_sort(arr):
    """
    Merge Sort: O(n log n) tiempo, O(n) espacio
    Estable, predecible, excelente para datos grandes
    MUY COMÚN EN ENTREVISTAS
    """
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left, right):
    """
    Función auxiliar para merge sort
    Demuestra comprensión de two-pointer technique
    """
    result = []
    i = j = 0
    
    # Merge ordenado
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:  # <= mantiene estabilidad
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # Agregar elementos restantes
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result

def quick_sort(arr):
    """
    Quick Sort: O(n log n) promedio, O(n²) peor caso, O(log n) espacio
    In-place, muy rápido en práctica, pero no estable
    ALGORITMO MÁS PREGUNTADO EN ENTREVISTAS
    """
    if len(arr) <= 1:
        return arr
    
    arr = arr.copy()
    _quick_sort_helper(arr, 0, len(arr) - 1)
    return arr

def _quick_sort_helper(arr, low, high):
    """Helper para quick sort - implementación in-place"""
    if low < high:
        # Particionar y obtener pivot index
        pivot_index = partition(arr, low, high)
        
        # Recursivamente ordenar elementos antes y después del pivot
        _quick_sort_helper(arr, low, pivot_index - 1)
        _quick_sort_helper(arr, pivot_index + 1, high)

def partition(arr, low, high):
    """
    Lomuto partition scheme - más fácil de recordar en entrevistas
    Alternativa: Hoare partition (más eficiente pero más complejo)
    """
    # Elegir último elemento como pivot
    pivot = arr[high]
    i = low - 1  # Index del elemento más pequeño
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    # Colocar pivot en posición correcta
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def heap_sort(arr):
    """
    Heap Sort: O(n log n) tiempo, O(1) espacio
    No estable, pero garantiza O(n log n) en peor caso
    Menos común en entrevistas, pero demuestra conocimiento avanzado
    """
    arr = arr.copy()
    n = len(arr)
    
    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        _heapify(arr, n, i)
    
    # Extract elements from heap one by one
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]  # Move current root to end
        _heapify(arr, i, 0)  # call heapify on reduced heap
    
    return arr

def _heapify(arr, n, i):
    """Heapify subtree rooted at index i"""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    if left < n and arr[left] > arr[largest]:
        largest = left
    
    if right < n and arr[right] > arr[largest]:
        largest = right
    
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        _heapify(arr, n, largest)

# ANÁLISIS DE COMPLEJIDAD - Pregunta común en entrevistas
COMPLEXITY_ANALYSIS = {
    "bubble_sort": {
        "time_best": "O(n)",      # Array ya ordenado
        "time_average": "O(n²)",
        "time_worst": "O(n²)",    # Array invertido
        "space": "O(1)",
        "stable": True,
        "in_place": True
    },
    "merge_sort": {
        "time_best": "O(n log n)",
        "time_average": "O(n log n)",
        "time_worst": "O(n log n)",
        "space": "O(n)",
        "stable": True,
        "in_place": False
    },
    "quick_sort": {
        "time_best": "O(n log n)",
        "time_average": "O(n log n)",
        "time_worst": "O(n²)",    # Pivot siempre el menor/mayor
        "space": "O(log n)",      # Stack recursivo
        "stable": False,
        "in_place": True
    },
    "heap_sort": {
        "time_best": "O(n log n)",
        "time_average": "O(n log n)",
        "time_worst": "O(n log n)",
        "space": "O(1)",
        "stable": False,
        "in_place": True
    }
}

def test_sorting_algorithms():
    """
    Testing comprehensivo - casos que siempre debes probar
    """
    test_cases = [
        [],                    # Array vacío
        [1],                   # Un elemento
        [2, 1],               # Dos elementos
        [3, 1, 4, 1, 5],      # Con duplicados
        [5, 4, 3, 2, 1],      # Orden inverso
        [1, 2, 3, 4, 5],      # Ya ordenado
        [1, 3, 2, 5, 4, 7, 6] # Caso general
    ]
    
    algorithms = [bubble_sort, merge_sort, quick_sort, heap_sort]
    
    for test_case in test_cases:
        expected = sorted(test_case)
        
        for algorithm in algorithms:
            result = algorithm(test_case)
            assert result == expected, f"{algorithm.__name__} falló con {test_case}"
    
    print("✅ Todos los tests de ordenamiento pasaron")
    
    # Test de performance (opcional, para entrevistas avanzadas)
    import time
    import random
    
    large_array = [random.randint(1, 1000) for _ in range(1000)]
    
    print("\n📊 Performance Comparison (1000 elementos):")
    for algorithm in algorithms:
        start_time = time.time()
        algorithm(large_array)
        end_time = time.time()
        print(f"{algorithm.__name__}: {(end_time - start_time)*1000:.2f}ms")

if __name__ == "__main__":
    test_sorting_algorithms()
