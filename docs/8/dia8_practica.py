"""
DÍA 8: PRÁCTICA - ANÁLISIS DE COMPLEJIDAD DE ALGORITMOS
Tiempo: 45 minutos de coding intensivo
Objetivo: Analizar y calcular Big O de diferentes soluciones
"""

import time
import random
from typing import List, Dict, Optional

# =============================================================================
# EXERCISE 1: ANÁLISIS DE ALGORITMOS DE BÚSQUEDA (10 minutos)
# =============================================================================

def linear_search_analysis(arr: List[int], target: int) -> tuple:
    """
    Implementa búsqueda lineal y analiza su complejidad
    
    TODO: 
    1. Implementa el algoritmo
    2. Analiza caso mejor, promedio y peor
    3. Determine complejidad espacial
    
    Return: (index, comparisons_made)
    """
    comparisons = 0
    
    for i in range(len(arr)):
        comparisons += 1
        if arr[i] == target:
            return i, comparisons  # Mejor caso: O(1)
    
    return -1, comparisons  # Peor caso: O(n)
    
    # ANÁLISIS:
    # Temporal: Mejor O(1), Promedio O(n/2), Peor O(n) → O(n)
    # Espacial: O(1) - solo variables auxiliares

def binary_search_analysis(arr: List[int], target: int) -> tuple:
    """
    Implementa búsqueda binaria y analiza su complejidad
    
    TODO:
    1. Implementa búsqueda binaria iterativa
    2. Cuenta comparisons realizadas
    3. Analiza por qué es O(log n)
    
    Prerequisito: arr debe estar ordenado
    """
    left, right = 0, len(arr) - 1
    comparisons = 0
    
    while left <= right:
        comparisons += 1
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid, comparisons
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1, comparisons
    
    # ANÁLISIS:
    # Temporal: O(log n) - divide por 2 cada iteración
    # Espacial: O(1) - iterativo usa espacio constante

def exponential_search_analysis(arr: List[int], target: int) -> tuple:
    """
    Búsqueda exponencial + binaria
    
    TODO: Implementa y analiza este algoritmo híbrido:
    1. Encuentra rango exponencialmente: 1, 2, 4, 8, 16...
    2. Aplica búsqueda binaria en el rango encontrado
    """
    if len(arr) == 0:
        return -1, 0
    
    if arr[0] == target:
        return 0, 1
    
    # Fase 1: Búsqueda exponencial del rango
    i = 1
    comparisons = 1  # Ya comparamos arr[0]
    
    while i < len(arr) and arr[i] <= target:
        comparisons += 1
        if arr[i] == target:
            return i, comparisons
        i *= 2
    
    # Fase 2: Búsqueda binaria en el rango [i//2, min(i, len(arr)-1)]
    left = i // 2
    right = min(i, len(arr) - 1)
    
    while left <= right:
        comparisons += 1
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid, comparisons
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1, comparisons
    
    # ANÁLISIS:
    # Temporal: O(log n) - ambas fases son logarítmicas
    # Ventaja: Mejor para arrays infinitos o muy grandes

# =============================================================================
# EXERCISE 2: ALGORITMOS DE ORDENAMIENTO - ANÁLISIS COMPARATIVO (15 minutos)
# =============================================================================

def bubble_sort_analysis(arr: List[int]) -> tuple:
    """
    Bubble Sort con análisis detallado
    
    TODO:
    1. Implementa bubble sort
    2. Cuenta swaps y comparisons
    3. Analiza por qué es O(n²)
    """
    arr_copy = arr.copy()
    n = len(arr_copy)
    comparisons = 0
    swaps = 0
    
    for i in range(n):
        swapped = False  # Optimización para detectar arrays ordenados
        
        for j in range(0, n - i - 1):
            comparisons += 1
            if arr_copy[j] > arr_copy[j + 1]:
                arr_copy[j], arr_copy[j + 1] = arr_copy[j + 1], arr_copy[j]
                swaps += 1
                swapped = True
        
        if not swapped:  # Si no hubo swaps, está ordenado
            break
    
    return arr_copy, comparisons, swaps
    
    # ANÁLISIS:
    # Mejor caso: O(n) - array ya ordenado, solo comparisons
    # Peor caso: O(n²) - array invertido, máximos swaps
    # Promedio: O(n²)
    # Espacial: O(1) - in-place

def selection_sort_analysis(arr: List[int]) -> tuple:
    """
    Selection Sort con análisis
    
    TODO:
    1. Implementa selection sort
    2. Analiza por qué siempre es O(n²)
    3. Compara con bubble sort
    """
    arr_copy = arr.copy()
    n = len(arr_copy)
    comparisons = 0
    swaps = 0
    
    for i in range(n):
        min_idx = i
        
        # Buscar el mínimo en el resto del array
        for j in range(i + 1, n):
            comparisons += 1
            if arr_copy[j] < arr_copy[min_idx]:
                min_idx = j
        
        # Swap si encontramos un mínimo diferente
        if min_idx != i:
            arr_copy[i], arr_copy[min_idx] = arr_copy[min_idx], arr_copy[i]
            swaps += 1
    
    return arr_copy, comparisons, swaps
    
    # ANÁLISIS:
    # Todos los casos: O(n²) - siempre recorre todo
    # Ventaja: Minimiza swaps - O(n) swaps máximo
    # Espacial: O(1)

def merge_sort_analysis(arr: List[int]) -> tuple:
    """
    Merge Sort con análisis recursivo
    
    TODO:
    1. Implementa merge sort
    2. Analiza por qué es O(n log n)
    3. Calcula complejidad espacial
    """
    operations = {'comparisons': 0, 'merges': 0}
    
    def merge_sort_recursive(arr):
        if len(arr) <= 1:
            return arr
        
        operations['merges'] += 1
        mid = len(arr) // 2
        left = merge_sort_recursive(arr[:mid])
        right = merge_sort_recursive(arr[mid:])
        
        return merge(left, right, operations)
    
    def merge(left, right, ops):
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            ops['comparisons'] += 1
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    sorted_arr = merge_sort_recursive(arr)
    return sorted_arr, operations['comparisons'], operations['merges']
    
    # ANÁLISIS:
    # Temporal: O(n log n) - log n niveles, O(n) merge por nivel
    # Espacial: O(n) - arrays auxiliares en recursión

# =============================================================================
# EXERCISE 3: ANÁLISIS DE ESTRUCTURAS DE DATOS (10 minutos)
# =============================================================================

class ListAnalysis:
    """Análisis de operaciones en listas Python"""
    
    def __init__(self):
        self.operations_count = 0
    
    def append_analysis(self, n: int) -> float:
        """
        Analiza append en lista
        
        TODO: 
        1. Mide tiempo de n appends
        2. Explica por qué es O(1) amortizado
        """
        arr = []
        start_time = time.perf_counter()
        
        for i in range(n):
            arr.append(i)  # O(1) amortizado
        
        end_time = time.perf_counter()
        return end_time - start_time
        
        # ANÁLISIS:
        # O(1) amortizado - ocasionalmente O(n) por resize
        # Array doubling strategy: 4, 8, 16, 32...
    
    def insert_at_beginning_analysis(self, n: int) -> float:
        """
        Analiza insert(0, x) en lista
        
        TODO: Explica por qué es O(n)
        """
        arr = list(range(1000))  # Lista base
        start_time = time.perf_counter()
        
        for i in range(n):
            arr.insert(0, i)  # O(n) - debe mover todos los elementos
        
        end_time = time.perf_counter()
        return end_time - start_time
        
        # ANÁLISIS:
        # O(n) - debe desplazar todos los elementos existentes
        # Cada insert(0, x) mueve n elementos hacia la derecha
    
    def pop_analysis(self) -> Dict[str, float]:
        """Compara pop() vs pop(0)"""
        arr1 = list(range(10000))
        arr2 = list(range(10000))
        
        # pop() from end - O(1)
        start_time = time.perf_counter()
        while arr1:
            arr1.pop()  # O(1)
        pop_end_time = time.perf_counter() - start_time
        
        # pop(0) from beginning - O(n)
        start_time = time.perf_counter()
        for _ in range(100):  # Solo 100 para no tardar mucho
            if arr2:
                arr2.pop(0)  # O(n)
        pop_start_time = time.perf_counter() - start_time
        
        return {
            'pop_end_O1': pop_end_time,
            'pop_start_On': pop_start_time
        }

class DictAnalysis:
    """Análisis de operaciones en diccionarios (hash tables)"""
    
    def hash_collision_analysis(self, n: int):
        """
        Simula y analiza colisiones en hash table
        
        TODO: Explica por qué promedio es O(1) pero peor caso O(n)
        """
        # Simulación de hash table simple
        hash_table = [[] for _ in range(n // 4)]  # Load factor alto
        collisions = 0
        
        for i in range(n):
            hash_val = hash(i) % len(hash_table)
            
            if hash_table[hash_val]:  # Ya hay elementos
                collisions += 1
            
            hash_table[hash_val].append(i)
        
        max_chain_length = max(len(chain) for chain in hash_table)
        
        return {
            'total_collisions': collisions,
            'max_chain_length': max_chain_length,
            'load_factor': n / len(hash_table)
        }
        
        # ANÁLISIS:
        # Promedio O(1) - distribución uniforme
        # Peor caso O(n) - todas las keys en mismo bucket

# =============================================================================
# EXERCISE 4: OPTIMIZACIÓN BASADA EN ANÁLISIS (10 minutos)
# =============================================================================

def find_duplicates_versions():
    """
    Múltiples versiones del mismo problema con diferentes complejidades
    
    Problema: Encontrar elementos duplicados en un array
    """
    
    def version_1_brute_force(arr: List[int]) -> List[int]:
        """
        Versión Brute Force
        
        TODO: Analiza la complejidad
        """
        duplicates = []
        n = len(arr)
        
        for i in range(n):                    # O(n)
            for j in range(i + 1, n):         # O(n)
                if arr[i] == arr[j]:          # O(1)
                    if arr[i] not in duplicates:  # O(k) donde k = len(duplicates)
                        duplicates.append(arr[i])
        
        return duplicates
        
        # ANÁLISIS:
        # Temporal: O(n² * k) - muy ineficiente
        # Espacial: O(k) donde k = número de duplicados
    
    def version_2_sorting(arr: List[int]) -> List[int]:
        """
        Versión con ordenamiento
        
        TODO: Implementa y analiza
        """
        if not arr:
            return []
        
        sorted_arr = sorted(arr)  # O(n log n)
        duplicates = []
        
        for i in range(1, len(sorted_arr)):  # O(n)
            if sorted_arr[i] == sorted_arr[i-1]:
                if not duplicates or duplicates[-1] != sorted_arr[i]:
                    duplicates.append(sorted_arr[i])
        
        return duplicates
        
        # ANÁLISIS:
        # Temporal: O(n log n) - dominado por sorting
        # Espacial: O(n) - sorted array + result
    
    def version_3_hash_set(arr: List[int]) -> List[int]:
        """
        Versión con hash set - óptima
        
        TODO: Implementa la versión más eficiente
        """
        seen = set()
        duplicates = set()
        
        for num in arr:  # O(n)
            if num in seen:      # O(1) promedio
                duplicates.add(num)  # O(1) promedio
            else:
                seen.add(num)    # O(1) promedio
        
        return list(duplicates)
        
        # ANÁLISIS:
        # Temporal: O(n) - óptimo
        # Espacial: O(n) - para los sets
    
    return {
        'brute_force_O_n2': version_1_brute_force,
        'sorting_O_nlogn': version_2_sorting,
        'hash_set_O_n': version_3_hash_set
    }

def two_sum_versions():
    """
    Problema clásico: Two Sum con diferentes enfoques
    
    Dado array y target, encontrar índices de dos números que sumen target
    """
    
    def two_sum_brute_force(nums: List[int], target: int) -> List[int]:
        """O(n²) - Brute force"""
        n = len(nums)
        
        for i in range(n):         # O(n)
            for j in range(i + 1, n):  # O(n)
                if nums[i] + nums[j] == target:  # O(1)
                    return [i, j]
        
        return []
        
        # Temporal: O(n²), Espacial: O(1)
    
    def two_sum_hash_map(nums: List[int], target: int) -> List[int]:
        """O(n) - Hash map approach"""
        num_to_index = {}
        
        for i, num in enumerate(nums):  # O(n)
            complement = target - num
            
            if complement in num_to_index:  # O(1) promedio
                return [num_to_index[complement], i]
            
            num_to_index[num] = i  # O(1) promedio
        
        return []
        
        # Temporal: O(n), Espacial: O(n)
    
    def two_sum_two_pointers(nums: List[int], target: int) -> List[int]:
        """
        O(n log n) - Two pointers (si necesitamos índices originales)
        O(n) - Si array ya está ordenado y no necesitamos índices
        """
        # Crear lista de (valor, índice_original)
        indexed_nums = [(nums[i], i) for i in range(len(nums))]  # O(n)
        indexed_nums.sort()  # O(n log n)
        
        left, right = 0, len(indexed_nums) - 1
        
        while left < right:  # O(n)
            current_sum = indexed_nums[left][0] + indexed_nums[right][0]
            
            if current_sum == target:
                return [indexed_nums[left][1], indexed_nums[right][1]]
            elif current_sum < target:
                left += 1
            else:
                right -= 1
        
        return []
        
        # Temporal: O(n log n), Espacial: O(n)
    
    return {
        'brute_force': two_sum_brute_force,
        'hash_map': two_sum_hash_map,
        'two_pointers': two_sum_two_pointers
    }

# =============================================================================
# BENCHMARK Y COMPARACIÓN DE ALGORITMOS
# =============================================================================

def run_complexity_benchmark():
    """
    Ejecuta benchmarks para validar análisis teórico
    """
    print("BENCHMARK DE COMPLEJIDADES")
    print("=" * 50)
    
    # Test 1: Algoritmos de búsqueda
    print("\n1. ALGORITMOS DE BÚSQUEDA")
    print("-" * 30)
    
    sizes = [1000, 5000, 10000]
    
    for size in sizes:
        arr = sorted(range(size))
        target = size - 1  # Último elemento (peor caso para linear)
        
        # Linear search
        start = time.perf_counter()
        linear_result, linear_comps = linear_search_analysis(arr, target)
        linear_time = time.perf_counter() - start
        
        # Binary search
        start = time.perf_counter()
        binary_result, binary_comps = binary_search_analysis(arr, target)
        binary_time = time.perf_counter() - start
        
        print(f"Size {size}:")
        print(f"  Linear:  {linear_time:.6f}s, {linear_comps} comparisons")
        print(f"  Binary:  {binary_time:.6f}s, {binary_comps} comparisons")
        print(f"  Speedup: {linear_time/binary_time:.1f}x")
    
    # Test 2: Algoritmos de ordenamiento
    print("\n2. ALGORITMOS DE ORDENAMIENTO")
    print("-" * 35)
    
    test_sizes = [100, 500, 1000]
    
    for size in test_sizes:
        # Array random para testing
        test_array = [random.randint(1, 1000) for _ in range(size)]
        
        # Bubble Sort
        start = time.perf_counter()
        bubble_result, bubble_comps, bubble_swaps = bubble_sort_analysis(test_array)
        bubble_time = time.perf_counter() - start
        
        # Selection Sort
        start = time.perf_counter()
        selection_result, selection_comps, selection_swaps = selection_sort_analysis(test_array)
        selection_time = time.perf_counter() - start
        
        # Merge Sort
        start = time.perf_counter()
        merge_result, merge_comps, merge_merges = merge_sort_analysis(test_array)
        merge_time = time.perf_counter() - start
        
        print(f"Size {size}:")
        print(f"  Bubble:    {bubble_time:.6f}s, {bubble_comps} comparisons")
        print(f"  Selection: {selection_time:.6f}s, {selection_comps} comparisons")
        print(f"  Merge:     {merge_time:.6f}s, {merge_comps} comparisons")
    
    # Test 3: Find Duplicates Comparison
    print("\n3. FIND DUPLICATES COMPARISON")
    print("-" * 35)
    
    duplicate_versions = find_duplicates_versions()
    
    test_arrays = {
        'small': [1, 2, 3, 2, 4, 5, 3],
        'medium': list(range(500)) + list(range(250)),  # Many duplicates
    }
    
    for test_name, test_arr in test_arrays.items():
        print(f"\nTest: {test_name} (size: {len(test_arr)})")
        
        for version_name, version_func in duplicate_versions.items():
            start = time.perf_counter()
            result = version_func(test_arr)
            elapsed = time.perf_counter() - start
            print(f"  {version_name}: {elapsed:.6f}s, found: {len(result)} duplicates")

# =============================================================================
# EJERCICIOS DE ANÁLISIS MANUAL
# =============================================================================

def manual_analysis_exercises():
    """
    Ejercicios para practicar análisis manual de complejidad
    """
    
    print("\nEJERCICIOS DE ANÁLISIS MANUAL")
    print("=" * 45)
    
    exercises = [
        {
            'name': 'Nested Loops with Variable Inner',
            'code': '''
def mystery1(n):
    total = 0
    for i in range(n):        # O(n)
        for j in range(i):    # O(i) - variable!
            total += 1        # O(1)
    return total
            ''',
            'answer': 'O(n²) - suma 0+1+2+...+(n-1) = n(n-1)/2',
            'complexity': 'Quadratic'
        },
        
        {
            'name': 'Logarithmic with Linear Inner',
            'code': '''
def mystery2(arr):
    n = len(arr)
    i = 1
    while i < n:              # O(log n) - i doubles
        for j in range(n):    # O(n)
            print(arr[j])     # O(1)
        i *= 2
            ''',
            'answer': 'O(n log n) - log n outer iterations, n inner operations',
            'complexity': 'Linearithmic'
        },
        
        {
            'name': 'Recursive Tree Analysis',
            'code': '''
def mystery3(n):
    if n <= 1:
        return 1
    return mystery3(n-1) + mystery3(n-1)
            ''',
            'answer': 'O(2^n) - cada llamada genera 2 llamadas recursivas',
            'complexity': 'Exponential'
        },
        
        {
            'name': 'Hash Table Operations',
            'code': '''
def mystery4(arr):
    seen = set()              # O(1) to create
    for num in arr:           # O(n)
        if num in seen:       # O(1) average
            return True       # O(1)
        seen.add(num)         # O(1) average
    return False
            ''',
            'answer': 'O(n) average case, O(n²) worst case (hash collisions)',
            'complexity': 'Linear (average)'
        }
    ]
    
    for i, exercise in enumerate(exercises, 1):
        print(f"\nEJERCICIO {i}: {exercise['name']}")
        print("Código:")
        print(exercise['code'])
        print(f"\n¿Cuál es la complejidad temporal?")
        print(f"Respuesta: {exercise['answer']}")
        print(f"Clasificación: {exercise['complexity']}")
        print("-" * 50)

# =============================================================================
# MAIN EXECUTION Y TESTING
# =============================================================================

def main():
    """
    Función principal para ejecutar todos los análisis y ejercicios
    """
    print("DÍA 8: ANÁLISIS PRÁCTICO DE COMPLEJIDAD ALGORÍTMICA")
    print("=" * 60)
    print("Objetivo: Dominar análisis Big O mediante práctica intensiva")
    print("Tiempo estimado: 45 minutos")
    
    # Ejecutar benchmark comparativo
    run_complexity_benchmark()
    
    # Análisis de estructuras de datos
    print("\n4. ANÁLISIS DE ESTRUCTURAS DE DATOS")
    print("-" * 40)
    
    list_analyzer = ListAnalysis()
    
    # Test append vs insert(0)
    append_time = list_analyzer.append_analysis(10000)
    insert_time = list_analyzer.insert_at_beginning_analysis(1000)  # Menor n para insert
    
    print(f"Append 10,000 elements: {append_time:.6f}s (O(1) amortized)")
    print(f"Insert at beginning 1,000 times: {insert_time:.6f}s (O(n) each)")
    
    # Test pop operations
    pop_results = list_analyzer.pop_analysis()
    print(f"Pop from end: {pop_results['pop_end_O1']:.6f}s")
    print(f"Pop from start: {pop_results['pop_start_On']:.6f}s")
    
    # Hash table analysis
    dict_analyzer = DictAnalysis()
    collision_stats = dict_analyzer.hash_collision_analysis(1000)
    print(f"\nHash table collision analysis:")
    print(f"  Collisions: {collision_stats['total_collisions']}")
    print(f"  Max chain length: {collision_stats['max_chain_length']}")
    print(f"  Load factor: {collision_stats['load_factor']:.2f}")
    
    # Ejercicios de análisis manual
    manual_analysis_exercises()
    
    # Resumen final
    print("\n" + "=" * 60)
    print("RESUMEN DEL DÍA 8")
    print("=" * 60)
    print("✅ Conceptos dominados:")
    print("   • Notación Big O, Omega, Theta")
    print("   • Análisis de casos: mejor, promedio, peor")
    print("   • Complejidad temporal vs espacial")
    print("   • Análisis de loops anidados")
    print("   • Complejidades de estructuras de datos Python")
    print("   • Optimización basada en análisis")
    
    print("\n📚 Para el día 9:")
    print("   • Implementación de algoritmos de búsqueda y ordenamiento")
    print("   • Binary search y variantes")
    print("   • Merge sort, quick sort desde cero")
    print("   • Análisis comparativo de performance")
    
    print("\n🎯 Métricas de éxito:")
    print("   □ Analiza correctamente complejidad de cualquier algoritmo")
    print("   □ Explica trade-offs entre diferentes enfoques")
    print("   □ Identifica oportunidades de optimización")
    print("   □ Justifica elección de estructuras de datos")

if __name__ == "__main__":
    main()
