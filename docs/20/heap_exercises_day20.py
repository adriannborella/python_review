"""
EJERCICIOS ADICIONALES - HEAP MASTERY
Practica estos ejercicios en los últimos 30 minutos
"""

import heapq
from typing import List
from collections import defaultdict


# EJERCICIO 1: IPO (Initial Public Offering)
def find_maximized_capital(k: int, w: int, profits: List[int], capital: List[int]) -> int:
    """
    PROBLEMA: Tienes w capital inicial y puedes hacer máximo k proyectos.
    Cada proyecto i requiere capital[i] y da profits[i].
    Maximiza el capital final.
    
    ENFOQUE: Greedy + Two Heaps
    - Min-heap para proyectos disponibles (ordenados por capital requerido)
    - Max-heap para proyectos que podemos hacer (ordenados por profit)
    
    Tu turno: ¡Implementa la solución!
    """
    # PISTA: Combina proyectos disponibles + greedy selection
    pass


# EJERCICIO 2: Smallest Range Covering Elements from K Lists
def smallest_range(nums: List[List[int]]) -> List[int]:
    """
    PROBLEMA: Dado k listas ordenadas, encuentra el rango [a,b] más pequeño
    tal que contenga al menos un elemento de cada lista.
    
    EJEMPLO:
    nums = [[4,10,15,24,26],[0,9,12,20],[5,18,22,30]]
    Output: [20,24]
    
    ENFOQUE: Min-heap + sliding window concept
    - Heap mantiene el elemento mínimo actual de cada lista
    - Track máximo para calcular rango
    
    Tu turno: ¡Resuelve este problema complejo!
    """
    # PISTA: (valor, lista_id, índice) en heap
    # Mantén track del máximo mientras mueves el mínimo
    pass


# EJERCICIO 3: Meeting Rooms II
def min_meeting_rooms(intervals: List[List[int]]) -> int:
    """
    PROBLEMA: Dado array de intervalos de meetings, encuentra el número
    mínimo de salas de reuniones necesarias.
    
    EJEMPLO:
    intervals = [[0,30],[5,10],[15,20]]
    Output: 2
    
    ENFOQUE: Sort + Min-heap
    - Ordena por start time
    - Heap mantiene end times de meetings activos
    
    Tu turno: ¡Implementa esta solución clásica!
    """
    # PISTA: Si start >= heap[0], reutiliza sala
    pass


# EJERCICIO 4: Super Ugly Number
def nth_super_ugly_number(n: int, primes: List[int]) -> int:
    """
    PROBLEMA: Extensión de ugly number con primes personalizados.
    Encuentra el n-ésimo super ugly number.
    
    EJEMPLO:
    n = 12, primes = [2,7,13,19]
    Output: 32
    
    ENFOQUE: Similar a ugly number pero con primes dados
    
    Tu turno: ¡Generaliza el problema de ugly numbers!
    """
    pass


# EJERCICIO 5: Twitter Design - Top K Tweets
class Twitter:
    """
    PROBLEMA: Diseña sistema simplificado de Twitter
    - postTweet(userId, tweetId): Usuario publica tweet
    - getNewsFeed(userId): Obtiene 10 tweets más recientes del feed
    - follow(followerId, followeeId): Seguir usuario
    - unfollow(followerId, followeeId): Dejar de seguir
    
    ENFOQUE: Heap para merge feeds + timestamp
    
    Tu turno: ¡Implementa este sistema!
    """
    
    def __init__(self):
        # PISTA: Necesitas tracks de tweets, follows, timestamps
        pass
    
    def postTweet(self, userId: int, tweetId: int) -> None:
        pass
    
    def getNewsFeed(self, userId: int) -> List[int]:
        # PISTA: Merge feeds de user + followees usando heap
        pass
    
    def follow(self, followerId: int, followeeId: int) -> None:
        pass
    
    def unfollow(self, followerId: int, followeeId: int) -> None:
        pass


# EJERCICIO 6: Rearrange String k Distance Apart
def rearrange_string(s: str, k: int) -> str:
    """
    PROBLEMA: Reorganiza string para que caracteres iguales estén
    al menos k posiciones apart.
    
    EJEMPLO:
    s = "aabbcc", k = 3
    Output: "abcabc" o similar
    
    ENFOQUE: Max-heap + cooldown queue
    
    Tu turno: ¡Extiende el problema de reorganize string!
    """
    pass


# SOLUCIONES DE REFERENCIA (Para verificar después de intentar)
def solutions():
    """
    SOLUCIONES DE REFERENCIA - SOLO MIRA DESPUÉS DE INTENTAR
    """
    
    def find_maximized_capital_solution(k: int, w: int, profits: List[int], capital: List[int]) -> int:
        """Solución IPO"""
        import heapq
        
        # Min-heap para proyectos (capital_requerido, profit, index)
        min_capital = [(capital[i], profits[i], i) for i in range(len(profits))]
        heapq.heapify(min_capital)
        
        # Max-heap para proyectos disponibles (profit negativo)
        max_profit = []
        
        current_capital = w
        
        for _ in range(k):
            # Mover proyectos disponibles al max-heap
            while min_capital and min_capital[0][0] <= current_capital:
                cap, prof, idx = heapq.heappop(min_capital)
                heapq.heappush(max_profit, -prof)
            
            # Si no hay proyectos disponibles, terminar
            if not max_profit:
                break
            
            # Tomar el proyecto más rentable
            current_capital += -heapq.heappop(max_profit)
        
        return current_capital
    
    
    def min_meeting_rooms_solution(intervals: List[List[int]]) -> int:
        """Solución Meeting Rooms II"""
        if not intervals:
            return 0
        
        # Ordenar por start time
        intervals.sort(key=lambda x: x[0])
        
        # Min-heap para end times
        heap = []
        
        for start, end in intervals:
            # Si hay una sala libre (meeting terminó)
            if heap and start >= heap[0]:
                heapq.heappop(heap)
            
            # Agregar end time de meeting actual
            heapq.heappush(heap, end)
        
        return len(heap)
    
    
    def twitter_solution():
        """Solución Twitter Design"""
        class TwitterSolution:
            def __init__(self):
                self.tweets = defaultdict(list)  # userId -> [(timestamp, tweetId)]
                self.follows = defaultdict(set)  # userId -> set of followeeIds
                self.timestamp = 0
            
            def postTweet(self, userId: int, tweetId: int) -> None:
                self.tweets[userId].append((self.timestamp, tweetId))
                self.timestamp += 1
            
            def getNewsFeed(self, userId: int) -> List[int]:
                # Obtener tweets del user + followees
                candidates = []
                
                # Tweets propios
                for timestamp, tweetId in self.tweets[userId]:
                    candidates.append((timestamp, tweetId))
                
                # Tweets de followees
                for followeeId in self.follows[userId]:
                    for timestamp, tweetId in self.tweets[followeeId]:
                        candidates.append((timestamp, tweetId))
                
                # Ordenar por timestamp (más reciente primero)
                candidates.sort(reverse=True)
                
                # Retornar top 10
                return [tweetId for _, tweetId in candidates[:10]]
            
            def follow(self, followerId: int, followeeId: int) -> None:
                if followerId != followeeId:
                    self.follows[followerId].add(followeeId)
            
            def unfollow(self, followerId: int, followeeId: int) -> None:
                self.follows[followerId].discard(followeeId)
        
        return TwitterSolution
    
    return {
        'ipo': find_maximized_capital_solution,
        'meeting_rooms': min_meeting_rooms_solution,
        'twitter': twitter_solution()
    }


# TESTING FRAMEWORK PARA TUS IMPLEMENTACIONES
def test_your_solutions():
    """Usa esto para probar tus implementaciones"""
    
    print("=== TESTING YOUR IMPLEMENTATIONS ===")
    
    # Test IPO
    try:
        k, w = 2, 0
        profits = [1, 2, 3]
        capital = [0, 1, 1]
        result = find_maximized_capital(k, w, profits, capital)
        expected = 4
        print(f"IPO: {result} (expected: {expected}) - {'✓' if result == expected else '✗'}")
    except:
        print("IPO: Not implemented yet")
    
    # Test Meeting Rooms
    try:
        intervals = [[0, 30], [5, 10], [15, 20]]
        result = min_meeting_rooms(intervals)
        expected = 2
        print(f"Meeting Rooms: {result} (expected: {expected}) - {'✓' if result == expected else '✗'}")
    except:
        print("Meeting Rooms: Not implemented yet")
    
    # Test Twitter
    try:
        twitter = Twitter()
        twitter.postTweet(1, 5)
        news_feed = twitter.getNewsFeed(1)
        expected = [5]
        print(f"Twitter: {news_feed} (expected: {expected}) - {'✓' if news_feed == expected else '✗'}")
    except:
        print("Twitter: Not implemented yet")


if __name__ == "__main__":
    print("🎯 EJERCICIOS HEAP - DÍA 20")
    print("Implementa las funciones marcadas con 'Tu turno'")
    print("Luego ejecuta test_your_solutions() para verificar")
    print("\n" + "="*50)
    
    test_your_solutions()
    
    print("\n💡 TIPS:")
    print("1. Siempre pregunta: ¿necesito min-heap o max-heap?")
    print("2. Para problemas de 'Top K': usa heap de tamaño K")
    print("3. Para merge operations: usa heap con índices")
    print("4. Para scheduling: combina heap con timestamps/priorities")
    print("5. Two heaps pattern: perfecto para medians/percentiles")
