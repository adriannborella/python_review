import time
import random
from typing import List, Dict, Optional

# =============================================================================
# EXERCISE 1: ANÁLISIS DE ALGORITMOS DE BÚSQUEDA (10 minutos)
# =============================================================================


def linear_search_analysis(arr: List[int], target: int) -> tuple:
    """
    Implementa búsqueda lineal y analiza su complejidad

    TODO:
    1. Implementa el algoritmo
    2. Analiza caso mejor, promedio y peor
    3. Determine complejidad espacial

    Return: (index, comparisons_made)
    """
    comparisons = 0

    for i in range(len(arr)):
        comparisons += 1
        if arr[i] == target:
            return i, comparisons  # Mejor caso: O(1)

    return -1, comparisons  # Peor caso: O(n)

    # ANÁLISIS:
    # Temporal: Mejor O(1), Promedio O(n/2), Peor O(n) → O(n)
    # Espacial: O(1) - solo variables auxiliares
