#**Implementa una LRU Cache** usando dict + doubly linked list

from collections import OrderedDict
class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        else:
            # Mueve el elemento al final para marcarlo como reciente
            self.cache.move_to_end(key)
            return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # Actualiza el valor y mueve al final
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            # Elimina el primer elemento (el menos reciente)
            self.cache.popitem(last=False)
        self.cache[key] = value  # Añade o actualiza el valor

if __name__ == "__main__":
    lru_cache = LRUCache(2)
    lru_cache.put(1, 1)  # cache is {1=1}
    lru_cache.put(2, 2)  # cache is {1=1, 2=2}
    print(lru_cache.get(1))  # returns 1
    lru_cache.put(3, 3)      # evicts key 2, cache is {1=1, 3=3}
    print(lru_cache.get(2))  # returns -1 (not found)
    lru_cache.put(4, 4)      # evicts key 1, cache is {3=3, 4=4}
    print(lru_cache.get(1))  # returns -1 (not found)
    print(lru_cache.get(3))  # returns 3
    print(lru_cache.get(4))  # returns 4