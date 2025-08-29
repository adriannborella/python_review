# Días 3-4: Python Avanzado
## Comprensiones, Generadores, Decoradores y LeetCode Easy

---

# **DÍA 3: Comprensiones y Generadores**

## **Primera Hora: Teoría y Conceptos**

### **0:00-0:15 - Conexión con Días Anteriores**
```python
# Quick review: Optimización del día anterior
words = ["python", "java", "python", "javascript", "python"]

# Approach del día 1-2: usando dict básico
word_count = {}
for word in words:
    word_count[word] = word_count.get(word, 0) + 1

# Hoy aprenderemos formas más elegantes y eficientes
```

### **0:15-0:40 - List Comprehensions Mastery**

#### **Sintaxis y Progression:**
```python
# Básico: transformación
squares = [x**2 for x in range(10)]

# Con filtro
even_squares = [x**2 for x in range(10) if x % 2 == 0]

# Múltiples variables
pairs = [(x, y) for x in range(3) for y in range(3)]

# Nested comprehensions
matrix = [[j for j in range(3)] for i in range(3)]
flattened = [item for row in matrix for item in row]

# Con funciones
def is_prime(n):
    return n > 1 and all(n % i != 0 for i in range(2, int(n**0.5) + 1))

primes = [x for x in range(100) if is_prime(x)]
```

#### **Dict y Set Comprehensions:**
```python
# Dictionary comprehensions
word_lengths = {word: len(word) for word in words}
word_count = {word: words.count(word) for word in set(words)}

# Filtering en dict comprehensions
long_words = {word: length for word, length in word_lengths.items() 
              if length > 5}

# Set comprehensions
unique_lengths = {len(word) for word in words}
vowel_words = {word for word in words if word[0].lower() in 'aeiou'}

# Comprehensions anidadas
nested_dict = {
    category: {item: len(item) for item in items}
    for category, items in data.items()
}
```

#### **Performance Comparison:**
```python
import timeit

# List comprehension vs loop tradicional
def traditional_loop():
    result = []
    for x in range(1000):
        if x % 2 == 0:
            result.append(x**2)
    return result

def list_comp():
    return [x**2 for x in range(1000) if x % 2 == 0]

# Generalmente comprehensions son 2-3x más rápidas
```

### **0:40-0:55 - Generators Deep Dive**

#### **Generator Functions:**
```python
def fibonacci_generator(n):
    """Generator que produce secuencia Fibonacci"""
    a, b = 0, 1
    count = 0
    while count < n:
        yield a
        a, b = b, a + b
        count += 1

# Uso
fib_gen = fibonacci_generator(10)
for num in fib_gen:
    print(num)  # Lazy evaluation!

def read_large_file(filename):
    """Memory-efficient file reading"""
    with open(filename, 'r') as file:
        for line in file:
            yield line.strip()  # Solo una línea en memoria
```

#### **Generator Expressions:**
```python
# Generator expression - como list comprehension pero lazy
squares_gen = (x**2 for x in range(1000000))  # No consume memoria inmediatamente
memory_efficient = sum(x**2 for x in range(1000000))  # Muy eficiente

# Pipeline de generators
def process_data(data):
    # Cada paso es lazy
    filtered = (x for x in data if x > 0)
    transformed = (x**2 for x in filtered)
    limited = (x for i, x in enumerate(transformed) if i < 100)
    return limited
```

#### **Ventajas de Generators:**
- **Memory Efficiency:** No cargan todo en memoria
- **Lazy Evaluation:** Computan valores on-demand
- **Infinite Sequences:** Pueden generar secuencias infinitas
- **Pipeline Processing:** Composición elegante de transformaciones

### **0:55-1:00 - Cuándo Usar Cada Uno**

**Decision Tree:**
- **List Comprehension:** Necesitas toda la data inmediatamente, datasets pequeños-medianos
- **Generator:** Datasets grandes, procesamiento pipeline, memory constraints
- **Traditional Loop:** Lógica compleja que no cabe en comprehension

---

## **Segunda Hora: Práctica con LeetCode**

### **1:00-1:20 - Ejercicio Práctico: Data Processing**

```python
# Dataset simulado para practice
sales_data = [
    {'product': 'laptop', 'price': 1200, 'category': 'electronics', 'quantity': 2},
    {'product': 'mouse', 'price': 25, 'category': 'electronics', 'quantity': 5},
    {'product': 'book', 'price': 15, 'category': 'education', 'quantity': 10},
    {'product': 'phone', 'price': 800, 'category': 'electronics', 'quantity': 1},
    # ... más datos
]

def analyze_sales_comprehensions(data):
    """
    Usar comprensiones para analysis eficiente
    """
    # TODO: Implementar usando comprehensions
    
    # 1. Total revenue por producto
    revenue_by_product = {}
    
    # 2. Productos caros (price > 100) por categoría
    expensive_by_category = {}
    
    # 3. Set de todas las categorías únicas
    categories = set()
    
    # 4. Dict de average price por categoría
    avg_prices = {}
    
    return revenue_by_product, expensive_by_category, categories, avg_prices

def process_large_dataset_generator(filename):
    """
    Procesa archivo grande usando generators
    """
    def read_sales_file(filename):
        # TODO: Generator que lee archivo línea por línea
        pass
    
    def parse_line(line):
        # TODO: Convierte línea CSV a dict
        pass
    
    def filter_valid_records(records):
        # TODO: Generator que filtra records válidos
        pass
    
    def calculate_metrics(records):
        # TODO: Procesa usando generators para memory efficiency
        pass
    
    # Pipeline completo
    raw_lines = read_sales_file(filename)
    parsed_records = (parse_line(line) for line in raw_lines)
    valid_records = filter_valid_records(parsed_records)
    return calculate_metrics(valid_records)
```

### **1:20-1:45 - LeetCode Easy Problems**

#### **Problem 1: Two Sum (Array + Dict comprehension)**
```python
def two_sum(nums, target):
    """
    LeetCode #1: Two Sum
    Encuentra índices de dos números que suman target
    
    Input: nums = [2,7,11,15], target = 9
    Output: [0,1] porque nums[0] + nums[1] = 9
    """
    # TODO: Implementar usando dict comprehension + enumeration
    # Hint: Crear dict de {value: index} y buscar complement
    
    pass

def two_sum_all_pairs(nums, target):
    """
    Variación: encuentra TODOS los pares que suman target
    """
    # TODO: Usar set comprehension para evitar duplicados
    pass
```

#### **Problem 2: Valid Anagram (Set operations)**
```python
def is_anagram(s, t):
    """
    LeetCode #242: Valid Anagram
    Determina si t es anagrama de s
    
    Input: s = "anagram", t = "nagaram"
    Output: True
    """
    # TODO: Implementar usando set/dict comprehensions
    # Considera múltiples approaches y su efficiency
    pass

def group_anagrams(strs):
    """
    LeetCode #49: Group Anagrams
    Agrupa strings que son anagramas
    """
    # TODO: Usar dict comprehension + tuple como key
    pass
```

#### **Problem 3: Contains Duplicate (Set efficiency)**
```python
def contains_duplicate(nums):
    """
    LeetCode #217: Contains Duplicate
    Retorna True si algún valor aparece al menos dos veces
    """
    # TODO: Multiple approaches usando set
    # 1. Set length comparison
    # 2. Set building with early termination
    pass

def contains_duplicate_within_k(nums, k):
    """
    Variación: duplicado dentro de k posiciones
    """
    # TODO: Sliding window con set
    pass
```

### **1:45-2:00 - Code Review y Optimization**

```python
def daily_review_session():
    """
    Review session para identificar mejoras
    """
    
    # Performance comparison template
    def compare_approaches(func1, func2, test_data):
        import timeit
        
        time1 = timeit.timeit(lambda: func1(test_data), number=1000)
        time2 = timeit.timeit(lambda: func2(test_data), number=1000)
        
        print(f"Approach 1: {time1:.4f}s")
        print(f"Approach 2: {time2:.4f}s")
        print(f"Speedup: {time1/time2:.2f}x")
    
    # TODO: Aplicar a las soluciones del día
```

---

# **DÍA 4: Decoradores y Funciones Avanzadas**

## **Primera Hora: Teoría y Conceptos**

### **0:00-0:15 - Bridge from Yesterday**
```python
# Uso de generators en decoradores (preview)
def timing_generator():
    """Generator que produce timestamps"""
    import time
    while True:
        yield time.time()

# Hoy aprenderemos a envolver funciones elegantemente
```

### **0:15-0:45 - Decoradores Fundamentals**

#### **Function as First-Class Objects:**
```python
def greet(name):
    return f"Hello, {name}!"

def shout(name):
    return f"HELLO, {name.upper()}!"

# Funciones son objetos
greeting_func = greet
print(greeting_func("World"))  # Hello, World!

# Funciones como argumentos
def apply_greeting(func, name):
    return func(name)

result = apply_greeting(shout, "python")  # HELLO, PYTHON!

# Funciones que retornan funciones
def make_multiplier(n):
    def multiplier(x):
        return x * n
    return multiplier

double = make_multiplier(2)
print(double(5))  # 10
```

#### **Decorador Básico:**
```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finished {func.__name__}")
        return result
    return wrapper

# Uso tradicional
def say_hello():
    print("Hello!")

decorated_hello = my_decorator(say_hello)

# Sintaxis @ (syntactic sugar)
@my_decorator
def say_goodbye():
    print("Goodbye!")

say_goodbye()  # Ejecuta con decorador automáticamente
```

#### **Decoradores Útiles para Entrevistas:**
```python
import time
import functools
from collections import defaultdict

def timing_decorator(func):
    """Mide tiempo de ejecución"""
    @functools.wraps(func)  # Preserva metadata de función original
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

def memoize(func):
    """Cache de resultados para optimización"""
    cache = {}
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Crear key hashable de argumentos
        key = str(args) + str(sorted(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapper

def retry(max_attempts=3, delay=1):
    """Decorador parametrizado para retry logic"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
                    continue
            raise last_exception
        return wrapper
    return decorator

# Uso de decorador parametrizado
@retry(max_attempts=5, delay=0.5)
def unreliable_api_call():
    import random
    if random.random() < 0.7:
        raise Exception("API failed")
    return "Success"
```

### **0:45-1:00 - Funciones Avanzadas**

#### **Args y Kwargs Mastery:**
```python
def flexible_function(*args, **kwargs):
    """Demuestra uso avanzado de args/kwargs"""
    print(f"Positional args: {args}")
    print(f"Keyword args: {kwargs}")
    
    # Unpacking en llamadas
    other_function(*args, **kwargs)

def parameter_validation(*args, required_kwargs=None, **kwargs):
    """Validación avanzada de parámetros"""
    required_kwargs = required_kwargs or []
    
    # Validar kwargs requeridos
    missing = [key for key in required_kwargs if key not in kwargs]
    if missing:
        raise ValueError(f"Missing required kwargs: {missing}")
    
    return args, kwargs

# Funciones de orden superior
def compose(*functions):
    """Compone múltiples funciones"""
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions)

# Ejemplo: compose(str.upper, str.strip, lambda x: x.replace(' ', '_'))
```

---

## **Segunda Hora: Práctica y LeetCode**

### **1:00-1:30 - Proyecto: Decorator Toolkit**

```python
class DecoratorToolkit:
    """
    Colección de decoradores útiles para entrevistas
    """
    
    @staticmethod
    def validate_types(**type_hints):
        """
        Decorador que valida tipos de argumentos
        
        @validate_types(x=int, y=str)
        def func(x, y):
            return f"{y}: {x}"
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # TODO: Implementar validación de tipos
                # Hint: usar inspect module para obtener signature
                pass
            return wrapper
        return decorator
    
    @staticmethod
    def rate_limit(calls_per_second=1):
        """
        Rate limiting decorator
        """
        def decorator(func):
            last_called = [0.0]  # Lista para mutabilidad en closure
            
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # TODO: Implementar rate limiting
                # Hint: usar time.time() y sleep si necesario
                pass
            return wrapper
        return decorator
    
    @staticmethod
    def cache_with_expiry(ttl_seconds=300):
        """
        Cache con time-to-live
        """
        def decorator(func):
            cache = {}
            timestamps = {}
            
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # TODO: Implementar cache con expiry
                # Hint: verificar timestamp + ttl
                pass
            return wrapper
        return decorator

# Tests para decoradores
@DecoratorToolkit.validate_types(x=int, y=str)
def test_function(x, y):
    return f"{y}: {x}"

@DecoratorToolkit.rate_limit(calls_per_second=2)
def api_call():
    return "API response"

@DecoratorToolkit.cache_with_expiry(ttl_seconds=60)
def expensive_computation(n):
    # Simula cálculo costoso
    return sum(i**2 for i in range(n))
```

### **1:30-1:50 - LeetCode Easy: Arrays y Strings**

#### **Problem 1: Remove Duplicates from Sorted Array**
```python
def remove_duplicates(nums):
    """
    LeetCode #26: Remove Duplicates from Sorted Array
    Modifica array in-place, retorna nueva longitud
    
    Input: nums = [1,1,2]
    Output: 2, nums = [1,2,_]
    """
    # TODO: Implementar usando two pointers
    # Bonus: implementar también con list comprehension approach
    pass

def remove_duplicates_generator_approach(nums):
    """
    Approach alternativo usando generators
    """
    # TODO: Crear generator que yielde elementos únicos
    pass
```

#### **Problem 2: Best Time to Buy and Sell Stock**
```python
def max_profit(prices):
    """
    LeetCode #121: Best Time to Buy and Sell Stock
    Encuentra máximo profit de una transacción
    
    Input: prices = [7,1,5,3,6,4]
    Output: 5 (buy at 1, sell at 6)
    """
    # TODO: Implementar O(n) solution
    # Bonus: implementar usando generator expressions
    pass

def max_profit_with_comprehension(prices):
    """
    Approach usando comprehensions para clarity
    """
    # TODO: Usar enumerate + comprehensions
    pass
```

#### **Problem 3: Valid Parentheses**
```python
def is_valid_parentheses(s):
    """
    LeetCode #20: Valid Parentheses
    Verifica si string tiene paréntesis balanceados
    
    Input: s = "()[]{}"
    Output: True
    """
    # TODO: Implementar usando stack (list)
    # Bonus: usar dict comprehension para mapping
    pass

def parentheses_with_generators(s):
    """
    Approach usando generators para memory efficiency
    """
    # TODO: Generator-based solution
    pass
```

### **1:50-2:00 - Code Review y Performance Analysis**

```python
def day3_performance_analysis():
    """
    Analiza performance de diferentes approaches
    """
    import timeit
    import sys
    
    # Comparar list comp vs generator para memory
    def memory_comparison():
        # TODO: Comparar sys.getsizeof() entre approaches
        pass
    
    def speed_comparison():
        # TODO: Timing de diferentes implementations
        pass
    
    # TODO: Documentar findings y trade-offs
```

---

# **DÍA 4: Decoradores Avanzados + More LeetCode**

## **Primera Hora: Decoradores Avanzados**

### **0:00-0:15 - Review + Advanced Preview**
```python
# Review de decoradores básicos del día 3
@timing_decorator
@memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Hoy: decoradores más sofisticados y casos de uso real
```

### **0:15-0:40 - Decoradores con Estado y Clases**

#### **Class-based Decorators:**
```python
class CallCounter:
    """Decorador que cuenta llamadas a función"""
    
    def __init__(self, func):
        self.func = func
        self.count = 0
        functools.update_wrapper(self, func)
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"{self.func.__name__} called {self.count} times")
        return self.func(*args, **kwargs)
    
    def reset_count(self):
        self.count = 0

@CallCounter
def example_function():
    return "Hello World"

# Uso
example_function()  # example_function called 1 times
print(example_function.count)  # 1
example_function.reset_count()
```

#### **Decoradores con Parámetros Complejos:**
```python
def access_control(allowed_roles=None, require_auth=True):
    """
    Decorador para control de acceso
    """
    allowed_roles = allowed_roles or []
    
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # TODO: Implementar lógica de autorización
            # Simular user context con kwargs
            user_role = kwargs.get('user_role', 'guest')
            
            if require_auth and user_role == 'guest':
                raise PermissionError("Authentication required")
            
            if allowed_roles and user_role not in allowed_roles:
                raise PermissionError(f"Role {user_role} not allowed")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

@access_control(allowed_roles=['admin', 'moderator'])
def delete_user(user_id, user_role=None):
    return f"User {user_id} deleted"

# Test
try:
    delete_user(123, user_role='admin')     # OK
    delete_user(123, user_role='user')      # PermissionError
except PermissionError as e:
    print(e)
```

#### **Property Decorators y Descriptors:**
```python
class SmartProperty:
    """
    Descriptor personalizado con validación
    """
    
    def __init__(self, validator=None, default=None):
        self.validator = validator
        self.default = default
        self.name = None
    
    def __set_name__(self, owner, name):
        self.name = f"_{name}"
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.name, self.default)
    
    def __set__(self, obj, value):
        if self.validator and not self.validator(value):
            raise ValueError(f"Invalid value for {self.name}")
        setattr(obj, self.name, value)

class Person:
    # Validators usando lambdas
    age = SmartProperty(validator=lambda x: isinstance(x, int) and 0 <= x <= 150)
    name = SmartProperty(validator=lambda x: isinstance(x, str) and len(x) > 0)
    
    def __init__(self, name, age):
        self.name = name
        self.age = age

# TODO: Test the descriptor
```

### **0:40-1:00 - Functools y Partial Applications**

```python
import functools
import operator

# Partial applications
def power(base, exponent):
    return base ** exponent

square = functools.partial(power, exponent=2)
cube = functools.partial(power, exponent=3)

print(square(5))  # 25
print(cube(3))    # 27

# Reduce para operaciones complejas
def factorial(n):
    return functools.reduce(operator.mul, range(1, n + 1), 1)

def find_gcd_multiple(*numbers):
    """Encuentra GCD de múltiples números"""
    import math
    return functools.reduce(math.gcd, numbers)

# Singledispatch para overloading
@functools.singledispatch
def process_data(arg):
    """Procesa datos según tipo"""
    raise NotImplementedError(f"No implementation for {type(arg)}")

@process_data.register
def _(arg: list):
    return [x**2 for x in arg]

@process_data.register  
def _(arg: dict):
    return {k: v**2 for k, v in arg.items()}

@process_data.register
def _(arg: str):
    return arg.upper()

# TODO: Test singledispatch con diferentes tipos
```

---

## **Segunda Hora: LeetCode + Integration**

### **1:00-1:25 - Advanced LeetCode Easy**

#### **Problem 1: Palindrome Number (String manipulation)**
```python
def is_palindrome_number(x):
    """
    LeetCode #9: Palindrome Number
    Determina si entero es palíndromo sin convertir a string
    """
    # TODO: Implementar sin string conversion
    # Bonus: implementar también con string + comprehension
    pass

@memoize  # Usar decorador del día anterior
def is_palindrome_optimized(x):
    """Versión optimizada con memoization"""
    # TODO: Implementar con cache
    pass
```

#### **Problem 2: Merge Two Sorted Lists (Generator approach)**
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    
    def __iter__(self):
        """Hacer ListNode iterable"""
        current = self
        while current:
            yield current.val
            current = current.next

def merge_two_lists(list1, list2):
    """
    LeetCode #21: Merge Two Sorted Lists
    """
    # TODO: Implementar merge eficiente
    # Bonus: usar generators para lazy evaluation
    pass

def merge_generator(list1, list2):
    """
    Generator que yielda elementos en orden
    """
    # TODO: Generator-based merge
    pass
```

#### **Problem 3: Remove Element (In-place operations)**
```python
def remove_element(nums, val):
    """
    LeetCode #27: Remove Element
    Remueve todas las instancias de val in-place
    """
    # TODO: Two-pointer technique
    # Bonus: implementar usando comprehensions y comparar
    pass

@timing_decorator
def remove_element_comprehension(nums, val):
    """Approach usando list comprehension"""
    # TODO: Implementar y comparar performance
    pass
```

### **1:25-1:45 - Proyecto Integrador: Decorator-Enhanced Data Processor**

```python
class DataProcessor:
    """
    Procesador de datos que usa todos los conceptos del día
    """
    
    def __init__(self):
        self.stats = defaultdict(int)
    
    @timing_decorator
    @memoize
    def process_dataset(self, data, transformations):
        """
        Aplica transformaciones a dataset
        transformations: lista de funciones a aplicar
        """
        # TODO: Usar reduce + partial applications
        pass
    
    @access_control(allowed_roles=['admin', 'analyst'])
    def sensitive_analysis(self, data, user_role=None):
        """
        Análisis que requiere permisos especiales
        """
        # TODO: Implementar análisis avanzado
        pass
    
    @retry(max_attempts=3)
    def fetch_external_data(self, source):
        """
        Simula fetch de datos externos con retry
        """
        # TODO: Simular API call que puede fallar
        pass
    
    @property
    def processing_stats(self):
        """
        Property que retorna estadísticas de procesamiento
        """
        # TODO: Usar dict comprehension para format stats
        pass

# TODO: Implementar tests comprehensivos
def test_data_processor():
    processor = DataProcessor()
    
    # Test data
    sample_data = list(range(1000))
    transformations = [
        lambda x: x**2,
        lambda x: x if x % 2 == 0 else 0,
        lambda x: x // 10
    ]
    
    # TODO: Test todos los métodos
    pass
```

### **1:45-2:00 - Optimization Challenge**

```python
def optimization_challenge():
    """
    Challenge que combina todos los conceptos
    """
    
    # Dataset grande para testing
    large_dataset = [
        {'id': i, 'value': i**2 % 100, 'category': f'cat_{i%10}'}
        for i in range(100000)
    ]
    
    # TODO: Implementar las siguientes funciones de manera óptima:
    
    def find_top_values_per_category(data, top_n=5):
        """
        Encuentra top N valores por categoría
        Usar: comprehensions + generators + functools
        """
        pass
    
    def statistical_summary(data):
        """
        Resumen estadístico usando decoradores para cache/timing
        """
        pass
    
    def data_pipeline(data, *transformations):
        """
        Pipeline de transformaciones usando compose
        """
        pass
    
    # Benchmark todas las implementaciones
    # TODO: Comparar approaches y documentar trade-offs
```

---

## **Checkpoint y Assessment**

### **Skills Validation - Día 4:**

#### **Mini Interview Simulation (15min):**
```python
def interview_question_day4():
    """
    Simula pregunta de entrevista combinando conceptos
    """
    
    # Pregunta: "Implementa un sistema de cache inteligente que:
    # 1. Cache resultados de funciones costosas
    # 2. Tenga TTL configurable  
    # 3. Limite número de entradas (LRU eviction)
    # 4. Proporcione statistics de hit/miss
    # 5. Use decoradores para aplicar a cualquier función"
    
    class SmartCache:
        # TODO: Implementación completa
        pass
    
    # Debe poder usarse como:
    # @SmartCache(max_size=100, ttl=300)
    # def expensive_function(x):
    #     return complex_calculation(x)
```

### **Learning Objectives Checklist:**

**Día 3:**
- [ ] Implemento list/dict/set comprehensions fluentemente
- [ ] Uso generators para memory efficiency
- [ ] Resuelvo 3+ LeetCode Easy usando comprehensions
- [ ] Explico cuándo usar comprehension vs loop tradicional

**Día 4:**
- [ ] Creo decoradores básicos y parametrizados
- [ ] Uso functools efectivamente (wraps, partial, reduce)
- [ ] Combino decoradores con generators/comprehensions
- [ ] Implemento descriptors básicos

### **Recursos Adicionales:**

**Para Profundizar:**
- [Python Decorator Library](https://github.com/lord63/awesome-python-decorator)
- [Functools Documentation](https://docs.python.org/3/library/functools.html)
- [Real Python: Functional Programming](https://realpython.com/python-functional-programming/)

**LeetCode Practice Queue:**
- Two Sum (#1)
- Valid Anagram (#242)  
- Contains Duplicate (#217)
- Remove Duplicates (#26)
- Best Time to Buy Stock (#121)
- Valid Parentheses (#20)

**Tomorrow Preview:** Días 5-6 cubrirán manejo de excepciones, context managers y *args/**kwargs mastery.

---

## **Homework y Preparación Día 5:**

### **Pre-work para Día 5:**
1. **Leer:** [Context Managers PEP 343](https://peps.python.org/pep-0343/)
2. **Revisar:** Ejemplos de with statements en código propio
3. **Preparar:** Lista de escenarios donde usarías context managers

### **Extended Practice (Opcional):**

#### **Challenge Problem: Advanced Generator Pipeline**
```python
def create_data_processing_pipeline():
    """
    Crea pipeline completo usando generators + decoradores
    """
    
    @timing_decorator
    def data_source(filename):
        """Generator que lee datos de archivo"""
        # TODO: Implementar file reading generator
        pass
    
    @memoize
    def transform_record(record):
        """Transforma un record individual"""
        # TODO: Expensive transformation con cache
        pass
    
    def filter_pipeline(data_gen, *filters):
        """
        Aplica múltiples filtros usando generator composition
        """
        # TODO: Chain filters usando functools.reduce
        pass
    
    def aggregation_pipeline(data_gen, aggregators):
        """
        Aplica agregaciones usando comprehensions
        """
        # TODO: Dict comprehension con múltiples aggregators
        pass
    
    # Complete pipeline
    def full_pipeline(filename, filters, aggregators):
        raw_data = data_source(filename)
        transformed = (transform_record(record) for record in raw_data)
        filtered = filter_pipeline(transformed, *filters)
        return aggregation_pipeline(filtered, aggregators)
    
    return full_pipeline

# Test el pipeline con datos simulados
```

#### **Advanced LeetCode Practice:**
```python
def bonus_leetcode_problems():
    """
    Problemas adicionales que combinan día 3-4 concepts
    """
    
    def single_number(nums):
        """
        LeetCode #136: Single Number
        Encuentra el número que aparece una sola vez
        TODO: Usar set operations elegantemente
        """
        pass
    
    def intersection_of_arrays(nums1, nums2):
        """
        LeetCode #349: Intersection of Two Arrays
        TODO: Múltiples approaches con set comprehensions
        """
        pass
    
    def first_unique_character(s):
        """
        LeetCode #387: First Unique Character
        TODO: Dict comprehension + enumerate
        """
        pass
    
    def reverse_string(s):
        """
        LeetCode #344: Reverse String (in-place)
        TODO: Usar slicing y comprehensions
        """
        pass

# Implementar todos con focus en elegancia + efficiency
```

---

## **Métricas de Éxito Días 3-4:**

### **Technical Mastery:**
- Implementas comprehensions complejas sin hesitar
- Creas decoradores para casos de uso reales
- Resuelves LeetCode Easy en <15min explicando approach
- Combinas múltiples conceptos en soluciones elegantes

### **Interview Readiness:**
- Explicas trade-offs entre comprehensions y loops tradicionales
- Justificas uso de generators vs lists
- Demuestras decoradores con ejemplos prácticos
- Optimizas código existente usando estos conceptos

### **Code Quality Indicators:**
- Código legible y pythónico
- Uso apropiado de each construct
- Performance consciousness
- Proper error handling y edge cases

### **Momentum Building:**
```python
# Daily progress tracker
progress_tracker = {
    'day_1': {'concepts_mastered': [], 'exercises_completed': [], 'confidence': 0},
    'day_2': {'concepts_mastered': [], 'exercises_completed': [], 'confidence': 0},
    'day_3': {'concepts_mastered': [], 'exercises_completed': [], 'confidence': 0},
    'day_4': {'concepts_mastered': [], 'exercises_completed': [], 'confidence': 0}
}

# TODO: Update diariamente y track progress
```

**¡Excelente trabajo en estos días fundamentales!** La base sólida que estás construyendo te permitirá tacklear problemas más complejos con confianza. 🎯