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

    def __init__(self, capacity, default_ttl):
        self.capacity = capacity
        self.ttl = default_ttl
        self.cache = {}

    def set(self, key, value):
        # Filter the old cache before check the capacity
        current_time = time.time()
        self.cache = {
            key: value
            for key, value in self.cache.items()
            if value["ttl"] - current_time <= self.ttl
        }

        if len(self.cache.keys()) == self.capacity:
            return Exception("Cache is full")

        self.cache[key] = {**value, "ttl": time.time()}

        print(f"New element added {key}")
        print(self.cache)

    def size(self):
        # Cantidad de elementos
        return len(self.cache.keys())
        # Tamaño de memoria
        return self.cache.__sizeof__()

    def get(self, key):
        result = self.cache[key].copy()
        del result["ttl"]
        return result

    def clear(self):
        self.cache.clear()


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
