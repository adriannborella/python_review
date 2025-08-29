import timeit
import sys

def compare_memory():
    """
    Compara el uso de memoria entre listas, tuplas y conjuntos.
    """

    # Comparación de memoria
    lista = [1, 2, 3, 4, 5]
    tupla = (1, 2, 3, 4, 5)
    conjunto = {1, 2, 3, 4, 5}

    print(f"Lista: {sys.getsizeof(lista)} bytes")
    print(f"Tupla: {sys.getsizeof(tupla)} bytes")
    print(f"Set: {sys.getsizeof(conjunto)} bytes")

def timing_comparisons():
    """
    Compara el tiempo de ejecución de operaciones comunes en listas y conjuntos.
    """

    # Operaciones en lista
    lista_timing = timeit.timeit('1000 in lista', 
                                 setup='lista = list(range(10000))', 
                                 number=1000)
    
    # Operaciones en conjunto
    set_timing = timeit.timeit('1000 in conjunto', 
                               setup='conjunto = set(range(10000))', 
                               number=1000)

    print(f"Tiempo de búsqueda en lista: {lista_timing} segundos")
    print(f"Tiempo de búsqueda en conjunto: {set_timing} segundos")

def find_common_elements(*lists):
    """
    Encuentra elementos comunes en múltiples listas
    Input: find_common_elements([1,2,3], [2,3,4], [3,4,5])
    Output: [3]
    """
    
    common_elements = set(lists[0])
    for lst in lists[1:]:
        common_elements.intersection_update(lst)
    
    print(f"Elementos comunes: {list(common_elements)}")
    return list(common_elements)

def remove_duplicates_preserve_order(items):
    """
    Remueve duplicados manteniendo orden original
    Input: [1,2,2,3,1,4]
    Output: [1,2,3,4]
    """
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

if __name__ == "__main__":
    compare_memory()
    timing_comparisons()

    find_common_elements([1,2,3], [2,3,4], [3,4,5])

    items = [5, 1, 4, 2, 2, 1, 3, 1, 4]
    unique_items = remove_duplicates_preserve_order(items)
    print(f"Elementos únicos preservando orden: {unique_items}")
    print(f"Elementos únicos: {set(items)}")