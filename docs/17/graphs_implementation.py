"""
GRAFOS - REPRESENTACIONES Y ALGORITMOS FUNDAMENTALES
===================================================

Los grafos son la estructura de datos más versátil:
- Modelan cualquier relación entre entidades
- Base para algoritmos como DFS, BFS, Dijkstra, etc.
- Aparecen en 70% de entrevistas senior

REPRESENTACIONES PRINCIPALES:
1. Adjacency List: {node: [neighbors]} - Más común
2. Adjacency Matrix: matrix[i][j] = edge exists
3. Edge List: [(node1, node2, weight)]

TIPOS DE GRAFOS:
- Directed vs Undirected
- Weighted vs Unweighted  
- Connected vs Disconnected
- Cyclic vs Acyclic (DAG)
"""

from collections import defaultdict, deque

class Graph:
    """
    Implementación de grafo usando adjacency list
    Soporta directed/undirected y weighted/unweighted
    """
    
    def __init__(self, directed=False):
        self.graph = defaultdict(list)  # adjacency list
        self.directed = directed
        self.vertices = set()
    
    def add_vertex(self, vertex):
        """Agregar vértice al grafo"""
        self.vertices.add(vertex)
        if vertex not in self.graph:
            self.graph[vertex] = []
    
    def add_edge(self, u, v, weight=1):
        """
        Agregar arista entre u y v
        Para undirected graph, agrega en ambas direcciones
        """
        self.add_vertex(u)
        self.add_vertex(v)
        
        # Agregar arista u -> v
        self.graph[u].append((v, weight))
        
        # Si es undirected, agregar v -> u también
        if not self.directed:
            self.graph[v].append((u, weight))
    
    def get_neighbors(self, vertex):
        """Obtener vecinos de un vértice"""
        return self.graph[vertex]
    
    def get_vertices(self):
        """Obtener todos los vértices"""
        return list(self.vertices)
    
    def has_edge(self, u, v):
        """Verificar si existe arista u -> v"""
        for neighbor, _ in self.graph[u]:
            if neighbor == v:
                return True
        return False
    
    def remove_edge(self, u, v):
        """Remover arista u -> v"""
        self.graph[u] = [(neighbor, weight) for neighbor, weight in self.graph[u] 
                         if neighbor != v]
        
        if not self.directed:
            self.graph[v] = [(neighbor, weight) for neighbor, weight in self.graph[v] 
                           if neighbor != u]
    
    def display(self):
        """Mostrar representación del grafo"""
        print(f"Graph ({'directed' if self.directed else 'undirected'}):")
        for vertex in sorted(self.vertices):
            neighbors = [f"{neighbor}({weight})" for neighbor, weight in self.graph[vertex]]
            print(f"  {vertex}: {neighbors}")
    
    def __str__(self):
        return f"Graph(vertices={len(self.vertices)}, directed={self.directed})"

# ========================
# ALGORITMOS FUNDAMENTALES
# ========================

def dfs_recursive(graph, start, visited=None):
    """
    Depth-First Search recursivo
    Complejidad: O(V + E) tiempo, O(V) espacio
    """
    if visited is None:
        visited = set()
    
    visited.add(start)
    result = [start]
    
    for neighbor, _ in graph.get_neighbors(start):
        if neighbor not in visited:
            result.extend(dfs_recursive(graph, neighbor, visited))
    
    return result

def dfs_iterative(graph, start):
    """
    Depth-First Search iterativo usando stack
    Complejidad: O(V + E) tiempo, O(V) espacio
    """
    visited = set()
    stack = [start]
    result = []
    
    while stack:
        vertex = stack.pop()
        
        if vertex not in visited:
            visited.add(vertex)
            result.append(vertex)
            
            # Agregar vecinos al stack (en orden reverso para consistencia)
            neighbors = [neighbor for neighbor, _ in graph.get_neighbors(vertex)]
            for neighbor in reversed(neighbors):
                if neighbor not in visited:
                    stack.append(neighbor)
    
    return result

def bfs(graph, start):
    """
    Breadth-First Search usando queue
    Complejidad: O(V + E) tiempo, O(V) espacio
    """
    visited = set()
    queue = deque([start])
    result = []
    
    visited.add(start)
    
    while queue:
        vertex = queue.popleft()
        result.append(vertex)
        
        for neighbor, _ in graph.get_neighbors(vertex):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return result

def find_path_dfs(graph, start, end, path=None):
    """
    Encontrar path usando DFS
    Retorna primer path encontrado (no necesariamente el más corto)
    """
    if path is None:
        path = []
    
    path = path + [start]
    
    if start == end:
        return path
    
    for neighbor, _ in graph.get_neighbors(start):
        if neighbor not in path:  # Evitar ciclos
            new_path = find_path_dfs(graph, neighbor, end, path)
            if new_path:
                return new_path
    
    return None

def find_shortest_path_bfs(graph, start, end):
    """
    Encontrar shortest path usando BFS
    BFS garantiza shortest path en grafos unweighted
    """
    if start == end:
        return [start]
    
    visited = set()
    queue = deque([(start, [start])])  # (vertex, path)
    visited.add(start)
    
    while queue:
        vertex, path = queue.popleft()
        
        for neighbor, _ in graph.get_neighbors(vertex):
            if neighbor == end:
                return path + [neighbor]
            
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return None  # No path found

def has_cycle_undirected(graph):
    """
    Detectar ciclo en grafo undirected usando DFS
    Complejidad: O(V + E)
    """
    visited = set()
    
    def dfs(vertex, parent):
        visited.add(vertex)
        
        for neighbor, _ in graph.get_neighbors(vertex):
            if neighbor not in visited:
                if dfs(neighbor, vertex):
                    return True
            elif neighbor != parent:
                # Back edge encontrado (ciclo)
                return True
        
        return False
    
    # Verificar todos los componentes
    for vertex in graph.get_vertices():
        if vertex not in visited:
            if dfs(vertex, -1):
                return True
    
    return False

def has_cycle_directed(graph):
    """
    Detectar ciclo en grafo directed usando DFS + colores
    Complejidad: O(V + E)
    """
    # Estados: 0=white (no visitado), 1=gray (procesando), 2=black (terminado)
    color = defaultdict(int)
    
    def dfs(vertex):
        if color[vertex] == 1:  # Gray - back edge (ciclo)
            return True
        if color[vertex] == 2:  # Black - ya procesado
            return False
        
        # Marcar como procesando
        color[vertex] = 1
        
        for neighbor, _ in graph.get_neighbors(vertex):
            if dfs(neighbor):
                return True
        
        # Marcar como terminado
        color[vertex] = 2
        return False
    
    # Verificar todos los vértices
    for vertex in graph.get_vertices():
        if color[vertex] == 0:
            if dfs(vertex):
                return True
    
    return False

def topological_sort(graph):
    """
    Ordenamiento topológico (solo para DAGs)
    Complejidad: O(V + E)
    """
    if not graph.directed:
        raise ValueError("Topological sort only for directed graphs")
    
    in_degree = defaultdict(int)
    
    # Calcular in-degree de cada vértice
    for vertex in graph.get_vertices():
        for neighbor, _ in graph.get_neighbors(vertex):
            in_degree[neighbor] += 1
    
    # Queue con vértices de in-degree 0
    queue = deque()
    for vertex in graph.get_vertices():
        if in_degree[vertex] == 0:
            queue.append(vertex)
    
    result = []
    
    while queue:
        vertex = queue.popleft()
        result.append(vertex)
        
        # Decrementar in-degree de vecinos
        for neighbor, _ in graph.get_neighbors(vertex):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Si no procesamos todos los vértices, hay ciclo
    if len(result) != len(graph.get_vertices()):
        raise ValueError("Graph has cycle - cannot perform topological sort")
    
    return result

def connected_components(graph):
    """
    Encontrar componentes conectados
    Complejidad: O(V + E)
    """
    visited = set()
    components = []
    
    def dfs_component(vertex, component):
        visited.add(vertex)
        component.append(vertex)
        
        for neighbor, _ in graph.get_neighbors(vertex):
            if neighbor not in visited:
                dfs_component(neighbor, component)
    
    for vertex in graph.get_vertices():
        if vertex not in visited:
            component = []
            dfs_component(vertex, component)
            components.append(component)
    
    return components

# ========================
# MATRIX REPRESENTATION
# ========================

class GraphMatrix:
    """
    Grafo usando adjacency matrix
    Mejor para grafos densos (muchas aristas)
    """
    
    def __init__(self, num_vertices, directed=False):
        self.num_vertices = num_vertices
        self.directed = directed
        self.matrix = [[0] * num_vertices for _ in range(num_vertices)]
        self.vertex_map = {}  # Mapear labels a indices
        self.reverse_map = {}  # Mapear indices a labels
        self.next_index = 0
    
    def add_vertex(self, label):
        """Agregar vértice con label"""
        if label not in self.vertex_map:
            self.vertex_map[label] = self.next_index
            self.reverse_map[self.next_index] = label
            self.next_index += 1
    
    def add_edge(self, u, v, weight=1):
        """Agregar arista con peso"""
        self.add_vertex(u)
        self.add_vertex(v)
        
        u_idx = self.vertex_map[u]
        v_idx = self.vertex_map[v]
        
        self.matrix[u_idx][v_idx] = weight
        
        if not self.directed:
            self.matrix[v_idx][u_idx] = weight
    
    def has_edge(self, u, v):
        """Verificar si existe arista"""
        if u not in self.vertex_map or v not in self.vertex_map:
            return False
        
        u_idx = self.vertex_map[u]
        v_idx = self.vertex_map[v]
        return self.matrix[u_idx][v_idx] != 0
    
    def get_neighbors(self, vertex):
        """Obtener vecinos de un vértice"""
        if vertex not in self.vertex_map:
            return []
        
        vertex_idx = self.vertex_map[vertex]
        neighbors = []
        
        for i in range(self.num_vertices):
            if self.matrix[vertex_idx][i] != 0:
                neighbor_label = self.reverse_map[i]
                weight = self.matrix[vertex_idx][i]
                neighbors.append((neighbor_label, weight))
        
        return neighbors
    
    def display(self):
        """Mostrar matriz de adyacencia"""
        print("Adjacency Matrix:")
        
        # Header con labels
        labels = [self.reverse_map.get(i, f"V{i}") for i in range(self.next_index)]
        print("     " + " ".join(f"{label:>3}" for label in labels))
        
        # Filas de la matriz
        for i in range(self.next_index):
            row_label = self.reverse_map.get(i, f"V{i}")
            row = [str(self.matrix[i][j]) for j in range(self.next_index)]
            print(f"{row_label:>3}: " + " ".join(f"{val:>3}" for val in row))

# ========================
# TESTING FRAMEWORK
# ========================

def create_sample_graph():
    """Crear grafo de ejemplo para testing"""
    #     A --- B
    #     |     |
    #     C --- D --- E
    #           |
    #           F
    
    g = Graph(directed=False)
    edges = [
        ('A', 'B'), ('A', 'C'),
        ('B', 'D'), ('C', 'D'),
        ('D', 'E'), ('D', 'F')
    ]
    
    for u, v in edges:
        g.add_edge(u, v)
    
    return g

def create_directed_graph():
    """Crear grafo dirigido para testing"""
    #  A → B → D
    #  ↓   ↓   ↑
    #  C → E → F
    
    g = Graph(directed=True)
    edges = [
        ('A', 'B'), ('A', 'C'),
        ('B', 'D'), ('B', 'E'),
        ('C', 'E'), ('E', 'F'),
        ('F', 'D')
    ]
    
    for u, v in edges:
        g.add_edge(u, v)
    
    return g

def test_graph_traversals():
    """Test algoritmos de recorrido"""
    print("=== TESTING GRAPH TRAVERSALS ===\n")
    
    g = create_sample_graph()
    g.display()
    
    start = 'A'
    print(f"\nTraversals starting from {start}:")
    
    dfs_rec = dfs_recursive(g, start)
    print(f"DFS Recursive:  {dfs_rec}")
    
    dfs_iter = dfs_iterative(g, start)
    print(f"DFS Iterative:  {dfs_iter}")
    
    bfs_result = bfs(g, start)
    print(f"BFS:            {bfs_result}")

def test_path_finding():
    """Test algoritmos de búsqueda de paths"""
    print("\n=== TESTING PATH FINDING ===\n")
    
    g = create_sample_graph()
    
    test_paths = [('A', 'F'), ('B', 'C'), ('A', 'E')]
    
    for start, end in test_paths:
        dfs_path = find_path_dfs(g, start, end)
        bfs_path = find_shortest_path_bfs(g, start, end)
        
        print(f"Path {start} → {end}:")
        print(f"  DFS path: {dfs_path}")
        print(f"  BFS path (shortest): {bfs_path}")

def test_cycle_detection():
    """Test detección de ciclos"""
    print("\n=== TESTING CYCLE DETECTION ===\n")
    
    # Test undirected graph
    undirected = create_sample_graph()
    has_cycle = has_cycle_undirected(undirected)
    print(f"Undirected graph has cycle: {has_cycle}")
    
    # Test directed graph
    directed = create_directed_graph()
    has_cycle_dir = has_cycle_directed(directed)
    print(f"Directed graph has cycle: {has_cycle_dir}")
    
    # Test DAG (Directed Acyclic Graph)
    dag = Graph(directed=True)
    dag_edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D')]
    for u, v in dag_edges:
        dag.add_edge(u, v)
    
    print(f"DAG has cycle: {has_cycle_directed(dag)}")
    
    # Test topological sort on DAG
    try:
        topo_order = topological_sort(dag)
        print(f"Topological order of DAG: {topo_order}")
    except ValueError as e:
        print(f"Topological sort failed: {e}")

def test_connected_components():
    """Test componentes conectados"""
    print("\n=== TESTING CONNECTED COMPONENTS ===\n")
    
    # Crear grafo con múltiples componentes
    #  A---B    D---E
    #  |        |
    #  C        F    G (isolated)
    
    g = Graph(directed=False)
    edges = [
        ('A', 'B'), ('A', 'C'),  # Componente 1
        ('D', 'E'), ('D', 'F')   # Componente 2
        # G estará aislado (Componente 3)
    ]
    
    for u, v in edges:
        g.add_edge(u, v)
    
    g.add_vertex('G')  # Vértice aislado
    
    components = connected_components(g)
    print(f"Connected components: {components}")
    print(f"Number of components: {len(components)}")

def test_matrix_representation():
    """Test representación con matriz"""
    print("\n=== TESTING MATRIX REPRESENTATION ===\n")
    
    gm = GraphMatrix(5, directed=True)
    
    # Agregar aristas
    edges = [('A', 'B', 2), ('A', 'C', 1), ('B', 'D', 3), ('C', 'D', 1), ('D', 'E', 2)]
    
    for u, v, weight in edges:
        gm.add_edge(u, v, weight)
    
    gm.display()
    
    print(f"\nNeighbors of A: {gm.get_neighbors('A')}")
    print(f"Has edge A→B: {gm.has_edge('A', 'B')}")
    print(f"Has edge B→A: {gm.has_edge('B', 'A')}")

def performance_comparison():
    """Comparar performance entre representaciones"""
    print("\n=== PERFORMANCE COMPARISON ===\n")
    
    import time
    
    # Test con grafo mediano
    n_vertices = 1000
    n_edges = 5000
    
    print(f"Testing with {n_vertices} vertices, {n_edges} edges")
    
    # Test Adjacency List
    start = time.time()
    g_list = Graph()
    for i in range(n_edges):
        u, v = i % n_vertices, (i * 7) % n_vertices
        g_list.add_edge(u, v)
    list_time = time.time() - start
    
    # Test DFS en adjacency list
    start = time.time()
    dfs_result = dfs_iterative(g_list, 0)
    dfs_list_time = time.time() - start
    
    print(f"Adjacency List - Build: {list_time:.4f}s, DFS: {dfs_list_time:.4f}s")
    print(f"DFS visited {len(dfs_result)} vertices")

if __name__ == "__main__":
    test_graph_traversals()
    test_path_finding()
    test_cycle_detection()
    test_connected_components()
    test_matrix_representation()
    performance_comparison()
