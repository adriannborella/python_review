"""
DÍA 8: BIG O Y ANÁLISIS DE COMPLEJIDAD
Semana 2 - Algoritmos y Complejidad
Tiempo: 2 horas (1h teoría + 1h práctica)

OBJETIVOS:
- Dominar notación Big O, Omega y Theta
- Analizar complejidad temporal y espacial
- Identificar patrones comunes de complejidad
- Optimizar algoritmos basándose en análisis
"""

import time
import sys
import matplotlib.pyplot as plt
from typing import List, Tuple
import random

# =============================================================================
# PARTE 1: FUNDAMENTOS DE ANÁLISIS DE COMPLEJIDAD
# =============================================================================


class ComplexityAnalyzer:
    """
    Herramienta para analizar y demostrar diferentes complejidades
    """

    def __init__(self):
        self.results = {}

    def measure_time(self, func, *args, **kwargs):
        """Mide tiempo de ejecución de una función"""
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        return result, end - start

    def measure_space(self, func, *args, **kwargs):
        """Simula medición de complejidad espacial"""
        import tracemalloc

        tracemalloc.start()

        result = func(*args, **kwargs)

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        return result, peak


# =============================================================================
# COMPLEJIDADES TEMPORALES FUNDAMENTALES
# =============================================================================


def complexity_o1_constant(arr: List[int], index: int) -> int:
    """
    O(1) - TIEMPO CONSTANTE

    Características:
    - Tiempo de ejecución independiente del tamaño de entrada
    - Acceso directo a elementos
    - Operaciones aritméticas básicas

    Ejemplos comunes:
    - Acceso a array por índice
    - Operaciones hash table
    - Push/pop en stack
    """
    if 0 <= index < len(arr):
        return arr[index]  # O(1) - acceso directo
    return -1


def complexity_on_linear(arr: List[int], target: int) -> int:
    """
    O(n) - TIEMPO LINEAL

    Características:
    - Tiempo proporcional al tamaño de entrada
    - Recorre cada elemento una vez
    - Búsqueda secuencial

    Ejemplos comunes:
    - Búsqueda lineal
    - Recorrido de array/lista
    - Algoritmos que procesan cada elemento
    """
    for i, value in enumerate(arr):  # O(n) - recorre n elementos
        if value == target:
            return i
    return -1


def complexity_olog_n_logarithmic(arr: List[int], target: int) -> int:
    """
    O(log n) - TIEMPO LOGARÍTMICO

    Características:
    - Divide el problema por la mitad en cada iteración
    - Muy eficiente para datasets grandes
    - Requiere datos ordenados (generalmente)

    Ejemplos comunes:
    - Búsqueda binaria
    - Árboles balanceados (BST)
    - Algoritmos divide y vencerás
    """
    left, right = 0, len(arr) - 1

    while left <= right:  # O(log n) - divide por 2 cada vez
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


def complexity_on_log_n_linearithmic(arr: List[int]) -> List[int]:
    """
    O(n log n) - TIEMPO LINEALRÍTMICO

    Características:
    - Combina operación lineal con logarítmica
    - Complejidad típica de algoritmos de ordenamiento eficientes
    - Divide y vencerás con merge

    Ejemplos comunes:
    - Merge Sort
    - Quick Sort (caso promedio)
    - Heap Sort
    """
    if len(arr) <= 1:
        return arr

    # Divide: O(log n) niveles
    mid = len(arr) // 2
    left = complexity_on_log_n_linearithmic(arr[:mid])
    right = complexity_on_log_n_linearithmic(arr[mid:])

    # Merge: O(n) en cada nivel
    return merge_sorted_arrays(left, right)


def merge_sorted_arrays(left: List[int], right: List[int]) -> List[int]:
    """Helper para merge sort - O(n)"""
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


def complexity_on2_quadratic(arr: List[int]) -> List[Tuple[int, int]]:
    """
    O(n²) - TIEMPO CUADRÁTICO

    Características:
    - Nested loops sobre la misma entrada
    - Tiempo crece exponencialmente con entrada
    - Ineficiente para datasets grandes

    Ejemplos comunes:
    - Bubble Sort, Selection Sort
    - Comparación de todos los pares
    - Algoritmos brute force
    """
    pairs = []

    for i in range(len(arr)):  # O(n)
        for j in range(i + 1, len(arr)):  # O(n) - nested
            pairs.append((arr[i], arr[j]))

    return pairs  # Total: O(n²)


def complexity_o2n_exponential(n: int) -> int:
    """
    O(2^n) - TIEMPO EXPONENCIAL

    Características:
    - Cada incremento duplica el tiempo
    - Extremadamente ineficiente
    - Solo viable para entradas muy pequeñas

    Ejemplos comunes:
    - Fibonacci recursivo naive
    - Algoritmos brute force para subset problems
    - Backtracking sin memoización
    """
    if n <= 1:
        return n

    # Cada llamada genera 2 llamadas más - O(2^n)
    return complexity_o2n_exponential(n - 1) + complexity_o2n_exponential(n - 2)


# =============================================================================
# COMPLEJIDADES ESPACIALES
# =============================================================================


def space_complexity_o1(arr: List[int]) -> int:
    """
    COMPLEJIDAD ESPACIAL O(1) - ESPACIO CONSTANTE

    Usa cantidad fija de memoria adicional
    """
    max_val = arr[0]  # O(1) espacio adicional

    for val in arr:
        if val > max_val:
            max_val = val

    return max_val


def space_complexity_on(arr: List[int]) -> List[int]:
    """
    COMPLEJIDAD ESPACIAL O(n) - ESPACIO LINEAL

    Memoria adicional proporcional a la entrada
    """
    # Crea nueva estructura de tamaño n
    doubled = []  # O(n) espacio adicional

    for val in arr:
        doubled.append(val * 2)

    return doubled


def space_complexity_on_recursive(arr: List[int], index: int = 0) -> int:
    """
    COMPLEJIDAD ESPACIAL O(n) - CALL STACK

    Recursión profunda consume O(n) en call stack
    """
    if index >= len(arr):
        return 0

    # Cada llamada recursiva usa O(1), pero son n llamadas
    return arr[index] + space_complexity_on_recursive(arr, index + 1)


# =============================================================================
# ANÁLISIS PRÁCTICO DE ALGORITMOS EXISTENTES
# =============================================================================


class AlgorithmAnalyzer:
    """
    Analizador práctico para diferentes tipos de algoritmos
    """

    @staticmethod
    def analyze_list_operations():
        """
        Analiza complejidades de operaciones comunes en listas
        """
        analysis = {
            "append": "O(1) amortized - agregar al final",
            "prepend": "O(n) - insertar al inicio requiere shift",
            "insert_middle": "O(n) - requiere shift de elementos",
            "access_by_index": "O(1) - acceso directo",
            "search_linear": "O(n) - buscar valor requiere recorrido",
            "delete_by_index": "O(n) - requiere shift después de borrar",
            "sort": "O(n log n) - Timsort (Python default)",
        }

        return analysis

    @staticmethod
    def analyze_dict_operations():
        """
        Analiza complejidades de operaciones en diccionarios (hash tables)
        """
        analysis = {
            "get": "O(1) promedio - acceso por hash",
            "set": "O(1) promedio - inserción por hash",
            "delete": "O(1) promedio - eliminación por hash",
            "keys": "O(n) - debe recorrer todas las keys",
            "values": "O(n) - debe recorrer todos los values",
            "items": "O(n) - debe recorrer todos los items",
            "in_operator": "O(1) promedio - verificación de existencia",
        }

        return analysis

    @staticmethod
    def analyze_string_operations():
        """
        Analiza complejidades de operaciones comunes en strings
        """
        analysis = {
            "concatenation": "O(n + m) - crear nuevo string",
            "slicing": "O(k) donde k es tamaño del slice",
            "find": "O(n * m) - nbuscar substrig",
            "replace": "O(n * m) - reemplazar todas las ocurrencias",
            "split": "O(n) - crear lista de substrings",
            "join": "O(n) - concatenar lista de strings",
            "upper_lower": "O(n) - transformar cada carácter",
        }

        return analysis


# =============================================================================
# HERRAMIENTAS DE BENCHMARKING
# =============================================================================


class ComplexityBenchmark:
    """
    Herramienta para medir y comparar algoritmos empíricamente
    """

    def __init__(self):
        self.results = {}

    def benchmark_algorithm(
        self, algorithm, sizes: List[int], data_generator=None, iterations=3
    ):
        """
        Benchmarka un algoritmo con diferentes tamaños de entrada
        """
        if data_generator is None:
            data_generator = lambda n: list(range(n))

        times = []

        for size in sizes:
            total_time = 0

            for _ in range(iterations):
                test_data = data_generator(size)

                start = time.perf_counter()
                algorithm(test_data)
                end = time.perf_counter()

                total_time += end - start

            avg_time = total_time / iterations
            times.append((size, avg_time))

        return times

    def compare_algorithms(self, algorithms: dict, sizes: List[int]):
        """
        Compara múltiples algoritmos
        """
        results = {}

        for name, algo in algorithms.items():
            print(f"Benchmarking {name}...")
            results[name] = self.benchmark_algorithm(algo, sizes)

        return results


# =============================================================================
# EJEMPLOS PRÁCTICOS DE ANÁLISIS
# =============================================================================


def analyze_nested_loops():
    """
    Ejemplos de análisis de loops anidados
    """

    def example_1(n):
        """¿Cuál es la complejidad?"""
        count = 0
        for i in range(n):  # O(n)
            for j in range(n):  # O(n)
                count += 1  # O(1)
        return count
        # Respuesta: O(n²)

    def example_2(n):
        """¿Cuál es la complejidad?"""
        count = 0
        for i in range(n):  # O(n)
            for j in range(i):  # O(i) - variable!
                count += 1  # O(1)
        return count
        # Análisis: i va de 0 a n-1
        # Total: 0 + 1 + 2 + ... + (n-1) = n(n-1)/2
        # Respuesta: O(n²) - términos de mayor orden

    def example_3(n):
        """¿Cuál es la complejidad?"""
        count = 0
        i = 1
        while i < n:  # O(log n) - i se duplica
            for j in range(n):  # O(n)
                count += 1  # O(1)
            i *= 2  # duplicar i
        return count
        # Respuesta: O(n log n)

    def example_4(arr):
        """¿Cuál es la complejidad?"""
        n = len(arr)
        for i in range(n):  # O(n)
            j = 1
            while j < n:  # O(log n)
                # Operación O(1)
                j *= 2
        # Respuesta: O(n log n)

    return {
        "O(n²) - nested n loops": example_1,
        "O(n²) - triangular loop": example_2,
        "O(n log n) - outer log, inner linear": example_3,
        "O(n log n) - linear outer, log inner": example_4,
    }


# =============================================================================
# EJERCICIOS DE PRÁCTICA
# =============================================================================


def practice_exercises():
    """
    Ejercicios para practicar análisis de complejidad
    """

    print("EJERCICIOS DE ANÁLISIS DE COMPLEJIDAD")
    print("=" * 50)

    # Ejercicio 1
    print("\nEJERCICIO 1: Analiza esta función")
    print("-" * 30)

    def mystery_function_1(arr):
        n = len(arr)
        for i in range(n):  # O(n)
            for j in range(0, n - i - 1):  # O(n - i -1) variable
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr  # O(n2)

    print("def mystery_function_1(arr):")
    print("    n = len(arr)")
    print("    for i in range(n):")
    print("        for j in range(0, n - i - 1):")
    print("            if arr[j] > arr[j + 1]:")
    print("                arr[j], arr[j + 1] = arr[j + 1], arr[j]")
    print("    return arr")
    print("\n¿Cuál es la complejidad temporal? ¿Y la espacial?")
    print("Respuesta: Temporal O(n²), Espacial O(1) - Es Bubble Sort")

    # Ejercicio 2
    print("\nEJERCICIO 2: Analiza esta función recursiva")
    print("-" * 40)

    def mystery_function_2(n):
        if n <= 1:
            return 1
        return mystery_function_2(n // 2) + mystery_function_2(n // 2)

    print("def mystery_function_2(n):")
    print("    if n <= 1:")
    print("        return 1")
    print("    return mystery_function_2(n//2) + mystery_function_2(n//2)")
    print("\n¿Cuál es la complejidad?")
    print("Pista: Dibuja el árbol de recursión")
    print("Respuesta: O(n) - aunque parece O(2^log n), se puede optimizar a O(log n)")

    # Ejercicio 3
    print("\nEJERCICIO 3: Función con múltiples loops")
    print("-" * 35)

    def mystery_function_3(arr):
        n = len(arr)

        # Loop 1
        for i in range(n):  # O(n)
            print(arr[i])

        # Loop 2
        for i in range(n):  # O(n)
            for j in range(n):  # O(n)
                print(arr[i], arr[j])

        # Loop 3
        for i in range(n):  # O(n)
            j = 1
            while j < n:  # O(log n)
                print(arr[i], j)
                j *= 2

        return True

    print("¿Cuál es la complejidad total?")
    print("Loop 1: O(n)")
    print("Loop 2: O(n²)")
    print("Loop 3: O(n log n)")
    print("Total: O(n) + O(n²) + O(n log n) = O(n²)")


# =============================================================================
# DEMO Y TESTING
# =============================================================================


def main_demo():
    """
    Demostración principal de conceptos de complejidad
    """
    print("BIG O ANALYSIS - DEMOSTRACIÓN PRÁCTICA")
    print("=" * 60)

    # Datos de prueba
    test_sizes = [100, 500, 1000, 2000]

    # Crear benchmark
    benchmark = ComplexityBenchmark()

    # Algoritmos para comparar
    algorithms = {
        "Linear Search O(n)": lambda arr: complexity_on_linear(arr, arr[-1]),
        "Binary Search O(log n)": lambda arr: complexity_olog_n_logarithmic(
            sorted(arr), arr[-1]
        ),
        "Bubble Sort O(n²)": lambda arr: complexity_on2_quadratic(
            arr[:10]
        ),  # Limitado para demo
    }

    # Comparar algoritmos
    print("\nCOMPARACIÓN EMPÍRICA DE ALGORITMOS:")
    print("-" * 40)

    results = benchmark.compare_algorithms(algorithms, [10, 50, 100])

    for algo_name, times in results.items():
        print(f"\n{algo_name}:")
        for size, time_taken in times:
            print(f"  n={size}: {time_taken:.6f}s")

    # Análisis de operaciones built-in
    print("\nANÁLISIS DE OPERACIONES PYTHON:")
    print("-" * 40)

    analyzer = AlgorithmAnalyzer()

    list_ops = analyzer.analyze_list_operations()
    print("\nOperaciones en Listas:")
    for op, complexity in list_ops.items():
        print(f"  {op}: {complexity}")

    dict_ops = analyzer.analyze_dict_operations()
    print("\nOperaciones en Diccionarios:")
    for op, complexity in dict_ops.items():
        print(f"  {op}: {complexity}")

    # Ejercicios de práctica
    practice_exercises()


if __name__ == "__main__":
    main_demo()
