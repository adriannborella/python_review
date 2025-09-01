"""
PROBLEMAS DE ENTREVISTA - HASH TABLES + GRAFOS
==============================================

Estos problemas combinan ambas estructuras y son MUY COMUNES:
- Two Sum y variaciones (95% probabilidad)
- Clone Graph (80% probabilidad)
- Course Schedule (75% probabilidad)
- Word Ladder (60% probabilidad)
- Group Anagrams (70% probabilidad)

¡Dominar estos patrones te dará una ventaja enorme!
"""

from collections import defaultdict, deque
import heapq

# ========================
# PROBLEMA 1: Two Sum y Variaciones
# ========================
# Leetcode 1 - ¡EL MÁS FAMOSO!

def two_sum(nums, target):
    """
    Clásico Two Sum - HashMap approach
    Complejidad: O(n) tiempo, O(n) espacio
    """
    seen = {}  # value -> index
    
    for i, num in enumerate(nums):
        complement = target - num
        
        if complement in seen:
            return [seen[complement], i]
        
        seen[num] = i
    
    return []  # No solution found

def two_sum_all_pairs(nums, target):
    """
    Encontrar TODOS los pares que suman target
    """
    seen = defaultdict(list)
    result = []
    
    for i, num in enumerate(nums):
        complement = target - num
        
        # Agregar todos los pares con el complement
        for j in seen[complement]:
            result.append([j, i])
        
        seen[num].append(i)
    
    return result

def three_sum(nums):
    """
    Three Sum - Leetcode 15
    Encontrar todos los triplets únicos que suman 0
    Complejidad: O(n²) tiempo, O(1) espacio extra
    """
    nums.sort()
    result = []
    n = len(nums)
    
    for i in range(n - 2):
        # Skip duplicates para el primer elemento
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        left, right = i + 1, n - 1
        
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            
            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                
                # Skip duplicates
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1
    
    return result

def four_sum(nums, target):
    """
    Four Sum - Leetcode 18
    Extensión del pattern de Three Sum
    """
    nums.sort()
    result = []
    n = len(nums)
    
    for i in range(n - 3):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        for j in range(i + 1, n - 2):
            if j > i + 1 and nums[j] == nums[j - 1]:
                continue
            
            left, right = j + 1, n - 1
            
            while left < right:
                total = nums[i] + nums[j] + nums[left] + nums[right]
                
                if total == target:
                    result.append([nums[i], nums[j], nums[left], nums[right]])
                    
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    
                    left += 1
                    right -= 1
                elif total < target:
                    left += 1
                else:
                    right -= 1
    
    return result

# ========================
# PROBLEMA 2: Group Anagrams
# ========================
# Leetcode 49 - Uso inteligente de hash tables

def group_anagrams_v1(strs):
    """
    Group Anagrams - Approach 1: Sort as key
    Complejidad: O(n * m log m) donde n=strings, m=avg length
    """
    groups = defaultdict(list)
    
    for s in strs:
        # Usar sorted string como key
        sorted_str = ''.join(sorted(s))
        groups[sorted_str].append(s)
    
    return list(groups.values())

def group_anagrams_v2(strs):
    """
    Group Anagrams - Approach 2: Character count as key
    Complejidad: O(n * m) - más eficiente!
    """
    groups = defaultdict(list)
    
    for s in strs:
        # Crear key basado en conteo de caracteres
        char_count = [0] * 26
        for char in s:
            char_count[ord(char) - ord('a')] += 1
        
        # Convertir a tuple para usar como key
        key = tuple(char_count)
        groups[key].append(s)
    
    return list(groups.values())

# ========================
# PROBLEMA 3: Clone Graph
# ========================
# Leetcode 133 - Combinación de hash + graph traversal

class GraphNode:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
    
    def __repr__(self):
        return f"Node({self.val})"

def clone_graph_dfs(node):
    """
    Clone graph usando DFS + HashMap
    Complejidad: O(V + E) tiempo, O(V) espacio
    """
    if not node:
        return None
    
    # HashMap: original_node -> cloned_node
    cloned = {}
    
    def dfs(original):
        if original in cloned:
            return cloned[original]
        
        # Crear clon del nodo actual
        clone = GraphNode(original.val)
        cloned[original] = clone
        
        # Clonar todos los vecinos recursivamente
        for neighbor in original.neighbors:
            clone.neighbors.append(dfs(neighbor))
        
        return clone
    
    return dfs(node)

def clone_graph_bfs(node):
    """
    Clone graph usando BFS + HashMap
    Complejidad: O(V + E) tiempo, O(V) espacio
    """
    if not node:
        return None
    
    cloned = {node: GraphNode(node.val)}
    queue = deque([node])
    
    while queue:
        original = queue.popleft()
        
        for neighbor in original.neighbors:
            if neighbor not in cloned:
                # Crear clon del vecino
                cloned[neighbor] = GraphNode(neighbor.val)
                queue.append(neighbor)
            
            # Conectar clon actual con clon del vecino
            cloned[original].neighbors.append(cloned[neighbor])
    
    return cloned[node]

# ========================
# PROBLEMA 4: Course Schedule
# ========================
# Leetcode 207 & 210 - Topological sort + cycle detection

def can_finish_courses(num_courses, prerequisites):
    """
    Course Schedule I - ¿Es posible completar todos los cursos?
    Esencialmente: ¿el grafo tiene ciclos?
    Complejidad: O(V + E)
    """
    # Construir grafo de dependencias
    graph = defaultdict(list)
    in_degree = [0] * num_courses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1
    
    # Kahn's algorithm para detección de ciclos
    queue = deque()
    for i in range(num_courses):
        if in_degree[i] == 0:
            queue.append(i)
    
    completed = 0
    
    while queue:
        course = queue.popleft()
        completed += 1
        
        # Decrementar in-degree de cursos dependientes
        for dependent in graph[course]:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
    
    return completed == num_courses

def find_course_order(num_courses, prerequisites):
    """
    Course Schedule II - Encontrar orden válido de cursos
    Complejidad: O(V + E)
    """
    graph = defaultdict(list)
    in_degree = [0] * num_courses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1
    
    queue = deque()
    for i in range(num_courses):
        if in_degree[i] == 0:
            queue.append(i)
    
    order = []
    
    while queue:
        course = queue.popleft()
        order.append(course)
        
        for dependent in graph[course]:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
    
    # Si no pudimos ordenar todos, hay ciclo
    return order if len(order) == num_courses else []

# ========================
# PROBLEMA 5: Word Ladder
# ========================
# Leetcode 127 - BFS en grafo implícito

def word_ladder_length(begin_word, end_word, word_list):
    """
    Word Ladder - Shortest transformation sequence
    Cada step cambia exactamente una letra
    Complejidad: O(M² × N) donde M=length, N=word count
    """
    if end_word not in word_list:
        return 0
    
    word_set = set(word_list)
    queue = deque([(begin_word, 1)])  # (word, length)
    visited = {begin_word}
    
    while queue:
        word, length = queue.popleft()
        
        if word == end_word:
            return length
        
        # Generar todas las transformaciones posibles
        for i in range(len(word)):
            for char in 'abcdefghijklmnopqrstuvwxyz':
                if char != word[i]:
                    new_word = word[:i] + char + word[i+1:]
                    
                    if new_word in word_set and new_word not in visited:
                        visited.add(new_word)
                        queue.append((new_word, length + 1))
    
    return 0  # No transformation possible

def word_ladder_bidirectional(begin_word, end_word, word_list):
    """
    Word Ladder optimizado - Bidirectional BFS
    Más eficiente: busca desde ambos extremos
    """
    if end_word not in word_list:
        return 0
    
    word_set = set(word_list)
    
    # Sets para BFS bidireccional
    begin_set = {begin_word}
    end_set = {end_word}
    visited = set()
    length = 1
    
    while begin_set and end_set:
        # Siempre expandir el set más pequeño
        if len(begin_set) > len(end_set):
            begin_set, end_set = end_set, begin_set
        
        next_set = set()
        
        for word in begin_set:
            for i in range(len(word)):
                for char in 'abcdefghijklmnopqrstuvwxyz':
                    if char != word[i]:
                        new_word = word[:i] + char + word[i+1:]
                        
                        # Si llegamos al otro set, encontramos path
                        if new_word in end_set:
                            return length + 1
                        
                        if new_word in word_set and new_word not in visited:
                            visited.add(new_word)
                            next_set.add(new_word)
        
        begin_set = next_set
        length += 1
    
    return 0

# ========================
# PROBLEMA 6: Number of Islands
# ========================
# Leetcode 200 - DFS/BFS en grid (grafo implícito)

def num_islands(grid):
    """
    Contar número de islas en grid 2D
    Usa DFS para marcar islas completas
    Complejidad: O(m * n)
    """
    if not grid or not grid[0]:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    islands = 0
    
    def dfs(r, c):
        # Boundary check y water check
        if (r < 0 or r >= rows or c < 0 or c >= cols or 
            grid[r][c] == '0'):
            return
        
        # Marcar como visitado
        grid[r][c] = '0'
        
        # Explorar 4 direcciones
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in directions:
            dfs(r + dr, c + dc)
    
    # Escanear toda la grid
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                islands += 1
                dfs(r, c)  # Marcar toda la isla
    
    return islands

def num_islands_bfs(grid):
    """
    Versión BFS del mismo problema
    Mismo complexity, diferente approach
    """
    if not grid or not grid[0]:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    islands = 0
    
    def bfs(start_r, start_c):
        queue = deque([(start_r, start_c)])
        grid[start_r][start_c] = '0'
        
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        while queue:
            r, c = queue.popleft()
            
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                
                if (0 <= nr < rows and 0 <= nc < cols and 
                    grid[nr][nc] == '1'):
                    grid[nr][nc] = '0'
                    queue.append((nr, nc))
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                islands += 1
                bfs(r, c)
    
    return islands

# ========================
# PROBLEMA 7: Valid Anagram
# ========================
# Leetcode 242 - Hash table básico pero importante

def is_anagram_v1(s, t):
    """
    Valid Anagram - Approach 1: Character counting
    Complejidad: O(n) tiempo, O(1) espacio (26 letters max)
    """
    if len(s) != len(t):
        return False
    
    char_count = {}
    
    # Contar caracteres en s
    for char in s:
        char_count[char] = char_count.get(char, 0) + 1
    
    # Decrementar con caracteres en t
    for char in t:
        if char not in char_count:
            return False
        char_count[char] -= 1
        if char_count[char] == 0:
            del char_count[char]
    
    return len(char_count) == 0

def is_anagram_v2(s, t):
    """
    Valid Anagram - Approach 2: Array counting (más eficiente)
    """
    if len(s) != len(t):
        return False
    
    # Array para 26 letras
    count = [0] * 26
    
    for i in range(len(s)):
        count[ord(s[i]) - ord('a')] += 1
        count[ord(t[i]) - ord('a')] -= 1
    
    return all(c == 0 for c in count)

# ========================
# PROBLEMA 8: Longest Consecutive Sequence
# ========================
# Leetcode 128 - Hash set inteligente

def longest_consecutive(nums):
    """
    Longest Consecutive Sequence
    Find longest sequence of consecutive integers
    Complejidad: O(n) tiempo, O(n) espacio
    """
    if not nums:
        return 0
    
    num_set = set(nums)
    longest = 0
    
    for num in num_set:
        # Solo empezar secuencia si es el inicio
        if num - 1 not in num_set:
            current_num = num
            current_length = 1
            
            # Extender secuencia hacia la derecha
            while current_num + 1 in num_set:
                current_num += 1
                current_length += 1
            
            longest = max(longest, current_length)
    
    return longest

# ========================
# PROBLEMA 9: Subarray Sum Equals K
# ========================
# Leetcode 560 - Prefix sum + hash map

def subarray_sum_equals_k(nums, k):
    """
    Count subarrays with sum equal to K
    Usa prefix sums + hash map
    Complejidad: O(n) tiempo, O(n) espacio
    """
    count = 0
    prefix_sum = 0
    sum_count = {0: 1}  # Para handle subarrays desde inicio
    
    for num in nums:
        prefix_sum += num
        
        # Si existe prefix_sum - k, encontramos subarray
        if prefix_sum - k in sum_count:
            count += sum_count[prefix_sum - k]
        
        # Actualizar count del prefix_sum actual
        sum_count[prefix_sum] = sum_count.get(prefix_sum, 0) + 1
    
    return count

# ========================
# PROBLEMA 10: LRU Cache
# ========================
# Leetcode 146 - Hash + Doubly Linked List

class LRUNode:
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    """
    LRU Cache - O(1) get y put operations
    Combina hash table + doubly linked list
    """
    
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}  # key -> node
        
        # Dummy head y tail para simplificar operaciones
        self.head = LRUNode()
        self.tail = LRUNode()
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _add_node(self, node):
        """Agregar nodo después del head"""
        node.prev = self.head
        node.next = self.head.next
        
        self.head.next.prev = node
        self.head.next = node
    
    def _remove_node(self, node):
        """Remover nodo de la linked list"""
        prev_node = node.prev
        next_node = node.next
        
        prev_node.next = next_node
        next_node.prev = prev_node
    
    def _move_to_head(self, node):
        """Mover nodo al head (mark as recently used)"""
        self._remove_node(node)
        self._add_node(node)
    
    def _pop_tail(self):
        """Remover último nodo (least recently used)"""
        last_node = self.tail.prev
        self._remove_node(last_node)
        return last_node
    
    def get(self, key):
        """
        Get value por key, mark as recently used
        Complejidad: O(1)
        """
        node = self.cache.get(key)
        
        if not node:
            return -1
        
        # Mover al head (mark as recently used)
        self._move_to_head(node)
        return node.value
    
    def put(self, key, value):
        """
        Put key-value, evict LRU si necesario
        Complejidad: O(1)
        """
        node = self.cache.get(key)
        
        if not node:
            new_node = LRUNode(key, value)
            
            if len(self.cache) >= self.capacity:
                # Evict LRU
                tail = self._pop_tail()
                del self.cache[tail.key]
            
            # Agregar nuevo nodo
            self.cache[key] = new_node
            self._add_node(new_node)
        else:
            # Actualizar valor existente
            node.value = value
            self._move_to_head(node)

# ========================
# PROBLEMA 11: Design Twitter
# ========================
# Leetcode 355 - Hash tables + heaps + design

class Twitter:
    """
    Design Twitter - Sistema de tweets y follows
    Combina múltiples estructuras de datos
    """
    
    def __init__(self):
        self.tweets = defaultdict(list)  # user_id -> [(timestamp, tweet_id)]
        self.follows = defaultdict(set)  # user_id -> set of followees
        self.timestamp = 0
    
    def post_tweet(self, user_id, tweet_id):
        """Post nuevo tweet"""
        self.timestamp += 1
        self.tweets[user_id].append((self.timestamp, tweet_id))
    
    def get_news_feed(self, user_id):
        """
        Get 10 most recent tweets from user + followees
        Usa heap para merge de múltiples sorted lists
        """
        # Obtener tweets del user y sus followees
        all_tweets = []
        
        # Tweets del usuario
        for timestamp, tweet_id in self.tweets[user_id]:
            all_tweets.append((timestamp, tweet_id))
        
        # Tweets de followees
        for followee in self.follows[user_id]:
            for timestamp, tweet_id in self.tweets[followee]:
                all_tweets.append((timestamp, tweet_id))
        
        # Ordenar por timestamp descendente y tomar top 10
        all_tweets.sort(reverse=True)
        return [tweet_id for _, tweet_id in all_tweets[:10]]
    
    def follow(self, follower_id, followee_id):
        """Follow otro usuario"""
        if follower_id != followee_id:  # No self-follow
            self.follows[follower_id].add(followee_id)
    
    def unfollow(self, follower_id, followee_id):
        """Unfollow usuario"""
        self.follows[follower_id].discard(followee_id)

# ========================
# TESTING FRAMEWORK
# ========================

def test_two_sum_variations():
    """Test Two Sum y variaciones"""
    print("=== TESTING TWO SUM VARIATIONS ===\n")
    
    nums = [2, 7, 11, 15, 2, 7]
    target = 9
    
    print(f"Array: {nums}, Target: {target}")
    print(f"Two Sum (first pair): {two_sum(nums[:], target)}")
    print(f"Two Sum (all pairs): {two_sum_all_pairs(nums, target)}")
    
    # Three Sum
    three_nums = [-1, 0, 1, 2, -1, -4]
    print(f"\nThree Sum array: {three_nums}")
    print(f"Three Sum result: {three_sum(three_nums[:])}")

def test_anagrams():
    """Test anagram problems"""
    print("\n=== TESTING ANAGRAM PROBLEMS ===\n")
    
    # Valid Anagram
    test_pairs = [("anagram", "nagaram"), ("rat", "car"), ("listen", "silent")]
    
    for s, t in test_pairs:
        result1 = is_anagram_v1(s, t)
        result2 = is_anagram_v2(s, t)
        print(f"'{s}' and '{t}' are anagrams: {result1} (v1), {result2} (v2)")
    
    # Group Anagrams
    words = ["eat", "tea", "tan", "ate", "nat", "bat"]
    print(f"\nGroup anagrams input: {words}")
    print(f"Groups (sorted): {group_anagrams_v1(words)}")
    print(f"Groups (count): {group_anagrams_v2(words)}")

def test_clone_graph():
    """Test graph cloning"""
    print("\n=== TESTING CLONE GRAPH ===\n")
    
    # Crear grafo de prueba: 1--2--4
    #                        |  |
    #                        3--+
    node1 = GraphNode(1)
    node2 = GraphNode(2)
    node3 = GraphNode(3)
    node4 = GraphNode(4)
    
    node1.neighbors = [node2, node3]
    node2.neighbors = [node1, node4]
    node3.neighbors = [node1]
    node4.neighbors = [node2]
    
    print("Original graph structure:")
    print(f"Node 1 neighbors: {[n.val for n in node1.neighbors]}")
    print(f"Node 2 neighbors: {[n.val for n in node2.neighbors]}")
    
    # Clone usando DFS
    cloned_dfs = clone_graph_dfs(node1)
    print(f"\nCloned (DFS) - Node 1 neighbors: {[n.val for n in cloned_dfs.neighbors]}")
    print(f"Different objects: {cloned_dfs is not node1}")
    
    # Clone usando BFS
    cloned_bfs = clone_graph_bfs(node1)
    print(f"Cloned (BFS) - Node 1 neighbors: {[n.val for n in cloned_bfs.neighbors]}")

def test_course_schedule():
    """Test course scheduling"""
    print("\n=== TESTING COURSE SCHEDULE ===\n")
    
    test_cases = [
        (2, [[1, 0]]),                    # Can finish: True
        (2, [[1, 0], [0, 1]]),           # Can finish: False (cycle)
        (4, [[1, 0], [2, 0], [3, 1], [3, 2]])  # Can finish: True
    ]
    
    for i, (num_courses, prereqs) in enumerate(test_cases, 1):
        can_finish = can_finish_courses(num_courses, prereqs)
        order = find_course_order(num_courses, prereqs)
        
        print(f"Test {i}: {num_courses} courses, prereqs: {prereqs}")
        print(f"   Can finish: {can_finish}")
        print(f"   Valid order: {order}")

def test_word_ladder():
    """Test word ladder transformation"""
    print("\n=== TESTING WORD LADDER ===\n")
    
    test_cases = [
        ("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]),  # Expected: 5
        ("hit", "cog", ["hot", "dot", "dog", "lot", "log"]),        # Expected: 0
        ("a", "c", ["a", "b", "c"])                                 # Expected: 2
    ]
    
    for i, (begin, end, word_list) in enumerate(test_cases, 1):
        length_basic = word_ladder_length(begin, end, word_list)
        length_bi = word_ladder_bidirectional(begin, end, word_list)
        
        print(f"Test {i}: '{begin}' → '{end}'")
        print(f"   Word list: {word_list}")
        print(f"   Shortest path length: {length_basic} (basic), {length_bi} (bidirectional)")

def test_islands():
    """Test number of islands"""
    print("\n=== TESTING NUMBER OF ISLANDS ===\n")
    
    grid1 = [
        ["1", "1", "1", "1", "0"],
        ["1", "1", "0", "1", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "0", "0", "0"]
    ]
    
    grid2 = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"]
    ]
    
    print("Grid 1:")
    for row in grid1:
        print("   " + " ".join(row))
    
    # Note: num_islands modifica grid, así que usar copias
    import copy
    islands1_dfs = num_islands(copy.deepcopy(grid1))
    islands1_bfs = num_islands_bfs(copy.deepcopy(grid1))
    
    print(f"Islands in grid 1: {islands1_dfs} (DFS), {islands1_bfs} (BFS)")
    
    print("\nGrid 2:")
    for row in grid2:
        print("   " + " ".join(row))
    
    islands2 = num_islands(copy.deepcopy(grid2))
    print(f"Islands in grid 2: {islands2}")

def test_lru_cache():
    """Test LRU Cache"""
    print("\n=== TESTING LRU CACHE ===\n")
    
    lru = LRUCache(2)  # Capacity = 2
    
    operations = [
        ("put", 1, 1),
        ("put", 2, 2),
        ("get", 1, None),      # Returns 1
        ("put", 3, 3),         # Evicts 2
        ("get", 2, None),      # Returns -1 (evicted)
        ("put", 4, 4),         # Evicts 1
        ("get", 1, None),      # Returns -1 (evicted)
        ("get", 3, None),      # Returns 3
        ("get", 4, None)       # Returns 4
    ]
    
    print("LRU Cache operations (capacity=2):")
    for op in operations:
        if op[0] == "put":
            lru.put(op[1], op[2])
            print(f"   put({op[1]}, {op[2]})")
        else:
            result = lru.get(op[1])
            print(f"   get({op[1]}) → {result}")

def test_twitter_design():
    """Test Twitter design"""
    print("\n=== TESTING TWITTER DESIGN ===\n")
    
    twitter = Twitter()
    
    operations = [
        ("postTweet", 1, 5),
        ("getNewsFeed", 1),
        ("follow", 1, 2),
        ("postTweet", 2, 6),
        ("getNewsFeed", 1),
        ("unfollow", 1, 2),
        ("getNewsFeed", 1)
    ]
    
    print("Twitter operations:")
    for op in operations:
        if op[0] == "postTweet":
            twitter.post_tweet(op[1], op[2])
            print(f"   User {op[1]} posted tweet {op[2]}")
        elif op[0] == "getNewsFeed":
            feed = twitter.get_news_feed(op[1])
            print(f"   User {op[1]} news feed: {feed}")
        elif op[0] == "follow":
            twitter.follow(op[1], op[2])
            print(f"   User {op[1]} followed user {op[2]}")
        elif op[0] == "unfollow":
            twitter.unfollow(op[1], op[2])
            print(f"   User {op[1]} unfollowed user {op[2]}")

def benchmark_hash_vs_linear():
    """Comparar hash table vs búsqueda lineal"""
    print("\n=== PERFORMANCE: HASH VS LINEAR SEARCH ===\n")
    
    import time
    import random
    
    # Crear datasets de prueba
    sizes = [1000, 10000, 100000]
    
    for size in sizes:
        data = list(range(size))
        search_items = [random.randint(0, size-1) for _ in range(1000)]
        
        print(f"Testing with {size:,} elements, 1000 searches:")
        
        # Hash table approach
        start = time.time()
        hash_set = set(data)
        hash_time = 0
        for item in search_items:
            start_search = time.time()
            found = item in hash_set
            hash_time += time.time() - start_search
        total_hash_time = time.time() - start
        
        # Linear search approach
        start = time.time()
        linear_time = 0
        for item in search_items:
            start_search = time.time()
            found = item in data
            linear_time += time.time() - start_search
        total_linear_time = time.time() - start
        
        print(f"   Hash searches: {hash_time:.6f}s")
        print(f"   Linear searches: {linear_time:.6f}s")
        print(f"   Speedup: {linear_time/hash_time:.0f}x faster\n")

# ========================
# PATRONES AVANZADOS
# ========================

def find_duplicate_number(nums):
    """
    Find Duplicate Number - Leetcode 287
    Array treated as linked list usando indices
    ¡Muy inteligente!
    """
    # Floyd's Cycle Detection (tortoise and hare)
    slow = fast = nums[0]
    
    # Encontrar intersection point
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    
    # Encontrar entrance al ciclo
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    
    return slow

def random_pick_with_weight(w):
    """
    Random Pick with Weight - Leetcode 528
    Prefix sums + binary search
    """
    import random
    import bisect
    
    def __init__(w):
        # Calcular prefix sums
        prefix_sums = []
        prefix_sum = 0
        for weight in w:
            prefix_sum += weight
            prefix_sums.append(prefix_sum)
        return prefix_sums
    
    def pick_index(prefix_sums):
        target = random.random() * prefix_sums[-1]
        # Binary search para encontrar índice
        return bisect.bisect_left(prefix_sums, target)
    
    prefix_sums = __init__(w)
    return pick_index(prefix_sums)

def alien_dictionary(words):
    """
    Alien Dictionary - Leetcode 269
    Topological sort para determinar orden de caracteres
    """
    # Construir grafo de dependencias entre caracteres
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    chars = set()
    
    # Obtener todos los caracteres
    for word in words:
        for char in word:
            chars.add(char)
    
    # Inicializar in-degrees
    for char in chars:
        in_degree[char] = 0
    
    # Comparar palabras adyacentes
    for i in range(len(words) - 1):
        word1, word2 = words[i], words[i + 1]
        min_len = min(len(word1), len(word2))
        
        # Encontrar primer carácter diferente
        for j in range(min_len):
            if word1[j] != word2[j]:
                if word2[j] not in graph[word1[j]]:
                    graph[word1[j]].append(word2[j])
                    in_degree[word2[j]] += 1
                break
        else:
            # Si word1 es prefix de word2 pero word1 es más largo → inválido
            if len(word1) > len(word2):
                return ""
    
    # Topological sort
    queue = deque()
    for char in chars:
        if in_degree[char] == 0:
            queue.append(char)
    
    result = []
    while queue:
        char = queue.popleft()
        result.append(char)
        
        for neighbor in graph[char]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Verificar si es válido (no hay ciclos)
    return ''.join(result) if len(result) == len(chars) else ""

# ========================
# TIPS PARA ENTREVISTAS
# ========================

"""
🎯 ESTRATEGIAS GANADORAS PARA HASH + GRAPH PROBLEMS:

HASH TABLES:
1. SIEMPRE CONSIDERA hash table para problemas de:
   - Lookup rápido O(1)
   - Counting/frequency problems
   - Two pointers optimization
   - Caching/memoization

2. PATRONES COMUNES:
   - Seen set: para detectar duplicados
   - Count map: para frequency analysis  
   - Complement map: para Two Sum pattern
   - Prefix sum map: para subarray problems

3. OPTIMIZACIONES:
   - Use array en lugar de dict si range conocido (ej: 26 letters)
   - Considera space vs time trade-offs
   - Para strings, considera rolling hash

GRAPHS:
1. IDENTIFICAR TIPO:
   - ¿Directed o undirected?
   - ¿Weighted o unweighted?
   - ¿Sparse o dense? (afecta representación)

2. ALGORITMO SELECTION:
   - DFS: Para path finding, cycle detection, topological sort
   - BFS: Para shortest path (unweighted), level-order
   - Union-Find: Para connectivity, MST

3. REPRESENTACIÓN:
   - Adjacency List: Default choice (space efficient)
   - Adjacency Matrix: Si necesitas O(1) edge lookup
   - Edge List: Para algoritmos específicos (Kruskal, etc.)

4. EDGE CASES:
   - Empty graph
   - Single vertex
   - Disconnected components
   - Self loops

PROBLEMAS HÍBRIDOS:
1. Clone problems: Hash map para track visitados
2. Path problems: Hash set para avoid revisiting
3. Cycle detection: Visited states con hash
4. Topological sort: In-degree tracking con hash

COMPLEJIDAD ANALYSIS:
- Always considerar V (vertices) y E (edges)
- Space complexity a menudo determinado por visited structures
- Hash operations son O(1) average, O(n) worst case
"""

if __name__ == "__main__":
    test_two_sum_variations()
    test_anagrams()
    test_clone_graph()
    test_course_schedule()
    test_word_ladder()
    test_islands()
    test_lru_cache()
    test_twitter_design()
    benchmark_hash_vs_linear()
    
    print("\n=== BONUS: ADVANCED PROBLEMS ===")
    
    # Test longest consecutive
    nums = [100, 4, 200, 1, 3, 2]
    longest = longest_consecutive(nums)
    print(f"\nLongest consecutive sequence in {nums}: {longest}")
    
    # Test subarray sum
    nums = [1, 1, 1]
    k = 2
    count = subarray_sum_equals_k(nums, k)
    print(f"Subarrays with sum {k} in {nums}: {count}")
    
    # Test find duplicate
    nums = [1, 3, 4, 2, 2]
    duplicate = find_duplicate_number(nums)
    print(f"Duplicate number in {nums}: {duplicate}")
    
    # Test alien dictionary
    words = ["wrt", "wrf", "er", "ett", "rftt"]
    alien_order = alien_dictionary(words)
    print(f"Alien dictionary order for {words}: '{alien_order}'")