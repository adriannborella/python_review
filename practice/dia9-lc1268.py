from typing import List


class Solution:
    def suggestedProducts(
        self, products: List[str], searchWord: str
    ) -> List[List[str]]:
        products.sort()

        result = []
        searchInput = ""
        for letter in searchWord:
            # Necesito buscar el indice para iterar
            # Binary Search # Hay un python Search?? y Filter, que algoritmos usan?
            left = 0
            right = len(products) - 1
            searchInput += letter

            while left < right:
                mid = left + (right - left) // 2

                if products[mid][: len(searchInput)] < searchInput:
                    left = mid + 1
                else:
                    right = mid

            suggestions = []
            for j in range(left, min(left + 3, len(products))):
                if j < len(products) and products[j].startswith(searchInput):
                    suggestions.append(products[j])

            result.append(suggestions)

        return result


sol = Solution()
# assert sol.suggestedProducts(
#     ["mobile", "mouse", "moneypot", "monitor", "mousepad"], "mouse"
# ) == [
#     ["mobile", "moneypot", "monitor"],
#     ["mobile", "moneypot", "monitor"],
#     ["mouse", "mousepad"],
#     ["mouse", "mousepad"],
#     ["mouse", "mousepad"],
# ]
assert sol.suggestedProducts(
    ["bags", "baggage", "banner", "box", "cloths"], "bags"
) == [
    ["baggage", "bags", "banner"],
    ["baggage", "bags", "banner"],
    ["baggage", "bags"],
    ["bags"],
]
