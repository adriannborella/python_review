import functools
import time
import functools
from collections import defaultdict
import inspect
from typing import List, Optional


def timing_decorator(func):
    """Mide tiempo de ejecución"""

    @functools.wraps(func)  # Preserva metadata de función original
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result

    return wrapper


def memoize(func):
    """Cache de resultados para optimización"""
    cache = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Crear key hashable de argumentos
        key = str(args) + str(sorted(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return wrapper


def retry(max_attempts=3, delay=1):
    """Decorador parametrizado para retry logic"""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
                    continue
            raise last_exception

        return wrapper

    return decorator


class DecoratorToolkit:
    """
    Colección de decoradores útiles para entrevistas
    """

    @staticmethod
    def validate_types(**type_hints):
        """
        Decorador que valida tipos de argumentos

        @validate_types(x=int, y=str)
        def func(x, y):
            return f"{y}: {x}"
        """

        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                for index, (variable_name, validate_class) in enumerate(
                    type_hints.items()
                ):
                    if isinstance(args[index], validate_class):
                        continue

                    raise Exception(
                        f"Variable {variable_name} must be {validate_class.__name__}"
                    )
                result = func(*args, **kwargs)
                return result

            return wrapper

        return decorator

    @staticmethod
    def rate_limit(calls_per_second=1):
        """
        Rate limiting decorator
        """

        def decorator(func):
            last_called = []  # Lista para mutabilidad en closure

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # TODO: Implementar rate limiting
                # Hint: usar time.time() y sleep si necesario
                start = time.time()

                last_called.append(start)

                if start - last_called[0] > 1:
                    last_called.clear()

                if len(last_called) > calls_per_second:
                    raise Exception(
                        f"Rate limit excedeed. Calls per second:{calls_per_second}"
                    )

                result = func(*args, **kwargs)
                return result

            return wrapper

        return decorator

    @staticmethod
    def cache_with_expiry(ttl_seconds=300):
        """
        Cache con time-to-live
        """

        def decorator(func):
            cache = {}
            timestamps = {}

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # TODO: Implementar cache con expiry
                # Hint: verificar timestamp + ttl
                key = str(args) + str(sorted(kwargs.items()))
                start = time.time()

                if key not in cache:
                    print("saving result in cache")
                    cache[key] = {"result": func(*args, **kwargs), "timestamp": start}
                else:
                    if start - cache[key]["timestamp"] > ttl_seconds:
                        # update the cache
                        print("Updating result in cache")
                        cache[key] = {
                            "result": func(*args, **kwargs),
                            "timestamp": start,
                        }

                print("Return from cache")
                return cache[key]["result"]

            return wrapper

        return decorator


# Tests para decoradores
@DecoratorToolkit.validate_types(x=int, y=str)
def test_function(x, y):
    return f"{y}: {x}"


# print(test_function(1, "test"))
# print(test_function("test", 1))


@DecoratorToolkit.rate_limit(calls_per_second=2)
def api_call():
    print("Calling API")
    return "API response"


# api_call()
# api_call()
# try:
#     api_call()
# except Exception as error:
#     print(error)
# time.sleep(1)
# api_call()


@DecoratorToolkit.cache_with_expiry(ttl_seconds=2)
def expensive_computation(n):
    # Simula cálculo costoso
    return sum(i**2 for i in range(n))


# print(expensive_computation(50))
# print(expensive_computation(20))
# time.sleep(1)
# print(expensive_computation(20))
# time.sleep(3)
# print(expensive_computation(20))


def removeDuplicates_mine_1(self, nums: List[int]) -> int:
    numbers_to_remove = []
    for index, number in enumerate(nums[1:]):
        if number == nums[index]:
            numbers_to_remove.append(number)

    for n in numbers_to_remove:
        nums.remove(n)
    return len(nums)


def removeDuplicates_best(self, nums: List[int]) -> int:
    i = 0
    for j in range(0, len(nums)):
        if nums[i] != nums[j]:
            i += 1
            nums[i] = nums[j]

    return i + 1


def removeDuplicates(self, nums: list[int]) -> int:
    if not nums:
        return 0

    # Initialize the index for the next unique element
    unique_index = 0

    # Iterate through the list starting from the second element
    for i in range(1, len(nums)):
        # If the current element is different from the last unique element
        if nums[i] != nums[unique_index]:
            unique_index += 1
            nums[unique_index] = nums[i]

    # The length of the unique elements is unique_index + 1
    return unique_index + 1


def max_profit_copilot(prices):
    """
    LeetCode #121: Best Time to Buy and Sell Stock
    Encuentra máximo profit de una transacción

    Input: prices = [7,1,5,3,6,4]
    Output: 5 (buy at 1, sell at 6)
    """
    # TODO: Implementar O(n) solution
    # Bonus: implementar usando generator expressions
    if not prices:
        return 0
    min_price = float("inf")
    max_profit = 0

    for price in prices:
        min_price = min(min_price, price)
        max_profit = max(max_profit, price - min_price)

    return max_profit


def maxProfit_mine(prices: List[int]) -> int:
    # 2
    # 2, 4
    # 2, 4, 1

    if len(prices) == 1:
        return 0

    buy_price = prices[0]
    sell_price = 0
    max_profit = 0

    for index, price in enumerate(prices[1:]):
        print(index, price, max_profit, buy_price, sell_price)
        if price > sell_price:
            new_profit = price - buy_price
            if new_profit > max_profit:
                print(f"set sell price {price}: {new_profit}")
                max_profit = new_profit
            sell_price = price

        if price < buy_price:
            new_profit = price - sell_price
            if new_profit > 0:
                print(f"set buy price, max_profit change:{max_profit}")
                max_profit = new_profit
            buy_price = price
            sell_price = 0

    print(f"Result {max_profit}")
    if max_profit < 0:
        return 0

    return max_profit


def maxProfit_opt1(self, prices: List[int]) -> int:
    min_price = float("inf")
    max_profit = 0

    for price in prices:
        if price < min_price:
            min_price = price

        elif price - min_price > max_profit:
            max_profit = price - min_price

    return max_profit


def maxProfit_best(prices: List[int]) -> int:
    max_profit = 0
    min_price = prices[0]
    for price in prices:
        max_profit = max(max_profit, price - min_price)
        min_price = min(min_price, price)
    return max_profit


# assert maxProfit_mine([7, 1, 5, 3, 6, 4]) == 5, "Test case 1 failed"
# assert maxProfit_mine([7, 6, 4, 3, 1]) == 0, "Test case 2 failed"
# assert maxProfit_mine([7]) == 0, "Test case 3 failed"
# assert maxProfit_mine([7, 2, 5, 1, 3, 6, 4]) == 5, "Test case 4 failed"
# assert maxProfit_mine([2, 4, 1]) == 2, "Test case 5 failed"
# assert maxProfit_mine([2, 4]) == 2, "Test case 6 failed"
# assert maxProfit_mine([4, 2]) == 0, "Test case 7 failed"
# assert maxProfit_mine([3, 2, 6, 5, 0, 3]) == 4, "Test case 8 failed"


def is_valid_parentheses_mine(s: str) -> bool:
    if len(s) == 1:
        return False

    def get_open_braket(bracket):
        options = {
            ")": "(",
            "]": "[",
            "}": "{",
        }
        return options[bracket]

    open_brakets = []
    for letter in s:
        if letter in {"(", "[", "{"}:
            open_brakets.append(letter)
        if letter in {")", "]", "}"}:
            if len(open_brakets) == 0 or open_brakets[-1] != get_open_braket(letter):
                return False
            open_brakets.pop()

    return len(open_brakets) == 0


def is_valid_parentheses(s):
    """
    LeetCode #20: Valid Parentheses
    Verifica si string tiene paréntesis balanceados

    Input: s = "()[]{}"
    Output: True
    """
    # TODO: Implementar usando stack (list)
    # Bonus: usar dict comprehension para mapping
    stack = []
    bracket_map = {")": "(", "]": "[", "}": "{"}

    for char in s:
        if char in bracket_map.values():
            stack.append(char)
        elif char in bracket_map.keys():
            if not stack or stack[-1] != bracket_map[char]:
                return False
            stack.pop()


def parentheses_with_generators(s):
    """
    Approach usando generators para memory efficiency
    """

    # TODO: Generator-based solution
    def generate_brackets(s):
        for char in s:
            yield char

    stack = []
    bracket_map = {")": "(", "]": "[", "}": "{"}

    for char in generate_brackets(s):
        if char in bracket_map.values():
            stack.append(char)
        elif char in bracket_map.keys():
            if not stack or stack[-1] != bracket_map[char]:
                return False
            stack.pop()

    return len(stack) == 0


# assert is_valid_parentheses_mine("()") == True, "Test case 1"
# assert is_valid_parentheses_mine("()[]{}") == True, "Test case 2"
# assert is_valid_parentheses_mine("(]") == False, "Test case 3"
# assert is_valid_parentheses_mine("([])") == True, "Test case 4"
# assert is_valid_parentheses_mine("([)]") == False, "Test case 5"
# assert is_valid_parentheses_mine("([[[[{{{]}}}]]])]") == False, "Test case 6"
# assert is_valid_parentheses_mine("){") == False, "Test case 7"


class CallCounter:
    """Decorador que cuenta llamadas a función"""

    def __init__(self, func):
        self.func = func
        self.count = 0
        functools.update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"{self.func.__name__} called {self.count} times")
        return self.func(*args, **kwargs)

    def reset_count(self):
        self.count = 0


@CallCounter
def example_function():
    return "Hello World"


# Uso
# example_function()  # example_function called 1 times
# print(example_function.count)  # 1
# example_function.reset_count()


import functools
import operator


# Partial applications
def power(base, exponent):
    return base**exponent


square = functools.partial(power, exponent=2)
cube = functools.partial(power, exponent=3)


# Reduce para operaciones complejas
def factorial(n):
    return functools.reduce(operator.mul, range(1, n + 1), 1)


def find_gcd_multiple(*numbers):
    """Encuentra GCD de múltiples números"""
    import math

    return functools.reduce(math.gcd, numbers)


# Singledispatch para overloading
@functools.singledispatch
def process_data(arg):
    """Procesa datos según tipo"""
    raise NotImplementedError(f"No implementation for {type(arg)}")


@process_data.register
def _(arg: list):
    return [x**2 for x in arg]


@process_data.register
def _(arg: dict):
    return {k: v**2 for k, v in arg.items()}


@process_data.register
def _(arg: str):
    return arg.upper()


# TODO: Test singledispatch con diferentes tipos


def is_palindrome_number_mine(x):
    """
    LeetCode #9: Palindrome Number
    Determina si entero es palíndromo sin convertir a string
    """
    # TODO: Implementar sin string conversion
    # Bonus: implementar también con string + comprehension
    if x < 0:
        return False
    aux = str(x)
    return aux == aux[::-1]


# assert is_palindrome_number_mine(121) == True
# assert is_palindrome_number_mine(-121) == False
# assert is_palindrome_number_mine(10) == False


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def merge_two_lists_mine(list1: Optional[ListNode], list2: Optional[ListNode]):
    """
    LeetCode #21: Merge Two Sorted Lists
    """
    # TODO: Implementar merge eficiente
    min_value = min(next1.val, next2.val)
    if next1.val == min_value:
        next_node = next1
        next1 = next1.next
    else:
        next_node = next2
        next2 = next2.next
    result = next_node
    current_node = result
    while next_node:
        print(f"Next 1: {next1}")
        print(f"Next 2: {next2}")

        if next1 and (not next2 or next1.val < next2.val):
            next_node = next1
            next1 = next1.next
        elif not next1 and not next2:
            next_node = False
        else:
            next_node = next2
            next2 = next2.next

        if next_node:
            current_node.next = next_node
            current_node = next_node
        print(f"Result: {result}")
    return result


# assert merge_two_lists_mine([1, 2, 4], [1, 3, 4]) == [1, 1, 2, 3, 4, 4], "Test case 1"


def remove_element_mine(nums: List[int], val: int) -> int:
    """
    LeetCode #27: Remove Element
    Remueve todas las instancias de val in-place
    """
    # TODO: Two-pointer technique
    # Bonus: implementar usando comprehensions y comparar
    next_position = 0
    count = 0
    for index in range(len(nums)):
        number = nums[index]
        if number != val:
            nums[next_position] = number
            next_position += 1
            count += 1

    print(nums[:count])
    return count


# assert remove_element_mine([3, 2, 2, 3], 3) == 2, "Test case 1"
# assert remove_element_mine([0, 1, 2, 2, 3, 0, 4, 2], 2) == 3, "Test case 2"


def single_number_mine(nums: List[int]) -> int:
    """
    LeetCode #136: Single Number
    Encuentra el número que aparece una sola vez
    TODO: Usar set operations elegantemente
    """
    aux = set()
    for number in nums:
        if number in aux:
            aux.remove(number)
        else:
            aux.add(number)

    return aux.pop()


# This problem is simple, so there are many possible solutions. However, we must solve it in O(n) time and O(1) space. Given these constraints, we cannot use data structures such as arrays, hashmaps, or sets. Without these data structures, it's impossible to keep track of multiple numbers that appear twice. In fact, I believe this is a problem that can be solved if you know the trick, but is very difficult if you don’t. The key to the solution is using XOR. Below, I will explain the four properties of XOR one by one.


# What is XOR?
# XOR (eXclusive OR) is a binary operation that compares two bits and outputs a result based on the following rules:
def singleNumber_best(self, nums: List[int]) -> int:
    res = 0
    for n in nums:
        res ^= n
    return res


# assert single_number_mine([2, 2, 1]) == 1, "test case 1"
# assert single_number_mine([4, 1, 2, 1, 2]) == 4, "test case 2"
# assert single_number_mine([3]) == 3, "test case 3"


def intersection_of_arrays(nums1, nums2):
    """
    LeetCode #349: Intersection of Two Arrays
    TODO: Múltiples approaches con set comprehensions
    """
    result = set(nums1).intersection(set(nums2))
    return list(result)


# assert intersection_of_arrays([1, 2, 2, 1], [2, 2]) == [2]

from collections import Counter


def first_unique_character_mine(s):
    """
    LeetCode #387: First Unique Character
    TODO: Dict comprehension + enumerate
    """
    # letters = {}
    # unique_letters = []
    # for index, letter in enumerate(s):
    #     # print(letters, unique_letters)
    #     if letter not in letters:
    #         unique_letters.append(letter)
    #         letters[letter] = index
    #     else:
    #         if letter in unique_letters:
    #             unique_letters.remove(letter)
    # result = -1
    # if len(unique_letters) > 0 and unique_letters[0] in letters:
    #     result = letters[unique_letters[0]]
    # return result
    letters = list(s)
    letters_counter = Counter(s)
    for letter, count in letters_counter.items():
        if count == 1:
            return letters.index(letter)
    return -1


def first_unique_character_other(s):
    # Step 1: Efficiently count all character occurrences in O(n) time.
    # For s = "loveleetcode", counts becomes:
    # Counter({'l': 2, 'o': 2, 'v': 1, 'e': 4, 't': 1, 'c': 1, 'd': 1})
    counts = Counter(s)

    # Step 2: Iterate through the string again to find the first unique one.
    for index, char in enumerate(s):
        # Check the frequency map for the character's count.
        if counts[char] == 1:
            return index

    # If the loop completes, no unique character was found.
    return -1


# assert first_unique_character_mine("leetcode") == 0, "test case 1"
# assert first_unique_character_mine("loveleetcode") == 2, "test case 2"
# assert first_unique_character_mine("aabb") == -1, "test case 3"
# assert first_unique_character_mine("lfeeltcode") == 1, "test case 4"


def reverse_string_mine(s):
    """
    LeetCode #344: Reverse String (in-place)
    TODO: Usar slicing y comprehensions
    """
    s.reverse()
    # to = len(s) // 2
    # for index in range(to):
    #     aux = s[index]
    #     change_index = -(index + 1)
    #     s[index] = s[change_index]
    #     s[change_index] = aux
    # print(f"Result. {s}")
    return s


assert reverse_string_mine(["h", "e", "l", "l", "o"]) == [
    "o",
    "l",
    "l",
    "e",
    "h",
], "test case 1"

assert reverse_string_mine(
    [
        "A",
        " ",
        "m",
        "a",
        "n",
        ",",
        " ",
        "a",
        " ",
        "p",
        "l",
        "a",
        "n",
        ",",
        " ",
        "a",
        " ",
        "c",
        "a",
        "n",
        "a",
        "l",
        ":",
        " ",
        "P",
        "a",
        "n",
        "a",
        "m",
        "a",
    ]
) == [
    "a",
    "m",
    "a",
    "n",
    "a",
    "P",
    " ",
    ":",
    "l",
    "a",
    "n",
    "a",
    "c",
    " ",
    "a",
    " ",
    ",",
    "n",
    "a",
    "l",
    "p",
    " ",
    "a",
    " ",
    ",",
    "n",
    "a",
    "m",
    " ",
    "A",
], "test case 2"


def addTwoNumbers_mine(
    self, l1: Optional[ListNode], l2: Optional[ListNode]
) -> Optional[ListNode]:
    def number_from_node(node: ListNode):
        result = []
        while node:
            result.append(str(node.val))
            node = node.next

        result.reverse()
        return int("".join(result))

    number1 = number_from_node(l1)
    number2 = number_from_node(l2)

    summ = number1 + number2
    iterator_list = list(str(summ))
    iterator_list.reverse()
    iterator_list = [int(n) for n in iterator_list]
    result = last_node = ListNode(val=iterator_list[0])

    for number in iterator_list[1:]:
        next_node = ListNode(val=number)
        last_node.next = next_node
        last_node = next_node

    return result
