"""
HASH TABLES - IMPLEMENTACIÓN COMPLETA DESDE CERO
===============================================

Una hash table combina:
1. Función hash: Convierte key → índice
2. Array: Almacena los valores
3. Collision handling: Maneja cuando dos keys → mismo índice

COMPLEJIDADES:
- Average case: O(1) para search/insert/delete
- Worst case: O(n) si muchas colisiones
- Space: O(n)

COLLISION HANDLING STRATEGIES:
1. Separate Chaining (implementaremos)
2. Open Addressing (Linear/Quadratic Probing)
3. Robin Hood Hashing (avanzado)
"""

class HashNode:
    """Nodo para separate chaining"""
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashTable:
    """
    Hash Table completa con separate chaining
    Implementación similar a dict de Python (simplificada)
    """
    
    def __init__(self, initial_capacity=16):
        self.capacity = initial_capacity
        self.size = 0
        self.buckets = [None] * self.capacity
        self.load_factor_threshold = 0.75
    
    def _hash(self, key):
        """
        Función hash simple pero efectiva
        Usa built-in hash() + módulo para distribución uniforme
        """
        return hash(key) % self.capacity
    
    def _resize(self):
        """
        Redimensionar cuando load factor > threshold
        Critical para mantener O(1) performance
        """
        old_buckets = self.buckets
        old_capacity = self.capacity
        
        # Duplicar capacidad
        self.capacity *= 2
        self.size = 0
        self.buckets = [None] * self.capacity
        
        # Re-insertar todos los elementos
        for head in old_buckets:
            current = head
            while current:
                self.put(current.key, current.value)
                current = current.next
    
    def put(self, key, value):
        """
        Insertar/actualizar key-value pair
        Complejidad: O(1) promedio, O(n) peor caso
        """
        # Resize si es necesario
        if self.size >= self.capacity * self.load_factor_threshold:
            self._resize()
        
        index = self._hash(key)
        head = self.buckets[index]
        
        # Si bucket está vacío
        if not head:
            self.buckets[index] = HashNode(key, value)
            self.size += 1
            return
        
        # Buscar si key ya existe
        current = head
        while current:
            if current.key == key:
                # Actualizar valor existente
                current.value = value
                return
            if not current.next:
                break
            current = current.next
        
        # Agregar al final de la cadena
        current.next = HashNode(key, value)
        self.size += 1
    
    def get(self, key):
        """
        Obtener valor por key
        Complejidad: O(1) promedio, O(n) peor caso
        """
        index = self._hash(key)
        current = self.buckets[index]
        
        while current:
            if current.key == key:
                return current.value
            current = current.next
        
        raise KeyError(f"Key '{key}' not found")
    
    def delete(self, key):
        """
        Eliminar key-value pair
        Complejidad: O(1) promedio, O(n) peor caso
        """
        index = self._hash(key)
        head = self.buckets[index]
        
        if not head:
            raise KeyError(f"Key '{key}' not found")
        
        # Si es el primer nodo
        if head.key == key:
            self.buckets[index] = head.next
            self.size -= 1
            return head.value
        
        # Buscar en la cadena
        current = head
        while current.next:
            if current.next.key == key:
                value = current.next.value
                current.next = current.next.next
                self.size -= 1
                return value
            current = current.next
        
        raise KeyError(f"Key '{key}' not found")
    
    def contains(self, key):
        """Verificar si key existe"""
        try:
            self.get(key)
            return True
        except KeyError:
            return False
    
    def keys(self):
        """Obtener todas las keys"""
        result = []
        for head in self.buckets:
            current = head
            while current:
                result.append(current.key)
                current = current.next
        return result
    
    def values(self):
        """Obtener todos los values"""
        result = []
        for head in self.buckets:
            current = head
            while current:
                result.append(current.value)
                current = current.next
        return result
    
    def items(self):
        """Obtener todos los key-value pairs"""
        result = []
        for head in self.buckets:
            current = head
            while current:
                result.append((current.key, current.value))
                current = current.next
        return result
    
    def load_factor(self):
        """Calcular load factor actual"""
        return self.size / self.capacity
    
    def display_structure(self):
        """Mostrar estructura interna (para debug)"""
        print(f"Hash Table (size: {self.size}, capacity: {self.capacity}, load: {self.load_factor():.2f})")
        for i, head in enumerate(self.buckets):
            if head:
                chain = []
                current = head
                while current:
                    chain.append(f"{current.key}:{current.value}")
                    current = current.next
                print(f"  Bucket {i}: {' -> '.join(chain)}")
    
    def __len__(self):
        return self.size
    
    def __str__(self):
        items = self.items()
        return "{" + ", ".join(f"'{k}': {v}" for k, v in items) + "}"

# ========================
# HASH SET IMPLEMENTATION
# ========================

class HashSet:
    """
    Hash Set usando la misma lógica de Hash Table
    Solo almacena keys, no values
    """
    
    def __init__(self, initial_capacity=16):
        self.hash_table = HashTable(initial_capacity)
    
    def add(self, key):
        """Agregar elemento al set"""
        self.hash_table.put(key, True)  # Value dummy
    
    def remove(self, key):
        """Remover elemento del set"""
        self.hash_table.delete(key)
    
    def contains(self, key):
        """Verificar si elemento existe"""
        return self.hash_table.contains(key)
    
    def __len__(self):
        return len(self.hash_table)
    
    def __str__(self):
        keys = self.hash_table.keys()
        return "{" + ", ".join(map(str, keys)) + "}"

# ========================
# HASH FUNCTIONS AVANZADAS
# ========================

def djb2_hash(key):
    """
    DJB2 Hash Function - Muy usada en sistemas reales
    Good distribution, simple to implement
    """
    hash_value = 5381
    for char in str(key):
        hash_value = ((hash_value << 5) + hash_value) + ord(char)
    return hash_value

def fnv_hash(key):
    """
    FNV Hash Function - Otra alternativa popular
    Fast, good distribution
    """
    FNV_OFFSET_BASIS = 2166136261
    FNV_PRIME = 16777619
    
    hash_value = FNV_OFFSET_BASIS
    for char in str(key):
        hash_value ^= ord(char)
        hash_value *= FNV_PRIME
        hash_value &= 0xFFFFFFFF  # Keep 32-bit
    
    return hash_value

class CustomHashTable(HashTable):
    """Hash table con función hash personalizable"""
    
    def __init__(self, hash_function=None, initial_capacity=16):
        super().__init__(initial_capacity)
        self.hash_function = hash_function or djb2_hash
    
    def _hash(self, key):
        return self.hash_function(key) % self.capacity

# ========================
# TESTING COMPREHENSIVO
# ========================

def test_hash_table():
    """Test completo de Hash Table"""
    print("=== TESTING HASH TABLE ===\n")
    
    ht = HashTable()
    
    # Test inserción
    print("1. INSERTIONS:")
    test_data = [
        ("name", "Alice"),
        ("age", 30),
        ("city", "New York"),
        ("country", "USA"),
        ("job", "Engineer")
    ]
    
    for key, value in test_data:
        ht.put(key, value)
        print(f"   Added {key}: {value}")
    
    print(f"   Final table: {ht}")
    ht.display_structure()
    
    # Test búsqueda
    print("\n2. SEARCHES:")
    for key in ["name", "age", "nonexistent"]:
        try:
            value = ht.get(key)
            print(f"   {key}: {value}")
        except KeyError as e:
            print(f"   {key}: {e}")
    
    # Test actualización
    print("\n3. UPDATES:")
    ht.put("age", 31)
    print(f"   Updated age: {ht.get('age')}")
    
    # Test eliminación
    print("\n4. DELETIONS:")
    deleted = ht.delete("city")
    print(f"   Deleted 'city': {deleted}")
    print(f"   Table after deletion: {ht}")
    
    # Test resize
    print("\n5. RESIZE TEST:")
    print(f"   Load factor before: {ht.load_factor():.2f}")
    
    # Agregar muchos elementos para forzar resize
    for i in range(20):
        ht.put(f"key_{i}", f"value_{i}")
    
    print(f"   Load factor after: {ht.load_factor():.2f}")
    print(f"   New capacity: {ht.capacity}")

def test_hash_set():
    """Test de Hash Set"""
    print("\n=== TESTING HASH SET ===\n")
    
    hs = HashSet()
    
    # Agregar elementos
    elements = [1, 2, 3, 4, 5, 3, 2, 1]  # Con duplicados
    print("Adding elements:", elements)
    
    for elem in elements:
        hs.add(elem)
    
    print(f"Set after additions: {hs}")
    print(f"Size: {len(hs)}")
    
    # Test contains
    for elem in [1, 6, 3, 10]:
        contains = hs.contains(elem)
        print(f"Contains {elem}: {contains}")

def compare_hash_functions():
    """Comparar diferentes funciones hash"""
    print("\n=== HASH FUNCTION COMPARISON ===\n")
    
    test_keys = ["python", "java", "javascript", "go", "rust", "scala"]
    
    print("Key distributions:")
    print("Key        | Built-in | DJB2     | FNV")
    print("-" * 45)
    
    for key in test_keys:
        builtin = hash(key) % 16
        djb2 = djb2_hash(key) % 16
        fnv = fnv_hash(key) % 16
        print(f"{key:10} | {builtin:8} | {djb2:8} | {fnv:8}")

if __name__ == "__main__":
    test_hash_table()
    test_hash_set()
    compare_hash_functions()
