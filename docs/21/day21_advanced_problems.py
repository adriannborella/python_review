"""
DÍA 21 - SEGUNDA HORA: PROBLEMAS AVANZADOS
Problemas que combinan múltiples algoritmos y estructuras
Preparación para entrevistas de nivel senior
"""

import heapq
from typing import List, Tuple, Dict, Set, Optional
from collections import defaultdict, deque, Counter
import bisect


# PROBLEMA 5: Serialize and Deserialize Binary Tree (Tree + String + Stack)
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Codec:
    """
    PROBLEMA: Serializar y deserializar árbol binario
    
    COMBINACIÓN: Tree Traversal + String Processing + Stack/Queue
    - Preorder traversal: para serialización
    - Queue: para deserialización level-by-level
    - String processing: encoding/decoding
    
    PATRÓN CLAVE: Encoding structured data + reconstruction
    """
    
    def serialize(self, root: TreeNode) -> str:
        """Codifica árbol a string usando preorder"""
        def preorder(node):
            if not node:
                vals.append("#")
            else:
                vals.append(str(node.val))
                preorder(node.left)
                preorder(node.right)
        
        vals = []
        preorder(root)
        return ','.join(vals)
    
    def deserialize(self, data: str) -> TreeNode:
        """Decodifica string a árbol"""
        def build():
            val = next(vals)
            if val == '#':
                return None
            
            node = TreeNode(int(val))
            node.left = build()
            node.right = build()
            return node
        
        vals = iter(data.split(','))
        return build()


# PROBLEMA 6: Sliding Window Maximum (Deque + Sliding Window)
def max_sliding_window_optimal(nums: List[int], k: int) -> List[int]:
    """
    PROBLEMA: Máximo en cada ventana deslizante (versión más eficiente)
    
    COMBINACIÓN: Deque + Sliding Window + Monotonic Queue
    - Deque: mantener candidatos en orden decreciente
    - Sliding Window: mover ventana eficientemente
    - Monotonic property: elementos útiles solamente
    
    COMPLEJIDAD: O(n) vs O(n log k) con heap
    
    PATRÓN CLAVE: Monotonic deque para min/max en sliding window
    """
    if not nums or k == 0:
        return []
    
    dq = deque()  # Stores indices
    result = []
    
    for i, num in enumerate(nums):
        # Remove indices that are out of current window
        while dq and dq[0] <= i - k:
            dq.popleft()
        
        # Remove indices whose corresponding values are smaller than current
        # (they will never be the maximum)
        while dq and nums[dq[-1]] <= num:
            dq.pop()
        
        dq.append(i)
        
        # Add maximum of current window to result
        if i >= k - 1:
            result.append(nums[dq[0]])
    
    return result


# PROBLEMA 7: Design Search Autocomplete System (Trie + Heap + String Processing)
class AutocompleteSystem:
    """
    PROBLEMA: Sistema de autocompletado como Google Search
    
    COMBINACIÓN: Trie + Heap + Hash Map + String Processing
    - Trie: prefix matching eficiente
    - Heap: top-k frequent sentences
    - Hash Map: tracking frequencies
    - String processing: input handling
    
    PATRÓN CLAVE: Prefix matching + ranking + real-time updates
    """
    
    class TrieNode:
        def __init__(self):
            self.children = {}
            self.is_sentence = False
            self.hot_degree = 0
    
    def __init__(self, sentences: List[str], times: List[int]):
        self.root = self.TrieNode()
        self.hot_sentences = {}  # sentence -> frequency
        self.current_sentence = ""
        self.current_node = self.root
        
        # Build trie with initial data
        for sentence, time in zip(sentences, times):
            self._add_sentence(sentence, time)
    
    def _add_sentence(self, sentence: str, hot_degree: int):
        """Agregar sentence al trie con frecuencia"""
        self.hot_sentences[sentence] = self.hot_sentences.get(sentence, 0) + hot_degree
        
        node = self.root
        for char in sentence:
            if char not in node.children:
                node.children[char] = self.TrieNode()
            node = node.children[char]
        
        node.is_sentence = True
        node.hot_degree = self.hot_sentences[sentence]
    
    def _search_sentences(self, node: 'TrieNode', prefix: str) -> List[Tuple[int, str]]:
        """DFS para encontrar todas las sentences con el prefix dado"""
        results = []
        
        if node.is_sentence:
            results.append((node.hot_degree, prefix))
        
        for char, child_node in node.children.items():
            results.extend(self._search_sentences(child_node, prefix + char))
        
        return results
    
    def input(self, c: str) -> List[str]:
        """Procesar carácter de input y retornar top 3 sugerencias"""
        if c == '#':
            # Terminar sentence actual
            self._add_sentence(self.current_sentence, 1)
            self.current_sentence = ""
            self.current_node = self.root
            return []
        
        self.current_sentence += c
        
        # Navegar en el trie
        if self.current_node and c in self.current_node.children:
            self.current_node = self.current_node.children[c]
        else:
            self.current_node = None
            return []
        
        # Encontrar todas las sentences con el prefix actual
        candidates = self._search_sentences(self.current_node, self.current_sentence)
        
        # Ordenar por frecuencia (desc) y luego alfabéticamente (asc)
        candidates.sort(key=lambda x: (-x[0], x[1]))
        
        # Retornar top 3
        return [sentence for _, sentence in candidates[:3]]


# PROBLEMA 8: Word Search II (Trie + DFS + Backtracking + 2D Array)
def find_words(board: List[List[str]], words: List[str]) -> List[str]:
    """
    PROBLEMA: Encontrar todas las palabras en un board 2D
    
    COMBINACIÓN: Trie + DFS + Backtracking + 2D Array Traversal
    - Trie: efficient prefix matching
    - DFS: explorar todas las direcciones
    - Backtracking: undo moves
    - 2D traversal: directions array
    
    OPTIMIZACIÓN: Pruning con trie vs buscar palabra por palabra
    
    PATRÓN CLAVE: Trie + DFS para multiple pattern matching
    """
    
    class TrieNode:
        def __init__(self):
            self.children = {}
            self.word = None  # Store complete word at end node
    
    # Build trie
    root = TrieNode()
    for word in words:
        node = root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.word = word
    
    def dfs(i: int, j: int, node: TrieNode):
        """DFS con backtracking desde posición (i,j)"""
        char = board[i][j]
        current_node = node.children.get(char)
        
        if not current_node:
            return
        
        # Si encontramos palabra completa
        if current_node.word:
            result.append(current_node.word)
            current_node.word = None  # Avoid duplicates
        
        # Marcar como visitado
        board[i][j] = '#'
        
        # Explorar 4 direcciones
        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            ni, nj = i + di, j + dj
            if (0 <= ni < len(board) and 0 <= nj < len(board[0]) and 
                board[ni][nj] != '#'):
                dfs(ni, nj, current_node)
        
        # Backtrack
        board[i][j] = char
        
        # Optimization: remove empty nodes
        if not current_node.children:
            del node.children[char]
    
    result = []
    
    # Try DFS from each cell
    for i in range(len(board)):
        for j in range(len(board[0])):
            dfs(i, j, root)
    
    return result


# PROBLEMA BONUS: Design Data Structure for Range Sum Queries (Segment Tree)
class NumArray:
    """
    PROBLEMA: Range Sum Query - Mutable
    
    ESTRUCTURA: Segment Tree
    - Build: O(n)
    - Update: O(log n)
    - Query: O(log n)
    
    PATRÓN CLAVE: Binary tree para range operations
    """
    
    def __init__(self, nums: List[int]):
        self.n = len(nums)
        # Segment tree array: tree[i] stores sum of range
        self.tree = [0] * (2 * self.n)
        
        # Build tree: fill leaves first, then internal nodes
        for i in range(self.n):
            self.tree[self.n + i] = nums[i]
        
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]
    
    def update(self, index: int, val: int) -> None:
        """Update value at index"""
        # Update leaf
        pos = index + self.n
        self.tree[pos] = val
        
        # Update internal nodes
        while pos > 1:
            self.tree[pos // 2] = self.tree[pos] + self.tree[pos ^ 1]
            pos //= 2
    
    def sumRange(self, left: int, right: int) -> int:
        """Sum of range [left, right]"""
        # Convert to tree indices
        left += self.n
        right += self.n
        
        total = 0
        while left <= right:
            # If left is odd (right child), add it and move to next
            if left % 2 == 1:
                total += self.tree[left]
                left += 1
            
            # If right is even (left child), add it and move to prev
            if right % 2 == 0:
                total += self.tree[right]
                right -= 1
            
            # Move to next level
            left //= 2
            right //= 2
        
        return total


# TESTING SEGUNDA HORA
def test_advanced_problems():
    """Testing de problemas avanzados"""
    
    print("=== TESTING PROBLEMA 5: SERIALIZE BINARY TREE ===")
    # Crear árbol: [1,2,3,null,null,4,5]
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.right.left = TreeNode(4)
    root.right.right = TreeNode(5)
    
    codec = Codec()
    serialized = codec.serialize(root)
    print(f"Serialized: {serialized}")
    
    deserialized = codec.deserialize(serialized)
    print(f"Deserialized successfully: {deserialized.val}")
    
    print("\n=== TESTING PROBLEMA 6: SLIDING WINDOW MAXIMUM ===")
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    result = max_sliding_window_optimal(nums, k)
    print(f"nums: {nums}, k: {k}")
    print(f"Sliding window maximums: {result}")
    
    print("\n=== TESTING PROBLEMA 7: AUTOCOMPLETE SYSTEM ===")
    sentences = ["i love you", "island", "iroman", "i love leetcode"]
    times = [5, 3, 2, 2]
    ac = AutocompleteSystem(sentences, times)
    
    print("Input 'i':")
    print(ac.input('i'))
    print("Input ' ':")
    print(ac.input(' '))
    print("Input 'a':")
    print(ac.input('a'))
    print("Input '#':")
    print(ac.input('#'))
    
    print("\n=== TESTING PROBLEMA 8: WORD SEARCH II ===")
    board = [
        ["o", "a", "a", "n"],
        ["e", "t", "a", "e"],
        ["i", "h", "k", "r"],
        ["i", "f", "l", "v"]
    ]
    words = ["oath", "pea", "eat", "rain"]
    found_words = find_words(board, words)
    print(f"Board: {board}")
    print(f"Words to find: {words}")
    print(f"Found words: {found_words}")
    
    print("\n=== TESTING BONUS: SEGMENT TREE ===")
    nums = [1, 3, 5, 7, 9, 11]
    num_array = NumArray(nums)
    print(f"Original array: {nums}")
    print(f"Sum of range [1, 3]: {num_array.sumRange(1, 3)}")
    num_array.update(1, 10)
    print(f"After update(1, 10):")
    print(f"Sum of range [1, 3]: {num_array.sumRange(1, 3)}")


if __name__ == "__main__":
    test_advanced_problems()


# ANÁLISIS FINAL: PATRONES MAESTROS PARA ENTREVISTAS
def master_patterns_analysis():
    """
    PATRONES MAESTROS IDENTIFICADOS - DÍA 21
    
    🎯 PATRÓN 1: MÚLTIPLES ESTRUCTURAS COMPLEMENTARIAS
    Ejemplo: LRU Cache (HashMap + Doubly Linked List)
    Cuándo usar: Necesitas diferentes complejidades para diferentes operaciones
    
    🎯 PATRÓN 2: BFS + DFS HÍBRIDO
    Ejemplo: Word Ladder II (BFS para distancia + DFS para paths)
    Cuándo usar: Shortest path + enumerar todas las soluciones
    
    🎯 PATRÓN 3: TRIE + DFS/BFS
    Ejemplo: Word Search II, Autocomplete
    Cuándo usar: Multiple pattern matching, prefix operations
    
    🎯 PATRÓN 4: MONOTONIC DEQUE
    Ejemplo: Sliding Window Maximum
    Cuándo usar: Min/Max en sliding window con O(n)
    
    🎯 PATRÓN 5: GRAPH + TOPOLOGICAL SORT
    Ejemplo: Alien Dictionary
    Cuándo usar: Ordering con constraints, dependency resolution
    
    🎯 PATRÓN 6: SEGMENT TREE / BIT
    Ejemplo: Range Sum Query
    Cuándo usar: Range operations con updates
    
    🎯 PATRÓN 7: HEAP + TIMESTAMP/PRIORITY
    Ejemplo: Twitter Timeline
    Cuándo usar: Merge multiple sorted streams
    
    💡 DECISIÓN FRAMEWORK PARA ENTREVISTAS:
    
    1. ¿Qué operaciones necesito que sean O(1)?
       → Hash Map + Linked List/Array
    
    2. ¿Necesito shortest path + todas las soluciones?
       → BFS + DFS combo
    
    3. ¿Multiple pattern matching?
       → Trie + DFS
    
    4. ¿Min/Max en sliding window?
       → Monotonic Deque
    
    5. ¿Ordering con dependencies?
       → Graph + Topological Sort
    
    6. ¿Range queries con updates?
       → Segment Tree
    
    7. ¿Merge sorted streams?
       → Heap con indices
    """
    pass


# SIMULACRO DE ENTREVISTA - PROBLEMA INTEGRADOR
def interview_simulation():
    """
    SIMULACRO: Diseña un sistema de recomendación de música
    
    REQUERIMIENTOS:
    1. Agregar canciones con metadata (artista, género, rating)
    2. Buscar canciones por prefix del título
    3. Recomendar top-K canciones similares a una dada
    4. Mantener historial de reproducciones del usuario
    5. Generar playlist personalizada
    
    ESTRUCTURAS NECESARIAS:
    - Trie: búsqueda por prefix
    - Hash Map: metadata storage
    - Heap: top-K recommendations
    - Graph: similaridad entre canciones
    - LRU: cache de recomendaciones
    
    TIEMPO: 45 minutos para diseño + implementación básica
    
    ¿Cómo empezarías? ¿Qué preguntas harías?
    """
    
    class Song:
        def __init__(self, id: int, title: str, artist: str, genre: str, rating: float):
            self.id = id
            self.title = title
            self.artist = artist
            self.genre = genre
            self.rating = rating
    
    class MusicRecommendationSystem:
        """
        ESQUELETO PARA IMPLEMENTAR EN ENTREVISTA
        Combina múltiples patrones aprendidos
        """
        
        def __init__(self):
            # TODO: Inicializar estructuras de datos
            # Trie para búsqueda, HashMap para songs, etc.
            pass
        
        def add_song(self, song: Song):
            """Agregar nueva canción al sistema"""
            # TODO: Agregar a trie, hash map, etc.
            pass
        
        def search_by_prefix(self, prefix: str) -> List[Song]:
            """Buscar canciones por prefix del título"""
            # TODO: Usar trie para búsqueda eficiente
            pass
        
        def get_recommendations(self, song_id: int, k: int) -> List[Song]:
            """Top-K canciones similares"""
            # TODO: Usar heap para top-K, similaridad por género/artista
            pass
        
        def play_song(self, user_id: int, song_id: int):
            """Registrar reproducción de usuario"""
            # TODO: Actualizar historial, afectar recomendaciones
            pass
        
        def generate_playlist(self, user_id: int, size: int) -> List[Song]:
            """Generar playlist personalizada"""
            # TODO: Combinar historial + ratings + diversidad
            pass
    
    return MusicRecommendationSystem


# CHECKLIST FINAL DÍA 21
def day21_checklist():
    """
    ✅ CHECKLIST DÍA 21 - ¿QUÉ HAS DOMINADO?
    
    ESTRUCTURAS INDIVIDUALES:
    □ Arrays y operaciones avanzadas
    □ Hash Maps y collision handling
    □ Linked Lists (single, double, circular)
    □ Stacks y Queues (incluyendo deque)
    □ Trees (binary, BST, traversals)
    □ Heaps (min, max, priority queue)
    □ Graphs (representation, traversal)
    
    ALGORITMOS FUNDAMENTALES:
    □ Sorting algorithms y análisis
    □ Binary search y variaciones
    □ DFS y BFS (iterativo y recursivo)
    □ Backtracking patterns
    □ Greedy algorithms
    □ Topological sort
    
    PATRONES COMBINADOS:
    □ Two pointers + sliding window
    □ Hash map + two pointers
    □ Heap + hash map (frequency problems)
    □ BFS + DFS hybrid
    □ Trie + DFS (multiple patterns)
    □ Graph + topological sort
    □ Multiple data structures (LRU cache)
    
    ANÁLISIS DE COMPLEJIDAD:
    □ Big O notation mastery
    □ Space-time tradeoffs
    □ Optimization strategies
    □ When to use which structure
    
    IMPLEMENTACIÓN:
    □ Clean, bug-free code
    □ Edge cases handling
    □ Code organization
    □ Testing mindset
    
    COMUNICACIÓN:
    □ Explain approach clearly
    □ Discuss alternatives
    □ Mention tradeoffs
    □ Ask clarifying questions
    
    SCORE: ___/24 (Objetivo: 20+ para estar listo para entrevistas)
    """
    pass