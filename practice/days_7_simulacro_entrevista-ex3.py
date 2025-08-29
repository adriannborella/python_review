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
# PROBLEMA 3: ALGORITMO STRING MANIPULATION (15 minutos)
# Encuentra el substring más largo sin caracteres repetidos
# =============================================================================


def longest_unique_substring(s):
    """
    Encuentra la longitud del substring más largo sin caracteres repetidos.

    Ejemplo:
    "abcabcbb" -> 3 ("abc")
    "bbbbb" -> 1 ("b")
    "pwwkew" -> 3 ("wke")

    Preguntas del entrevistador:
    1. ¿Qué enfoque usarías? (Sliding window)
    2. ¿Cómo trackeas caracteres únicos?
    3. ¿Cuál es la complejidad temporal?

    TODO: Implementa usando sliding window technique
    """
    if len(s) <= 1:
        return 0, s

    result = aux_word = ""
    seen = set()

    for character in s:
        if character not in seen:
            aux_word += character
            seen.add(character)
        else:
            if len(result) < len(aux_word):
                result = aux_word
            seen.clear()

            seen.add(character)
            aux_word = character

    if len(result) < len(aux_word):
        result = aux_word
    # print(f"result: {result}")
    return len(result), result

    if not s:
        return 0

    # Sliding window approach
    char_index = {}  # Mapeo char -> último índice visto
    left = 0
    max_length = 0

    for right in range(len(s)):
        char = s[right]

        # Si el caracter ya existe en la ventana actual
        if char in char_index and char_index[char] >= left:
            # Mover left pointer después de la última ocurrencia
            left = char_index[char] + 1

        # Actualizar el índice del caracter
        char_index[char] = right

        # Calcular longitud actual y actualizar máximo
        current_length = right - left + 1
        max_length = max(max_length, current_length)

    return max_length


assert longest_unique_substring("abcabcbb") == (3, "abc")
assert longest_unique_substring("bbbbb") == (1, "b")
assert longest_unique_substring("pwwkew") == (3, "wke")
assert longest_unique_substring("abcdef") == (6, "abcdef")


def longest_unique_substring_with_details(s):
    """
    Versión que también retorna el substring
    """
    if not s:
        return 0, ""

    char_index = {}
    left = 0
    max_length = 0
    result_start = 0

    for right in range(len(s)):
        char = s[right]

        if char in char_index and char_index[char] >= left:
            left = char_index[char] + 1

        char_index[char] = right

        current_length = right - left + 1
        if current_length > max_length:
            max_length = current_length
            result_start = left

    return max_length, s[result_start : result_start + max_length]


# Test cases
test_strings = ["abcabcbb", "bbbbb", "pwwkew", "", "abcdef", "aab"]

print("\nPROBLEMA 3: LONGEST UNIQUE SUBSTRING")
print("-" * 50)
for s in test_strings:
    length, substring = longest_unique_substring(s)
    print(f"'{s}' -> Length: {length}, Substring: '{substring}'")
