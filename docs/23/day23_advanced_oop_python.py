"""
DÍA 23 - PYTHON OOP AVANZADO
Magic Methods, Properties, Descriptors y técnicas avanzadas
Nivel senior para entrevistas técnicas
"""

from typing import Any, Dict, List, Optional, Union, Iterator
from functools import wraps, total_ordering
from collections.abc import MutableSequence
import operator
import copy


# ========================================
# MAGIC METHODS - DUNDER METHODS
# ========================================

@total_ordering  # Decorator que genera todos los comparison methods
class Money:
    """
    EJEMPLO COMPLETO: Magic Methods para clase Money
    
    MAGIC METHODS CUBIERTOS:
    - __init__, __str__, __repr__
    - __eq__, __lt__ (con @total_ordering)
    - __add__, __sub__, __mul__, __truediv__
    - __hash__, __bool__
    - __getitem__, __setitem__ (para conversiones)
    """
    
    # Class attribute para supported currencies
    SUPPORTED_CURRENCIES = {'USD', 'EUR', 'GBP', 'JPY'}
    EXCHANGE_RATES = {
        ('USD', 'EUR'): 0.85,
        ('USD', 'GBP'): 0.73,
        ('USD', 'JPY'): 110.0,
        ('EUR', 'USD'): 1.18,
        ('EUR', 'GBP'): 0.86,
        ('EUR', 'JPY'): 129.0,
        ('GBP', 'USD'): 1.37,
        ('GBP', 'EUR'): 1.16,
        ('GBP', 'JPY'): 150.0,
        ('JPY', 'USD'): 0.009,
        ('JPY', 'EUR'): 0.008,
        ('JPY', 'GBP'): 0.007,
    }
    
    def __init__(self, amount: float, currency: str = 'USD'):
        if currency not in self.SUPPORTED_CURRENCIES:
            raise ValueError(f"Unsupported currency: {currency}")
        
        self.amount = round(amount, 2)
        self.currency = currency.upper()
    
    # String Representation
    def __str__(self) -> str:
        """Human-readable representation"""
        return f"{self.currency} {self.amount:,.2f}"
    
    def __repr__(self) -> str:
        """Developer-friendly representation"""
        return f"Money({self.amount}, '{self.currency}')"
    
    # Equality and Comparison
    def __eq__(self, other: 'Money') -> bool:
        """Equality comparison - convert to same currency"""
        if not isinstance(other, Money):
            return NotImplemented
        
        # Convert other to self's currency for comparison
        other_converted = self._convert_currency(other, self.currency)
        return abs(self.amount - other_converted.amount) < 0.01
    
    def __lt__(self, other: 'Money') -> bool:
        """Less than comparison - @total_ordering generates the rest"""
        if not isinstance(other, Money):
            return NotImplemented
        
        other_converted = self._convert_currency(other, self.currency)
        return self.amount < other_converted.amount
    
    # Arithmetic Operations
    def __add__(self, other: Union['Money', float, int]) -> 'Money':
        """Addition: Money + Money or Money + number"""
        if isinstance(other, Money):
            other_converted = self._convert_currency(other, self.currency)
            return Money(self.amount + other_converted.amount, self.currency)
        elif isinstance(other, (int, float)):
            return Money(self.amount + other, self.currency)
        return NotImplemented
    
    def __radd__(self, other: Union[float, int]) -> 'Money':
        """Right addition: number + Money"""
        return self.__add__(other)
    
    def __sub__(self, other: Union['Money', float, int]) -> 'Money':
        """Subtraction"""
        if isinstance(other, Money):
            other_converted = self._convert_currency(other, self.currency)
            return Money(self.amount - other_converted.amount, self.currency)
        elif isinstance(other, (int, float)):
            return Money(self.amount - other, self.currency)
        return NotImplemented
    
    def __mul__(self, other: Union[float, int]) -> 'Money':
        """Multiplication: Money * number"""
        if isinstance(other, (int, float)):
            return Money(self.amount * other, self.currency)
        return NotImplemented
    
    def __rmul__(self, other: Union[float, int]) -> 'Money':
        """Right multiplication: number * Money"""
        return self.__mul__(other)
    
    def __truediv__(self, other: Union[float, int]) -> 'Money':
        """Division: Money / number"""
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("Cannot divide money by zero")
            return Money(self.amount / other, self.currency)
        return NotImplemented
    
    # Hash and Boolean
    def __hash__(self) -> int:
        """Make Money hashable - can be used in sets/dicts"""
        # Convert to USD for consistent hashing across currencies
        usd_amount = self._convert_to_usd().amount
        return hash((round(usd_amount, 2), 'USD'))
    
    def __bool__(self) -> bool:
        """Boolean conversion - False if amount is 0"""
        return self.amount != 0
    
    # Container-like behavior for currency conversion
    def __getitem__(self, currency: str) -> 'Money':
        """Get money in different currency: money['EUR']"""
        return self._convert_currency(self, currency)
    
    def __setitem__(self, currency: str, amount: float):
        """Set amount in different currency: money['EUR'] = 100"""
        if currency == self.currency:
            self.amount = round(amount, 2)
        else:
            # Convert amount from given currency to self.currency
            temp_money = Money(amount, currency)
            converted = self._convert_currency(temp_money, self.currency)
            self.amount = converted.amount
    
    # Helper methods
    def _convert_currency(self, money: 'Money', target_currency: str) -> 'Money':
        """Convert money to target currency"""
        if money.currency == target_currency:
            return Money(money.amount, target_currency)
        
        # Get exchange rate
        rate_key = (money.currency, target_currency)
        if rate_key in self.EXCHANGE_RATES:
            rate = self.EXCHANGE_RATES[rate_key]
            return Money(money.amount * rate, target_currency)
        else:
            raise ValueError(f"No exchange rate for {money.currency} -> {target_currency}")
    
    def _convert_to_usd(self) -> 'Money':
        """Convert to USD for hash consistency"""
        if self.currency == 'USD':
            return Money(self.amount, 'USD')
        return self._convert_currency(self, 'USD')
    
    # Additional useful methods
    def abs(self) -> 'Money':
        """Absolute value"""
        return Money(abs(self.amount), self.currency)
    
    def round(self, decimals: int = 2) -> 'Money':
        """Round to specified decimals"""
        return Money(round(self.amount, decimals), self.currency)


# ========================================
# PROPERTIES Y DESCRIPTORS AVANZADOS
# ========================================

class Descriptor:
    """
    BASE DESCRIPTOR CLASS
    
    DESCRIPTOR PROTOCOL:
    - __get__(self, obj, objtype=None)
    - __set__(self, obj, value) 
    - __delete__(self, obj)
    - __set_name__(self, owner, name)
    """
    
    def __init__(self, name: str = None):
        self.name = name
    
    def __set_name__(self, owner, name):
        """Called when descriptor is assigned to class attribute"""
        self.name = name
        self.private_name = f'_{name}'
    
    def __get__(self, obj, objtype=None):
        """Called when attribute is accessed"""
        if obj is None:
            return self
        return getattr(obj, self.private_name, None)
    
    def __set__(self, obj, value):
        """Called when attribute is set"""
        setattr(obj, self.private_name, value)
    
    def __delete__(self, obj):
        """Called when attribute is deleted"""
        delattr(obj, self.private_name)


class ValidatedAttribute(Descriptor):
    """
    DESCRIPTOR CON VALIDACIÓN
    
    Ejemplo de descriptor que valida valores antes de asignar
    """
    
    def __init__(self, validation_func=None, doc=None):
        super().__init__()
        self.validation_func = validation_func
        self.__doc__ = doc
    
    def __set__(self, obj, value):
        if self.validation_func:
            if not self.validation_func(value):
                raise ValueError(f"Invalid value for {self.name}: {value}")
        super().__set__(obj, value)


class TypedAttribute(Descriptor):
    """
    DESCRIPTOR CON TYPE CHECKING
    
    Enforces type checking on assignment
    """
    
    def __init__(self, expected_type, doc=None):
        super().__init__()
        self.expected_type = expected_type
        self.__doc__ = doc
    
    def __set__(self, obj, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"{self.name} must be of type {self.expected_type.__name__}, "
                          f"got {type(value).__name__}")
        super().__set__(obj, value)


class RangeAttribute(Descriptor):
    """
    DESCRIPTOR CON RANGE VALIDATION
    
    Validates value is within specified range
    """
    
    def __init__(self, min_val=None, max_val=None, doc=None):
        super().__init__()
        self.min_val = min_val
        self.max_val = max_val
        self.__doc__ = doc
    
    def __set__(self, obj, value):
        if self.min_val is not None and value < self.min_val:
            raise ValueError(f"{self.name} must be >= {self.min_val}")
        if self.max_val is not None and value > self.max_val:
            raise ValueError(f"{self.name} must be <= {self.max_val}")
        super().__set__(obj, value)


class Person:
    """
    EJEMPLO: Using Advanced Descriptors
    
    Demuestra diferentes tipos de descriptors en acción
    """
    
    # Type-checked attributes
    name = TypedAttribute(str, "Person's name")
    age = TypedAttribute(int, "Person's age")
    
    # Range-validated attributes  
    height = RangeAttribute(0.5, 3.0, "Height in meters")
    weight = RangeAttribute(1.0, 500.0, "Weight in kg")
    
    # Custom validated attribute
    email = ValidatedAttribute(
        lambda x: '@' in x and '.' in x,
        "Valid email address"
    )
    
    def __init__(self, name: str, age: int, height: float, weight: float, email: str):
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight
        self.email = email
    
    @property
    def bmi(self) -> float:
        """Calculated property - BMI"""
        return round(self.weight / (self.height ** 2), 2)
    
    @property
    def age_category(self) -> str:
        """Derived property based on age"""
        if self.age < 13:
            return "Child"
        elif self.age < 18:
            return "Teenager"
        elif self.age < 60:
            return "Adult"
        else:
            return "Senior"
    
    def __str__(self) -> str:
        return f"{self.name} ({self.age}yo, BMI: {self.bmi})"


# ========================================
# ADVANCED PROPERTY PATTERNS
# ========================================

class Temperature:
    """
    ADVANCED PROPERTIES EXAMPLE
    
    Demuestra:
    - Property con setter y deleter
    - Cached properties
    - Property validation
    - Multiple property representations
    """
    
    def __init__(self, celsius: float = 0.0):
        self._celsius = celsius
        self._fahrenheit_cache = None
        self._kelvin_cache = None
    
    @property
    def celsius(self) -> float:
        """Temperature in Celsius"""
        return self._celsius
    
    @celsius.setter
    def celsius(self, value: float):
        """Set temperature in Celsius with validation"""
        if value < -273.15:  # Absolute zero
            raise ValueError("Temperature cannot be below absolute zero (-273.15°C)")
        
        self._celsius = value
        # Invalidate caches
        self._fahrenheit_cache = None
        self._kelvin_cache = None
    
    @celsius.deleter
    def celsius(self):
        """Reset to 0°C"""
        self._celsius = 0.0
        self._fahrenheit_cache = None
        self._kelvin_cache = None
    
    @property
    def fahrenheit(self) -> float:
        """Temperature in Fahrenheit (cached)"""
        if self._fahrenheit_cache is None:
            self._fahrenheit_cache = (self._celsius * 9/5) + 32
        return self._fahrenheit_cache
    
    @fahrenheit.setter
    def fahrenheit(self, value: float):
        """Set temperature via Fahrenheit"""
        celsius_value = (value - 32) * 5/9
        self.celsius = celsius_value  # Use celsius setter for validation
    
    @property
    def kelvin(self) -> float:
        """Temperature in Kelvin (cached)"""
        if self._kelvin_cache is None:
            self._kelvin_cache = self._celsius + 273.15
        return self._kelvin_cache
    
    @kelvin.setter
    def kelvin(self, value: float):
        """Set temperature via Kelvin"""
        celsius_value = value - 273.15
        self.celsius = celsius_value  # Use celsius setter for validation
    
    def __str__(self) -> str:
        return f"{self.celsius:.1f}°C ({self.fahrenheit:.1f}°F, {self.kelvin:.1f}K)"
    
    def __repr__(self) -> str:
        return f"Temperature({self.celsius})"


# ========================================
# CONTEXT MANAGERS PERSONALIZADOS
# ========================================

class Timer:
    """
    CONTEXT MANAGER: Timer para medir performance
    
    PROTOCOLO CONTEXT MANAGER:
    - __enter__(self)
    - __exit__(self, exc_type, exc_val, exc_tb)
    """
    
    def __init__(self, description: str = "Operation"):
        self.description = description
        self.start_time = None
        self.end_time = None
    
    def __enter__(self) -> 'Timer':
        """Enter context - start timing"""
        import time
        self.start_time = time.perf_counter()
        print(f"⏱️  Starting: {self.description}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context - stop timing and report"""
        import time
        self.end_time = time.perf_counter()
        duration = self.end_time - self.start_time
        
        if exc_type is None:
            print(f"✅ Completed: {self.description} in {duration:.4f} seconds")
        else:
            print(f"❌ Failed: {self.description} after {duration:.4f} seconds")
            print(f"   Error: {exc_type.__name__}: {exc_val}")
        
        # Return False to propagate exceptions
        return False
    
    @property
    def duration(self) -> float:
        """Get duration after context exits"""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0.0


class DatabaseTransaction:
    """
    CONTEXT MANAGER: Database Transaction
    
    Simula transacción de base de datos con rollback automático
    """
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.transaction_id = None
        self.operations = []
    
    def __enter__(self) -> 'DatabaseTransaction':
        """Start transaction"""
        import uuid
        self.transaction_id = str(uuid.uuid4())[:8]
        print(f"🔄 Starting transaction {self.transaction_id}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Commit or rollback transaction"""
        if exc_type is None:
            # No exception - commit
            print(f"✅ Committing transaction {self.transaction_id}")
            print(f"   Operations: {len(self.operations)}")
            return True
        else:
            # Exception occurred - rollback
            print(f"🔄 Rolling back transaction {self.transaction_id}")
            print(f"   Reason: {exc_type.__name__}: {exc_val}")
            self._rollback()
            return False  # Don't suppress exception
    
    def execute(self, sql: str, params: tuple = ()):
        """Execute SQL within transaction"""
        operation = f"SQL: {sql[:50]}..." if len(sql) > 50 else f"SQL: {sql}"
        self.operations.append(operation)
        print(f"  📝 {operation}")
        
        # Simulate error for demo
        if "ERROR" in sql.upper():
            raise ValueError("Simulated SQL error")
    
    def _rollback(self):
        """Rollback operations"""
        print(f"   🔙 Rolled back {len(self.operations)} operations")
        self.operations.clear()


# ========================================
# TESTING Y DEMOSTRACIÓN
# ========================================

def demonstrate_magic_methods():
    """Demostración de magic methods"""
    
    print("=" * 60)
    print("🎩 DEMOSTRACIÓN DE MAGIC METHODS")
    print("=" * 60)
    
    # Crear objetos Money
    usd_money = Money(100, 'USD')
    eur_money = Money(85, 'EUR')
    
    print(f"💰 Created: {usd_money} and {eur_money}")
    print(f"💰 Repr: {repr(usd_money)}")
    
    # Arithmetic operations
    total = usd_money + eur_money
    print(f"💰 Addition: {usd_money} + {eur_money} = {total}")
    
    doubled = usd_money * 2
    print(f"💰 Multiplication: {usd_money} * 2 = {doubled}")
    
    half = usd_money / 2
    print(f"💰 Division: {usd_money} / 2 = {half}")
    
    # Comparison
    print(f"💰 Comparison: {usd_money} > {eur_money} = {usd_money > eur_money}")
    print(f"💰 Equality: {usd_money} == Money(100, 'USD') = {usd_money == Money(100, 'USD')}")
    
    # Container-like behavior
    print(f"💰 Currency conversion: {usd_money}['EUR'] = {usd_money['EUR']}")
    
    # Hash and set operations
    money_set = {usd_money, Money(100, 'USD'), eur_money}
    print(f"💰 Set size (should be 2 due to hashing): {len(money_set)}")
    
    # Boolean conversion
    zero_money = Money(0)
    print(f"💰 Boolean: bool({usd_money}) = {bool(usd_money)}")
    print(f"💰 Boolean: bool({zero_money}) = {bool(zero_money)}")


def demonstrate_descriptors():
    """Demostración de descriptors avanzados"""
    
    print("\n" + "=" * 60)
    print("🔍 DEMOSTRACIÓN DE DESCRIPTORS")
    print("=" * 60)
    
    try:
        # Crear persona con descriptors
        person = Person("Alice", 30, 1.70, 65.0, "alice@example.com")
        print(f"👤 Created: {person}")
        print(f"📊 BMI: {person.bmi}")
        print(f"📊 Age Category: {person.age_category}")
        
        # Test validaciones
        print("\n🧪 Testing validations:")
        
        # Type validation
        try:
            person.age = "thirty"  # Should fail
        except TypeError as e:
            print(f"✅ Type validation works: {e}")
        
        # Range validation
        try:
            person.height = 5.0  # Should fail (too tall)
        except ValueError as e:
            print(f"✅ Range validation works: {e}")
        
        # Custom validation
        try:
            person.email = "invalid-email"  # Should fail
        except ValueError as e:
            print(f"✅ Custom validation works: {e}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def demonstrate_properties():
    """Demostración de properties avanzadas"""
    
    print("\n" + "=" * 60)
    print("🌡️  DEMOSTRACIÓN DE PROPERTIES AVANZADAS")
    print("=" * 60)
    
    # Temperature with advanced properties
    temp = Temperature(25.0)
    print(f"🌡️  Created: {temp}")
    
    # Set via different scales
    temp.fahrenheit = 86.0
    print(f"🌡️  After setting Fahrenheit to 86°F: {temp}")
    
    temp.kelvin = 300.0
    print(f"🌡️  After setting Kelvin to 300K: {temp}")
    
    # Test validation
    try:
        temp.celsius = -300.0  # Should fail (below absolute zero)
    except ValueError as e:
        print(f"✅ Temperature validation works: {e}")


def demonstrate_context_managers():
    """Demostración de context managers"""
    
    print("\n" + "=" * 60)
    print("🎯 DEMOSTRACIÓN DE CONTEXT MANAGERS")
    print("=" * 60)
    
    # Timer context manager
    with Timer("Heavy computation simulation"):
        import time
        time.sleep(0.1)  # Simulate work
        result = sum(i**2 for i in range(1000))
        print(f"🔢 Computation result: {result}")
    
    # Database transaction (successful)
    print("\n💾 Successful transaction:")
    with DatabaseTransaction("postgresql://localhost:5432/db") as tx:
        tx.execute("INSERT INTO users (name) VALUES ('Alice')")
        tx.execute("UPDATE users SET age = 30 WHERE name = 'Alice'")
    
    # Database transaction (with error)
    print("\n💾 Failed transaction:")
    try:
        with DatabaseTransaction("postgresql://localhost:5432/db") as tx:
            tx.execute("INSERT INTO users (name) VALUES ('Bob')")
            tx.execute("ERROR: This will cause rollback")  # This will fail
    except ValueError:
        print("Transaction was properly rolled back")


if __name__ == "__main__":
    demonstrate_magic_methods()
    demonstrate_descriptors()
    demonstrate_properties()
    demonstrate_context_managers()


# ========================================
# EJERCICIOS PARA PRACTICAR
# ========================================

class AdvancedExercises:
    """
    Ejercicios avanzados para dominar conceptos
    """
    
    @staticmethod
    def exercise_1_vector_class():
        """
        EJERCICIO 1: Vector Mathematical Class
        
        Implementa clase Vector con:
        - Magic methods para arithmetic (+, -, *, /, **)
        - Comparison methods (<, >, ==, etc.)
        - len(), str(), repr()
        - Indexing y slicing support
        - dot product, cross product methods
        """
        print("📝 EJERCICIO 1: Mathematical Vector class")
        print("   - Arithmetic operations")
        print("   - Comparison methods")  
        print("   - Container protocol")
        print("   - Mathematical operations")
    
    @staticmethod
    def exercise_2_smart_property():
        """
        EJERCICIO 2: Smart Property System
        
        Implementa descriptor que:
        - Cache valores expensive computations
        - Log accesos y modificaciones
        - Validate con custom functions
        - Support lazy loading
        """
        print("📝 EJERCICIO 2: Smart Property Descriptor")
        print("   - Caching mechanism")
        print("   - Access logging")
        print("   - Validation system")
        print("   - Lazy loading")
    
    @staticmethod
    def exercise_3_context_manager_pool():
        """
        EJERCICIO 3: Resource Pool Context Manager
        
        Implementa context manager para:
        - Database connection pool
        - Automatic resource cleanup
        - Resource limits and timeouts
        - Error handling y retry logic
        """
        print("📝 EJERCICIO 3: Resource Pool Context Manager")
        print("   - Connection pooling")
        print("   - Automatic cleanup")
        print("   - Timeout handling")
        print("   - Error recovery")


if __name__ == "__main__":
    demonstrate_magic_methods()
    demonstrate_descriptors()
    demonstrate_properties()
    demonstrate_context_managers()
    
    print("\n" + "="*60)
    print("📚 EJERCICIOS ADICIONALES")
    print("="*60)
    
    exercises = AdvancedExercises()
    exercises.exercise_1_vector_class()
    exercises.exercise_2_smart_property() 
    exercises.exercise_3_context_manager_pool()