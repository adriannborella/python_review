def merge_k_sorted_arrays(arrays):
    """
    Fusiona K arrays ordenados en un solo array ordenado.

    Análisis de complejidad:
    - Tiempo: O(N log K) donde N = total elementos, K = número de arrays
    - Espacio: O(N) para el resultado + O(K) para el heap
    """
    import heapq

    # Heap que almacena (valor, array_index, element_index)
    min_heap = []

    # Inicializar heap con primer elemento de cada array
    for i, arr in enumerate(arrays):
        if arr:  # Solo si el array no está vacío
            heapq.heappush(min_heap, (arr[0], i, 0))

    result = []

    while min_heap:
        val, arr_idx, elem_idx = heapq.heappop(min_heap)
        result.append(val)

        # Si hay más elementos en este array, agregamos el siguiente
        if elem_idx + 1 < len(arrays[arr_idx]):
            next_val = arrays[arr_idx][elem_idx + 1]
            heapq.heappush(min_heap, (next_val, arr_idx, elem_idx + 1))

    return result


# Test
arrays = [[1, 4, 5], [1, 3, 4], [2, 6]]
print(f"Merged: {merge_k_sorted_arrays(arrays)}")
# Output: [1, 1, 2, 3, 4, 4, 5, 6]
