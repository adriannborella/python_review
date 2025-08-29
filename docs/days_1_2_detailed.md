# Días 1-2: Fundamentos Python Core
## Estructuras de Datos Nativas + Complejidades Temporales

---

# **DÍA 1: Listas y Diccionarios**

## **Primera Hora: Teoría y Conceptos**

### **0:00-0:15 - Repaso Conceptual**
**Objetivos del día:**
- Dominar operaciones fundamentales de listas y diccionarios
- Entender complejidades temporales de cada operación
- Identificar cuándo usar cada estructura de datos

### **0:15-0:40 - Listas (Lists) Deep Dive**

#### **Operaciones Básicas y sus Complejidades:**
```python
# Creación - O(n)
lista = [1, 2, 3, 4, 5]
lista_comp = [x**2 for x in range(1000)]  # List comprehension

# Acceso por índice - O(1)
elemento = lista[2]

# Inserción
lista.append(6)        # O(1) - al final
lista.insert(0, 0)     # O(n) - al inicio o medio
lista.extend([7, 8])   # O(k) donde k es longitud de iterable

# Eliminación
lista.pop()           # O(1) - último elemento
lista.pop(0)          # O(n) - primer elemento
lista.remove(3)       # O(n) - busca y elimina
del lista[1]          # O(n) - elimina por índice

# Búsqueda
if 5 in lista:        # O(n) - búsqueda lineal
    print("Found")

# Ordenamiento
lista.sort()          # O(n log n) - in-place
sorted_lista = sorted(lista)  # O(n log n) - nueva lista
```

#### **Conceptos Importantes:**
- **Dynamic Array:** Las listas crecen automáticamente
- **Memory Layout:** Elementos contiguos en memoria
- **Amortized O(1):** append() promediado en el tiempo

### **0:40-0:50 - Diccionarios (Dictionaries)**

```python
# Creación - O(n)
dic = {'a': 1, 'b': 2, 'c': 3}
dic_comp = {str(i): i**2 for i in range(100)}

# Acceso - O(1) promedio, O(n) peor caso
valor = dic['a']
valor = dic.get('d', 0)  # Con default

# Inserción/Actualización - O(1) promedio
dic['d'] = 4
dic.update({'e': 5, 'f': 6})

# Eliminación - O(1) promedio
del dic['a']
valor = dic.pop('b', None)

# Iteración - O(n)
for key in dic:           # Sobre keys
for value in dic.values(): # Sobre values
for k, v in dic.items():  # Sobre pares key-value
```

#### **Hash Tables Fundamentals:**
- **Hash Function:** Convierte keys en índices
- **Collision Handling:** Python usa open addressing
- **Load Factor:** Ratio de slots ocupados
- **Resizing:** Se redimensiona cuando load factor > 0.66

### **0:50-1:00 - Síntesis y Notas**
**Cuándo usar cada estructura:**
- **Lista:** Orden importa, acceso por índice, elementos duplicados
- **Diccionario:** Acceso rápido por clave, mapeo key-value

---

## **Segunda Hora: Práctica Intensiva**

### **1:00-1:45 - Ejercicios Progresivos**

#### **Ejercicio 1: List Operations (15min)**
```python
def analyze_list_operations():
    """
    Implementa y mide tiempo de diferentes operaciones
    """
    import time
    
    # TODO: Implementar y cronometrar:
    # 1. Crear lista de 100,000 elementos
    # 2. Acceder a elemento en posición 50,000
    # 3. Insertar elemento al inicio vs final
    # 4. Buscar elemento existente vs no existente
    # 5. Eliminar elemento del inicio vs final
    
    # Starter code:
    large_list = list(range(100000))
    
    # Tu implementación aquí
    pass

# Ejecutar y documentar resultados
```

#### **Ejercicio 2: Dictionary Performance (15min)**
```python
def dictionary_vs_list_search():
    """
    Compara performance de búsqueda en dict vs list
    """
    # TODO: 
    # 1. Crear lista con 10,000 números aleatorios
    # 2. Crear diccionario con mismos números como keys
    # 3. Buscar 1,000 números aleatorios en ambas estructuras
    # 4. Comparar tiempos de ejecución
    
    import random
    import time
    
    # Tu implementación aquí
    pass
```

#### **Ejercicio 3: Real-world Application (15min)**
```python
def word_frequency_counter(text):
    """
    Cuenta frecuencia de palabras en texto
    Optimiza para performance
    """
    # TODO: Implementar contador eficiente
    # Considera: case sensitivity, punctuation, empty strings
    pass

def group_by_property(items, key_func):
    """
    Agrupa items por resultado de key_func
    Ejemplo: group_by_property(students, lambda x: x.grade)
    """
    # TODO: Implementar agrupación eficiente
    pass

# Test data
sample_text = """
Python is an amazing programming language. 
Python is easy to learn and Python is powerful.
Many developers love Python for its simplicity.
"""
```

### **1:45-1:55 - Testing y Validation**
```python
# Tests unitarios para verificar implementaciones
def test_implementations():
    # Verificar correctness de todas las funciones
    # Validar edge cases
    # Confirmar complejidades esperadas
    pass
```

### **1:55-2:00 - Reflexión del Día**
**Preguntas de autoevaluación:**
1. ¿Puedo explicar por qué dict lookup es O(1)?
   1. Los diccionarios usan matemáticas (función hash) para convertir claves en direcciones de memoria, permitiendo acceso directo en lugar de búsqueda secuencial. ¡Por eso son tan eficientes!
2. ¿Cuándo preferiría list sobre dict y viceversa?
   1. Usa LISTA cuando:
    ✅ Necesitas mantener orden específico
    ✅ Accedes por posición (primero, último, índice n)
    ✅ Permites elementos duplicados
    ✅ Haces operaciones como sort, reverse, append
    ✅ Iteras secuencialmente la mayoría del tiempo

    Usa DICCIONARIO cuando:
    ✅ Necesitas búsquedas rápidas por clave
    ✅ Tienes relación clave-valor natural
    ✅ Haces conteos o agrupaciones
    ✅ Necesitas cache/memoización
    ✅ Las claves son únicas e identifican elementos

3. ¿Qué optimizaciones aplicaría en código real?

---

# **DÍA 2: Sets, Tuplas y Optimizaciones**

## **Primera Hora: Teoría y Conceptos**

### **0:00-0:15 - Review + Preview**
- Repaso rápido de listas y diccionarios
- Objetivo: Completar toolkit de estructuras básicas

### **0:15-0:35 - Sets Deep Dive**

```python
# Creación y características
conjunto = {1, 2, 3, 4, 5}
set_from_list = set([1, 2, 2, 3, 3])  # Elimina duplicados
empty_set = set()  # NO usar {} - eso es dict vacío

# Operaciones fundamentales - O(1) promedio
conjunto.add(6)
conjunto.remove(1)      # KeyError si no existe
conjunto.discard(1)     # No error si no existe
elemento = conjunto.pop()  # Elimina elemento arbitrario

# Operaciones de conjunto - Muy eficientes
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}

union = set1 | set2              # {1, 2, 3, 4, 5, 6}
interseccion = set1 & set2       # {3, 4}
diferencia = set1 - set2         # {1, 2}
dif_simetrica = set1 ^ set2      # {1, 2, 5, 6}

# Métodos equivalentes
union = set1.union(set2)
interseccion = set1.intersection(set2)
```

#### **Casos de Uso Principales:**
- **Eliminar duplicados:** `unique_items = set(list_with_dupes)`
- **Membership testing:** `if item in my_set:` - Muy rápido
- **Operaciones matemáticas:** Unión, intersección, diferencia

### **0:35-0:50 - Tuplas y Inmutabilidad**

```python
# Creación y características
tupla = (1, 2, 3, 4, 5)
tupla_single = (42,)  # Nota la coma para tupla de un elemento
tupla_sin_parentesis = 1, 2, 3, 4, 5  # Tuple packing

# Inmutabilidad
# tupla[0] = 10  # TypeError! No se puede modificar

# Operaciones permitidas - O(1) para acceso
elemento = tupla[2]
longitud = len(tupla)

# Búsqueda - O(n)
indice = tupla.index(3)
veces = tupla.count(2)

# Tuple unpacking - Muy útil
a, b, c, d, e = tupla
primer, *resto, ultimo = tupla  # Extended unpacking
```

#### **Ventajas de Tuplas:**
- **Inmutabilidad:** Thread-safe, hashable
- **Performance:** Más rápidas que listas para acceso
- **Memory:** Menos overhead que listas
- **Dictionary keys:** Pueden ser keys en diccionarios

### **0:50-1:00 - Memory y Performance Insights**

```python
import sys

# Comparación de memoria
lista = [1, 2, 3, 4, 5]
tupla = (1, 2, 3, 4, 5)
conjunto = {1, 2, 3, 4, 5}

print(f"Lista: {sys.getsizeof(lista)} bytes")
print(f"Tupla: {sys.getsizeof(tupla)} bytes")
print(f"Set: {sys.getsizeof(conjunto)} bytes")

# Timing comparisons
import timeit

# Membership testing
lista_timing = timeit.timeit('1000 in lista', 
                           setup='lista = list(range(10000))', 
                           number=1000)
set_timing = timeit.timeit('1000 in conjunto', 
                         setup='conjunto = set(range(10000))', 
                         number=1000)
```

---

## **Segunda Hora: Práctica Avanzada**

### **1:00-1:30 - Ejercicios de Aplicación**

#### **Ejercicio 1: Set Operations Mastery (15min)**
```python
def find_common_elements(*lists):
    """
    Encuentra elementos comunes en múltiples listas
    Input: find_common_elements([1,2,3], [2,3,4], [3,4,5])
    Output: [3]
    """
    # TODO: Implementar usando sets de manera eficiente
    pass

def remove_duplicates_preserve_order(items):
    """
    Remueve duplicados manteniendo orden original
    Input: [1,2,2,3,1,4]
    Output: [1,2,3,4]
    """
    # TODO: Combinar set + list para eficiencia
    pass

def symmetric_difference_multiple(*sets):
    """
    Encuentra elementos que están en exactamente uno de los sets
    """
    # TODO: Usar operaciones de set
    pass
```

#### **Ejercicio 2: Tuple Applications (15min)**
```python
def create_coordinate_system():
    """
    Sistema de coordenadas usando tuplas
    """
    # TODO: 
    # 1. Crear clase Point usando namedtuple
    # 2. Implementar cálculos de distancia
    # 3. Usar tuplas como keys en dict para memoization
    from collections import namedtuple
    pass

def swap_variables_demo():
    """
    Demuestra diferentes formas de intercambiar variables
    """
    # TODO: 
    # 1. Intercambio tradicional con temp
    # 2. Intercambio pythónico con tuplas
    # 3. Intercambio múltiple
    pass
```

### **1:30-1:50 - Proyecto Integrador**
```python
class DataAnalyzer:
    """
    Analizador de datos que demuestra uso óptimo de estructuras
    """
    
    def __init__(self):
        self.data = []
        self.cache = {}  # Para memoization
        self.unique_values = set()
        
    def add_record(self, record):
        """
        Agrega registro y mantiene estructuras actualizadas
        record: tuple de (id, category, value, timestamp)
        """
        # TODO: Implementar
        pass
    
    def get_statistics(self):
        """
        Retorna estadísticas usando todas las estructuras eficientemente
        """
        # TODO: Usar dict para conteos, set para únicos, tuple para resultados
        pass
    
    def find_outliers(self, threshold=2.0):
        """
        Encuentra valores atípicos usando set operations
        """
        # TODO: Implementar detección de outliers
        pass
    
    def group_by_category(self):
        """
        Agrupa datos por categoría optimizando performance
        """
        # TODO: Usar defaultdict + sets
        pass

# Test del analyzer
analyzer = DataAnalyzer()
# TODO: Agregar datos de prueba y validar
```

### **1:50-2:00 - Review y Documentación**

#### **Performance Summary Table:**
```python
def create_performance_cheatsheet():
    """
    Crea tabla de referencia de complejidades
    """
    operations = {
        'List': {
            'Access': 'O(1)',
            'Search': 'O(n)',
            'Insertion': 'O(1) append, O(n) insert',
            'Deletion': 'O(1) pop, O(n) remove'
        },
        'Dict': {
            'Access': 'O(1) avg',
            'Search': 'O(1) avg', 
            'Insertion': 'O(1) avg',
            'Deletion': 'O(1) avg'
        },
        'Set': {
            'Access': 'N/A',
            'Search': 'O(1) avg',
            'Insertion': 'O(1) avg', 
            'Deletion': 'O(1) avg'
        },
        'Tuple': {
            'Access': 'O(1)',
            'Search': 'O(n)',
            'Insertion': 'Immutable',
            'Deletion': 'Immutable'
        }
    }
    # TODO: Imprimir tabla formateada
```

---

## **Recursos y Material de Apoyo**

### **Documentación Oficial:**
- [Python Data Structures](https://docs.python.org/3/tutorial/datastructures.html)
- [Built-in Types](https://docs.python.org/3/library/stdtypes.html)

### **Testing Framework:**
```python
import unittest
import time
from collections import defaultdict

class TestDataStructures(unittest.TestCase):
    
    def test_list_operations(self):
        # TODO: Tests para verificar correctness
        pass
    
    def test_performance_requirements(self):
        # TODO: Tests que validen complejidades
        pass
    
    def test_edge_cases(self):
        # TODO: Empty collections, large datasets, etc.
        pass

if __name__ == '__main__':
    unittest.main()
```

### **Ejercicios Adicionales (Si terminas temprano):**

1. **Implementa una LRU Cache** usando dict + doubly linked list
La caché LRU (Least Recently Used) es una técnica de gestión de memoria caché que elimina los elementos menos recientemente utilizados cuando la caché se llena, dando espacio para nuevos elementos. En esencia, prioriza la retención de datos que han sido accedidos más recientemente, asumiendo que estos son más propensos a ser utilizados de nuevo en el futuro. 
¿Cómo funciona?
1. Acceso a datos:
Cada vez que se accede a un elemento en la caché, se considera el más recientemente utilizado y se mueve a la parte superior de la estructura de datos de la caché. 
2. Llenado de la caché:
Cuando la caché alcanza su capacidad máxima y se intenta insertar un nuevo elemento, el elemento menos recientemente utilizado (es decir, el que está en la parte inferior de la estructura de datos) se elimina para hacer espacio. 
3. Implementación:
Comúnmente, una caché LRU se implementa utilizando una combinación de una lista doblemente enlazada y un mapa hash. 
La lista doblemente enlazada mantiene el orden de uso de los elementos (el más reciente al principio, el menos reciente al final). 
El mapa hash permite un acceso rápido a los elementos por su clave. 
Ventajas de LRU:
Eficiencia:
LRU ofrece un buen equilibrio entre rendimiento y uso de memoria, lo que lo hace adecuado para muchas aplicaciones.
Predicción:
Se centra únicamente en la frecuencia de acceso, lo que permite que sus decisiones de desalojo sean predecibles y consistentes.
Popularidad:
Muchos sistemas, como bases de datos, navegadores web y sistemas operativos, utilizan LRU debido a su eficacia. 
Desventajas de LRU:
Complejidad:
La implementación puede ser más compleja que otras políticas de reemplazo de caché.
Requisitos de memoria:
Puede requerir más memoria que otras estrategias si la caché es demasiado pequeña, ya que debe mantener la estructura de la lista doblemente enlazada.
Error detection:
La detección de errores puede ser más difícil en comparación con otros algoritmos

2. **Crea un Bloom Filter** básico usando sets
Un filtro Bloom es una estructura de datos probabilística que se utiliza para verificar si un elemento pertenece a un conjunto, con la posibilidad de falsos positivos pero sin falsos negativos. Es eficiente en términos de espacio, ocupando un tamaño fijo y pequeño, ideal para conjuntos muy grandes. 

Funcionamiento:
1. Inicialización:
Se crea un vector de bits, inicialmente todos en 0, y un conjunto de funciones hash. 
2. Inserción:
Para agregar un elemento, se aplica cada función hash al elemento. Los bits en las posiciones indicadas por los resultados de las funciones hash se establecen en 1. 
3. Búsqueda:
Para verificar si un elemento pertenece, se aplican las mismas funciones hash. Si todos los bits en las posiciones resultantes son 1, el elemento "puede estar" en el conjunto (posible falso positivo). Si al menos uno es 0, el elemento "no está" en el conjunto. 
Ventajas:
Eficiencia en espacio: Usa una cantidad fija y pequeña de memoria, independientemente del tamaño del conjunto. 
Velocidad: Las operaciones de inserción y búsqueda son rápidas, típicamente O(k), donde k es el número de funciones hash. 
No hay falsos negativos: Si el filtro indica que un elemento no está, es seguro que no está. 
Desventajas:
Posibles falsos positivos:
El filtro puede indicar que un elemento está presente cuando en realidad no lo está. 
No se pueden eliminar elementos:
Una vez que un elemento se inserta, no se puede eliminar de manera segura, ya que podría afectar a otros elementos. 
Aplicaciones:
Caché: Verificar si un elemento está en la caché antes de acceder a una fuente de datos más lenta. 
Detección de spam: Identificar mensajes de correo electrónico o URLs sospechosas. 
Verificación de contraseñas: Comprobar si una contraseña ya ha sido utilizada. 
Bases de datos: Optimizar consultas buscando elementos en un conjunto grande. 
Redis: Redis proporciona un módulo de filtro Bloom. 
Apache Parquet: Se utiliza en filtros Bloom de bloque dividido para optimizar el almacenamiento. 

3. **Benchmark diferentes approaches** para eliminar duplicados
En español, "benchmark" se refiere a un punto de referencia o criterio de comparación. Se utiliza para evaluar el rendimiento de algo, ya sea un producto, servicio, proceso, o incluso una estrategia, comparándolo con algo establecido como estándar o con el rendimiento de otros similares. En esencia, es una herramienta para medir y mejorar. 
4. **Implementa defaultdict** desde cero usando dict

---

## **Objetivos de Aprendizaje - Checklist**

### **Día 1:**
- [ ] Explico diferencias entre list y dict con ejemplos
- [ ] Identifico complejidad temporal de operaciones básicas
- [ ] Implemento búsqueda eficiente usando estructuras apropiadas
- [ ] Resuelvo problemas de conteo y agrupación

### **Día 2:**
- [ ] Uso sets para operaciones de conjunto eficientemente
- [ ] Aplico tuplas en contextos apropiados (immutability)
- [ ] Combino diferentes estructuras para soluciones óptimas
- [ ] Puedo justificar elección de estructura para problema dado

### **Assessment Final:**
Deberías poder resolver en <10min:
```python
def interview_question(words_list):
    """
    Dada una lista de palabras, encuentra:
    1. Palabras únicas (sin duplicados)
    2. Palabras que aparecen más de una vez
    3. Conteo de cada palabra
    4. Las 3 palabras más frecuentes
    
    Optimiza para mejor complejidad temporal posible.
    """
    # Tu solución debe usar las estructuras apropiadas
    pass
```

**¡Éxito en estos primeros días fundamentales!** 🚀

Reglas de Decisión Rápida:
Usa SET cuando:
✅ Necesitas eliminar duplicados
✅ Haces muchas verificaciones de "existe/no existe"
✅ Realizas operaciones matemáticas entre conjuntos
✅ No te importa el orden de elementos
✅ Solo necesitas elementos únicos
Usa DICT cuando:
✅ Tienes relación clave-valor
✅ Necesitas búsquedas rápidas por identificador
✅ Haces conteos o agrupaciones
✅ Implementas cache/memoización
✅ Manejas configuración o metadatos
Usa TUPLA cuando:
✅ Los datos no deben cambiar (inmutabilidad)
✅ Necesitas usar como key en diccionario
✅ Retornas múltiples valores de función
✅ Representas coordenadas o datos estructurados
✅ Haces unpacking o intercambio de variables