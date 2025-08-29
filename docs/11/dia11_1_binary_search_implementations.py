"""
BINARY SEARCH - Implementaciones para Entrevistas
Complejidad: O(log n) tiempo, O(1) espacio (iterativo)
"""

def binary_search_iterative(arr, target):
    """
    Implementación iterativa clásica - MÁS RECOMENDADA EN ENTREVISTAS
    Menos propensa a errores de stack overflow
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        # Evita overflow: mid = (left + right) // 2 puede fallar con números grandes
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

def binary_search_recursive(arr, target, left=0, right=None):
    """
    Implementación recursiva - Para demostrar comprensión completa
    """
    if right is None:
        right = len(arr) - 1
    
    if left > right:
        return -1
    
    mid = left + (right - left) // 2
    
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)

def binary_search_leftmost(arr, target):
    """
    Encuentra el índice más a la izquierda del target
    Útil para: find first occurrence, insert position
    """
    left, right = 0, len(arr)
    
    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid
    
    return left

def binary_search_rightmost(arr, target):
    """
    Encuentra el índice más a la derecha del target
    Útil para: find last occurrence
    """
    left, right = 0, len(arr)
    
    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] <= target:
            left = mid + 1
        else:
            right = mid
    
    return left - 1

# CASOS DE PRUEBA - Siempre incluir en entrevistas
def test_binary_search():
    """
    Testing comprehensivo - demuestra thinking como senior
    """
    # Caso normal
    arr = [1, 3, 5, 7, 9, 11, 13]
    assert binary_search_iterative(arr, 7) == 3
    assert binary_search_recursive(arr, 7) == 3
    
    # Target no existe
    assert binary_search_iterative(arr, 6) == -1
    
    # Edge cases
    assert binary_search_iterative([], 5) == -1  # Array vacío
    assert binary_search_iterative([5], 5) == 0  # Un elemento
    assert binary_search_iterative([1, 2], 1) == 0  # Primer elemento
    assert binary_search_iterative([1, 2], 2) == 1  # Último elemento
    
    # Con duplicados
    arr_dup = [1, 2, 2, 2, 3, 4, 5]
    assert binary_search_leftmost(arr_dup, 2) == 1  # Primera ocurrencia
    assert binary_search_rightmost(arr_dup, 2) == 3  # Última ocurrencia
    
    print("✅ Todos los tests de Binary Search pasaron")

if __name__ == "__main__":
    test_binary_search()
