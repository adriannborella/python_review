"""
DÍA 21 - EVALUACIÓN FINAL Y PREPARACIÓN
Assessment completo + roadmap hacia simulacro del día 28
"""

from typing import List, Dict, Tuple
import time


# MINI-EVALUACIÓN CRONOMETRADA (20 minutos)
class TimedChallenges:
    """
    Desafíos cronometrados para medir tu progreso
    Objetivo: Resolver correctamente en tiempo límite
    """
    
    @staticmethod
    def challenge_1_arrays_hashing(time_limit=5):
        """
        CHALLENGE 1: Two Sum Variations (5 minutos)
        
        Dado array y target, retorna:
        1. Indices de dos números que suman target
        2. Todos los pares únicos que suman target
        3. Tres números que suman target más cercano
        """
        def two_sum(nums: List[int], target: int) -> List[int]:
            # TODO: Implementar en < 2 min
            pass
        
        def two_sum_all_pairs(nums: List[int], target: int) -> List[List[int]]:
            # TODO: Implementar en < 2 min
            pass
        
        def three_sum_closest(nums: List[int], target: int) -> int:
            # TODO: Implementar en < 3 min
            pass
        
        return two_sum, two_sum_all_pairs, three_sum_closest
    
    @staticmethod
    def challenge_2_linked_lists(time_limit=5):
        """
        CHALLENGE 2: Linked List Mastery (5 minutos)
        
        Implementa:
        1. Reverse linked list
        2. Merge two sorted lists
        3. Detect cycle y encontrar inicio
        """
        class ListNode:
            def __init__(self, val=0, next=None):
                self.val = val
                self.next = next
        
        def reverse_list(head: ListNode) -> ListNode:
            # TODO: Implementar en < 2 min
            pass
        
        def merge_two_lists(l1: ListNode, l2: ListNode) -> ListNode:
            # TODO: Implementar en < 2 min
            pass
        
        def detect_cycle_start(head: ListNode) -> ListNode:
            # TODO: Implementar en < 3 min (Floyd's algorithm)
            pass
        
        return reverse_list, merge_two_lists, detect_cycle_start
    
    @staticmethod
    def challenge_3_trees_graphs(time_limit=7):
        """
        CHALLENGE 3: Trees & Graphs (7 minutos)
        
        Implementa:
        1. Binary tree level order traversal
        2. Validate BST
        3. Number of islands (DFS)
        """
        class TreeNode:
            def __init__(self, val=0, left=None, right=None):
                self.val = val
                self.left = left
                self.right = right
        
        def level_order(root: TreeNode) -> List[List[int]]:
            # TODO: BFS implementation < 3 min
            pass
        
        def is_valid_bst(root: TreeNode) -> bool:
            # TODO: In-order or bounds checking < 2 min
            pass
        
        def num_islands(grid: List[List[str]]) -> int:
            # TODO: DFS/BFS on 2D grid < 3 min
            pass
        
        return level_order, is_valid_bst, num_islands
    
    @staticmethod
    def challenge_4_dynamic_patterns(time_limit=8):
        """
        CHALLENGE 4: Advanced Patterns (8 minutos)
        
        Implementa:
        1. LRU Cache (básico)
        2. Top K frequent elements
        3. Sliding window maximum
        """
        
        def lru_cache_basic(capacity: int):
            # TODO: Implementar estructura básica < 4 min
            pass
        
        def top_k_frequent(nums: List[int], k: int) -> List[int]:
            # TODO: Heap approach < 2 min
            pass
        
        def max_sliding_window(nums: List[int], k: int) -> List[int]:
            # TODO: Deque approach < 3 min
            pass
        
        return lru_cache_basic, top_k_frequent, max_sliding_window


# SISTEMA DE SCORING AUTOMÁTICO
class PerformanceTracker:
    """
    Sistema para trackear tu performance y identificar áreas débiles
    """
    
    def __init__(self):
        self.scores = {
            'arrays_hashing': 0,
            'linked_lists': 0,
            'trees_graphs': 0,
            'heaps_priority': 0,
            'dynamic_patterns': 0,
            'time_management': 0,
            'code_quality': 0,
            'communication': 0
        }
        self.weak_areas = []
        self.strong_areas = []
    
    def evaluate_solution(self, category: str, solution_func, test_cases: List, time_taken: float):
        """
        Evalúa una solución basada en correctness, eficiencia y tiempo
        """
        score = 0
        
        # Test correctness (50 puntos)
        correct_cases = 0
        for test_case in test_cases:
            try:
                expected, actual = test_case['expected'], solution_func(test_case['input'])
                if expected == actual:
                    correct_cases += 1
            except Exception as e:
                print(f"Error in test case: {e}")
        
        correctness_score = (correct_cases / len(test_cases)) * 50
        score += correctness_score
        
        # Time efficiency (30 puntos)
        target_time = test_cases[0].get('target_time', 300)  # 5 min default
        if time_taken <= target_time:
            time_score = 30
        elif time_taken <= target_time * 1.5:
            time_score = 20
        elif time_taken <= target_time * 2:
            time_score = 10
        else:
            time_score = 0
        
        score += time_score
        
        # Code quality (20 puntos) - manual assessment
        quality_score = self._assess_code_quality(solution_func)
        score += quality_score
        
        self.scores[category] = score
        
        if score < 60:
            self.weak_areas.append(category)
        elif score > 85:
            self.strong_areas.append(category)
        
        return score
    
    def _assess_code_quality(self, func) -> int:
        """
        Manual code quality assessment
        TODO: Implement static analysis or manual checklist
        """
        return 15  # Placeholder - should be manual assessment
    
    def generate_report(self) -> str:
        """
        Genera reporte detallado de performance
        """
        total_score = sum(self.scores.values()) / len(self.scores)
        
        report = f"""
        
========================================
       REPORTE DE PERFORMANCE - DÍA 21
========================================

📊 SCORE GENERAL: {total_score:.1f}/100

📋 DESGLOSE POR CATEGORÍA:
Arrays & Hashing:     {self.scores['arrays_hashing']}/100
Linked Lists:         {self.scores['linked_lists']}/100
Trees & Graphs:       {self.scores['trees_graphs']}/100
Heaps & Priority:     {self.scores['heaps_priority']}/100
Dynamic Patterns:     {self.scores['dynamic_patterns']}/100
Time Management:      {self.scores['time_management']}/100
Code Quality:         {self.scores['code_quality']}/100
Communication:        {self.scores['communication']}/100

🔴 ÁREAS DÉBILES: {', '.join(self.weak_areas) if self.weak_areas else 'Ninguna'}
🟢 ÁREAS FUERTES: {', '.join(self.strong_areas) if self.strong_areas else 'En desarrollo'}

📈 RECOMENDACIONES PARA DÍA 22-27:
"""
        
        # Generar recomendaciones basadas en weak areas
        recommendations = self._generate_recommendations()
        report += recommendations
        
        report += f"""

🎯 PREPARACIÓN PARA SIMULACRO DÍA 28:
{'✅ LISTO' if total_score >= 75 else '⚠️  NECESITA MÁS PRÁCTICA'}

========================================
        """
        
        return report
    
    def _generate_recommendations(self) -> str:
        """
        Genera recomendaciones específicas basadas en áreas débiles
        """
        recommendations = ""
        
        if 'arrays_hashing' in self.weak_areas:
            recommendations += """
- Practica más problems de Two Sum variations
- Revisa hash map collision handling
- Domina sliding window patterns
"""
        
        if 'linked_lists' in self.weak_areas:
            recommendations += """
- Practica manipulación de punteros
- Revisa Floyd's cycle detection
- Implementa todas las operaciones desde cero
"""
        
        if 'trees_graphs' in self.weak_areas:
            recommendations += """
- Practica BFS/DFS iterativo y recursivo
- Revisa tree traversal patterns
- Domina graph representation (adjacency list/matrix)
"""
        
        if 'dynamic_patterns' in self.weak_areas:
            recommendations += """
- Practica más problemas combinando estructuras
- Revisa LRU cache implementation
- Domina heap + hash map patterns
"""
        
        return recommendations


# SIMULACRO MOCK INTERVIEW SETUP
class MockInterviewSetup:
    """
    Setup para mock interview del día 28
    """
    
    @staticmethod
    def behavioral_questions():
        """
        Preguntas comportamentales típicas - prepara historias STAR
        """
        questions = [
            "Tell me about a challenging technical problem you solved",
            "Describe a time when you had to learn a new technology quickly",
            "How do you handle disagreements with team members about technical decisions?",
            "Tell me about a time when you had to optimize code for performance",
            "Describe your approach to debugging a complex issue",
            "How do you stay updated with new technologies and best practices?"
        ]
        
        framework = """
        FRAMEWORK STAR PARA RESPUESTAS:
        
        S - SITUATION: Context del problema
        T - TASK: Tu responsabilidad específica
        A - ACTION: Qué acciones tomaste (específicas y técnicas)
        R - RESULT: Outcome medible
        
        TIPS:
        - 2-3 minutos máximo por respuesta
        - Focus en tu contribución individual
        - Incluye números/métricas cuando sea posible
        - Muestra aprendizaje de errores
        """
        
        return questions, framework
    
    @staticmethod
    def technical_interview_structure():
        """
        Estructura típica de entrevista técnica
        """
        structure = """
        ESTRUCTURA TÍPICA (45-60 minutos):
        
        1. INTRODUCCIÓN (5 min):
           - Brief self introduction
           - Revisar background
           
        2. PROBLEMA TÉCNICO (30-40 min):
           - Clarifying questions (5 min)
           - Approach discussion (5 min)
           - Coding (20-25 min)
           - Testing & optimization (5 min)
           
        3. FOLLOW-UP QUESTIONS (10 min):
           - Complexity analysis
           - Alternative approaches
           - System design considerations
           
        4. YOUR QUESTIONS (5 min):
           - Technical culture
           - Team structure
           - Growth opportunities
        """
        
        return structure
    
    @staticmethod
    def common_interview_problems():
        """
        Problemas más comunes en entrevistas por empresa
        """
        problems_by_company = {
            "Google": [
                "Two Sum variants",
                "Binary Tree problems",
                "Graph traversal",
                "Dynamic Programming",
                "System Design (for senior)"
            ],
            "Facebook/Meta": [
                "Binary Tree Vertical Order",
                "Valid Palindrome variations",
                "Merge Intervals",
                "LRU Cache",
                "Group Anagrams"
            ],
            "Amazon": [
                "Top K Frequent Elements",
                "Number of Islands",
                "Word Ladder",
                "LRU Cache",
                "Critical Connections"
            ],
            "Microsoft": [
                "Reverse Linked List",
                "Binary Tree Level Order",
                "Merge Two Sorted Lists",
                "Valid Parentheses",
                "Climbing Stairs"
            ],
            "Apple": [
                "Binary Tree problems",
                "Array manipulation",
                "String processing",
                "Graph algorithms",
                "Design problems"
            ]
        }
        
        return problems_by_company


# PLAN DE ESTUDIO DÍA 22-27
def study_plan_week4():
    """
    Plan detallado para la semana 4 basado en performance día 21
    """
    plan = """
    
📅 PLAN DE ESTUDIO SEMANA 4 (DÍA 22-27)

🎯 OBJETIVO: Preparación intensiva para mock interview día 28

DÍA 22 (OOP Fundamentals):
- Mañana: Clases, herencia, polimorfismo
- Tarde: Design patterns (Singleton, Factory)
- Práctica: 2 problemas OOP de LeetCode

DÍA 23 (Python OOP Avanzado):
- Mañana: Magic methods, properties, descriptors
- Tarde: Custom containers, operator overloading
- Práctica: Implementar estructura de datos custom

DÍA 24 (Testing y TDD):
- Mañana: unittest, pytest, mocking
- Tarde: TDD para mini-proyecto
- Práctica: Tests para código del día 21

DÍA 25 (Testing Avanzado):
- Mañana: Coverage, integration tests
- Tarde: Performance testing
- Práctica: Test suite completo

DÍA 26 (Project Day):
- Todo el día: Mini-aplicación con OOP + tests
- Entregable: Sistema de biblioteca completo
- Focus: Code organization, testing, documentation

DÍA 27 (Repaso Final):
- Mañana: Revisar áreas débiles identificadas
- Tarde: Práctica de whiteboard coding
- Noche: Preparar historias STAR para behavioral

DÍA 28 (SIMULACRO):
- Mock interview completo
- Technical + behavioral + system design
- Feedback detallado y plan de mejora
    """
    
    return plan


if __name__ == "__main__":
    print("🎯 EVALUACIÓN FINAL DÍA 21")
    print("="*50)
    
    # Inicializar tracker
    tracker = PerformanceTracker()
    
    print("\n📊 Para obtener tu reporte completo:")
    print("1. Completa los timed challenges")
    print("2. Ejecuta las funciones de evaluación") 
    print("3. Genera reporte con tracker.generate_report()")
    
    print("\n📅 PRÓXIMOS PASOS:")
    print("- Día 22-23: OOP Fundamentals & Advanced")
    print("- Día 24-25: Testing & TDD")
    print("- Día 26: Project Day")
    print("- Día 27: Final Review")
    print("- Día 28: 🎯 MOCK INTERVIEW")
    
    # Setup para mock interview
    mock_setup = MockInterviewSetup()
    behavioral_q, star_framework = mock_setup.behavioral_questions()
    
    print(f"\n💡 PREPARA HISTORIAS STAR PARA:")
    for i, q in enumerate(behavioral_q[:3], 1):
        print(f"{i}. {q}")
    
    print(f"\n{star_framework}")
    
    print("\n🚀 ¡Estás en el camino correcto!")
    print("Las próximas semanas consolidarán todo tu conocimiento.")
