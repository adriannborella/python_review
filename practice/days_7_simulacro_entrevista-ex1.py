"""
SIMULACRO DE ENTREVISTA TÉCNICA - DÍA 7
Duración: 45 minutos
Formato: Live coding session

INSTRUCCIONES:
- Piensa en voz alta mientras programas
- Pregunta por clarificaciones cuando sea necesario
- Optimiza gradualmente (primera versión que funcione, luego optimizar)
- Considera edge cases
"""

# =============================================================================
# PROBLEMA 1: MERGE INTERVALS (15 minutos)
# Nivel: Medio - Muy común en entrevistas
# =============================================================================


def merge_intervals(intervals):
    """
    Dada una lista de intervalos, merge todos los intervalos superpuestos.

    Ejemplo:
    Input: [[1,3],[2,6],[8,10],[15,18]]
    Output: [[1,6],[8,10],[15,18]]

    Input: [[1,4],[4,5]]
    Output: [[1,5]]

    Pasos del entrevistador:
    1. ¿Cómo abordarías este problema?
    2. ¿Cuál sería la complejidad temporal?
    3. ¿Qué edge cases consideras?

    TODO: Implementa la solución
    Tiempo límite: 15 minutos
    """

    result = []

    if len(intervals) <= 1:
        return result

    intervals.sort(key=lambda x: x[0])

    result.append(intervals[0])

    for current in intervals[1:]:
        last_merged = result[-1]
        if current[0] <= last_merged[1]:
            result[-1] = [last_merged[0], max(last_merged[1], current[1])]
        else:
            result.append(current)
    return result

    # Tu solución aquí
    if not intervals:
        return []

    # Paso 1: Ordenar por inicio de intervalo
    intervals.sort(key=lambda x: x[0])

    # Paso 2: Merge intervalos superpuestos
    merged = [intervals[0]]

    for current in intervals[1:]:
        last_merged = merged[-1]

        # Si hay superposición, hacer merge
        if current[0] <= last_merged[1]:
            merged[-1] = [last_merged[0], max(last_merged[1], current[1])]
        else:
            # No hay superposición, agregar nuevo intervalo
            merged.append(current)

    return merged


assert merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]) == [
    [1, 6],
    [8, 10],
    [15, 18],
], "Test case 1"
assert merge_intervals([[1, 4], [2, 3]]) == [[1, 4]], "Test case 2"


# Test cases
test_cases_intervals = [
    [[1, 3], [2, 6], [8, 10], [15, 18]],
    [[1, 4], [4, 5]],
    [[1, 4], [2, 3]],
    [],
    [[1, 1], [2, 2], [3, 3]],
]

print("PROBLEMA 1: MERGE INTERVALS")
print("-" * 40)
for i, case in enumerate(test_cases_intervals):
    result = merge_intervals(case)
    print(f"Test {i+1}: {case} -> {result}")
