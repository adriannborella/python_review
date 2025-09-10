"""
DÍA 22 - SOLID PRINCIPLES & DESIGN PATTERNS
Principios fundamentales del diseño de software
Patterns más comunes en entrevistas técnicas
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Protocol, Optional, Union
from enum import Enum
import json


# ========================================
# SOLID PRINCIPLE 1: SINGLE RESPONSIBILITY
# ========================================

# ❌ VIOLACIÓN SRP - Clase que hace demasiadas cosas
class BadUserManager:
    """EJEMPLO DE VIOLACIÓN SRP - ¡NO HAGAS ESTO!"""
    
    def __init__(self):
        self.users = []
    
    def add_user(self, user_data):
        # Responsabilidad 1: Gestión de usuarios
        pass
    
    def validate_email(self, email):
        # Responsabilidad 2: Validación
        pass
    
    def send_welcome_email(self, user):
        # Responsabilidad 3: Comunicación
        pass
    
    def save_to_database(self, user):
        # Responsabilidad 4: Persistencia
        pass
    
    def generate_user_report(self, user_id):
        # Responsabilidad 5: Reporting
        pass


# ✅ CORRECTO - Siguiendo SRP
class User:
    """Responsabilidad única: Representar un usuario"""
    
    def __init__(self, user_id: str, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.created_at = None
    
    def get_info(self) -> Dict[str, str]:
        return {
            'id': self.user_id,
            'name': self.name,
            'email': self.email
        }


class EmailValidator:
    """Responsabilidad única: Validar emails"""
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None


class EmailService:
    """Responsabilidad única: Enviar emails"""
    
    def send_welcome_email(self, user: User) -> bool:
        print(f"📧 Sending welcome email to {user.name} at {user.email}")
        return True
    
    def send_notification(self, user: User, message: str) -> bool:
        print(f"📧 Notification to {user.email}: {message}")
        return True


class UserRepository:
    """Responsabilidad única: Persistencia de usuarios"""
    
    def __init__(self):
        self._users: Dict[str, User] = {}
    
    def save(self, user: User) -> bool:
        self._users[user.user_id] = user
        return True
    
    def find_by_id(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)
    
    def get_all(self) -> List[User]:
        return list(self._users.values())


class UserService:
    """Responsabilidad única: Lógica de negocio de usuarios"""
    
    def __init__(self, repository: UserRepository, email_service: EmailService):
        self.repository = repository
        self.email_service = email_service
    
    def create_user(self, user_id: str, name: str, email: str) -> Optional[User]:
        # Validar email
        if not EmailValidator.is_valid_email(email):
            return None
        
        # Crear usuario
        user = User(user_id, name, email)
        
        # Guardar
        if self.repository.save(user):
            # Enviar bienvenida
            self.email_service.send_welcome_email(user)
            return user
        
        return None


# ========================================
# SOLID PRINCIPLE 2: OPEN/CLOSED PRINCIPLE
# ========================================

class Shape(ABC):
    """Base abstraction para OCP"""
    
    @abstractmethod
    def calculate_area(self) -> float:
        pass


class Circle(Shape):
    """Implementación específica - cerrada para modificación"""
    
    def __init__(self, radius: float):
        self.radius = radius
    
    def calculate_area(self) -> float:
        return 3.14159 * self.radius ** 2


class Rectangle(Shape):
    """Nueva forma - abierta para extensión"""
    
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def calculate_area(self) -> float:
        return self.width * self.height


class Triangle(Shape):
    """Otra extensión sin modificar código existente"""
    
    def __init__(self, base: float, height: float):
        self.base = base
        self.height = height
    
    def calculate_area(self) -> float:
        return 0.5 * self.base * self.height


class AreaCalculator:
    """
    SIGUIENDO OCP: Abierto para extensión (nuevas formas),
    cerrado para modificación (no necesita cambios)
    """
    
    def calculate_total_area(self, shapes: List[Shape]) -> float:
        return sum(shape.calculate_area() for shape in shapes)
    
    def get_areas_report(self, shapes: List[Shape]) -> Dict[str, float]:
        report = {}
        for i, shape in enumerate(shapes):
            shape_type = type(shape).__name__
            report[f"{shape_type}_{i}"] = shape.calculate_area()
        return report


# ========================================
# SOLID PRINCIPLE 3: LISKOV SUBSTITUTION
# ========================================

class Bird(ABC):
    """Base class para LSP"""
    
    @abstractmethod
    def move(self) -> str:
        pass


class FlyingBird(Bird):
    """Subclass para pájaros que vuelan"""
    
    @abstractmethod
    def fly(self) -> str:
        pass
    
    def move(self) -> str:
        return self.fly()


class WalkingBird(Bird):
    """Subclass para pájaros que caminan"""
    
    @abstractmethod
    def walk(self) -> str:
        pass
    
    def move(self) -> str:
        return self.walk()


class Eagle(FlyingBird):
    """LSP: Eagle puede reemplazar FlyingBird"""
    
    def fly(self) -> str:
        return "🦅 Eagle soars high in the sky"


class Sparrow(FlyingBird):
    """LSP: Sparrow puede reemplazar FlyingBird"""
    
    def fly(self) -> str:
        return "🐦 Sparrow flies quickly between trees"


class Penguin(WalkingBird):
    """LSP: Penguin puede reemplazar WalkingBird (no FlyingBird)"""
    
    def walk(self) -> str:
        return "🐧 Penguin waddles on ice"
    
    def swim(self) -> str:
        return "🏊 Penguin swims expertly underwater"


class BirdSanctuary:
    """
    LSP EN ACCIÓN: Puede trabajar con cualquier Bird
    sin conocer implementación específica
    """
    
    def __init__(self):
        self.birds: List[Bird] = []
    
    def add_bird(self, bird: Bird):
        self.birds.append(bird)
    
    def morning_activity(self) -> List[str]:
        """Todos los pájaros se mueven de su manera natural"""
        activities = []
        for bird in self.birds:
            activity = bird.move()  # Polimorfismo + LSP
            activities.append(f"{type(bird).__name__}: {activity}")
        return activities


# ========================================
# SOLID PRINCIPLE 4: INTERFACE SEGREGATION
# ========================================

# ❌ VIOLACIÓN ISP - Interface muy grande
class BadWorkerInterface(ABC):
    """INTERFACE PROBLEMÁTICA - Muy amplia"""
    
    @abstractmethod
    def work(self): pass
    
    @abstractmethod
    def eat(self): pass
    
    @abstractmethod
    def sleep(self): pass
    
    @abstractmethod
    def program(self): pass  # No todos los workers programan!
    
    @abstractmethod
    def manage_team(self): pass  # No todos son managers!


# ✅ CORRECTO - Interfaces específicas (ISP)
class Workable(Protocol):
    """Interface pequeña y específica"""
    def work(self) -> str: ...


class Eatable(Protocol):
    """Interface para entidades que comen"""
    def eat(self) -> str: ...


class Sleepable(Protocol):
    """Interface para entidades que duermen"""
    def sleep(self) -> str: ...


class Programmable(Protocol):
    """Interface específica para programadores"""
    def program(self) -> str:
        return f"{self.name} is writing clean code"
    
    def debug_code(self) -> str:
        return f"{self.name} is fixing bugs"


class Manager:
    """Manager implementa diferentes interfaces"""
    
    def __init__(self, name: str):
        self.name = name
    
    def work(self) -> str:
        return f"{self.name} is planning and coordinating"
    
    def eat(self) -> str:
        return f"{self.name} is eating in executive dining"
    
    def sleep(self) -> str:
        return f"{self.name} is resting"
    
    def manage_team(self) -> str:
        return f"{self.name} is leading the team"
    
    def conduct_meeting(self) -> str:
        return f"{self.name} is running a productive meeting"


class Robot:
    """Robot solo implementa interfaces apropiadas"""
    
    def __init__(self, model: str):
        self.model = model
    
    def work(self) -> str:
        return f"{self.model} robot is performing automated tasks"
    
    def program(self) -> str:
        return f"{self.model} robot is executing programmed instructions"
    
    def debug_code(self) -> str:
        return f"{self.model} robot is running diagnostics"
    
    # Note: Robot NO implementa eat() o sleep() - no los necesita!


# ========================================
# SOLID PRINCIPLE 5: DEPENDENCY INVERSION
# ========================================

# ❌ VIOLACIÓN DIP - Dependencia concreta
class BadOrderService:
    """Depende directamente de implementaciones concretas"""
    
    def __init__(self):
        self.email_sender = EmailService()  # Dependencia concreta
        self.db = UserRepository()          # Dependencia concreta
    
    def process_order(self, order_data):
        # Lógica acoplada a implementaciones específicas
        pass


# ✅ CORRECTO - Dependency Inversion
class NotificationService(ABC):
    """Abstracción para notificaciones"""
    
    @abstractmethod
    def send_notification(self, recipient: str, message: str) -> bool:
        pass


class PaymentGateway(ABC):
    """Abstracción para pagos"""
    
    @abstractmethod
    def process_payment(self, amount: float, payment_data: Dict) -> Dict:
        pass


class OrderRepository(ABC):
    """Abstracción para persistencia de órdenes"""
    
    @abstractmethod
    def save_order(self, order: Dict) -> str:
        pass
    
    @abstractmethod
    def get_order(self, order_id: str) -> Optional[Dict]:
        pass


# Implementaciones concretas
class EmailNotificationService(NotificationService):
    """Implementación concreta de notificaciones por email"""
    
    def send_notification(self, recipient: str, message: str) -> bool:
        print(f"📧 Email to {recipient}: {message}")
        return True


class SMSNotificationService(NotificationService):
    """Implementación alternativa - SMS"""
    
    def send_notification(self, recipient: str, message: str) -> bool:
        print(f"📱 SMS to {recipient}: {message}")
        return True


class StripePaymentGateway(PaymentGateway):
    """Implementación concreta - Stripe"""
    
    def process_payment(self, amount: float, payment_data: Dict) -> Dict:
        return {
            'success': True,
            'transaction_id': 'stripe_123',
            'amount': amount
        }


class DatabaseOrderRepository(OrderRepository):
    """Implementación concreta - Database"""
    
    def __init__(self):
        self._orders: Dict[str, Dict] = {}
    
    def save_order(self, order: Dict) -> str:
        import uuid
        order_id = str(uuid.uuid4())
        self._orders[order_id] = order
        return order_id
    
    def get_order(self, order_id: str) -> Optional[Dict]:
        return self._orders.get(order_id)


class OrderService:
    """
    SIGUIENDO DIP: Depende de abstracciones, no de concreciones
    """
    
    def __init__(self, 
                 notification_service: NotificationService,
                 payment_gateway: PaymentGateway,
                 order_repository: OrderRepository):
        # Dependency Injection - depende de abstracciones
        self.notification_service = notification_service
        self.payment_gateway = payment_gateway
        self.order_repository = order_repository
    
    def process_order(self, order_data: Dict) -> Dict:
        """Procesar orden usando abstracciones"""
        
        # Procesar pago
        payment_result = self.payment_gateway.process_payment(
            order_data['amount'], 
            order_data['payment_data']
        )
        
        if not payment_result['success']:
            return {'success': False, 'error': 'Payment failed'}
        
        # Guardar orden
        order_id = self.order_repository.save_order(order_data)
        
        # Notificar cliente
        self.notification_service.send_notification(
            order_data['customer_email'],
            f"Order {order_id} confirmed!"
        )
        
        return {
            'success': True,
            'order_id': order_id,
            'transaction_id': payment_result['transaction_id']
        }


# ========================================
# DESIGN PATTERN 1: SINGLETON
# ========================================

class DatabaseConnection:
    """
    SINGLETON PATTERN
    
    CUÁNDO USAR:
    - Database connections
    - Configuration managers  
    - Logging services
    - Cache managers
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Solo inicializar una vez
        if not DatabaseConnection._initialized:
            self.connection_string = "postgresql://localhost:5432/mydb"
            self.is_connected = False
            DatabaseConnection._initialized = True
    
    def connect(self) -> bool:
        """Simular conexión a base de datos"""
        if not self.is_connected:
            print(f"🔌 Connecting to {self.connection_string}")
            self.is_connected = True
        return self.is_connected
    
    def disconnect(self):
        """Cerrar conexión"""
        if self.is_connected:
            print("🔌 Disconnecting from database")
            self.is_connected = False
    
    def execute_query(self, query: str) -> str:
        """Ejecutar query"""
        if not self.is_connected:
            self.connect()
        return f"Executed: {query}"


# ========================================
# DESIGN PATTERN 2: FACTORY METHOD
# ========================================

class Animal(ABC):
    """Product interface"""
    
    @abstractmethod
    def make_sound(self) -> str:
        pass
    
    @abstractmethod
    def get_species(self) -> str:
        pass


class Dog(Animal):
    """Concrete product"""
    
    def make_sound(self) -> str:
        return "Woof! Woof!"
    
    def get_species(self) -> str:
        return "Canis lupus"


class Cat(Animal):
    """Concrete product"""
    
    def make_sound(self) -> str:
        return "Meow! Meow!"
    
    def get_species(self) -> str:
        return "Felis catus"


class Bird(Animal):
    """Concrete product"""
    
    def make_sound(self) -> str:
        return "Tweet! Tweet!"
    
    def get_species(self) -> str:
        return "Aves"


class AnimalFactory:
    """
    FACTORY METHOD PATTERN
    
    CUÁNDO USAR:
    - Creación de objetos complejos
    - Diferentes implementaciones de misma interface
    - Configuración basada en parámetros
    """
    
    @staticmethod
    def create_animal(animal_type: str) -> Animal:
        """Factory method para crear animales"""
        
        animal_types = {
            'dog': Dog,
            'cat': Cat,
            'bird': Bird
        }
        
        animal_class = animal_types.get(animal_type.lower())
        if animal_class:
            return animal_class()
        else:
            raise ValueError(f"Unknown animal type: {animal_type}")
    
    @staticmethod
    def get_available_types() -> List[str]:
        """Retorna tipos disponibles"""
        return ['dog', 'cat', 'bird']


# ========================================
# DESIGN PATTERN 3: OBSERVER
# ========================================

class Observer(ABC):
    """Observer interface"""
    
    @abstractmethod
    def update(self, subject: 'Subject', data: Any):
        pass


class Subject(ABC):
    """Subject interface"""
    
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer):
        """Agregar observer"""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer):
        """Remover observer"""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, data: Any = None):
        """Notificar a todos los observers"""
        for observer in self._observers:
            observer.update(self, data)


class StockPrice(Subject):
    """
    OBSERVER PATTERN EJEMPLO: Stock Price Monitoring
    
    CUÁNDO USAR:
    - Event-driven systems
    - Model-View architectures
    - Publish-Subscribe patterns
    """
    
    def __init__(self, symbol: str, price: float):
        super().__init__()
        self.symbol = symbol
        self._price = price
    
    @property
    def price(self) -> float:
        return self._price
    
    @price.setter
    def price(self, new_price: float):
        old_price = self._price
        self._price = new_price
        
        # Notificar cambio
        self.notify({
            'symbol': self.symbol,
            'old_price': old_price,
            'new_price': new_price,
            'change': new_price - old_price
        })


class EmailAlert(Observer):
    """Observer concreto - Email alerts"""
    
    def __init__(self, email: str):
        self.email = email
    
    def update(self, subject: Subject, data: Any):
        if isinstance(subject, StockPrice):
            change = data['change']
            symbol = data['symbol']
            new_price = data['new_price']
            
            if abs(change) > 5.0:  # Solo alertas para cambios > $5
                print(f"📧 Email to {self.email}: {symbol} moved to ${new_price:.2f} (${change:+.2f})")


class SMSAlert(Observer):
    """Observer concreto - SMS alerts"""
    
    def __init__(self, phone: str):
        self.phone = phone
    
    def update(self, subject: Subject, data: Any):
        if isinstance(subject, StockPrice):
            change = data['change']
            symbol = data['symbol']
            
            if abs(change) > 10.0:  # Solo SMS para cambios grandes > $10
                print(f"📱 SMS to {self.phone}: {symbol} major move: ${change:+.2f}")


class TradingBot(Observer):
    """Observer concreto - Automated trading"""
    
    def __init__(self, strategy: str):
        self.strategy = strategy
        self.trades = []
    
    def update(self, subject: Subject, data: Any):
        if isinstance(subject, StockPrice):
            change = data['change']
            symbol = data['symbol']
            price = data['new_price']
            
            # Simple strategy
            if self.strategy == "momentum" and change > 15.0:
                trade = f"BUY {symbol} at ${price:.2f}"
                self.trades.append(trade)
                print(f"🤖 TradingBot: {trade}")
            elif self.strategy == "contrarian" and change < -15.0:
                trade = f"BUY {symbol} at ${price:.2f} (contrarian)"
                self.trades.append(trade)
                print(f"🤖 TradingBot: {trade}")


# ========================================
# TESTING Y DEMOSTRACIÓN
# ========================================

def demonstrate_solid_principles():
    """Demostración completa de principios SOLID"""
    
    print("=" * 60)
    print("🏛️  DEMOSTRACIÓN DE PRINCIPIOS SOLID")
    print("=" * 60)
    
    # 1. SINGLE RESPONSIBILITY
    print("\n1️⃣  SINGLE RESPONSIBILITY PRINCIPLE:")
    repo = UserRepository()
    email_service = EmailService()
    user_service = UserService(repo, email_service)
    
    user = user_service.create_user("u001", "Alice", "alice@example.com")
    if user:
        print(f"✅ Created user: {user.get_info()}")
    
    # 2. OPEN/CLOSED PRINCIPLE
    print("\n2️⃣  OPEN/CLOSED PRINCIPLE:")
    shapes = [
        Circle(5.0),
        Rectangle(4.0, 6.0),
        Triangle(3.0, 4.0)
    ]
    
    calculator = AreaCalculator()
    total_area = calculator.calculate_total_area(shapes)
    print(f"📐 Total area: {total_area:.2f}")
    
    areas_report = calculator.get_areas_report(shapes)
    for shape, area in areas_report.items():
        print(f"  {shape}: {area:.2f}")
    
    # 3. LISKOV SUBSTITUTION
    print("\n3️⃣  LISKOV SUBSTITUTION PRINCIPLE:")
    sanctuary = BirdSanctuary()
    sanctuary.add_bird(Eagle())
    sanctuary.add_bird(Sparrow())
    sanctuary.add_bird(Penguin())
    
    activities = sanctuary.morning_activity()
    for activity in activities:
        print(f"  {activity}")
    
    # 4. INTERFACE SEGREGATION
    print("\n4️⃣  INTERFACE SEGREGATION PRINCIPLE:")
    dev = Developer("Bob")
    manager = Manager("Carol")
    robot = Robot("R2D2")
    
    workers = [dev, manager, robot]
    for worker in workers:
        print(f"  {worker.work()}")
    
    # 5. DEPENDENCY INVERSION
    print("\n5️⃣  DEPENDENCY INVERSION PRINCIPLE:")
    
    # Puede cambiar implementaciones fácilmente
    notification = EmailNotificationService()  # o SMSNotificationService()
    payment = StripePaymentGateway()
    repository = DatabaseOrderRepository()
    
    order_service = OrderService(notification, payment, repository)
    
    order_data = {
        'amount': 99.99,
        'customer_email': 'customer@example.com',
        'payment_data': {'card': '1234-5678-9012-3456'}
    }
    
    result = order_service.process_order(order_data)
    print(f"📦 Order processed: {result}")


def demonstrate_design_patterns():
    """Demostración de design patterns"""
    
    print("\n" + "=" * 60)
    print("🎨 DEMOSTRACIÓN DE DESIGN PATTERNS")
    print("=" * 60)
    
    # 1. SINGLETON
    print("\n1️⃣  SINGLETON PATTERN:")
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    
    print(f"Same instance? {db1 is db2}")
    db1.connect()
    print(f"DB2 is connected? {db2.is_connected}")  # True porque es la misma instancia
    
    # 2. FACTORY METHOD
    print("\n2️⃣  FACTORY METHOD PATTERN:")
    factory = AnimalFactory()
    
    for animal_type in ['dog', 'cat', 'bird']:
        animal = factory.create_animal(animal_type)
        print(f"  {animal_type.title()}: {animal.make_sound()}")
    
    # 3. OBSERVER
    print("\n3️⃣  OBSERVER PATTERN:")
    
    # Crear stock y observers
    apple_stock = StockPrice("AAPL", 150.0)
    
    email_alert = EmailAlert("trader@example.com")
    sms_alert = SMSAlert("+1234567890")
    trading_bot = TradingBot("momentum")
    
    # Subscribir observers
    apple_stock.attach(email_alert)
    apple_stock.attach(sms_alert)
    apple_stock.attach(trading_bot)
    
    print("📊 Simulating stock price changes:")
    
    # Cambios de precio disparan notificaciones
    apple_stock.price = 157.0  # +$7 cambio
    apple_stock.price = 143.0  # -$14 cambio
    apple_stock.price = 165.0  # +$22 cambio
    
    print(f"\n🤖 Trading bot made {len(trading_bot.trades)} trades:")
    for trade in trading_bot.trades:
        print(f"  {trade}")


if __name__ == "__main__":
    demonstrate_solid_principles()
    demonstrate_design_patterns()


# ========================================
# EJERCICIOS PARA ENTREVISTAS
# ========================================

def interview_exercises():
    """
    Ejercicios típicos de entrevistas OOP
    """
    
    exercises = """
    
🎯 EJERCICIOS TÍPICOS DE ENTREVISTAS OOP:
    
1. DESIGN A PARKING LOT SYSTEM:
   - Diferentes tipos de vehículos
   - Diferentes tamaños de espacios
   - Pricing strategy
   - Availability tracking
   
   🔑 Evalúa: OOP design, SOLID principles, scalability
    
2. DESIGN A LIBRARY MANAGEMENT SYSTEM:
   - Books, Members, Librarians
   - Borrowing/returning workflow
   - Fine calculation
   - Search functionality
   
   🔑 Evalúa: Class relationships, business logic, state management
    
3. DESIGN A CHESS GAME:
   - Pieces con diferentes movimientos
   - Board representation
   - Game rules y validation
   - Turn management
   
   🔑 Evalúa: Inheritance, polymorphism, complex rules
    
4. DESIGN A COFFEE SHOP ORDERING SYSTEM:
   - Different coffee types
   - Customizations (size, milk, etc.)
   - Pricing calculation
   - Order processing
   
   🔑 Evalúa: Decorator pattern, strategy pattern, composition
    
💡 APPROACH PARA ENTREVISTAS OOP:
    
1. CLARIFY REQUIREMENTS:
   - "What specific features should I focus on?"
   - "Should I consider scalability for millions of users?"
   - "Are there any specific constraints?"
    
2. IDENTIFY MAIN ENTITIES:
   - Nouns en requirements = potential classes
   - Relationships entre entities
   - Responsibilities de cada class
    
3. APPLY SOLID PRINCIPLES:
   - Start con SRP - una responsabilidad por clase
   - Consider extensibility (OCP)
   - Design clean interfaces (ISP)
    
4. CHOOSE APPROPRIATE PATTERNS:
   - Factory for object creation complexity
   - Observer for event-driven features
   - Strategy for algorithm variations
   - Decorator for feature combinations
    
5. CODE ITERATIVELY:
   - Start con basic structure
   - Add complexity gradually
   - Refactor cuando sea necesario
   - Explain trade-offs
    """
    
    print(exercises)


# CHECKLIST FINAL DÍA 22
def day22_checklist():
    """
    ✅ CHECKLIST DÍA 22 - OOP FUNDAMENTALS
    
    PRINCIPIOS OOP:
    □ Encapsulación: Private/protected attributes, properties
    □ Herencia: Abstract classes, concrete implementations
    □ Polimorfismo: Same interface, different behavior
    □ Abstracción: Hide complexity, expose interface
    
    SOLID PRINCIPLES:
    □ Single Responsibility: One reason to change
    □ Open/Closed: Open for extension, closed for modification
    □ Liskov Substitution: Subtypes must be substitutable
    □ Interface Segregation: Small, specific interfaces
    □ Dependency Inversion: Depend on abstractions
    
    DESIGN PATTERNS:
    □ Singleton: Single instance management
    □ Factory Method: Object creation abstraction
    □ Observer: Event-driven notifications
    
    PYTHON ESPECÍFICO:
    □ ABC module para abstract classes
    □ @property decorators
    □ Protocol para duck typing
    □ __magic__ methods understanding
    
    INTERVIEW SKILLS:
    □ Can design class hierarchies
    □ Can justify design decisions
    □ Can discuss trade-offs
    □ Can apply patterns appropriately
    
    SCORE: ___/19 (Objetivo: 16+ para continuar con día 23)
    """
    pass


if __name__ == "__main__":
    demonstrate_solid_principles()
    demonstrate_design_patterns()
    print("\n")
    interview_exercises()
    print("\n")
    day22_checklist() ...
    def debug_code(self) -> str: ...


class Manageable(Protocol):
    """Interface específica para managers"""
    def manage_team(self) -> str: ...
    def conduct_meeting(self) -> str: ...


# Implementaciones que usan solo interfaces necesarias
class Developer:
    """Implementa solo interfaces relevantes"""
    
    def __init__(self, name: str):
        self.name = name
    
    def work(self) -> str:
        return f"{self.name} is working on features"
    
    def eat(self) -> str:
        return f"{self.name} is eating lunch"
    
    def sleep(self) -> str:
        return f"{self.name} is sleeping"
    
    def program(self) -> str: