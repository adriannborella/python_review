"""
DÍA 22 - OOP FUNDAMENTALS & SOLID PRINCIPLES
Dominar los pilares de la programación orientada a objetos en Python
Preparación para entrevistas de diseño y arquitectura
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Union
from enum import Enum
import copy


# ========================================
# PILAR 1: ENCAPSULACIÓN
# ========================================

class BankAccount:
    """
    EJEMPLO: Encapsulación apropiada
    
    CONCEPTOS CLAVE:
    - Private attributes (_balance)
    - Properties para controlled access
    - Data validation en setters
    - Information hiding
    """
    
    def __init__(self, account_number: str, initial_balance: float = 0.0):
        self._account_number = account_number  # Protected
        self.__balance = initial_balance       # Private (name mangling)
        self._transaction_history = []         # Protected
    
    @property
    def balance(self) -> float:
        """Getter para balance - read-only access"""
        return self.__balance
    
    @property
    def account_number(self) -> str:
        """Account number es read-only"""
        return self._account_number
    
    def deposit(self, amount: float) -> bool:
        """
        Depositar dinero con validación
        Retorna True si exitoso, False si no
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        self.__balance += amount
        self._record_transaction("DEPOSIT", amount)
        return True
    
    def withdraw(self, amount: float) -> bool:
        """
        Retirar dinero con validación
        Retorna True si exitoso, False si fondos insuficientes
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        
        if amount > self.__balance:
            return False  # Fondos insuficientes
        
        self.__balance -= amount
        self._record_transaction("WITHDRAWAL", -amount)
        return True
    
    def _record_transaction(self, transaction_type: str, amount: float):
        """Método protegido para registrar transacciones"""
        import datetime
        transaction = {
            'type': transaction_type,
            'amount': amount,
            'timestamp': datetime.datetime.now(),
            'balance_after': self.__balance
        }
        self._transaction_history.append(transaction)
    
    def get_transaction_history(self) -> List[Dict]:
        """Retorna copia de historial (no referencia directa)"""
        return copy.deepcopy(self._transaction_history)
    
    def __str__(self) -> str:
        return f"Account({self._account_number}): ${self.__balance:.2f}"
    
    def __repr__(self) -> str:
        return f"BankAccount('{self._account_number}', {self.__balance})"


# ========================================
# PILAR 2: HERENCIA
# ========================================

class Vehicle(ABC):
    """
    CLASE BASE ABSTRACTA: Vehicle
    
    CONCEPTOS CLAVE:
    - Abstract methods (@abstractmethod)
    - Template method pattern
    - Common functionality en base class
    - Polimorfismo preparado
    """
    
    def __init__(self, brand: str, model: str, year: int):
        self.brand = brand
        self.model = model
        self.year = year
        self._is_running = False
    
    @abstractmethod
    def start_engine(self) -> str:
        """Cada vehículo tiene forma diferente de encender"""
        pass
    
    @abstractmethod
    def stop_engine(self) -> str:
        """Cada vehículo tiene forma diferente de apagar"""
        pass
    
    @abstractmethod
    def get_fuel_type(self) -> str:
        """Tipo de combustible varía por vehículo"""
        pass
    
    # Template method - define algoritmo general
    def start_trip(self) -> List[str]:
        """
        TEMPLATE METHOD PATTERN
        Define los pasos generales, subclases implementan detalles
        """
        steps = []
        steps.append("🔍 Checking vehicle condition...")
        steps.append(self.start_engine())
        steps.append("🚗 Vehicle ready for trip!")
        self._is_running = True
        return steps
    
    def stop_trip(self) -> List[str]:
        """Template method para terminar viaje"""
        steps = []
        steps.append("🛑 Ending trip...")
        steps.append(self.stop_engine())
        steps.append("🔒 Trip ended safely")
        self._is_running = False
        return steps
    
    @property
    def is_running(self) -> bool:
        return self._is_running
    
    def get_info(self) -> str:
        """Información común de todos los vehículos"""
        return f"{self.year} {self.brand} {self.model}"


class Car(Vehicle):
    """
    HERENCIA CONCRETA: Car extends Vehicle
    
    CONCEPTOS CLAVE:
    - Implementación de métodos abstractos
    - Extensión de funcionalidad
    - super() para reutilizar código padre
    """
    
    def __init__(self, brand: str, model: str, year: int, doors: int = 4):
        super().__init__(brand, model, year)
        self.doors = doors
        self._fuel_level = 100.0  # Porcentaje
    
    def start_engine(self) -> str:
        if self._fuel_level <= 0:
            return "❌ Cannot start - No fuel!"
        return f"🔑 Car engine started - Fuel: {self._fuel_level}%"
    
    def stop_engine(self) -> str:
        return "🔧 Car engine stopped"
    
    def get_fuel_type(self) -> str:
        return "Gasoline"
    
    def drive(self, distance: float) -> str:
        """Funcionalidad específica de Car"""
        if not self.is_running:
            return "❌ Start engine first!"
        
        fuel_consumption = distance * 0.1  # 0.1% por unidad de distancia
        if self._fuel_level < fuel_consumption:
            return "❌ Not enough fuel for this trip!"
        
        self._fuel_level -= fuel_consumption
        return f"🚗 Drove {distance} units - Fuel remaining: {self._fuel_level:.1f}%"


class ElectricCar(Vehicle):
    """
    HERENCIA CON VARIACIÓN: ElectricCar
    
    CONCEPTOS CLAVE:
    - Misma interface, implementación diferente
    - Atributos específicos del subtipo
    - Override de comportamiento
    """
    
    def __init__(self, brand: str, model: str, year: int, battery_capacity: float):
        super().__init__(brand, model, year)
        self.battery_capacity = battery_capacity  # kWh
        self._battery_level = 100.0  # Porcentaje
    
    def start_engine(self) -> str:
        if self._battery_level <= 5:
            return "❌ Cannot start - Battery too low!"
        return f"⚡ Electric motor started - Battery: {self._battery_level}%"
    
    def stop_engine(self) -> str:
        return "🔌 Electric motor stopped"
    
    def get_fuel_type(self) -> str:
        return "Electric"
    
    def charge(self, hours: float) -> str:
        """Funcionalidad específica de ElectricCar"""
        charge_rate = 10.0  # 10% por hora
        charge_amount = min(hours * charge_rate, 100.0 - self._battery_level)
        self._battery_level += charge_amount
        return f"🔋 Charged for {hours}h - Battery now: {self._battery_level:.1f}%"
    
    def get_range(self) -> float:
        """Retorna rango estimado en km"""
        return (self._battery_level / 100.0) * self.battery_capacity * 5  # 5km por kWh


# ========================================
# PILAR 3: POLIMORFISMO
# ========================================

class VehicleFleet:
    """
    DEMOSTRACIÓN DE POLIMORFISMO
    
    CONCEPTOS CLAVE:
    - Interface común para diferentes tipos
    - Runtime method resolution
    - Duck typing complementario
    """
    
    def __init__(self):
        self.vehicles: List[Vehicle] = []
    
    def add_vehicle(self, vehicle: Vehicle):
        """Acepta cualquier subtipo de Vehicle"""
        self.vehicles.append(vehicle)
    
    def start_all_vehicles(self) -> Dict[str, List[str]]:
        """
        POLIMORFISMO EN ACCIÓN
        Cada vehículo responde de manera diferente al mismo mensaje
        """
        results = {}
        for i, vehicle in enumerate(self.vehicles):
            results[f"{vehicle.get_info()}"] = vehicle.start_trip()
        return results
    
    def get_fleet_info(self) -> List[Dict]:
        """Información de toda la flota usando polimorfismo"""
        fleet_info = []
        for vehicle in self.vehicles:
            info = {
                'info': vehicle.get_info(),
                'fuel_type': vehicle.get_fuel_type(),  # Método polimórfico
                'is_running': vehicle.is_running,
                'type': type(vehicle).__name__
            }
            
            # Duck typing - si tiene batería, incluir nivel
            if hasattr(vehicle, '_battery_level'):
                info['battery_level'] = vehicle._battery_level
            elif hasattr(vehicle, '_fuel_level'):
                info['fuel_level'] = vehicle._fuel_level
            
            fleet_info.append(info)
        
        return fleet_info


# ========================================
# PILAR 4: ABSTRACCIÓN
# ========================================

class PaymentProcessor(ABC):
    """
    ABSTRACCIÓN: Define interface sin implementación
    
    CONCEPTOS CLAVE:
    - Contract definition
    - Implementation hiding
    - Standardized interface
    """
    
    @abstractmethod
    def validate_payment(self, amount: float, **kwargs) -> bool:
        """Validar datos de pago"""
        pass
    
    @abstractmethod
    def process_payment(self, amount: float, **kwargs) -> Dict:
        """Procesar pago y retornar resultado"""
        pass
    
    @abstractmethod
    def get_transaction_fee(self, amount: float) -> float:
        """Calcular comisión"""
        pass
    
    # Método concreto común
    def generate_receipt(self, transaction_result: Dict) -> str:
        """Template para generar recibo"""
        if transaction_result.get('success', False):
            return f"""
📧 PAYMENT RECEIPT
Amount: ${transaction_result['amount']:.2f}
Fee: ${transaction_result['fee']:.2f}
Transaction ID: {transaction_result['transaction_id']}
Status: SUCCESS ✅
            """.strip()
        else:
            return f"""
❌ PAYMENT FAILED
Error: {transaction_result.get('error', 'Unknown error')}
            """.strip()


class CreditCardProcessor(PaymentProcessor):
    """Implementación concreta para tarjetas de crédito"""
    
    def validate_payment(self, amount: float, **kwargs) -> bool:
        card_number = kwargs.get('card_number', '')
        cvv = kwargs.get('cvv', '')
        
        # Validaciones básicas
        if amount <= 0 or amount > 10000:  # Límite de $10,000
            return False
        
        if len(card_number) != 16 or not card_number.isdigit():
            return False
        
        if len(cvv) != 3 or not cvv.isdigit():
            return False
        
        return True
    
    def process_payment(self, amount: float, **kwargs) -> Dict:
        import uuid
        
        if not self.validate_payment(amount, **kwargs):
            return {
                'success': False,
                'error': 'Invalid payment details',
                'amount': amount
            }
        
        fee = self.get_transaction_fee(amount)
        
        # Simular procesamiento
        return {
            'success': True,
            'amount': amount,
            'fee': fee,
            'transaction_id': str(uuid.uuid4())[:8],
            'processor': 'Credit Card'
        }
    
    def get_transaction_fee(self, amount: float) -> float:
        return amount * 0.029  # 2.9%


class PayPalProcessor(PaymentProcessor):
    """Implementación concreta para PayPal"""
    
    def validate_payment(self, amount: float, **kwargs) -> bool:
        email = kwargs.get('email', '')
        
        if amount <= 0 or amount > 5000:  # Límite menor que credit card
            return False
        
        if '@' not in email or '.' not in email:
            return False
        
        return True
    
    def process_payment(self, amount: float, **kwargs) -> Dict:
        import uuid
        
        if not self.validate_payment(amount, **kwargs):
            return {
                'success': False,
                'error': 'Invalid PayPal details',
                'amount': amount
            }
        
        fee = self.get_transaction_fee(amount)
        
        return {
            'success': True,
            'amount': amount,
            'fee': fee,
            'transaction_id': f"PP-{str(uuid.uuid4())[:8]}",
            'processor': 'PayPal'
        }
    
    def get_transaction_fee(self, amount: float) -> float:
        return amount * 0.034 + 0.30  # 3.4% + $0.30


# ========================================
# TESTING Y DEMOSTRACIÓN
# ========================================

def demonstrate_oop_principles():
    """Demostración completa de principios OOP"""
    
    print("=" * 60)
    print("🏛️  DEMOSTRACIÓN DE PRINCIPIOS OOP")
    print("=" * 60)
    
    # 1. ENCAPSULACIÓN
    print("\n1️⃣  ENCAPSULACIÓN:")
    account = BankAccount("ACC-001", 1000.0)
    print(f"Initial: {account}")
    
    account.deposit(500.0)
    print(f"After deposit: {account}")
    
    success = account.withdraw(200.0)
    print(f"Withdrawal success: {success}, Balance: ${account.balance}")
    
    # Intentar acceder a atributo privado (fallará)
    print(f"Transaction history length: {len(account.get_transaction_history())}")
    
    # 2. HERENCIA Y POLIMORFISMO
    print("\n2️⃣  HERENCIA Y POLIMORFISMO:")
    
    # Crear flota de vehículos
    fleet = VehicleFleet()
    
    car = Car("Toyota", "Camry", 2023, doors=4)
    electric_car = ElectricCar("Tesla", "Model 3", 2023, battery_capacity=75.0)
    
    fleet.add_vehicle(car)
    fleet.add_vehicle(electric_car)
    
    # Polimorfismo: mismo método, comportamiento diferente
    start_results = fleet.start_all_vehicles()
    for vehicle, steps in start_results.items():
        print(f"\n🚗 {vehicle}:")
        for step in steps:
            print(f"  {step}")
    
    # Información de flota (polimorfismo + duck typing)
    print("\n📊 Fleet Information:")
    for info in fleet.get_fleet_info():
        print(f"  {info}")
    
    # 3. ABSTRACCIÓN
    print("\n3️⃣  ABSTRACCIÓN:")
    
    # Diferentes procesadores de pago
    processors = [
        CreditCardProcessor(),
        PayPalProcessor()
    ]
    
    payments = [
        {'amount': 100.0, 'card_number': '1234567890123456', 'cvv': '123'},
        {'amount': 50.0, 'email': 'user@example.com'}
    ]
    
    for processor, payment_data in zip(processors, payments):
        result = processor.process_payment(**payment_data)
        receipt = processor.generate_receipt(result)
        print(f"\n💳 {type(processor).__name__}:")
        print(receipt)


if __name__ == "__main__":
    demonstrate_oop_principles()


# ========================================
# EJERCICIOS PARA PRACTICAR
# ========================================

class PracticeExercises:
    """
    Ejercicios para dominar OOP fundamentals
    """
    
    @staticmethod
    def exercise_1_shape_hierarchy():
        """
        EJERCICIO 1: Jerarquía de Formas Geométricas
        
        Implementa:
        - Shape (clase abstracta)
        - Circle, Rectangle, Triangle (subclases)
        - Métodos: area(), perimeter(), get_info()
        - Polimorfismo en lista de shapes
        """
        print("📝 EJERCICIO 1: Implementar jerarquía de shapes")
        print("   - Clase abstracta Shape")
        print("   - Subclases: Circle, Rectangle, Triangle")
        print("   - Polimorfismo para calcular áreas")
    
    @staticmethod
    def exercise_2_employee_system():
        """
        EJERCICIO 2: Sistema de Empleados
        
        Implementa:
        - Employee (base class)
        - FullTimeEmployee, PartTimeEmployee, Contractor
        - Diferentes métodos de cálculo de salario
        - Encapsulación de datos sensibles
        """
        print("📝 EJERCICIO 2: Sistema de empleados")
        print("   - Herencia con diferentes tipos")
        print("   - Encapsulación de información salary")
        print("   - Polimorfismo en cálculo de pagos")
    
    @staticmethod
    def exercise_3_inventory_system():
        """
        EJERCICIO 3: Sistema de Inventario
        
        Implementa:
        - Product (con encapsulación)
        - Category hierarchy
        - Inventory manager
        - Observer pattern para stock alerts
        """
        print("📝 EJERCICIO 3: Sistema de inventario")
        print("   - Encapsulación de stock levels")
        print("   - Herencia para categorías")
        print("   - Abstracción para notifications")


# TIP PARA ENTREVISTAS
def oop_interview_tips():
    """
    Tips específicos para entrevistas OOP
    """
    tips = """
    
🎯 TIPS PARA ENTREVISTAS OOP:
    
1. SIEMPRE MENCIONA LOS 4 PILARES:
   - Encapsulación: Data hiding + controlled access
   - Herencia: Code reuse + is-a relationship
   - Polimorfismo: Same interface, different behavior
   - Abstracción: Hide complexity, show interface
    
2. JUSTIFICA TUS DECISIONES:
   - ¿Por qué elegiste herencia vs composición?
   - ¿Cuándo usar abstract classes vs interfaces?
   - ¿Cómo balanceas flexibilidad vs simplicidad?
    
3. PRINCIPIOS SOLID (próximo):
   - Single Responsibility
   - Open/Closed
   - Liskov Substitution
   - Interface Segregation
   - Dependency Inversion
    
4. PATTERNS COMUNES:
   - Factory Method
   - Observer
   - Strategy
   - Template Method
    
5. PYTHON-SPECIFIC:
   - @property decorators
   - __magic__ methods
   - Duck typing vs explicit inheritance
   - ABC module usage
    """
    
    print(tips)
