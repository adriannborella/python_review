from typing import List
from utils import track_time
from memory_profiler import profile
from collections import Counter, defaultdict


@profile
def traditional_loop():
    result = []
    for x in range(10000):
        if x % 2 == 0:
            result.append(x**2)
    return result


@profile
def list_comp():
    return [x**2 for x in range(10000) if x % 2 == 0]


@profile
def fibonacci_generator(n):
    """Generator que produce secuencia Fibonacci"""
    a, b = 0, 1
    count = 0
    while count < n:
        yield a
        a, b = b, a + b
        count += 1


sales_data = [
    {"product": "laptop", "price": 1200, "category": "electronics", "quantity": 2},
    {"product": "mouse", "price": 25, "category": "electronics", "quantity": 5},
    {"product": "book", "price": 15, "category": "education", "quantity": 10},
    {"product": "phone", "price": 800, "category": "electronics", "quantity": 1},
    {"product": "laptop", "price": 800, "category": "electronics", "quantity": 2},
    # ... más datos
]


@profile
@track_time
def analyze_sales_comprehensions_mine(data):
    """
    Usar comprensiones para analysis eficiente
    """
    # 1. Total revenue por producto
    iterator = (item for item in data)

    result = {
        "revenue": {},
        "expensive_products": set(),
        "categories": set(),
        "avg_prices": {},
    }
    for item in iterator:
        # Revenue per product
        result["revenue"][item["product"]] = result["revenue"].get(
            item["product"], 0
        ) + (item["price"] * item["quantity"])

        # Expensive products
        if item["price"] > 100:
            result["expensive_products"].add(item["product"])
        # Unique categories
        result["categories"].add(item["category"])

        # Average price per category
        category_data = result["avg_prices"].get(
            item["category"],
            {
                "total_price": 0,
                "count": 0,
            },
        )
        category_data["total_price"] += item["price"]
        category_data["count"] += 1

    return (
        result["revenue"],
        result["expensive_products"],
        result["categories"],
        result["avg_prices"],
    )


@profile
@track_time
def analyze_sales_comprehensions(data):
    """
    Usar comprensiones para analysis eficiente
    """
    # 1. Total revenue por producto

    revenue_by_product = {
        item["product"]: item["price"] * item["quantity"] for item in data
    }

    # 2. Productos caros (price > 100) por categoría
    expensive_by_category = {
        category: [
            item
            for item in data
            if item["category"] == category and item["price"] > 100
        ]
        for category in set(item["category"] for item in data)
    }

    # 3. Set de todas las categorías únicas
    categories = {item["category"] for item in data}

    # 4. Dict de average price por categoría
    avg_prices = {
        category: sum(item["price"] for item in data if item["category"] == category)
        / len([item for item in data if item["category"] == category])
        for category in categories
    }

    return revenue_by_product, expensive_by_category, categories, avg_prices


def process_large_dataset_generator(filename):
    """
    Procesa archivo grande usando generators
    """

    def read_sales_file(filename):
        # TODO: Generator que lee archivo línea por línea
        pass

    def parse_line(line):
        # TODO: Convierte línea CSV a dict
        pass

    def filter_valid_records(records):
        # TODO: Generator que filtra records válidos
        pass

    def calculate_metrics(records):
        # TODO: Procesa usando generators para memory efficiency
        pass

    # Pipeline completo
    raw_lines = read_sales_file(filename)
    parsed_records = (parse_line(line) for line in raw_lines)
    valid_records = filter_valid_records(parsed_records)
    return calculate_metrics(valid_records)

    # 1. Total revenue por producto
    revenue_by_product = {}

    # 2. Productos caros (price > 100) por categoría
    expensive_by_category = {}

    # 3. Set de todas las categorías únicas
    categories = set()

    # 4. Dict de average price por categoría
    avg_prices = {}

    return revenue_by_product, expensive_by_category, categories, avg_prices


def process_large_dataset_generator(filename):
    """
    Procesa archivo grande usando generators
    """

    def read_sales_file(filename):
        # TODO: Generator que lee archivo línea por línea
        pass

    def parse_line(line):
        # TODO: Convierte línea CSV a dict
        pass

    def filter_valid_records(records):
        # TODO: Generator que filtra records válidos
        pass

    def calculate_metrics(records):
        # TODO: Procesa usando generators para memory efficiency
        pass

    # Pipeline completo
    raw_lines = read_sales_file(filename)
    parsed_records = (parse_line(line) for line in raw_lines)
    valid_records = filter_valid_records(parsed_records)
    return calculate_metrics(valid_records)


def two_sum(nums, target):
    """
    LeetCode #1: Two Sum
    Encuentra índices de dos números que suman target

    Input: nums = [2,7,11,15], target = 9
    Output: [0,1] porque nums[0] + nums[1] = 9
    """
    # TODO: Implementar usando dict comprehension + enumeration
    # Hint: Crear dict de {value: index} y buscar complement
    num_dict = {num: i for i, num in enumerate(nums)}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_dict and num_dict[complement] != i:
            return [i, num_dict[complement]]
    return None


def is_anagram(s, t):
    """
    LeetCode #242: Valid Anagram
    Determina si t es anagrama de s

    Input: s = "anagram", t = "nagaram"
    Output: True
    """
    # TODO: Implementar usando set/dict comprehensions
    # Considera múltiples approaches y su efficiency
    if len(s) != len(t):
        return False
    count_s = {char: s.count(char) for char in set(s)}
    count_t = {char: t.count(char) for char in set(t)}
    return count_s == count_t


def groupAnagrams_mine(self, strs: List[str]) -> List[List[str]]:
    result = []
    index_used = set()

    for index_i in range(len(strs)):
        if index_i in index_used:
            continue

        w1 = strs[index_i]
        group = [w1]

        w1_counter = Counter(w1)

        for index_y in range(index_i + 1, len(strs)):
            if index_y in index_used:
                continue

            w2 = strs[index_y]

            if len(w1) == len(w2):
                w2_counter = Counter(w2)

                if w1_counter == w2_counter:
                    group.append(w2)
                    index_used.add(index_y)

        result.append(group)

    return result


def group_anagrams(strs):
    """
    LeetCode #49: Group Anagrams
    Agrupa strings que son anagramas
    """
    # TODO: Usar dict comprehension + tuple como key
    anagrams = {}
    for s in strs:
        key = tuple(sorted(s))
        if key not in anagrams:
            anagrams[key] = []
        anagrams[key].append(s)
    return list(anagrams.values())


def groupAnagrams_best(self, strs: List[str]) -> List[List[str]]:
    d = defaultdict(list)
    for i in strs:
        key = "".join(sorted(i))
        d[key].append(i)
    return list(d.values())


def contains_duplicate(nums):
    """
    LeetCode #217: Contains Duplicate
    Retorna True si algún valor aparece al menos dos veces
    """
    # TODO: Multiple approaches usando set
    # 1. Set length comparison
    # 2. Set building with early termination
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False


def containsDuplicate_best(self, nums: List[int]) -> bool:
    numsSet = set(nums)
    return not len(numsSet) == len(nums)


def containsDuplicate_mine(self, nums: List[int]) -> bool:
    comparation = {n for n in nums}
    return len(nums) != len(comparation)


def containsNearbyDuplicate_mine(self, nums: List[int], k: int) -> bool:
    group_numbers = defaultdict(list)
    for i, n in enumerate(nums):
        group_numbers[n].append(i)
        if len(group_numbers[n]) >= 2:
            for index in range(len(group_numbers[n]) - 1):
                diff = group_numbers[n][index] - group_numbers[n][index + 1]
                if abs(diff) <= k:
                    return True


def contains_duplicate_within_k(nums, k):
    """
    Variación: duplicado dentro de k posiciones
    """
    # TODO: Sliding window con set
    seen = {}
    for i, num in enumerate(nums):
        if num in seen and i - seen[num] <= k:
            return True
        seen[num] = i
    return False


analyze_sales_comprehensions(data=sales_data)
analyze_sales_comprehensions_mine(data=sales_data)
