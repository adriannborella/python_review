"""
DÍA 7: EJERCICIOS DE CONSOLIDACIÓN - FUNDAMENTOS PYTHON
Tiempo estimado: 35 minutos
Nivel: Intermedio - Senior Interview Prep
"""

# =============================================================================
# EJERCICIO 1: ANÁLISIS DE COMPLEJIDAD Y OPTIMIZACIÓN
# Tiempo: 8 minutos
# =============================================================================

from collections import Counter


def find_duplicates_v1(nums):
    """
    Versión inicial - Analiza la complejidad temporal y espacial
    Luego optimiza este algoritmo

    Complejidad temporal = Exponencial
    Complejidad Espacial = Lineal
    """
    duplicates = []
    counter_number = Counter(nums)
    for key, value in counter_number.items():
        if value > 1:
            duplicates.append(key)
    # for i in range(len(nums)):
    #     for j in range(i + 1, len(nums)):
    #         if nums[i] == nums[j] and nums[i] not in duplicates:
    #             duplicates.append(nums[i])
    return duplicates


def find_duplicates_optimized(nums):
    """
    TODO: Implementa una versión optimizada
    Objetivo: O(n) tiempo, O(n) espacio
    """
    # Tu solución aquí
    seen = set()
    duplicates = set()

    for num in nums:
        if num in seen:
            duplicates.add(num)
        else:
            seen.add(num)

    return list(duplicates)


# Test cases
test_nums = [1, 2, 3, 2, 4, 5, 3, 6, 1]
print("Original:", find_duplicates_v1(test_nums))
print("Optimized:", find_duplicates_optimized(test_nums))

# =============================================================================
# EJERCICIO 2: COMPREHENSIONS Y GENERADORES
# Tiempo: 10 minutos
# =============================================================================


def data_processor():
    """
    Simula procesamiento de datos con diferentes enfoques
    Compara memoria y rendimiento
    """
    # Dataset simulado
    raw_data = range(1, 1000000)  # 1 millón de elementos

    # TODO: Convierte estos bucles a comprehensions

    # 1. Filtrar números pares y elevar al cuadrado
    squares_traditional = []
    for num in raw_data:
        if num % 2 == 0:
            squares_traditional.append(num**2)

    # Versión comprehension:
    squares_comp = [num**2 for num in raw_data if num % 2 == 0]

    # 2. Crear generador para el mismo proceso (memory efficient)
    squares_gen = (num**2 for num in raw_data if num % 2 == 0)

    return squares_comp, squares_gen


# =============================================================================
# EJERCICIO 3: DECORADORES AVANZADOS
# Tiempo: 12 minutos
# =============================================================================

import time
import functools


def performance_monitor(func):
    """
    TODO: Implementa un decorador que:
    1. Mida tiempo de ejecución
    2. Cuente llamadas a la función
    3. Log de parámetros (solo en debug mode)
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Tu implementación aquí
        start_time = time.time()

        # Incrementar contador (usar hasattr para inicializar)
        if not hasattr(wrapper, "call_count"):
            wrapper.call_count = 0
        wrapper.call_count += 1

        # Ejecutar función
        result = func(*args, **kwargs)

        # Calcular tiempo
        execution_time = time.time() - start_time

        print(
            f"{func.__name__} ejecutada en {execution_time:.4f}s (llamada #{wrapper.call_count})"
        )

        return result

    return wrapper


class APIRateLimiter:
    """
    TODO: Implementa un decorador de clase para rate limiting
    Máximo 5 llamadas por minuto
    """

    def __init__(self, max_calls=5, time_window=60):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = []

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_time = time.time()

            # Limpiar llamadas antiguas
            self.calls = [
                call_time
                for call_time in self.calls
                if current_time - call_time < self.time_window
            ]

            # Verificar límite
            if len(self.calls) >= self.max_calls:
                raise Exception(
                    f"Rate limit exceeded: {self.max_calls} calls per {self.time_window}s"
                )

            # Registrar llamada
            self.calls.append(current_time)

            return func(*args, **kwargs)

        return wrapper


# Ejemplo de uso
@performance_monitor
@APIRateLimiter(max_calls=3, time_window=10)
def expensive_api_call(data):
    """Simula llamada API costosa"""
    time.sleep(0.1)  # Simular latencia
    return f"Processed: {len(data)} items"


# =============================================================================
# EJERCICIO 4: CONTEXT MANAGERS PERSONALIZADOS
# Tiempo: 5 minutos
# =============================================================================


class DatabaseTransaction:
    """
    TODO: Implementa un context manager para transacciones DB
    Debe manejar commit/rollback automáticamente
    """

    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connection = None
        self.transaction = None

    def __enter__(self):
        # Simular conexión a DB
        print(f"Connecting to {self.connection_string}")
        self.connection = f"Connected to {self.connection_string}"
        self.transaction = "Transaction started"
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            print("Transaction committed successfully")
        else:
            print(f"Transaction rolled back due to: {exc_val}")

        print("Connection closed")
        return False  # Re-raise exception si existe


# Uso del context manager
try:
    with DatabaseTransaction("postgresql://localhost:5432/testdb") as db:
        print("Executing database operations...")
        # Simular error condicional
        # raise ValueError("Simulated DB error")
        print("Operations completed successfully")
except Exception as e:
    print(f"Handled error: {e}")

# =============================================================================
# EJERCICIO BONUS: ALGORITMO COMBINADO
# Tiempo: Si queda tiempo
# =============================================================================


def word_frequency_analyzer(text):
    """
    TODO: Implementa un analizador que:
    1. Use comprehensions para limpieza
    2. Maneje excepciones elegantemente
    3. Retorne Top 5 palabras más frecuentes
    """
    try:
        # Limpiar y tokenizar
        import re

        words = [
            word.lower() for word in re.findall(r"\b\w+\b", text) if len(word) > 2
        ]  # Filtrar palabras cortas

        # Contar frecuencias
        word_count = {}
        for word in words:
            word_count[word] = word_count.get(word, 0) + 1

        # Top 5 usando sorted
        top_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:5]

        return top_words

    except Exception as e:
        print(f"Error analyzing text: {e}")
        return []


# Test del analizador
sample_text = """
Python is an amazing programming language. Python is easy to learn and Python
is powerful for data science. Many developers love Python because Python
has excellent libraries and Python community support.
"""

print("\nWord Frequency Analysis:")
for word, count in word_frequency_analyzer(sample_text):
    print(f"{word}: {count}")

# =============================================================================
# VALIDACIÓN DE EJERCICIOS
# =============================================================================


def run_validation_tests():
    """Ejecuta tests básicos para validar las implementaciones"""
    print("\n" + "=" * 60)
    print("VALIDACIÓN DE EJERCICIOS")
    print("=" * 60)

    # Test 1: Duplicados
    test_cases = [[1, 2, 3, 2, 4, 5, 3, 6, 1], [1, 1, 1, 1], [1, 2, 3, 4, 5], []]

    print("\n1. Test Find Duplicates:")
    for i, case in enumerate(test_cases):
        result = find_duplicates_optimized(case)
        print(f"   Case {i+1}: {case} -> {result}")

    # Test 2: Decorador
    print("\n2. Test Performance Monitor:")
    try:
        for i in range(3):
            result = expensive_api_call([1, 2, 3, 4, 5])
            print(f"   Result: {result}")
    except Exception as e:
        print(f"   Rate limit test passed: {e}")

    # Test 3: Context Manager
    print("\n3. Test Context Manager:")
    # Ya se ejecutó arriba

    print("\n" + "=" * 60)
    print("¡Ejercicios completados! Procede al simulacro de entrevista")
    print("=" * 60)


if __name__ == "__main__":
    run_validation_tests()
