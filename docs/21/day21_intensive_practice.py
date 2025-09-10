"""
DÍA 21 - PRÁCTICA INTENSIVA COMBINADA
Problemas Medium que combinan múltiples estructuras de datos
Objetivo: Dominar la selección y combinación de estructuras
"""

import heapq
from typing import List, Optional, Dict, Set
from collections import defaultdict, deque, Counter
import bisect


# PROBLEMA 1: LRU CACHE (Hash Map + Doubly Linked List)
class LRUCache:
    """
    PROBLEMA: Implementa una LRU (Least Recently Used) Cache
    
    COMBINACIÓN: Hash Map + Doubly Linked List
    - Hash Map: O(1) access
    - Doubly Linked List: O(1) insertion/deletion
    
    COMPLEJIDAD: get() O(1), put() O(1)
    
    PATRÓN CLAVE: Cuando necesitas O(1) access + O(1) ordering updates
    """
    
    class Node:
        def __init__(self, key=0, val=0):
            self.key = key
            self.val = val
            self.prev = None
            self.next = None
    
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key -> node
        
        # Dummy head y tail para simplificar operaciones
        self.head = self.Node()
        self.tail = self.Node()
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _add_to_head(self, node):
        """Agregar nodo inmediatamente después del head"""
        node.prev = self.head
        node.next = self.head.next
        
        self.head.next.prev = node
        self.head.next = node
    
    def _remove_node(self, node):
        """Remover nodo de la lista"""
        node.prev.next = node.next
        node.next.prev = node.prev
    
    def _move_to_head(self, node):
        """Mover nodo existente al head (más reciente)"""
        self._remove_node(node)
        self._add_to_head(node)
    
    def _remove_tail(self):
        """Remover último nodo (menos reciente)"""
        last_node = self.tail.prev
        self._remove_node(last_node)
        return last_node
    
    def get(self, key: int) -> int:
        """Obtener valor y marcar como reciente"""
        if key in self.cache:
            node = self.cache[key]
            # Mover a head (más reciente)
            self._move_to_head(node)
            return node.val
        return -1
    
    def put(self, key: int, value: int) -> None:
        """Insertar/actualizar valor"""
        if key in self.cache:
            # Actualizar valor existente
            node = self.cache[key]
            node.val = value
            self._move_to_head(node)
        else:
            # Nuevo valor
            new_node = self.Node(key, value)
            
            if len(self.cache) >= self.capacity:
                # Remover LRU
                tail = self._remove_tail()
                del self.cache[tail.key]
            
            # Agregar nuevo nodo
            self.cache[key] = new_node
            self._add_to_head(new_node)


# PROBLEMA 2: Word Ladder II (BFS + DFS + Backtracking)
def find_ladders(begin_word: str, end_word: str, word_list: List[str]) -> List[List[str]]:
    """
    PROBLEMA: Encuentra TODAS las secuencias de transformación más cortas
    
    COMBINACIÓN: BFS + Hash Map + DFS + Backtracking
    - BFS: Encontrar distancia mínima
    - Hash Map: Tracking de predecessors
    - DFS: Construir todas las paths
    
    EJEMPLO: begin="hit", end="cog", wordList=["hot","dot","dog","lot","log","cog"]
    Output: [["hit","hot","dot","dog","cog"],["hit","hot","lot","log","cog"]]
    
    PATRÓN CLAVE: BFS para shortest path + DFS para enumerar todas las soluciones
    """
    if end_word not in word_list:
        return []
    
    word_set = set(word_list)
    word_set.add(begin_word)
    
    # BFS para encontrar distancias mínimas
    queue = deque([begin_word])
    visited = {begin_word: 0}
    predecessors = defaultdict(list)
    found = False
    level = 0
    
    while queue and not found:
        level += 1
        for _ in range(len(queue)):
            current_word = queue.popleft()
            
            # Generar todas las transformaciones posibles
            for i in range(len(current_word)):
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    if c == current_word[i]:
                        continue
                    
                    next_word = current_word[:i] + c + current_word[i+1:]
                    
                    if next_word not in word_set:
                        continue
                    
                    if next_word == end_word:
                        found = True
                        predecessors[next_word].append(current_word)
                    elif next_word not in visited:
                        visited[next_word] = level
                        predecessors[next_word].append(current_word)
                        queue.append(next_word)
                    elif visited[next_word] == level:
                        predecessors[next_word].append(current_word)
    
    # DFS para construir todas las paths
    result = []
    
    def dfs(word, path):
        if word == begin_word:
            result.append([begin_word] + path[::-1])
            return
        
        for predecessor in predecessors[word]:
            dfs(predecessor, path + [word])
    
    if found:
        dfs(end_word, [])
    
    return result


# PROBLEMA 3: Design Twitter (Hash Map + Heap + OOP)
class Twitter:
    """
    PROBLEMA: Sistema simplificado de Twitter con timeline
    
    COMBINACIÓN: Hash Map + Min-Heap + Timestamp + Set
    - Hash Map: user tweets y follows
    - Heap: merge timelines eficientemente 
    - Set: manage follows/unfollows
    - Timestamp: ordenar tweets
    
    PATRÓN CLAVE: Merge multiple sorted streams usando heap
    """
    
    def __init__(self):
        self.time = 0
        self.tweets = defaultdict(list)  # userId -> [(time, tweetId), ...]
        self.follows = defaultdict(set)  # userId -> {followeeId, ...}
    
    def postTweet(self, userId: int, tweetId: int) -> None:
        """Publicar tweet con timestamp"""
        self.tweets[userId].append((self.time, tweetId))
        self.time += 1
    
    def getNewsFeed(self, userId: int) -> List[int]:
        """Obtener 10 tweets más recientes del news feed"""
        # Heap para merge: (-time, tweetId, userId, index)
        heap = []
        
        # Agregar tweets propios
        if userId in self.tweets and self.tweets[userId]:
            tweets = self.tweets[userId]
            time, tweet_id = tweets[-1]  # Más reciente
            heapq.heappush(heap, (-time, tweet_id, userId, len(tweets) - 1))
        
        # Agregar tweets de followees
        for followee_id in self.follows[userId]:
            if followee_id in self.tweets and self.tweets[followee_id]:
                tweets = self.tweets[followee_id]
                time, tweet_id = tweets[-1]  # Más reciente
                heapq.heappush(heap, (-time, tweet_id, followee_id, len(tweets) - 1))
        
        # Extraer top 10 tweets
        result = []
        for _ in range(10):
            if not heap:
                break
            
            neg_time, tweet_id, user_id, idx = heapq.heappop(heap)
            result.append(tweet_id)
            
            # Agregar siguiente tweet del mismo usuario si existe
            if idx > 0:
                tweets = self.tweets[user_id]
                time, next_tweet_id = tweets[idx - 1]
                heapq.heappush(heap, (-time, next_tweet_id, user_id, idx - 1))
        
        return result
    
    def follow(self, followerId: int, followeeId: int) -> None:
        """Seguir usuario"""
        if followerId != followeeId:
            self.follows[followerId].add(followeeId)
    
    def unfollow(self, followerId: int, followeeId: int) -> None:
        """Dejar de seguir usuario"""
        self.follows[followerId].discard(followeeId)


# PROBLEMA 4: Alien Dictionary (Graph + Topological Sort + DFS)
def alien_order(words: List[str]) -> str:
    """
    PROBLEMA: Determinar orden del alfabeto alien basado en palabras ordenadas
    
    COMBINACIÓN: Graph + Topological Sort + Hash Map + Set
    - Graph: representar orden de caracteres
    - Topological Sort: encontrar orden válido
    - Hash Map: adjacency list + in-degree
    
    EJEMPLO: words = ["wrt","wrf","er","ett","rftt"]
    Output: "wertf"
    
    PATRÓN CLAVE: Constraint-based ordering = Topological Sort
    """
    # Construir grafo
    graph = defaultdict(set)
    in_degree = {}
    
    # Inicializar todos los caracteres con in-degree 0
    for word in words:
        for char in word:
            in_degree[char] = 0
    
    # Construir edges del grafo comparando palabras adyacentes
    for i in range(len(words) - 1):
        word1, word2 = words[i], words[i + 1]
        min_len = min(len(word1), len(word2))
        
        # Caso especial: palabra más larga viene antes de prefijo
        if len(word1) > len(word2) and word1[:min_len] == word2[:min_len]:
            return ""  # Orden inválido
        
        # Encontrar primer carácter diferente
        for j in range(min_len):
            if word1[j] != word2[j]:
                char1, char2 = word1[j], word2[j]
                
                # Agregar edge si no existe
                if char2 not in graph[char1]:
                    graph[char1].add(char2)
                    in_degree[char2] += 1
                break
    
    # Topological Sort usando Kahn's algorithm
    queue = deque([char for char in in_degree if in_degree[char] == 0])
    result = []
    
    while queue:
        char = queue.popleft()
        result.append(char)
        
        # Procesar vecinos
        for neighbor in graph[char]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Verificar si hay ciclo
    if len(result) == len(in_degree):
        return ''.join(result)
    else:
        return ""  # Ciclo detectado


# TESTING FRAMEWORK
def test_intensive_problems():
    """Prueba todos los problemas implementados"""
    
    print("=== TESTING PROBLEMA 1: LRU CACHE ===")
    lru = LRUCache(2)
    lru.put(1, 1)
    lru.put(2, 2)
    print(f"get(1): {lru.get(1)}")  # Expected: 1
    lru.put(3, 3)  # Evicts key 2
    print(f"get(2): {lru.get(2)}")  # Expected: -1
    lru.put(4, 4)  # Evicts key 1
    print(f"get(1): {lru.get(1)}")  # Expected: -1
    print(f"get(3): {lru.get(3)}")  # Expected: 3
    print(f"get(4): {lru.get(4)}")  # Expected: 4
    
    print("\n=== TESTING PROBLEMA 2: WORD LADDER II ===")
    begin_word = "hit"
    end_word = "cog"
    word_list = ["hot", "dot", "dog", "lot", "log", "cog"]
    paths = find_ladders(begin_word, end_word, word_list)
    print(f"Begin: {begin_word}, End: {end_word}")
    print(f"Word list: {word_list}")
    print(f"All shortest paths: {paths}")
    
    print("\n=== TESTING PROBLEMA 3: TWITTER ===")
    twitter = Twitter()
    twitter.postTweet(1, 5)
    print(f"User 1 news feed: {twitter.getNewsFeed(1)}")  # [5]
    twitter.follow(1, 2)
    twitter.postTweet(2, 6)
    print(f"User 1 news feed: {twitter.getNewsFeed(1)}")  # [6, 5]
    twitter.unfollow(1, 2)
    print(f"User 1 news feed: {twitter.getNewsFeed(1)}")  # [5]
    
    print("\n=== TESTING PROBLEMA 4: ALIEN DICTIONARY ===")
    words1 = ["wrt", "wrf", "er", "ett", "rftt"]
    result1 = alien_order(words1)
    print(f"Words: {words1}")
    print(f"Alien order: '{result1}'")
    
    words2 = ["z", "x"]
    result2 = alien_order(words2)
    print(f"Words: {words2}")
    print(f"Alien order: '{result2}'")


if __name__ == "__main__":
    test_intensive_problems()


# ANÁLISIS DE PATRONES IDENTIFICADOS
def pattern_analysis():
    """
    PATRONES CLAVE IDENTIFICADOS EN PROBLEMAS COMPLEJOS:
    
    1. HASH MAP + LINKED LIST (LRU Cache):
       - Cuando necesitas O(1) access + O(1) ordering
       - Dummy nodes simplifican edge cases
       - Patrón común en caches y LFU/LRU
    
    2. BFS + DFS COMBINADOS (Word Ladder II):
       - BFS: encontrar shortest distance
       - DFS: enumerar todas las soluciones
       - Predecessors map: reconstruir paths
    
    3. MULTIPLE DATA STRUCTURES (Twitter):
       - Hash Map: datos principales
       - Heap: merge sorted streams
       - Set: relaciones many-to-many
       - Timestamp: ordenar eventos
    
    4. GRAPH + TOPOLOGICAL SORT (Alien Dictionary):
       - Constraints → Graph edges
       - Kahn's algorithm: in-degree tracking
       - Cycle detection: len(result) != len(nodes)
    
    TIPS PARA ENTREVISTAS:
    - Identifica qué operaciones necesitas ser O(1)
    - Combina estructuras para optimizar diferentes aspectos
    - Piensa en invariantes que debes mantener
    - Considera edge cases desde el diseño
    """
    pass
