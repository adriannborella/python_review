"""
DÍA 23 - SEGUNDA HORA: CUSTOM CONTAINERS & METACLASSES
Técnicas avanzadas de Python OOP para nivel senior
Custom containers, metaclasses, y patterns sofisticados
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union, Iterator, Tuple
from collections.abc import MutableSequence, MutableMapping
import operator
import functools
from weakref import WeakKeyDictionary


# ========================================
# CUSTOM CONTAINERS - SEQUENCE PROTOCOL
# ========================================

class CircularList(MutableSequence):
    """
    CUSTOM CONTAINER: Circular List
    
    SEQUENCE PROTOCOL METHODS:
    - __len__, __getitem__, __setitem__, __delitem__, insert
    - __iter__, __contains__, __reversed__
    - extend, append, remove, pop, clear, etc. (inherited from MutableSequence)
    
    FEATURES:
    - Circular indexing (index wraps around)
    - No IndexError for valid circular indices
    - All standard list operations
    """
    
    def __init__(self, items=None):
        self._items = list(items) if items else []
    
    def __len__(self) -> int:
        """Return length of the list"""
        return len(self._items)
    
    def __getitem__(self, index: Union[int, slice]) -> Any:
        """Get item with circular indexing"""
        if not self._items:
            raise IndexError("CircularList is empty")
        
        if isinstance(index, slice):
            # Handle slice objects
            start, stop, step = index.indices(len(self._items))
            return [self._items[i % len(self._items)] for i in range(start, stop, step)]
        
        # Circular indexing for single items
        circular_index = index % len(self._items)
        return self._items[circular_index]
    
    def __setitem__(self, index: Union[int, slice], value: Any):
        """Set item with circular indexing"""
        if not self._items:
            raise IndexError("CircularList is empty")
        
        if isinstance(index, slice):
            # Handle slice assignment
            start, stop, step = index.indices(len(self._items))
            indices = list(range(start, stop, step))
            if len(indices) != len(value):
                raise ValueError("Slice assignment length mismatch")
            for i, v in zip(indices, value):
                self._items[i % len(self._items)] = v
        else:
            circular_index = index % len(self._items)
            self._items[circular_index] = value
    
    def __delitem__(self, index: Union[int, slice]):
        """Delete item(s) - removes from actual list"""
        if isinstance(index, slice):
            del self._items[index]
        else:
            if not self._items:
                raise IndexError("CircularList is empty")
            actual_index = index % len(self._items)
            del self._items[actual_index]
    
    def insert(self, index: int, value: Any):
        """Insert item at index (required by MutableSequence)"""
        if self._items:
            circular_index = index % len(self._items)
            self._items.insert(circular_index, value)
        else:
            self._items.insert(0, value)
    
    def __iter__(self) -> Iterator:
        """Iterate over items (normal, not circular)"""
        return iter(self._items)
    
    def __reversed__(self) -> Iterator:
        """Reverse iterator"""
        return reversed(self._items)
    
    def __contains__(self, item: Any) -> bool:
        """Check if item is in the list"""
        return item in self._items
    
    def __str__(self) -> str:
        """String representation"""
        return f"CircularList({self._items})"
    
    def __repr__(self) -> str:
        """Developer representation"""
        return f"CircularList({self._items!r})"
    
    def rotate(self, n: int = 1):
        """Rotate items n positions (positive = right, negative = left)"""
        if self._items and n:
            n = n % len(self._items)  # Normalize rotation
            self._items = self._items[-n:] + self._items[:-n]
    
    def cycle(self, n: int) -> Iterator:
        """Generator that cycles through items n times"""
        if not self._items:
            return
        
        count = 0
        while count < n:
            for item in self._items:
                yield item
                count += 1
                if count >= n:
                    return


# ========================================
# CUSTOM CONTAINERS - MAPPING PROTOCOL
# ========================================

class CaseInsensitiveDict(MutableMapping):
    """
    CUSTOM MAPPING: Case-Insensitive Dictionary
    
    MAPPING PROTOCOL METHODS:
    - __getitem__, __setitem__, __delitem__, __iter__, __len__
    - keys(), values(), items(), get(), pop(), etc. (inherited)
    
    FEATURES:
    - Case-insensitive key access
    - Preserves original key casing
    - All standard dict operations
    """
    
    def __init__(self, data=None):
        self._data = {}  # Internal storage: lowercase_key -> (original_key, value)
        if data:
            self.update(data)
    
    def __getitem__(self, key: str) -> Any:
        """Get value by key (case-insensitive)"""
        return self._data[key.lower()][1]
    
    def __setitem__(self, key: str, value: Any):
        """Set value by key (case-insensitive, preserves original key)"""
        lower_key = key.lower()
        if lower_key in self._data:
            # Update value, keep original key
            original_key = self._data[lower_key][0]
            self._data[lower_key] = (original_key, value)
        else:
            # New key
            self._data[lower_key] = (key, value)
    
    def __delitem__(self, key: str):
        """Delete key-value pair (case-insensitive)"""
        del self._data[key.lower()]
    
    def __iter__(self) -> Iterator[str]:
        """Iterate over original keys"""
        for original_key, _ in self._data.values():
            yield original_key
    
    def __len__(self) -> int:
        """Return number of items"""
        return len(self._data)
    
    def __contains__(self, key: str) -> bool:
        """Check if key exists (case-insensitive)"""
        return key.lower() in self._data
    
    def __str__(self) -> str:
        """String representation"""
        items = {original_key: value for original_key, value in self._data.values()}
        return str(items)
    
    def __repr__(self) -> str:
        """Developer representation"""
        items = {original_key: value for original_key, value in self._data.values()}
        return f"CaseInsensitiveDict({items!r})"


# ========================================
# METACLASSES FUNDAMENTALS
# ========================================

class SingletonMeta(type):
    """
    METACLASS: Singleton Pattern Implementation
    
    METACLASS METHODS:
    - __new__(cls, name, bases, attrs)
    - __call__(cls, *args, **kwargs)
    
    Garantiza que solo existe una instancia de cada clase
    """
    
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        """Called when creating instance of class"""
        if cls not in cls._instances:
            # Create new instance only if doesn't exist
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
    
    def __new__(mcs, name, bases, attrs):
        """Called when creating the class itself"""
        # Add some debugging info
        attrs['_created_by_singleton_meta'] = True
        return super().__new__(mcs, name, bases, attrs)


class DatabaseConnection(metaclass=SingletonMeta):
    """
    EJEMPLO: Using Singleton Metaclass
    
    No matter how many times you instantiate, same object is returned
    """
    
    def __init__(self, connection_string: str = "default"):
        # Only initialize once
        if not hasattr(self, 'initialized'):
            self.connection_string = connection_string
            self.is_connected = False
            self.initialized = True
            print(f"🔌 Creating database connection: {connection_string}")
    
    def connect(self):
        """Connect to database"""
        if not self.is_connected:
            self.is_connected = True
            print(f"✅ Connected to {self.connection_string}")
    
    def disconnect(self):
        """Disconnect from database"""
        if self.is_connected:
            self.is_connected = False
            print(f"❌ Disconnected from {self.connection_string}")


class ValidationMeta(type):
    """
    METACLASS: Automatic Validation Methods
    
    Automatically creates validation methods for attributes
    """
    
    def __new__(mcs, name, bases, attrs):
        """Create validation methods for attributes with validators"""
        
        # Find attributes that need validation
        validators = {}
        for attr_name, attr_value in list(attrs.items()):
            if attr_name.startswith('validate_'):
                # This is a validator function
                validated_attr = attr_name[9:]  # Remove 'validate_' prefix
                validators[validated_attr] = attr_value
        
        # Create properties with validation
        for attr_name, validator_func in validators.items():
            private_attr = f'_{attr_name}'
            
            def make_property(attr, validator, private):
                def getter(self):
                    return getattr(self, private, None)
                
                def setter(self, value):
                    if not validator(self, value):
                        raise ValueError(f"Invalid value for {attr}: {value}")
                    setattr(self, private, value)
                
                return property(getter, setter)
            
            attrs[attr_name] = make_property(attr_name, validator_func, private_attr)
        
        return super().__new__(mcs, name, bases, attrs)


class User(metaclass=ValidationMeta):
    """
    EJEMPLO: Using Validation Metaclass
    
    Validation methods are automatically converted to properties
    """
    
    def __init__(self, name: str, age: int, email: str):
        self.name = name
        self.age = age
        self.email = email
    
    def validate_name(self, value: str) -> bool:
        """Validate name is non-empty string"""
        return isinstance(value, str) and len(value.strip()) > 0
    
    def validate_age(self, value: int) -> bool:
        """Validate age is reasonable"""
        return isinstance(value, int) and 0 <= value <= 150
    
    def validate_email(self, value: str) -> bool:
        """Validate email format"""
        return isinstance(value, str) and '@' in value and '.' in value
    
    def __str__(self) -> str:
        return f"User(name='{self.name}', age={self.age}, email='{self.email}')"


# ========================================
# ADVANCED PATTERNS WITH METACLASSES
# ========================================

class RegistryMeta(type):
    """
    METACLASS: Automatic Class Registration
    
    Maintains registry of all classes created with this metaclass
    """
    
    registry = {}
    
    def __new__(mcs, name, bases, attrs):
        """Register class when it's created"""
        cls = super().__new__(mcs, name, bases, attrs)
        
        # Register the class
        mcs.registry[name] = cls
        
        # Add registry access method to class
        cls.get_registry = classmethod(lambda c: mcs.registry.copy())
        
        return cls


class APIHandler(metaclass=RegistryMeta):
    """Base API handler class"""
    
    def handle(self, request):
        """Handle API request"""
        return {"status": "success", "handler": self.__class__.__name__}


class UserHandler(APIHandler):
    """Handle user-related requests"""
    
    def handle(self, request):
        return {"status": "success", "handler": "UserHandler", "resource": "users"}


class ProductHandler(APIHandler):
    """Handle product-related requests"""
    
    def handle(self, request):
        return {"status": "success", "handler": "ProductHandler", "resource": "products"}


class OrderHandler(APIHandler):
    """Handle order-related requests"""
    
    def handle(self, request):
        return {"status": "success", "handler": "OrderHandler", "resource": "orders"}


# ========================================
# ADVANCED DECORATOR PATTERNS
# ========================================

class classproperty:
    """
    DESCRIPTOR: Class Property (like @property but for classes)
    
    Allows properties that work on the class itself, not instances
    """
    
    def __init__(self, func):
        self.func = func
    
    def __get__(self, obj, objtype=None):
        """Called when property is accessed"""
        if objtype is None:
            objtype = type(obj)
        return self.func(objtype)


def auto_repr(*attrs):
    """
    CLASS DECORATOR: Automatic __repr__ method
    
    Generates __repr__ based on specified attributes
    """
    def decorator(cls):
        def __repr__(self):
            attr_strs = []
            for attr in attrs:
                if hasattr(self, attr):
                    value = getattr(self, attr)
                    attr_strs.append(f"{attr}={value!r}")
            return f"{cls.__name__}({', '.join(attr_strs)})"
        
        cls.__repr__ = __repr__
        return cls
    
    return decorator


def cached_method(func):
    """
    METHOD DECORATOR: Cache method results
    
    Caches method results based on arguments
    """
    cache_attr = f"_cache_{func.__name__}"
    
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        # Get or create cache for this instance
        if not hasattr(self, cache_attr):
            setattr(self, cache_attr, {})
        cache = getattr(self, cache_attr)
        
        # Create cache key
        key = (args, tuple(sorted(kwargs.items())))
        
        if key not in cache:
            cache[key] = func(self, *args, **kwargs)
        
        return cache[key]
    
    return wrapper


@auto_repr('name', 'age', 'department')
class Employee:
    """
    EJEMPLO: Using Advanced Decorators
    
    Demuestra class decorator y method caching
    """
    
    total_employees = 0  # Class variable
    
    def __init__(self, name: str, age: int, department: str):
        self.name = name
        self.age = age
        self.department = department
        Employee.total_employees += 1
    
    @classproperty
    def employee_count(cls) -> int:
        """Class property - accessible on class itself"""
        return cls.total_employees
    
    @cached_method
    def calculate_bonus(self, performance_rating: float, base_bonus: float = 1000.0) -> float:
        """
        Expensive calculation - results are cached
        """
        print(f"🔄 Calculating bonus for {self.name}...")  # Shows when actually calculated
        import time
        time.sleep(0.1)  # Simulate expensive calculation
        
        return base_bonus * performance_rating * (1 + self.age * 0.01)
    
    def get_info(self) -> dict:
        """Get employee information"""
        return {
            'name': self.name,
            'age': self.age,
            'department': self.department,
            'employee_number': Employee.total_employees
        }


# ========================================
# ADVANCED COMPOSITION PATTERNS
# ========================================

class Mixin:
    """
    BASE MIXIN CLASS
    
    Provides common functionality for multiple inheritance
    """
    pass


class TimestampMixin(Mixin):
    """
    MIXIN: Add timestamp functionality to any class
    
    Provides created_at and updated_at timestamps
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        import datetime
        self.created_at = datetime.datetime.now()
        self.updated_at = self.created_at
    
    def touch(self):
        """Update the updated_at timestamp"""
        import datetime
        self.updated_at = datetime.datetime.now()
    
    @property
    def age_in_seconds(self) -> float:
        """Get age of object in seconds"""
        import datetime
        return (datetime.datetime.now() - self.created_at).total_seconds()


class SerializableMixin(Mixin):
    """
    MIXIN: Add serialization functionality
    
    Provides JSON serialization/deserialization
    """
    
    def to_dict(self) -> dict:
        """Convert object to dictionary"""
        result = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):  # Skip private attributes
                if hasattr(value, 'to_dict'):
                    result[key] = value.to_dict()
                elif isinstance(value, (str, int, float, bool, type(None))):
                    result[key] = value
                else:
                    result[key] = str(value)  # Fallback to string
        return result
    
    def to_json(self) -> str:
        """Convert object to JSON string"""
        import json
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create instance from dictionary"""
        return cls(**data)


class ValidatedMixin(Mixin):
    """
    MIXIN: Add validation functionality
    
    Provides automatic validation on attribute changes
    """
    
    def __setattr__(self, name, value):
        """Override attribute setting to add validation"""
        # Check if there's a validator method
        validator_name = f"validate_{name}"
        if hasattr(self, validator_name):
            validator = getattr(self, validator_name)
            if callable(validator):
                if not validator(value):
                    raise ValueError(f"Invalid value for {name}: {value}")
        
        super().__setattr__(name, value)


class Document(TimestampMixin, SerializableMixin, ValidatedMixin):
    """
    EJEMPLO: Multiple Inheritance with Mixins
    
    Combines functionality from multiple mixins
    """
    
    def __init__(self, title: str, content: str, author: str):
        super().__init__()  # Initialize all mixins
        self.title = title
        self.content = content
        self.author = author
    
    def validate_title(self, value: str) -> bool:
        """Validate title is non-empty"""
        return isinstance(value, str) and len(value.strip()) > 0
    
    def validate_author(self, value: str) -> bool:
        """Validate author is non-empty"""
        return isinstance(value, str) and len(value.strip()) > 0
    
    def __str__(self) -> str:
        return f"Document: '{self.title}' by {self.author}"


# ========================================
# TESTING Y DEMOSTRACIÓN
# ========================================

def demonstrate_custom_containers():
    """Demostración de custom containers"""
    
    print("=" * 60)
    print("📦 DEMOSTRACIÓN DE CUSTOM CONTAINERS")
    print("=" * 60)
    
    # CircularList
    print("\n🔄 CircularList:")
    circular = CircularList([1, 2, 3, 4, 5])
    print(f"Created: {circular}")
    print(f"Normal access [1]: {circular[1]}")
    print(f"Circular access [7]: {circular[7]}")  # Should be circular[2]
    print(f"Negative access [-1]: {circular[-1]}")
    
    # Modify with circular indexing
    circular[10] = "ten"  # Should modify circular[0]
    print(f"After circular[10] = 'ten': {circular}")
    
    # Test rotation
    circular.rotate(2)
    print(f"After rotate(2): {circular}")
    
    # CaseInsensitiveDict
    print("\n🔤 CaseInsensitiveDict:")
    ci_dict = CaseInsensitiveDict()
    ci_dict['Name'] = 'Alice'
    ci_dict['AGE'] = 30
    ci_dict['email'] = 'alice@example.com'
    
    print(f"Created: {ci_dict}")
    print(f"Access 'name': {ci_dict['name']}")  # Should work
    print(f"Access 'NAME': {ci_dict['NAME']}")  # Should work
    print(f"'Email' in dict: {'Email' in ci_dict}")  # Should be True


def demonstrate_metaclasses():
    """Demostración de metaclasses"""
    
    print("\n" + "=" * 60)
    print("🏭 DEMOSTRACIÓN DE METACLASSES")
    print("=" * 60)
    
    # Singleton metaclass
    print("\n🔐 Singleton Metaclass:")
    db1 = DatabaseConnection("postgresql://localhost/db1")
    db2 = DatabaseConnection("postgresql://localhost/db2")  # Should be same instance
    
    print(f"Same instance? {db1 is db2}")
    print(f"Connection string: {db1.connection_string}")  # Should be from first creation
    
    # Validation metaclass
    print("\n✅ Validation Metaclass:")
    try:
        user = User("Alice", 25, "alice@example.com")
        print(f"Created: {user}")
        
        # Test validation
        user.age = 200  # Should work but be unusual
        print(f"Set age to 200: {user}")
        
        user.age = -5  # Should fail
    except ValueError as e:
        print(f"Validation error: {e}")
    
    # Registry metaclass
    print("\n📋 Registry Metaclass:")
    registry = APIHandler.get_registry()
    print(f"Registered handlers: {list(registry.keys())}")
    
    # Test handlers
    user_handler = UserHandler()
    result = user_handler.handle({"action": "get_users"})
    print(f"Handler result: {result}")


def demonstrate_advanced_patterns():
    """Demostración de patterns avanzados"""
    
    print("\n" + "=" * 60)
    print("🎨 DEMOSTRACIÓN DE PATTERNS AVANZADOS")
    print("=" * 60)
    
    # Advanced decorators
    print("\n🏷️  Advanced Decorators:")
    emp1 = Employee("Alice", 30, "Engineering")
    emp2 = Employee("Bob", 25, "Marketing")
    
    print(f"Employee 1: {emp1}")  # auto_repr in action
    print(f"Employee count: {Employee.employee_count}")  # classproperty
    
    # Cached method
    bonus1 = emp1.calculate_bonus(4.5)  # Will calculate
    bonus2 = emp1.calculate_bonus(4.5)  # Will use cache
    print(f"Bonus (first call): ${bonus1:.2f}")
    print(f"Bonus (cached): ${bonus2:.2f}")
    
    # Mixins
    print("\n🔧 Multiple Inheritance with Mixins:")
    doc = Document("Python Guide", "Advanced OOP techniques...", "Senior Dev")
    print(f"Document: {doc}")
    print(f"Age in seconds: {doc.age_in_seconds:.2f}")
    
    # Serialization
    doc_dict = doc.to_dict()
    print(f"Serialized keys: {list(doc_dict.keys())}")
    
    # Validation through mixin
    try:
        doc.title = ""  # Should fail validation
    except ValueError as e:
        print(f"Mixin validation error: {e}")


if __name__ == "__main__":
    demonstrate_custom_containers()
    demonstrate_metaclasses()
    demonstrate_advanced_patterns()


# ========================================
# INTERVIEW TIPS PARA TÉCNICAS AVANZADAS
# ========================================

def advanced_interview_tips():
    """
    Tips específicos para técnicas avanzadas en entrevistas
    """
    
    tips = """
    
🎯 TIPS PARA ENTREVISTAS - TÉCNICAS AVANZADAS:
    
1. CUÁNDO MENCIONAR TÉCNICAS AVANZADAS:
   ✅ Si el problema realmente las requiere
   ✅ Para demostrar conocimiento profundo
   ✅ Cuando pregunten específicamente
   
   ❌ No uses por usar - mantén simplicidad cuando sea posible
   
2. MAGIC METHODS MÁS IMPORTANTES:
   - __str__, __repr__: Siempre implementa estos
   - __eq__, __hash__: Para objetos en sets/dicts
   - __len__, __getitem__: Para containers
   - __enter__, __exit__: Para context managers
   
3. CUSTOM CONTAINERS - CUÁNDO IMPLEMENTAR:
   - Necesitas behavior específico no disponible en built-ins
   - Quieres interface familiar pero con twist
   - Performance requirements específicos
   
4. METACLASSES - USA CON PRECAUCIÓN:
   - Singletons (aunque hay mejores formas)
   - Automatic registration/validation
   - Framework development
   - "Si no estás seguro si necesitas metaclass, no lo necesitas"
   
5. DESCRIPTORS VS PROPERTIES:
   - Properties: Para single class
   - Descriptors: Para reusable validation/logic across classes
   
6. MIXINS VS INHERITANCE:
   - Inheritance: "is-a" relationship
   - Mixins: "can-do" functionality
   - Composition over inheritance cuando sea posible
   
7. CÓMO PRESENTAR EN ENTREVISTA:
   - Empieza simple, agrega complexity gradualmente
   - Explica trade-offs y alternativas
   - Menciona cuándo NO usar estas técnicas
   - Code para maintainability, no para show-off
   
8. RED FLAGS PARA EVITAR:
   - Overengineering simple problems
   - Usar técnicas avanzadas sin justificación
   - No explicar por qué elegiste cierto approach
   - Ignorar readability por cleverness
    
💡 RECUERDA: En entrevistas, claridad > cleverness
    """
    
    print(tips)


# CHECKLIST FINAL DÍA 23
def day23_checklist():
    """
    ✅ CHECKLIST DÍA 23 - PYTHON OOP AVANZADO
    
    MAGIC METHODS:
    □ __str__, __repr__ para representation
    □ __eq__, __hash__ para equality y hashing
    □ Arithmetic methods (__add__, __sub__, etc.)
    □ Container methods (__len__, __getitem__, etc.)
    □ Context manager (__enter__, __exit__)
    
    PROPERTIES & DESCRIPTORS:
    □ @property con getter/setter/deleter
    □ Custom descriptors para validation
    □ Descriptor protocol understanding
    □ Diferencias entre properties y descriptors
    
    CUSTOM CONTAINERS:
    □ MutableSequence protocol
    □ MutableMapping protocol
    □ Implementar container behavior
    □ Handle edge cases apropiadamente
    
    METACLASSES:
    □ Conceptos básicos de metaclasses
    □ __new__ vs __init__ en metaclasses
    □ Class creation process
    □ Cuándo usar y cuándo NO usar
    
    ADVANCED PATTERNS:
    □ Mixins y multiple inheritance
    □ Class decorators
    □ Method caching y optimization
    □ Composition patterns
    
    INTERVIEW SKILLS:
    □ Can explain when to use advanced techniques
    □ Can discuss trade-offs
    □ Knows when NOT to use complex solutions
    □ Can implement clean, readable code
    
    SCORE: ___/24 (Objetivo: 20+ para continuar con día 24)
    """
    pass


if __name__ == "__main__":
    demonstrate_custom_containers()
    demonstrate_metaclasses()
    demonstrate_advanced_patterns()
    print("\n")
    advanced_interview_tips()
    print("\n")
    day23_checklist()