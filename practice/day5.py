def climbing_stairs_with_validation(n: int) -> int:
    """
    LeetCode #70: Climbingtairs
    Con input validation y overflow protection
    """
    # 4
    # 1. 1 + 1 + 1 + 1
    # 2. 2 + 2
    # 3. 1 + 1 + 2
    # 4. 1 + 2 + 1
    # 5. 2 + 1 + 1

    # 5
    # 1. 1 + 1 + 1 + 1 + 1
    # 2. 1 + 1 + 1 + 2
    # 3. 1 + 1 + 2 + 1
    # 4. 1 + 2 + 1 + 1
    # 5. 2 + 1 + 1 + 1
    # 6. 2 + 2 + 1
    # 7. 1 + 2 + 2
    # 8. 2 + 1 + 2

    # 6
    # 1. 1 + 1 + 1 + 1 + 1 + 1 *
    # 2. 1 + 1 + 1 + 1 + 2
    # 3. 1 + 1 + 1 + 2 + 1
    # 4. 1 + 1 + 2 + 1 + 1
    # 5. 1 + 2 + 1 + 1 + 1
    # 6. 2 + 1 + 1 + 1 + 1
    # 7. 1 + 1 + 2 + 2 Aca tuve el error al no considerar el 2 en todas las posiciones
    # 8. 1 + 2 + 2 + 1
    # 9. 2 + 2 + 1 + 1
    # 10. 2 + 1 + 1 + 1
    # 11. 2 + 2 + 2 *
    # 12. 2 + 2 + 2
    # 13. 2 + 2 + 2

    # Siempre puede hacer una opcion por todos 1
    if n <= 3:
        return n

    result = 1

    to = (n // 2) + 1
    result += sum(range(to, n))
    if n % 2 == 0:
        result += 1
    print(f"Result: {result}")
    return result


from contextlib import contextmanager
from functools import lru_cache
from typing import List


class Solution:
    def climbStairs(self, n: int) -> int:
        @lru_cache(maxsize=None)
        def ways(t: int) -> int:
            if t <= 1:
                return 1
            return ways(t - 1) + ways(t - 2)

        return ways(n)


# assert climbing_stairs_with_validation(1) == 1, "Test case 0"
# assert climbing_stairs_with_validation(2) == 2, "Test case 1"
# assert climbing_stairs_with_validation(3) == 3, "Test case 2"
# assert climbing_stairs_with_validation(4) == 5, "Test case 3"
# assert climbing_stairs_with_validation(5) == 8, "Test case 4"
# assert climbing_stairs_with_validation(6) == 13, "Test case 5"
# assert climbing_stairs_with_validation(8) == 34, "Test case 5"
# assert climbing_stairs_with_validation(10) == 89, "Test case 5"
# assert Solution().climbStairs(6) == 13, "Test case 5"


def function_signature_mastery():
    """
    Demuestra todos los patrones de argumentos
    """

    def complex_function(
        req_arg,
        req_arg2,
        opt_arg="default",
        *args,
        kw_only_arg,
        kw_only_opt="default",
        **kwargs,
    ):
        """
        Función que demuestra todos los tipos de argumentos
        """
        return {
            "required": [req_arg, req_arg2],
            "optional": opt_arg,
            "varargs": args,
            "keyword_only": kw_only_arg,
            "keyword_optional": kw_only_opt,
            "extra_kwargs": kwargs,
        }

    print(complex_function(1, 2, 3, 4, 5, kw_only_arg=6, kw_only_opt=7, extra_arg=8))
    print(complex_function(1, 2, 3, 4, 5, kw_only_arg=6, extra_arg=8))
    print(complex_function(1, 2, 3, 4, 5, 6, 7, 8))
    print(complex_function(1, 2, 3, 4, 5, 6, 7, 8, kw_only_arg=9))
    print(complex_function(1, 2, 3, 4, 5, 6, 7, 8, kw_only_arg=9, extra_arg=10))


def str_str_robust_mine(haystack, needle):
    """
    LeetCode #28: Implement strStr()
    Encuentra primera ocurrencia de needle en haystack
    Con robust input validation
    """
    try:
        # TODO: Input validation
        if not isinstance(haystack, str) or not isinstance(needle, str):
            raise TypeError("Both arguments must be strings")

        if not needle:  # Empty needle
            return 0

        # TODO: Implementar búsqueda eficiente
        # Bonus: implementar KMP algorithm approach
        aux = [letter for letter in needle]
        comparations = []
        result = -1
        for index, letter in enumerate(haystack):
            if aux[0] == letter:
                # Start a new comparation
                comparations.append(0)

            for index_c, comparation in enumerate(comparations):
                if comparation == -1:
                    continue
                if aux[comparation] == letter:
                    comparations[index_c] += 1
                else:
                    comparations[index_c] = -1

                if comparations[index_c] == len(aux):
                    result = index - len(aux) + 1
                    print(f"Result: {result}")
                    return result

        print(f"Result: {result}")
        return result

    except TypeError as e:
        print(f"Type error: {e}")
        return -1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return -1


def strStr_best(self, haystack: str, needle: str) -> int:
    for index in range(len(haystack) - len(needle) + 1):
        if haystack[index : index + len(needle)] == needle:
            return index
    return -1


# assert str_str_robust_mine("sadbutsad", "sad") == 0, "Test case 1"
# assert str_str_robust_mine("leetcode", "leeto") == -1, "Test case 2"
# assert str_str_robust_mine("a", "a") == 0, "Test case 3"
# assert str_str_robust_mine("mississippi", "issip") == 4, "Test case 4"


def str_str_robust(haystack, needle):
    """
    LeetCode #28: Implement strStr()
    Encuentra primera ocurrencia de needle en haystack
    Con robust input validation
    """
    try:
        # TODO: Input validation
        if not isinstance(haystack, str) or not isinstance(needle, str):
            raise TypeError("Both arguments must be strings")

        if not needle:  # Empty needle
            return 0

        # KMP Algorithm Implementation
        def build_lps_array(pattern):
            """
            Build Longest Proper Prefix which is also Suffix array
            For pattern "issip":
            i s s i p
            0 0 0 1 0
            """
            lps = [0] * len(pattern)
            length = 0  # Length of previous longest prefix suffix
            i = 1

            while i < len(pattern):
                if pattern[i] == pattern[length]:
                    length += 1
                    lps[i] = length
                    i += 1
                else:
                    if length != 0:
                        length = lps[length - 1]
                    else:
                        lps[i] = 0
                        i += 1
            return lps

        # Build LPS array for needle
        lps = build_lps_array(needle)

        # KMP search
        i = 0  # Index for haystack
        j = 0  # Index for needle

        while i < len(haystack):
            if haystack[i] == needle[j]:
                i += 1
                j += 1

            if j == len(needle):
                return i - j  # Found pattern at index i-j
            elif i < len(haystack) and haystack[i] != needle[j]:
                if j != 0:
                    j = lps[j - 1]  # Use LPS to skip characters
                else:
                    i += 1

        return -1  # Pattern not found

    except TypeError as e:
        print(f"Type error: {e}")
        return -1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return -1


# Test the KMP implementation
# print("Testing KMP implementation:")
# print(
#     f'str_str_robust("mississippi", "issip") = {str_str_robust("mississippi", "issip")}'
# )
# print(f'str_str_robust("sadbutsad", "sad") = {str_str_robust("sadbutsad", "sad")}')
# print(f'str_str_robust("leetcode", "leeto") = {str_str_robust("leetcode", "leeto")}')
# print(f'str_str_robust("a", "a") = {str_str_robust("a", "a")}')
@contextmanager
def array_processing_session(max_memory_mb=100):
    """Context manager que monitorea memory usage"""
    import psutil

    process = psutil.Process()
    initial_memory = process.memory_info().rss / 1024 / 1024

    try:
        yield
    finally:
        final_memory = process.memory_info().rss / 1024 / 1024
        memory_used = final_memory - initial_memory
        print(f"Memory used: {memory_used:.2f} MB")

        if memory_used > max_memory_mb:
            print(f"Warning: Memory usage exceeded {max_memory_mb} MB")


def plus_one_robust_mine(digits: list):
    """
    LeetCode #66: Plus One
    Con overflow detection y memory management
    """
    try:
        # TODO: Implementar con validation
        if not digits or not all(isinstance(d, int) and 0 <= d <= 9 for d in digits):
            raise ValueError("Invalid digit array")

        # TODO: Implementar algoritmo usando comprehensions
        # Handle carry propagation elegantemente
        carry = 1

        for index in range(1, len(digits) + 1):
            update_index = -index
            new_value = digits[update_index] + carry
            if new_value > 9:
                digits[update_index] = 0
                carry = 1
            else:
                digits[update_index] = new_value
                carry = 0

            if carry == 0:
                break

        if carry != 0:
            digits.insert(0, carry)
        print(f"Result: {digits}")
        return digits

    except ValueError as e:
        print(f"Validation error: {e}")
        return []
    except MemoryError:
        print("Result too large for memory")
        return []


# with array_processing_session(120):
#     assert plus_one_robust_mine([1, 2, 3]) == [1, 2, 4], "Test case 1"
# assert plus_one_robust_mine([4, 3, 2, 1]) == [4, 3, 2, 2], "Test case 2"
# assert plus_one_robust_mine([9]) == [1, 0], "Test case 3"
# assert plus_one_robust_mine([9, 9, 9, 9, 9]) == [1, 0, 0, 0, 0, 0], "Test case 4"
# assert plus_one_robust_mine([8, 9, 9, 9]) == [9, 0, 0, 0], "Test case 5"


class Solution:
    def longestCommonPrefix_mine(self, strs: List[str]) -> str:
        result = ""
        index = 0
        # check empty strings
        first_str = strs[0]
        for index in range(len(first_str)):
            compare_letter = first_str[index]
            for arr in strs:
                if index >= len(arr):
                    return result

                if arr[index] != compare_letter:
                    return result

            result += compare_letter
            print(f"Result: {result}")

        return result

    def romanToInt(self, s: str) -> int:
        letters_values = {
            "I": 1,
            "IV": 4,
            "V": 5,
            "IX": 9,
            "X": 10,
            "XL": 40,
            "L": 50,
            "XC": 90,
            "C": 100,
            "CD": 400,
            "D": 500,
            "CM": 900,
            "M": 1000,
        }
        result = 0
        # IV = 4 IX = 9 | XL = 50 XC = 90 | CD = 400 CM = 900
        # III = 3
        # LVIII = 58
        # MCMXCIV = 1994
        if len(s) == 1:
            return letters_values[s]
        arr = [letter for letter in s]
        aux = arr[0]
        for index in range(1, len(s)):
            symbol = aux + arr[index]
            if symbol in ["I", "X", "C"]:
                aux = symbol
                continue

            if symbol in letters_values:
                result += letters_values[symbol]
                aux = ""
            else:
                result += letters_values[aux]
                aux = arr[index]
        if aux:
            result += letters_values[aux]
        print(f"Result: {result}")
        return result

    def romanToInt_best(self, s: str) -> int:
        translations = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
        number = 0
        s = s.replace("IV", "IIII").replace("IX", "VIIII")
        s = s.replace("XL", "XXXX").replace("XC", "LXXXX")
        s = s.replace("CD", "CCCC").replace("CM", "DCCCC")
        for char in s:
            number += translations[char]
        return number


assert Solution().romanToInt("II") == 2, "Test case 1"
assert Solution().romanToInt("I") == 1, "Test case 2"
assert Solution().romanToInt("IV") == 4, "Test case 3"
assert Solution().romanToInt("LVIII") == 58, "Test case 4"
assert Solution().romanToInt("MCMXCIV") == 1994, "Test case 5"


# assert (
#     Solution().longestCommonPrefix_mine(["flower", "flow", "flight"]) == "fl"
# ), "Test case 1"
# assert (
#     Solution().longestCommonPrefix_mine(["dog", "racecar", "car"]) == ""
# ), "Test case 2"
# assert Solution().longestCommonPrefix_mine(["dog", "", "car"]) == "", "Test case 3"
# assert (
#     Solution().longestCommonPrefix_mine(["dog", "dogoo", "dogwww"]) == "dog"
# ), "Test case 4"
# assert (
#     Solution().longestCommonPrefix_mine(["dogsss", "dog", "dogww"]) == "dog"
# ), "Test case 5"
# assert (
#     Solution().longestCommonPrefix_mine(["dogsss", "dogwww", "dog"]) == "dog"
# ), "Test case 6"
