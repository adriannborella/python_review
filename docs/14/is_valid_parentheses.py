def is_valid_parentheses(s):
    """
    Pregunta inicial: Verificar paréntesis balanceados básicos.
    Extensiones típicas en entrevista:
    1. Múltiples tipos de brackets
    2. Nested structures
    3. Minimum additions to make valid
    """

    # Mapeo de brackets
    bracket_map = {")": "(", "}": "{", "]": "["}
    stack = []

    for char in s:
        if char in bracket_map:  # Closing bracket
            if not stack or stack.pop() != bracket_map[char]:
                return False
        else:  # Opening bracket
            stack.append(char)

    return len(stack) == 0


def min_additions_to_make_valid(s):
    """
    Extensión: Mínimas adiciones para hacer válido.
    """
    open_needed = 0  # ')' que necesitan '('
    close_needed = 0  # '(' que necesitan ')'

    for char in s:
        if char == "(":
            close_needed += 1
        elif char == ")":
            if close_needed > 0:
                close_needed -= 1
            else:
                open_needed += 1

    return open_needed + close_needed


# Tests
test_cases = ["()", "()[]{}", "(]", "([)]", "{[]}"]
for case in test_cases:
    valid = is_valid_parentheses(case)
    additions = min_additions_to_make_valid(case)
    print(f"'{case}': Valid={valid}, Min additions={additions}")
