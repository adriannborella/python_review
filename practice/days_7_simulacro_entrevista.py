"""
SIMULACRO DE ENTREVISTA TÉCNICA - DÍA 7
Duración: 45 minutos
Formato: Live coding session

INSTRUCCIONES:
- Piensa en voz alta mientras programas
- Pregunta por clarificaciones cuando sea necesario
- Optimiza gradualmente (primera versión que funcione, luego optimizar)
- Considera edge cases
"""

# =============================================================================
# PROBLEMA 1: MERGE INTERVALS (15 minutos)
# Nivel: Medio - Muy común en entrevistas
# =============================================================================

def merge_intervals(intervals):
    """
    Dada una lista de intervalos, merge todos los intervalos superpuestos.
    
    Ejemplo:
    Input: [[1,3],[2,6],[8,10],[15,18]]
    Output: [[1,6],[8,10],[15,18]]
    
    Input: [[1,4],[4,5]]
    Output: [[1,5]]
    
    Pasos del entrevistador:
    1. ¿Cómo abordarías este problema?
    2. ¿Cuál sería la complejidad temporal?
    3. ¿Qué edge cases consideras?
    
    TODO: Implementa la solución
    Tiempo límite: 15 minutos
    """
    
    # Tu solución aquí
    if not intervals:
        return []
    
    # Paso 1: Ordenar por inicio de intervalo
    intervals.sort(key=lambda x: x[0])
    
    # Paso 2: Merge intervalos superpuestos
    merged = [intervals[0]]
    merged.
    for current in intervals[1:]:
        last_merged = merged[-1]
        
        # Si hay superposición, hacer merge
        if current[0] <= last_merged[1]:
            merged[-1] = [last_merged[0], max(last_merged[1], current[1])]
        else:
            # No hay superposición, agregar nuevo intervalo
            merged.append(current)
    
    return merged

# Test cases
test_cases_intervals = [
    [[1,3],[2,6],[8,10],[15,18]],
    [[1,4],[4,5]],
    [[1,4],[2,3]],
    [],
    [[1,1],[2,2],[3,3]]
]

print("PROBLEMA 1: MERGE INTERVALS")
print("-" * 40)
for i, case in enumerate(test_cases_intervals):
    result = merge_intervals(case)
    print(f"Test {i+1}: {case} -> {result}")

# =============================================================================
# PROBLEMA 2: DESIGN PATTERN - CACHE SYSTEM (15 minutos)
# Implementa un sistema de cache con TTL (Time To Live)
# =============================================================================

import time
from collections import OrderedDict

class TTLCache:
    """
    Implementa un cache con las siguientes características:
    1. Capacidad máxima
    2. TTL (Time To Live) por entrada
    3. LRU eviction cuando se alcanza capacidad máxima
    
    Preguntas del entrevistador:
    1. ¿Cómo manejarías la expiración automática?
    2. ¿Qué estructura de datos usarías?
    3. ¿Cómo optimizarías las operaciones get/set?
    
    TODO: Implementa la clase completa
    """
    
    def __init__(self, capacity=100, default_ttl=300):
        self.capacity = capacity
        self.default_ttl = default_ttl
        self.cache = OrderedDict()  # Para LRU
        self.expiry_times = {}      # Mapeo key -> timestamp de expiración
    
    def _is_expired(self, key):
        """Verifica si una key ha expirado"""
        if key not in self.expiry_times:
            return True
        return time.time() > self.expiry_times[key]
    
    def _cleanup_expired(self):
        """Limpia entradas expiradas"""
        current_time = time.time()
        expired_keys = [
            key for key, expiry in self.expiry_times.items() 
            if current_time > expiry
        ]
        
        for key in expired_keys:
            self.cache.pop(key, None)
            self.expiry_times.pop(key, None)
    
    def get(self, key):
        """Obtiene valor del cache"""
        # Limpiar expirados
        self._cleanup_expired()
        
        # Verificar si existe y no ha expirado
        if key not in self.cache or self._is_expired(key):
            return None
        
        # Mover al final (LRU)
        value = self.cache.pop(key)
        self.cache[key] = value
        
        return value
    
    def set(self, key, value, ttl=None):
        """Establece valor en el cache"""
        # Usar TTL por defecto si no se especifica
        if ttl is None:
            ttl = self.default_ttl
        
        # Limpiar expirados
        self._cleanup_expired()
        
        # Si ya existe, actualizar
        if key in self.cache:
            self.cache.pop(key)
        
        # Si está lleno, remover el menos usado (LRU)
        elif len(self.cache) >= self.capacity:
            oldest_key = next(iter(self.cache))
            self.cache.pop(oldest_key)
            self.expiry_times.pop(oldest_key, None)
        
        # Agregar nuevo valor
        self.cache[key] = value
        self.expiry_times[key] = time.time() + ttl
    
    def size(self):
        """Retorna el tamaño actual del cache (sin expirados)"""
        self._cleanup_expired()
        return len(self.cache)
    
    def clear(self):
        """Limpia todo el cache"""
        self.cache.clear()
        self.expiry_times.clear()

# Test del cache
print("\nPROBLEMA 2: TTL CACHE SYSTEM")
print("-" * 40)

cache = TTLCache(capacity=3, default_ttl=2)  # 2 segundos TTL

# Test operaciones básicas
cache.set("user:1", {"name": "Alice", "age": 30})
cache.set("user:2", {"name": "Bob", "age": 25})
cache.set("user:3", {"name": "Charlie", "age": 35})

print(f"Cache size: {cache.size()}")
print(f"Get user:1: {cache.get('user:1')}")

# Test capacidad máxima (LRU eviction)
cache.set("user:4", {"name": "David", "age": 40})
print(f"After adding user:4, size: {cache.size()}")
print(f"Get user:1 (should be evicted): {cache.get('user:1')}")

# Test TTL expiration
print("Waiting for TTL expiration...")
time.sleep(2.1)  # Esperar a que expiren
print(f"After TTL expiration, size: {cache.size()}")

# =============================================================================
# PROBLEMA 3: ALGORITMO STRING MANIPULATION (15 minutos)
# Encuentra el substring más largo sin caracteres repetidos
# =============================================================================

def longest_unique_substring(s):
    """
    Encuentra la longitud del substring más largo sin caracteres repetidos.
    
    Ejemplo:
    "abcabcbb" -> 3 ("abc")
    "bbbbb" -> 1 ("b")
    "pwwkew" -> 3 ("wke")
    
    Preguntas del entrevistador:
    1. ¿Qué enfoque usarías? (Sliding window)
    2. ¿Cómo trackeas caracteres únicos?
    3. ¿Cuál es la complejidad temporal?
    
    TODO: Implementa usando sliding window technique
    """
    
    if not s:
        return 0
    
    # Sliding window approach
    char_index = {}  # Mapeo char -> último índice visto
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        char = s[right]
        
        # Si el caracter ya existe en la ventana actual
        if char in char_index and char_index[char] >= left:
            # Mover left pointer después de la última ocurrencia
            left = char_index[char] + 1
        
        # Actualizar el índice del caracter
        char_index[char] = right
        
        # Calcular longitud actual y actualizar máximo
        current_length = right - left + 1
        max_length = max(max_length, current_length)
    
    return max_length

def longest_unique_substring_with_details(s):
    """
    Versión que también retorna el substring
    """
    if not s:
        return 0, ""
    
    char_index = {}
    left = 0
    max_length = 0
    result_start = 0
    
    for right in range(len(s)):
        char = s[right]
        
        if char in char_index and char_index[char] >= left:
            left = char_index[char] + 1
        
        char_index[char] = right
        
        current_length = right - left + 1
        if current_length > max_length:
            max_length = current_length
            result_start = left
    
    return max_length, s[result_start:result_start + max_length]

# Test cases
test_strings = [
    "abcabcbb",
    "bbbbb",
    "pwwkew",
    "",
    "abcdef",
    "aab"
]

print("\nPROBLEMA 3: LONGEST UNIQUE SUBSTRING")
print("-" * 50)
for s in test_strings:
    length, substring = longest_unique_substring_with_details(s)
    print(f"'{s}' -> Length: {length}, Substring: '{substring}'")

# =============================================================================
# QUESTIONS BEHAVIORALES - PREPARACIÓN
# =============================================================================

print("\n" + "="*60)
print("PREGUNTAS COMPORTAMENTALES - PREPARACIÓN")
print("="*60)

behavioral_questions = {
    "Resolución de Problemas": [
        "Describe un problema técnico complejo que resolviste recientemente",
        "¿Cómo abordas un problema cuando no conoces la solución inmediatamente?",
        "Cuéntame sobre una vez que tuviste que debuggear un issue difícil"
    ],
    
    "Trabajo en Equipo": [
        "Describe una situación donde tuviste que trabajar con un compañero difícil",
        "¿Cómo manejas disagreements técnicos en code reviews?",
        "Cuéntame sobre un proyecto donde fuiste mentor de otro desarrollador"
    ],
    
    "Liderazgo Técnico": [
        "Describe una decisión técnica difícil que tuviste que tomar",
        "¿Cómo convences a tu equipo de adoptar una nueva tecnología/enfoque?",
        "Cuéntame sobre una vez que mejoraste significativamente el performance de un sistema"
    ]
}

print("\nPreparate respuestas usando el formato STAR:")
print("Situation - Task - Action - Result")
print("\nCategorías de preguntas:")

for category, questions in behavioral_questions.items():
    print(f"\n{category.upper()}:")
    for i, question in enumerate(questions, 1):
        print(f"  {i}. {question}")

# =============================================================================
# FEEDBACK Y EVALUACIÓN
# =============================================================================

def evaluate_performance():
    """
    Criterios de evaluación para el simulacro
    """
    criteria = {
        "Problem Solving": {
            "description": "Capacidad para descomponer problemas complejos",
            "indicators": [
                "Hizo preguntas clarificadoras",
                "Identificó edge cases",
                "Propuso múltiples enfoques",
                "Explicó trade-offs"
            ]
        },
        "Coding Skills": {
            "description": "Calidad del código producido",
            "indicators": [
                "Código limpio y legible",
                "Manejo correcto de estructuras de datos",
                "Optimización apropiada",
                "Testing básico considerado"
            ]
        },
        "Communication": {
            "description": "Capacidad de explicar soluciones",
            "indicators": [
                "Pensamiento en voz alta",
                "Explicación clara de algoritmos",
                "Justificación de decisiones",
                "Receptivo a feedback"
            ]
        }
    }
    
    print("\n" + "="*60)
    print("CRITERIOS DE EVALUACIÓN")
    print("="*60)
    
    for skill, details in criteria.items():
        print(f"\n{skill.upper()}:")
        print(f"  {details['description']}")
        print("  Indicadores:")
        for indicator in details['indicators']:
            print(f"    □ {indicator}")
    
    print("\n" + "="*60)
    print("PRÓXIMOS PASOS:")
    print("="*60)
    print("□ Identificar áreas de mejora")
    print("□ Practicar problemas similares en LeetCode")
    print("□ Preparar historias STAR para behaviorales")
    print("□ Review de conceptos débiles identificados")
    print("□ Continuar con Semana 2: Algoritmos y Complejidad")

if __name__ == "__main__":
    evaluate_performance()
