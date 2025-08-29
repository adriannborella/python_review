"""
DÍA 8: EJERCICIOS ADICIONALES - ANÁLISIS DE COMPLEJIDAD
Tiempo extra: 30-45 minutos (opcional)
Para profundizar conceptos y preparar día 9

INSTRUCCIONES:
- Analiza cada función ANTES de ver la respuesta
- Piensa en casos mejor, promedio y peor
- Considera tanto complejidad temporal como espacial
"""

# =============================================================================
# CHALLENGE 1: ANÁLISIS DE ALGORITMOS RECURSIVOS
# =============================================================================

def fibonacci_naive(n):
    """
    ¿Cuál es la complejidad de esta implementación de Fibonacci?
    Pista: Dibuja el árbol de recursión
    """
    if n <= 1:
        return n
    return fibonacci_naive(n-1) + fibonacci_naive(n-2)

# RESPUESTA: O(2^n) temporal, O(n) espacial por call stack

def fibonacci_memoized(n, memo={}):
    """
    ¿Cómo cambia la complejidad con memoización?
    """
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    
    memo[n] = fibonacci_memoized(n-1, memo) + fibonacci_memoized(n-2, memo)
    return memo[n]

# RESPUESTA: O(n) temporal, O(n) espacial - cada subproblema se resuelve una vez

def fibonacci_iterative(n):
    """
    ¿Y con enfoque iterativo?
    """
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    
    return b

# RESPUESTA: O(n) temporal, O(1) espacial - óptimo

# =============================================================================
# CHALLENGE 2: ANÁLISIS DE ALGORITMOS DE STRINGS
# =============================================================================

def is_palindrome_v1(s):
    """
    Versión 1: ¿Cuál es la complejidad?
    """
    return s == s[::-1]

# RESPUESTA: O(n) temporal y espacial - s[::-1] crea nuevo string

def is_palindrome_v2(s):
    """
    Versión 2: ¿Es más eficiente?
    """
    left, right = 0, len(s) - 1
    
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    
    return True

# RESPUESTA: O(n) temporal, O(1) espacial - más eficiente en memoria

def longest_common_subsequence_naive(text1, text2):
    """
    LCS recursivo naive: ¿Complejidad?
    """
    if not text1 or not text2:
        return 0
    
    if text1[0] == text2[0]:
        return 1 + longest_common_subsequence_naive(text1[1:], text2[1:])
    
    return max(
        longest_common_subsequence_naive(text1[1:], text2),
        longest_common_subsequence_naive(text1, text2[1:])
    )

# RESPUESTA: O(2^(m+n)) - exponencial, muy ineficiente

def longest_common_subsequence_dp(text1, text2):
    """
    LCS con programación dinámica: ¿Complejidad?
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]

# RESPUESTA: O(m*n) temporal y espacial - mucho mejor que naive

# =============================================================================
# CHALLENGE 3: ANÁLISIS DE ALGORITMOS DE GRAFOS BÁSICOS
# =============================================================================

def has_cycle_dfs(graph, node, visited, rec_stack):
    """
    Detección de ciclo en grafo dirigido usando DFS
    ¿Cuál es la complejidad?
    
    graph: dict de adjacency list
    """
    visited[node] = True
    rec_stack[node] = True
    
    for neighbor in graph.get(node, []):
        if not visited.get(neighbor, False):
            if has_cycle_dfs(graph, neighbor, visited, rec_stack):
                return True
        elif rec_stack.get(neighbor, False):
            return True
    
    rec_stack[node] = False
    return False

# RESPUESTA: O(V + E) temporal, O(V) espacial
# V = vértices, E = aristas

def shortest_path_bfs(graph, start, end):
    """
    Camino más corto usando BFS
    ¿Complejidad para grafo no ponderado?
    """
    from collections import deque
    
    if start == end:
        return [start]
    
    queue = deque([(start, [start])])
    visited = {start}
    
    while queue:
        node, path = queue.popleft()
        
        for neighbor in graph.get(node, []):
            if neighbor == end:
                return path + [neighbor]
            
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return None

# RESPUESTA: O(V + E) temporal, O(V) espacial - óptimo para grafos no ponderados

# =============================================================================
# CHALLENGE 4: ANÁLISIS DE PROBLEMAS CLÁSICOS DE PROGRAMACIÓN
# =============================================================================

def three_sum_naive(nums, target=0):
    """
    3Sum problema: encontrar tripletas que sumen target
    Versión naive: ¿Complejidad?
    """
    result = []
    n = len(nums)
    
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if nums[i] + nums[j] + nums[k] == target:
                    result.append([nums[i], nums[j], nums[k]])
    
    return result

# RESPUESTA: O(n³) temporal, O(1) espacial extra (sin contar result)

def three_sum_optimized(nums, target=0):
    """
    3Sum optimizado con sorting + two pointers
    ¿Mejora la complejidad?
    """
    nums.sort()  # O(n log n)
    result = []
    n = len(nums)
    
    for i in range(n - 2):  # O(n)
        if i > 0 and nums[i] == nums[i-1]:
            continue  # Skip duplicates
        
        left, right = i + 1, n - 1
        
        while left < right:  # O(n) en total para todos los i
            current_sum = nums[i] + nums[left] + nums[right]
            
            if current_sum == target:
                result.append([nums[i], nums[left], nums[right]])
                
                # Skip duplicates
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
            elif current_sum < target:
                left += 1
            else:
                right -= 1
    
    return result

# RESPUESTA: O(n²) temporal, O(1) espacial extra - mejor que naive

def subarray_sum_equals_k_naive(nums, k):
    """
    Contar subarrays que suman k
    Versión naive: ¿Complejidad?
    """
    count = 0
    n = len(nums)
    
    for i in range(n):
        for j in range(i, n):
            if sum(nums[i:j+1]) == k:
                count += 1
    
    return count

# RESPUESTA: O(n³) - por el sum() interno en cada iteración

def subarray_sum_equals_k_optimized(nums, k):
    """
    Usando prefix sum y hash map
    ¿Mejora significativa?
    """
    count = 0
    prefix_sum = 0
    sum_count = {0: 1}  # prefix_sum: frequency
    
    for num in nums:
        prefix_sum += num
        
        # Si existe prefix_sum - k, significa que hay subarray con suma k
        if prefix_sum - k in sum_count:
            count += sum_count[prefix_sum - k]
        
        # Actualizar frecuencia del prefix_sum actual
        sum_count[prefix_sum] = sum_count.get(prefix_sum, 0) + 1
    
    return count

# RESPUESTA: O(n) temporal, O(n) espacial - dramática mejora

# =============================================================================
# CHALLENGE 5: ANÁLISIS DE ALGORITMOS DE BACKTRACKING
# =============================================================================

def generate_parentheses_backtrack(n):
    """
    Generar todas las combinaciones válidas de n pares de paréntesis
    ¿Cuál es la complejidad?
    """
    result = []
    
    def backtrack(current, open_count, close_count):
        # Base case
        if len(current) == 2 * n:
            result.append(current)
            return
        
        # Add opening parenthesis
        if open_count < n:
            backtrack(current + "(", open_count + 1, close_count)
        
        # Add closing parenthesis
        if close_count < open_count:
            backtrack(current + ")", open_count, close_count + 1)
    
    backtrack("", 0, 0)
    return result

# RESPUESTA: O(4^n / sqrt(n)) temporal - Catalan number
# O(4^n / sqrt(n)) espacial - para almacenar todas las soluciones

def n_queens_backtrack(n):
    """
    N-Queens problema usando backtracking
    ¿Complejidad en el peor caso?
    """
    result = []
    board = [-1] * n  # board[i] = j means queen at (i, j)
    
    def is_safe(row, col):
        for i in range(row):
            # Check column and diagonals
            if (board[i] == col or 
                board[i] - i == col - row or 
                board[i] + i == col + row):
                return False
        return True
    
    def backtrack(row):
        if row == n:
            result.append(board[:])
            return
        
        for col in range(n):
            if is_safe(row, col):
                board[row] = col
                backtrack(row + 1)
                # No need to reset board[row] as we'll overwrite it
    
    backtrack(0)
    return result

# RESPUESTA: O(n!) temporal en peor caso - aunque en práctica es mejor
# debido a pruning. Espacial O(n²) para almacenar soluciones

# =============================================================================
# EJERCICIOS DE ANÁLISIS RÁPIDO
# =============================================================================

def quick_analysis_exercises():
    """
    Ejercicios rápidos para practicar reconocimiento de patrones
    """
    
    exercises = [
        {
            'code': '''
for i in range(n):
    for j in range(n, 0, -1):
        print(i, j)
            ''',
            'complexity': 'O(n²)',
            'explanation': 'Loops anidados independientes, ambos O(n)'
        },
        
        {
            'code': '''
i = n
while i > 1:
    print(i)
    i = i // 2
            ''',
            'complexity': 'O(log n)',
            'explanation': 'i se divide por 2 cada iteración'
        },
        
        {
            'code': '''
for i in range(n):
    j = 1
    while j < n:
        print(i, j)
        j *= 3
            ''',
            'complexity': 'O(n log n)',
            'explanation': 'Outer O(n), inner O(log₃ n) ≈ O(log n)'
        },
        
        {
            'code': '''
def mystery(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = mystery(arr[:mid])
    right = mystery(arr[mid:])
    
    return merge(left, right)  # O(n)
            ''',
            'complexity': 'O(n log n)',
            'explanation': 'Divide y vencerás: log n niveles, O(n) trabajo por nivel'
        },
        
        {
            'code': '''
for i in range(n):
    for j in range(i * i):
        print(i, j)
            ''',
            'complexity': 'O(n³)',
            'explanation': 'Inner loop va hasta i²: suma de 0² + 1² + ... + (n-1)² ≈ n³/3'
        }
    ]
    
    return exercises

# =============================================================================
# SPACE COMPLEXITY CHALLENGES
# =============================================================================

def space_complexity_challenges():
    """
    Ejercicios específicos para análisis de complejidad espacial
    """
    
    def challenge_1(n):
        """¿Complejidad espacial?"""
        result = []
        for i in range(n):
            result.append(i * 2)
        return result
        # RESPUESTA: O(n) - array result crece con n
    
    def challenge_2(arr):
        """¿Complejidad espacial?"""
        max_val = arr[0]
        for val in arr:
            if val > max_val:
                max_val = val
        return max_val
        # RESPUESTA: O(1) - solo variable max_val
    
    def challenge_3(n):
        """¿Complejidad espacial?"""
        if n <= 0:
            return 1
        return n * challenge_3(n - 1)
        # RESPUESTA: O(n) - call stack de profundidad n
    
    def challenge_4(matrix):
        """¿Complejidad espacial?"""
        rows, cols = len(matrix), len(matrix[0])
        transposed = [[0] * rows for _ in range(cols)]
        
        for i in range(rows):
            for j in range(cols):
                transposed[j][i] = matrix[i][j]
        
        return transposed
        # RESPUESTA: O(rows * cols) - nueva matriz del mismo tamaño
    
    def challenge_5(s):
        """¿Complejidad espacial?"""
        char_count = {}
        for char in s:
            char_count[char] = char_count.get(char, 0) + 1
        return char_count
        # RESPUESTA: O(k) donde k = número de caracteres únicos
        # En el peor caso O(n) si todos los caracteres son únicos

# =============================================================================
# PRACTICAL OPTIMIZATION EXERCISES
# =============================================================================

def optimization_challenges():
    """
    Ejercicios de optimización basados en análisis de complejidad
    """
    
    # Challenge 1: Optimizar búsqueda de elemento común
    def find_common_elements_v1(arr1, arr2):
        """Versión inicial - ¿Cómo optimizar?"""
        common = []
        for item1 in arr1:        # O(n)
            for item2 in arr2:    # O(m)
                if item1 == item2 and item1 not in common:  # O(k)
                    common.append(item1)
        return common
        # COMPLEJIDAD: O(n * m * k) - muy ineficiente
    
    def find_common_elements_v2(arr1, arr2):
        """Versión optimizada usando sets"""
        set1 = set(arr1)      # O(n)
        set2 = set(arr2)      # O(m)
        return list(set1 & set2)  # O(min(n, m))
        # COMPLEJIDAD: O(n + m) - mucho mejor
    
    # Challenge 2: Optimizar conteo de caracteres
    def count_chars_v1(text):
        """Versión inicial"""
        result = {}
        for char in text:     # O(n)
            count = 0
            for c in text:    # O(n) - ineficiente!
                if c == char:
                    count += 1
            result[char] = count
        return result
        # COMPLEJIDAD: O(n²) - muy malo
    
    def count_chars_v2(text):
        """Versión optimizada"""
        result = {}
        for char in text:     # O(n)
            result[char] = result.get(char, 0) + 1  # O(1) promedio
        return result
        # COMPLEJIDAD: O(n) - óptimo
    
    # Challenge 3: Optimizar suma de subarray máximo
    def max_subarray_sum_v1(arr):
        """Versión brute force"""
        max_sum = float('-inf')
        n = len(arr)
        
        for i in range(n):        # O(n)
            for j in range(i, n): # O(n)
                current_sum = sum(arr[i:j+1])  # O(n) - problema!
                max_sum = max(max_sum, current_sum)
        
        return max_sum
        # COMPLEJIDAD: O(n³) - terrible
    
    def max_subarray_sum_v2(arr):
        """Kadane's algorithm - óptimo"""
        max_ending_here = max_so_far = arr[0]
        
        for i in range(1, len(arr)):  # O(n)
            max_ending_here = max(arr[i], max_ending_here + arr[i])
            max_so_far = max(max_so_far, max_ending_here)
        
        return max_so_far
        # COMPLEJIDAD: O(n) - óptimo
    
    return {
        'common_elements': {
            'v1_inefficient': find_common_elements_v1,
            'v2_optimized': find_common_elements_v2
        },
        'count_chars': {
            'v1_inefficient': count_chars_v1,
            'v2_optimized': count_chars_v2
        },
        'max_subarray': {
            'v1_brute_force': max_subarray_sum_v1,
            'v2_kadane': max_subarray_sum_v2
        }
    }

# =============================================================================
# COMPLEXITY ESTIMATION PRACTICE
# =============================================================================

def complexity_estimation_drills():
    """
    Ejercicios para estimar complejidad rápidamente
    """
    
    drills = [
        {
            'description': 'Buscar todos los pares que sumen un valor específico',
            'naive_approach': 'Nested loops comparando todos los pares',
            'naive_complexity': 'O(n²)',
            'optimized_approach': 'Hash map para almacenar complementos',
            'optimized_complexity': 'O(n)',
            'space_tradeoff': 'O(1) → O(n) espacio adicional'
        },
        
        {
            'description': 'Encontrar el k-ésimo elemento más grande',
            'naive_approach': 'Ordenar array completo',
            'naive_complexity': 'O(n log n)',
            'optimized_approach': 'Min-heap de tamaño k o QuickSelect',
            'optimized_complexity': 'O(n log k) o O(n) promedio',
            'space_tradeoff': 'O(1) → O(k) para heap'
        },
        
        {
            'description': 'Verificar si un string es anagrama de otro',
            'naive_approach': 'Ordenar ambos strings y comparar',
            'naive_complexity': 'O(n log n)',
            'optimized_approach': 'Contar frecuencia de caracteres',
            'optimized_complexity': 'O(n)',
            'space_tradeoff': 'O(1) → O(k) donde k = alfabeto único'
        },
        
        {
            'description': 'Encontrar substring común más largo',
            'naive_approach': 'Comparar todos los substrings posibles',
            'naive_complexity': 'O(n³)',
            'optimized_approach': 'Programación dinámica',
            'optimized_complexity': 'O(n * m)',
            'space_tradeoff': 'O(1) → O(n * m) para tabla DP'
        }
    ]
    
    return drills

# =============================================================================
# TESTING Y VALIDACIÓN
# =============================================================================

def run_homework_tests():
    """
    Tests para validar las implementaciones de los challenges
    """
    print("TESTING HOMEWORK EXERCISES")
    print("=" * 40)
    
    # Test optimization challenges
    optimizers = optimization_challenges()
    
    # Test common elements
    arr1 = [1, 2, 3, 4, 5]
    arr2 = [3, 4, 5, 6, 7]
    
    print("\n1. Common Elements Test:")
    result_v1 = optimizers['common_elements']['v1_inefficient'](arr1, arr2)
    result_v2 = optimizers['common_elements']['v2_optimized'](arr1, arr2)
    print(f"V1 (O(n*m*k)): {result_v1}")
    print(f"V2 (O(n+m)): {sorted(result_v2)}")
    print(f"Results match: {sorted(result_v1) == sorted(result_v2)}")
    
    # Test character counting
    test_text = "hello world"
    print(f"\n2. Character Count Test ('{test_text}'):")
    count_v1 = optimizers['count_chars']['v1_inefficient'](test_text)
    count_v2 = optimizers['count_chars']['v2_optimized'](test_text)
    print(f"V1 (O(n²)): {count_v1}")
    print(f"V2 (O(n)): {count_v2}")
    print(f"Results match: {count_v1 == count_v2}")
    
    # Test max subarray
    test_array = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print(f"\n3. Max Subarray Sum Test {test_array}:")
    max_v1 = optimizers['max_subarray']['v1_brute_force'](test_array)
    max_v2 = optimizers['max_subarray']['v2_kadane'](test_array)
    print(f"V1 (O(n³)): {max_v1}")
    print(f"V2 (O(n) Kadane): {max_v2}")
    print(f"Results match: {max_v1 == max_v2}")
    
    # Test Fibonacci implementations
    print(f"\n4. Fibonacci Comparison (n=10):")
    n = 10
    
    import time
    
    start = time.perf_counter()
    fib_naive = fibonacci_naive(n)
    time_naive = time.perf_counter() - start
    
    start = time.perf_counter()
    fib_memo = fibonacci_memoized(n, {})
    time_memo = time.perf_counter() - start
    
    start = time.perf_counter()
    fib_iter = fibonacci_iterative(n)
    time_iter = time.perf_counter() - start
    
    print(f"Naive (O(2^n)): {fib_naive} in {time_naive:.6f}s")
    print(f"Memoized (O(n)): {fib_memo} in {time_memo:.6f}s")
    print(f"Iterative (O(n)): {fib_iter} in {time_iter:.6f}s")
    print(f"All results match: {fib_naive == fib_memo == fib_iter}")

# =============================================================================
# STUDY GUIDE PARA DÍA 9
# =============================================================================

def prepare_for_day_9():
    """
    Guía de estudio para preparar el día 9: Algoritmos de Búsqueda y Ordenamiento
    """
    
    study_guide = {
        'review_concepts': [
            'Dominaste análisis Big O',
            'Puedes calcular complejidad de loops anidados',
            'Entiendes diferencia entre temporal vs espacial',
            'Reconoces patrones comunes (O(n²), O(n log n), etc.)'
        ],
        
        'day_9_preview': [
            'Implementación de Binary Search desde cero',
            'Variantes de Binary Search (first/last occurrence)',
            'Bubble Sort, Selection Sort paso a paso',
            'Merge Sort y Quick Sort detallado',
            'Análisis comparativo de algoritmos de sorting'
        ],
        
        'practice_problems': [
            'LeetCode Binary Search problems (Easy/Medium)',
            'Implementar sorting algorithms sin mirar referencia',
            'Analizar trade-offs entre diferentes approaches',
            'Timing comparisons entre algoritmos'
        ],
        
        'key_questions': [
            '¿Cuándo usar Binary Search vs Linear Search?',
            '¿Por qué Quick Sort es O(n log n) promedio pero O(n²) peor caso?',
            '¿Cuándo Merge Sort es mejor que Quick Sort?',
            '¿Cómo afecta el tipo de datos al performance?'
        ]
    }
    
    return study_guide

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """
    Ejecutar todos los ejercicios adicionales del día 8
    """
    print("DÍA 8: EJERCICIOS ADICIONALES - ANÁLISIS DE COMPLEJIDAD")
    print("=" * 65)
    
    # Ejecutar tests
    run_homework_tests()
    
    # Mostrar ejercicios de análisis rápido
    print("\n" + "=" * 40)
    print("EJERCICIOS DE RECONOCIMIENTO RÁPIDO")
    print("=" * 40)
    
    quick_exercises = quick_analysis_exercises()
    for i, exercise in enumerate(quick_exercises, 1):
        print(f"\nEjercicio {i}:")
        print("Código:")
        print(exercise['code'])
        print(f"Complejidad: {exercise['complexity']}")
        print(f"Explicación: {exercise['explanation']}")
        print("-" * 30)
    
    # Drills de estimación
    print("\n" + "=" * 40)
    print("DRILLS DE ESTIMACIÓN DE COMPLEJIDAD")
    print("=" * 40)
    
    estimation_drills = complexity_estimation_drills()
    for i, drill in enumerate(estimation_drills, 1):
        print(f"\nDrill {i}: {drill['description']}")
        print(f"  Enfoque naive: {drill['naive_approach']} → {drill['naive_complexity']}")
        print(f"  Optimizado: {drill['optimized_approach']} → {drill['optimized_complexity']}")
        print(f"  Trade-off: {drill['space_tradeoff']}")
    
    # Guía de estudio para día 9
    study_guide = prepare_for_day_9()
    
    print("\n" + "=" * 40)
    print("PREPARACIÓN PARA DÍA 9")
    print("=" * 40)
    
    print("\n✅ Conceptos que deberías dominar:")
    for concept in study_guide['review_concepts']:
        print(f"  • {concept}")
    
    print("\n📚 Lo que veremos mañana:")
    for topic in study_guide['day_9_preview']:
        print(f"  • {topic}")
    
    print("\n🎯 Práctica recomendada esta noche:")
    for practice in study_guide['practice_problems']:
        print(f"  • {practice}")
    
    print("\n❓ Preguntas clave para reflexionar:")
    for question in study_guide['key_questions']:
        print(f"  • {question}")
    
    print("\n" + "=" * 65)
    print("¡EXCELENTE TRABAJO EN EL DÍA 8!")
    print("Has dominado el análisis de complejidad, una skill fundamental")
    print("para cualquier entrevista técnica de nivel senior.")
    print("\n🚀 ¡Listo para conquistar algoritmos de búsqueda y ordenamiento!")
    print("=" * 65)

if __name__ == "__main__":
    main()
