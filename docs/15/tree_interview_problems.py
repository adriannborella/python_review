"""
PROBLEMAS TÍPICOS DE ENTREVISTA - ÁRBOLES BINARIOS
==================================================

Estos son los problemas MÁS FRECUENTES en entrevistas.
Cada uno incluye múltiples enfoques y análisis de complejidad.
¡Practica hasta poder resolverlos en menos de 15 minutos!
"""

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# ========================
# PROBLEMA 1: Validate BST
# ========================
# Leetcode 98 - ¡SÚPER COMÚN!

def is_valid_bst_v1(root):
    """
    Validar BST - Approach 1: Inorder traversal
    Idea: Inorder de BST debe ser estrictamente creciente
    Complejidad: O(n) tiempo, O(n) espacio
    """
    def inorder(node):
        if not node:
            return []
        return inorder(node.left) + [node.val] + inorder(node.right)
    
    values = inorder(root)
    
    # Verificar que sea estrictamente creciente
    for i in range(1, len(values)):
        if values[i] <= values[i-1]:
            return False
    return True

def is_valid_bst_v2(root):
    """
    Validar BST - Approach 2: Min-Max bounds (ÓPTIMO)
    Idea: Cada nodo debe estar en un rango [min, max]
    Complejidad: O(n) tiempo, O(h) espacio
    """
    def validate(node, min_val, max_val):
        if not node:
            return True
        
        if node.val <= min_val or node.val >= max_val:
            return False
        
        return (validate(node.left, min_val, node.val) and 
                validate(node.right, node.val, max_val))
    
    return validate(root, float('-inf'), float('inf'))

def is_valid_bst_v3(root):
    """
    Validar BST - Approach 3: Inorder con una variable
    Idea: Track el valor anterior durante inorder
    Complejidad: O(n) tiempo, O(h) espacio
    """
    def inorder(node):
        nonlocal prev
        if not node:
            return True
        
        # Procesar subtree izquierdo
        if not inorder(node.left):
            return False
        
        # Verificar orden
        if prev is not None and node.val <= prev:
            return False
        prev = node.val
        
        # Procesar subtree derecho
        return inorder(node.right)
    
    prev = None
    return inorder(root)

# ========================
# PROBLEMA 2: Tree Traversals
# ========================
# ¡Pueden pedir cualquier combinación!

def binary_tree_inorder(root):
    """
    Inorder Traversal - Iterativo
    Complejidad: O(n) tiempo, O(h) espacio
    """
    if not root:
        return []
    
    result = []
    stack = []
    current = root
    
    while stack or current:
        # Ir hasta la izquierda
        while current:
            stack.append(current)
            current = current.left
        
        # Procesar nodo
        current = stack.pop()
        result.append(current.val)
        
        # Ir a la derecha
        current = current.right
    
    return result

def binary_tree_level_order(root):
    """
    Level Order Traversal (BFS)
    Complejidad: O(n) tiempo, O(w) espacio (w = ancho máximo)
    """
    if not root:
        return []
    
    result = []
    queue = [root]
    
    while queue:
        level_size = len(queue)
        level_values = []
        
        for _ in range(level_size):
            node = queue.pop(0)
            level_values.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(level_values)
    
    return result

# ========================
# PROBLEMA 3: Maximum Depth
# ========================
# Leetcode 104 - Problema de calentamiento

def max_depth_recursive(root):
    """
    Profundidad máxima - Recursivo
    Complejidad: O(n) tiempo, O(h) espacio
    """
    if not root:
        return 0
    
    left_depth = max_depth_recursive(root.left)
    right_depth = max_depth_recursive(root.right)
    
    return 1 + max(left_depth, right_depth)

def max_depth_iterative(root):
    """
    Profundidad máxima - Iterativo (BFS)
    Complejidad: O(n) tiempo, O(w) espacio
    """
    if not root:
        return 0
    
    queue = [(root, 1)]  # (nodo, profundidad)
    max_depth = 0
    
    while queue:
        node, depth = queue.pop(0)
        max_depth = max(max_depth, depth)
        
        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))
    
    return max_depth

# ========================
# PROBLEMA 4: Same Tree
# ========================
# Leetcode 100 - Comparación de estructuras

def is_same_tree(p, q):
    """
    Verificar si dos árboles son idénticos
    Complejidad: O(min(m,n)) tiempo, O(min(m,n)) espacio
    """
    # Ambos None
    if not p and not q:
        return True
    
    # Uno None, otro no
    if not p or not q:
        return False
    
    # Valores diferentes
    if p.val != q.val:
        return False
    
    # Recursivamente comparar subtrees
    return (is_same_tree(p.left, q.left) and 
            is_same_tree(p.right, q.right))

# ========================
# PROBLEMA 5: Symmetric Tree
# ========================
# Leetcode 101 - Simetría

def is_symmetric(root):
    """
    Verificar si árbol es simétrico
    Complejidad: O(n) tiempo, O(h) espacio
    """
    def is_mirror(left, right):
        # Ambos None
        if not left and not right:
            return True
        
        # Uno None, otro no
        if not left or not right:
            return False
        
        # Valores iguales y subtrees simétricamente espejados
        return (left.val == right.val and 
                is_mirror(left.left, right.right) and
                is_mirror(left.right, right.left))
    
    if not root:
        return True
    
    return is_mirror(root.left, root.right)

# ========================
# PROBLEMA 6: Path Sum
# ========================
# Leetcode 112 - Suma de caminos

def has_path_sum(root, target_sum):
    """
    Verificar si existe camino raíz->hoja con suma target
    Complejidad: O(n) tiempo, O(h) espacio
    """
    if not root:
        return False
    
    # Si es hoja, verificar suma
    if not root.left and not root.right:
        return root.val == target_sum
    
    # Recursivamente buscar en subtrees
    remaining = target_sum - root.val
    return (has_path_sum(root.left, remaining) or 
            has_path_sum(root.right, remaining))

def path_sum_all_paths(root, target_sum):
    """
    Encontrar TODOS los caminos raíz->hoja con suma target
    Leetcode 113
    """
    def dfs(node, remaining, path, result):
        if not node:
            return
        
        path.append(node.val)
        
        # Si es hoja y suma correcta
        if not node.left and not node.right and remaining == node.val:
            result.append(path[:])  # Copia del path
        else:
            # Continuar búsqueda
            dfs(node.left, remaining - node.val, path, result)
            dfs(node.right, remaining - node.val, path, result)
        
        path.pop()  # Backtrack
    
    result = []
    dfs(root, target_sum, [], result)
    return result

# ========================
# PROBLEMA 7: Lowest Common Ancestor
# ========================
# Leetcode 235 (BST) / 236 (Binary Tree) - MUY COMÚN!

def lowest_common_ancestor_bst(root, p, q):
    """
    LCA en BST - Aprovecha la propiedad de BST
    Complejidad: O(h) tiempo, O(1) espacio iterativo
    """
    while root:
        # Ambos en subtree izquierdo
        if p.val < root.val and q.val < root.val:
            root = root.left
        # Ambos en subtree derecho  
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            # Split point - este es el LCA
            return root
    return None

def lowest_common_ancestor_bt(root, p, q):
    """
    LCA en Binary Tree general
    Complejidad: O(n) tiempo, O(h) espacio
    """
    if not root or root == p or root == q:
        return root
    
    # Buscar en ambos subtrees
    left = lowest_common_ancestor_bt(root.left, p, q)
    right = lowest_common_ancestor_bt(root.right, p, q)
    
    # Si ambos subtrees retornan algo, este nodo es LCA
    if left and right:
        return root
    
    # Retornar el que no sea None
    return left if left else right

# ========================
# PROBLEMA 8: Diameter of Tree
# ========================
# Leetcode 543 - Path más largo

def diameter_of_binary_tree(root):
    """
    Encontrar el diámetro (camino más largo entre dos nodos)
    Complejidad: O(n) tiempo, O(h) espacio
    """
    def height_and_diameter(node):
        if not node:
            return 0, 0  # (altura, diámetro)
        
        left_height, left_diameter = height_and_diameter(node.left)
        right_height, right_diameter = height_and_diameter(node.right)
        
        # Altura de este nodo
        current_height = 1 + max(left_height, right_height)
        
        # Diámetro pasando por este nodo
        diameter_through_node = left_height + right_height
        
        # Diámetro máximo hasta ahora
        max_diameter = max(left_diameter, right_diameter, diameter_through_node)
        
        return current_height, max_diameter
    
    _, diameter = height_and_diameter(root)
    return diameter

# ========================
# PROBLEMA 9: Serialize/Deserialize
# ========================
# Leetcode 297 - Muy avanzado pero aparece!

class Codec:
    """Serializar y deserializar árbol binario"""
    
    def serialize(self, root):
        """Serializar árbol a string"""
        def preorder(node):
            if not node:
                vals.append("null")
            else:
                vals.append(str(node.val))
                preorder(node.left)
                preorder(node.right)
        
        vals = []
        preorder(root)
        return ",".join(vals)
    
    def deserialize(self, data):
        """Deserializar string a árbol"""
        def build():
            val = next(vals)
            if val == "null":
                return None
            
            node = TreeNode(int(val))
            node.left = build()
            node.right = build()
            return node
        
        vals = iter(data.split(","))
        return build()

# ========================
# TESTING FRAMEWORK
# ========================

def create_test_tree():
    """Crear árbol de prueba estándar"""
    #       5
    #      / \
    #     3   8
    #    / \   \
    #   2   4   9
    root = TreeNode(5)
    root.left = TreeNode(3)
    root.right = TreeNode(8)
    root.left.left = TreeNode(2)
    root.left.right = TreeNode(4)
    root.right.right = TreeNode(9)
    return root

def create_invalid_bst():
    """Crear árbol que NO es BST"""
    #       5
    #      / \
    #     3   8
    #    / \   \
    #   2   6   9  ← 6 > 5, debería estar a la derecha!
    root = TreeNode(5)
    root.left = TreeNode(3)
    root.right = TreeNode(8)
    root.left.left = TreeNode(2)
    root.left.right = TreeNode(6)  # ¡Inválido!
    root.right.right = TreeNode(9)
    return root

def test_all_problems():
    """Test comprehensivo de todos los problemas"""
    print("=== TESTING TREE INTERVIEW PROBLEMS ===\n")
    
    # Setup
    valid_tree = create_test_tree()
    invalid_tree = create_invalid_bst()
    
    # Test 1: Validate BST
    print("1. VALIDATE BST:")
    print(f"   Valid tree (v1): {is_valid_bst_v1(valid_tree)}")
    print(f"   Valid tree (v2): {is_valid_bst_v2(valid_tree)}")
    print(f"   Valid tree (v3): {is_valid_bst_v3(valid_tree)}")
    print(f"   Invalid tree: {is_valid_bst_v2(invalid_tree)}")
    
    # Test 2: Traversals
    print("\n2. TRAVERSALS:")
    print(f"   Inorder: {binary_tree_inorder(valid_tree)}")
    print(f"   Level order: {binary_tree_level_order(valid_tree)}")
    
    # Test 3: Max Depth
    print("\n3. MAX DEPTH:")
    print(f"   Recursive: {max_depth_recursive(valid_tree)}")
    print(f"   Iterative: {max_depth_iterative(valid_tree)}")
    
    # Test 4: Same Tree
    print("\n4. SAME TREE:")
    tree_copy = create_test_tree()
    print(f"   Same tree: {is_same_tree(valid_tree, tree_copy)}")
    print(f"   Different trees: {is_same_tree(valid_tree, invalid_tree)}")
    
    # Test 5: Path Sum
    print("\n5. PATH SUM:")
    # Path: 5->3->2 = 10
    print(f"   Has path sum 10: {has_path_sum(valid_tree, 10)}")
    print(f"   Has path sum 15: {has_path_sum(valid_tree, 15)}")
    print(f"   All paths sum 10: {path_sum_all_paths(valid_tree, 10)}")
    
    # Test 6: Diameter
    print("\n6. DIAMETER:")
    print(f"   Diameter: {diameter_of_binary_tree(valid_tree)}")
    
    # Test 7: Serialize/Deserialize
    print("\n7. SERIALIZE/DESERIALIZE:")
    codec = Codec()
    serialized = codec.serialize(valid_tree)
    print(f"   Serialized: {serialized[:50]}...")
    deserialized = codec.deserialize(serialized)
    print(f"   Round-trip successful: {is_same_tree(valid_tree, deserialized)}")

# ========================
# TIPS PARA ENTREVISTAS
# ========================

"""
🎯 ESTRATEGIAS GANADORAS PARA ENTREVISTAS:

1. SIEMPRE PREGUNTA:
   - ¿Puede haber nodos duplicados?
   - ¿El árbol está balanceado?
   - ¿Qué hacer con árbol vacío?

2. PATRONES COMUNES:
   - DFS recursivo: Para la mayoría de problemas
   - BFS iterativo: Para level-order, shortest path
   - Two pointers: Para tree comparisons

3. OPTIMIZACIONES:
   - Recursivo vs Iterativo (pregunta cuál prefieren)
   - Space optimization: Morris traversal (avanzado)
   - Early termination: Stop cuando encuentres la respuesta

4. EDGE CASES CRÍTICOS:
   - Árbol vacío (root = None)
   - Árbol con un solo nodo
   - Árbol completamente desbalanceado
   - Valores negativos/duplicados

5. COMPLEJIDADES TÍPICAS:
   - Tiempo: O(n) para visitar todos los nodos
   - Espacio: O(h) para recursión, O(w) para BFS
   - h = altura, w = ancho máximo

6. BONUS POINTS:
   - Mencionar Morris Traversal (O(1) space)
   - Discutir balancing (AVL, Red-Black)
   - Hablar de aplicaciones reales (file systems, decision trees)
"""

if __name__ == "__main__":
    test_all_problems()