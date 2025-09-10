# RECORRIDOS DE ÁRBOLES BINARIOS - CONCEPTOS FUNDAMENTALES

"""
Los tres recorridos fundamentales que DEBES dominar para entrevistas:

1. INORDER (Izquierda -> Raíz -> Derecha)
   - En BST: produce elementos en orden ASCENDENTE
   - Uso: Obtener elementos ordenados, validar BST
   - Complejidad: O(n) tiempo, O(h) espacio (h = altura)

2. PREORDER (Raíz -> Izquierda -> Derecha) 
   - Procesa raíz ANTES que los hijos
   - Uso: Copiar/serializar árbol, obtener path desde raíz
   - Complejidad: O(n) tiempo, O(h) espacio

3. POSTORDER (Izquierda -> Derecha -> Raíz)
   - Procesa raíz DESPUÉS que los hijos
   - Uso: Eliminar nodos, calcular tamaño, liberar memoria
   - Complejidad: O(n) tiempo, O(h) espacio

EJEMPLO VISUAL:
        5
       / \
      3   8
     / \   \
    2   4   9

INORDER:   [2, 3, 4, 5, 8, 9] ← ¡Ordenado!
PREORDER:  [5, 3, 2, 4, 8, 9] ← Raíz primero
POSTORDER: [2, 4, 3, 9, 8, 5] ← Raíz último
"""


class TreeNode:
    """Definición estándar de nodo para árboles binarios"""

    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return f"TreeNode({self.val})"


# IMPLEMENTACIONES RECURSIVAS (Las más elegantes para entrevistas)


def inorder_recursive(root: TreeNode):
    """
    Recorrido inorder recursivo
    Patrón: left -> process -> right
    """
    result = []

    def inorder_helper(node):
        if not node:
            return

        inorder_helper(node.left)  # Procesar izquierda
        result.append(node.val)  # Procesar raíz
        inorder_helper(node.right)  # Procesar derecha

    inorder_helper(root)
    return result


def preorder_recursive(root):
    """
    Recorrido preorder recursivo
    Patrón: process -> left -> right
    """
    result = []

    def preorder_helper(node):
        if not node:
            return

        result.append(node.val)  # Procesar raíz PRIMERO
        preorder_helper(node.left)  # Procesar izquierda
        preorder_helper(node.right)  # Procesar derecha

    preorder_helper(root)
    return result


def postorder_recursive(root):
    """
    Recorrido postorder recursivo
    Patrón: left -> right -> process
    """
    result = []

    def postorder_helper(node):
        if not node:
            return

        postorder_helper(node.left)  # Procesar izquierda
        postorder_helper(node.right)  # Procesar derecha
        result.append(node.val)  # Procesar raíz ÚLTIMO

    postorder_helper(root)
    return result


# IMPLEMENTACIONES ITERATIVAS (Impresionan en entrevistas)


def inorder_iterative(root):
    """Inorder iterativo usando stack"""
    if not root:
        return []

    result = []
    stack = []
    current = root

    while stack or current:
        # Ir hasta el nodo más a la izquierda
        while current:
            stack.append(current)
            current = current.left

        # Procesar el nodo
        current = stack.pop()
        result.append(current.val)

        # Moverse al subtree derecho
        current = current.right

    return result


def preorder_iterative(root):
    """Preorder iterativo usando stack"""
    if not root:
        return []

    result = []
    stack = [root]

    while stack:
        node = stack.pop()
        result.append(node.val)

        # Importante: Right primero, luego left (por el LIFO del stack)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    return result


def postorder_iterative(root):
    """Postorder iterativo - el más complejo"""
    if not root:
        return []

    result = []
    stack = []
    last_visited = None
    current = root

    while stack or current:
        if current:
            stack.append(current)
            current = current.left
        else:
            peek_node = stack[-1]
            # Si right child existe y no ha sido procesado
            if peek_node.right and last_visited != peek_node.right:
                current = peek_node.right
            else:
                result.append(peek_node.val)
                last_visited = stack.pop()

    return result


# FUNCIÓN DE TESTING
def test_traversals():
    """Test con el ejemplo del árbol"""
    #        5
    #       / \
    #      3   8
    #     / \   \
    #    2   4   9

    root = TreeNode(5)
    root.left = TreeNode(3)
    root.right = TreeNode(8)
    root.left.left = TreeNode(2)
    root.left.right = TreeNode(4)
    root.right.right = TreeNode(9)

    print("=== RESULTADOS ESPERADOS ===")
    print("INORDER:  [2, 3, 4, 5, 8, 9]")
    print("PREORDER: [5, 3, 2, 4, 8, 9]")
    print("POSTORDER:[2, 4, 3, 9, 8, 5]")

    print("\n=== RECURSIVOS ===")
    print(f"INORDER:   {inorder_recursive(root)}")
    print(f"PREORDER:  {preorder_recursive(root)}")
    print(f"POSTORDER: {postorder_recursive(root)}")

    print("\n=== ITERATIVOS ===")
    print(f"INORDER:   {inorder_iterative(root)}")
    print(f"PREORDER:  {preorder_iterative(root)}")
    print(f"POSTORDER: {postorder_iterative(root)}")


if __name__ == "__main__":
    test_traversals()
