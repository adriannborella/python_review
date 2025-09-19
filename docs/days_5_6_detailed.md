# Días 5-6: Manejo de Excepciones y Context Managers
## Exception Handling + Context Managers + Args/Kwargs Mastery

---

# **DÍA 5: Exception Handling y Defensive Programming**

## **Primera Hora: Teoría y Conceptos**

### **0:00-0:15 - Connection to Previous Days**
```python
# Review: Los decoradores del día 4 pueden manejar excepciones
@retry(max_attempts=3)
def fragile_operation():
    # Hoy aprenderemos a manejar estas situaciones robustamente
    pass

# Objetivo: Escribir código robusto que maneja errores elegantemente
```

### **0:15-0:45 - Exception Hierarchy y Best Practices**

#### **Python Exception Hierarchy:**
```python
"""
BaseException
 +-- SystemExit
 +-- KeyboardInterrupt
 +-- GeneratorExit
 +-- Exception
      +-- StopIteration
      +-- ArithmeticError
      |    +-- ZeroDivisionError
      |    +-- OverflowError
      +-- LookupError
      |    +-- IndexError
      |    +-- KeyError
      +-- ValueError
      +-- TypeError
      +-- OSError
           +-- FileNotFoundError
           +-- PermissionError
"""

# Regla fundamental: Catch específico, no genérico
try:
    value = my_dict['key']
except KeyError:  # ✅ Específico
    value = default_value

try:
    process_data()
except Exception:  # ❌ Muy genérico, evitar
    pass
```

#### **Manejo de Excepciones Avanzado:**
```python
def robust_division(a, b):
    """
    División robusta con manejo completo de errores
    """
    try:
        # Validación de tipos
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("Arguments must be numbers")
        
        # Validación de negocio
        if b == 0:
            raise ValueError("Division by zero not allowed")
        
        result = a / b
        
        # Validación de resultado
        if abs(result) > 1e10:  # Overflow check
            raise OverflowError("Result too large")
            
        return result
        
    except TypeError as e:
        print(f"Type error: {e}")
        raise  # Re-raise para que caller pueda manejar
    except ValueError as e:
        print(f"Value error: {e}")
        return float('inf') if a > 0 else float('-inf')
    except OverflowError as e:
        print(f"Overflow: {e}")
        return float('inf') if (a > 0) == (b > 0) else float('-inf')
    finally:
        # Cleanup code que SIEMPRE se ejecuta
        print(f"Division operation completed for {a}/{b}")

# Multiple exception handling
def process_user_input(data):
    try:
        # Múltiples operaciones que pueden fallar
        parsed = json.loads(data)
        validated = validate_schema(parsed)
        processed = transform_data(validated)
        return processed
        
    except (json.JSONDecodeError, KeyError) as e:
        # Maneja múltiples tipos relacionados
        raise ValueError(f"Invalid input format: {e}")
    except ValidationError as e:
        # Exception específica de dominio
        raise ValueError(f"Validation failed: {e}")
    except Exception as e:
        # Log inesperado pero no crash
        logger.error(f"Unexpected error: {e}")
        raise ProcessingError("Internal processing error")
```

#### **Custom Exceptions para Entrevistas:**
```python
class APIError(Exception):
    """Base exception para API errors"""
    def __init__(self, message, status_code=500, details=None):
        super().__init__(message)
        self.status_code = status_code
        self.details = details or {}
    
    def __str__(self):
        return f"APIError({self.status_code}): {super().__str__()}"

class ValidationError(APIError):
    """Error de validación de datos"""
    def __init__(self, field, message):
        super().__init__(f"Validation failed for {field}: {message}", 
                        status_code=400)
        self.field = field

class RateLimitError(APIError):
    """Error de rate limiting"""
    def __init__(self, retry_after=60):
        super().__init__("Rate limit exceeded", status_code=429)
        self.retry_after = retry_after

# Uso en aplicación real
def api_endpoint(data):
    try:
        if not data.get('email'):
            raise ValidationError('email', 'Email is required')
        
        if check_rate_limit(data['email']):
            raise RateLimitError(retry_after=120)
            
        return process_request(data)
        
    except ValidationError:
        # Log y return error response
        raise
    except RateLimitError as e:
        # Add retry-after header logic
        raise
    except Exception as e:
        # Convert unexpected errors
        raise APIError("Internal server error")
```

### **0:45-1:00 - Exception Patterns for Interview**

```python
# Pattern 1: EAFP (Easier to Ask for Forgiveness than Permission)
def eafp_example(data, key):
    """Pythonic way - try first, handle exception"""
    try:
        return data[key].upper()
    except KeyError:
        return "default"
    except AttributeError:
        return str(data[key]).upper()

# vs LBYL (Look Before You Leap) - menos pythónico
def lbyl_example(data, key):
    """Less pythonic - check everything first"""
    if key in data and hasattr(data[key], 'upper'):
        return data[key].upper()
    elif key in data:
        return str(data[key]).upper()
    else:
        return "default"

# Pattern 2: Exception chaining para debugging
def chain_exceptions_example():
    try:
        risky_operation()
    except OriginalError as e:
        raise ProcessingError("Failed to process data") from e
        # Preserva stack trace original + agrega contexto

# Pattern 3: Suppressing exceptions cuando apropiado
from contextlib import suppress

def cleanup_files(filenames):
    for filename in filenames:
        with suppress(FileNotFoundError):
            os.remove(filename)  # No crash si file no existe
```

---

## **Segunda Hora: Práctica Intensiva**

### **1:00-1:30 - Exception Handling Masterclass**

#### **Ejercicio 1: Robust File Processor (15min)**
```python
import json
import csv
from pathlib import Path

class FileProcessor:
    """
    Procesador robusto de archivos con exception handling completo
    """
    
    def __init__(self):
        self.errors = []
        self.processed_count = 0
    
    def process_json_file(self, filepath):
        """
        Procesa archivo JSON con manejo completo de errores
        """
        try:
            # TODO: Implementar con manejo robusto de:
            # - FileNotFoundError
            # - PermissionError  
            # - JSONDecodeError
            # - UnicodeDecodeError
            # - MemoryError (archivos muy grandes)
            
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
            # Validación de estructura
            if not isinstance(data, (list, dict)):
                raise ValueError("JSON must contain list or dict")
                
            return self._process_data(data)
            
        except FileNotFoundError:
            error_msg = f"File not found: {filepath}"
            self.errors.append(error_msg)
            raise FileProcessingError(error_msg)
        except PermissionError:
            # TODO: Implementar manejo
            pass
        except json.JSONDecodeError as e:
            # TODO: Implementar con detalles específicos
            pass
        except Exception as e:
            # TODO: Logging + custom exception
            pass
        finally:
            # TODO: Cleanup y logging
            pass
    
    def _process_data(self, data):
        """Procesa datos validados"""
        # TODO: Implementar processing con error handling interno
        pass

# Custom exceptions para el processor
class FileProcessingError(Exception):
    pass

class DataValidationError(Exception):
    pass
```

#### **Ejercicio 2: API Client con Retry Logic (15min)**
```python
import time
import random
from enum import Enum

class HTTPStatus(Enum):
    OK = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    SERVER_ERROR = 500
    BAD_GATEWAY = 502

class APIClient:
    """
    Cliente API con robust error handling y retry logic
    """
    
    def __init__(self, base_url, max_retries=3):
        self.base_url = base_url
        self.max_retries = max_retries
        self.request_count = 0
    
    def make_request(self, endpoint, data=None):
        """
        Hace request con retry automático para errores recuperables
        """
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                # TODO: Implementar request logic
                response = self._simulate_api_call(endpoint, data)
                
                # Validate response
                if response['status'] == HTTPStatus.OK:
                    return response['data']
                elif response['status'] in [HTTPStatus.BAD_REQUEST, HTTPStatus.UNAUTHORIZED]:
                    # No retry para client errors
                    raise ClientError(f"Client error: {response['status']}")
                else:
                    # Server errors - retry
                    raise ServerError(f"Server error: {response['status']}")
                    
            except ServerError as e:
                last_exception = e
                if attempt < self.max_retries:
                    # Exponential backoff
                    delay = (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(delay)
                    continue
                else:
                    break
            except ClientError:
                # No retry para client errors
                raise
            except Exception as e:
                # Unexpected errors
                last_exception = NetworkError(f"Unexpected error: {e}")
                break
        
        # Si llegamos aquí, todos los retries fallaron
        raise last_exception
    
    def _simulate_api_call(self, endpoint, data):
        """Simula API call con errores aleatorios"""
        self.request_count += 1
        
        # TODO: Simular diferentes tipos de errores/responses
        # Usar random para simular network issues
        pass

# Custom exceptions para API client
class APIException(Exception):
    pass

class ClientError(APIException):
    pass

class ServerError(APIException):
    pass

class NetworkError(APIException):
    pass
```

### **1:30-1:50 - LeetCode con Exception Handling**

#### **Robust LeetCode Solutions:**
```python
def valid_palindrome_robust(s):
    """
    LeetCode #125: Valid Palindrome
    Con robust input validation y error handling
    """
    try:
        # TODO: Implementar con validation completa
        # Handle: None input, non-string input, unicode issues
        if not isinstance(s, str):
            raise TypeError("Input must be string")
        
        # Process usando comprehensions + exception handling
        cleaned = ''.join(char.lower() for char in s if char.isalnum())
        return cleaned == cleaned[::-1]
        
    except TypeError as e:
        print(f"Type error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def climbing_stairs_with_validation(n):
    """
    LeetCode #70: Climbing Stairs
    You are climbing a staircase. It takes n steps to reach the top.

    Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?
    Con input validation y overflow protection
    """
    try:
        # TODO: Implementar con validation
        # Handle: negative n, very large n, non-integer n
        pass
    except (TypeError, ValueError) as e:
        # TODO: Handle input errors
        pass
    except OverflowError as e:
        # TODO: Handle very large results
        pass
```

### **1:50-2:00 - Error Recovery Patterns**

```python
class ResilientDataProcessor:
    """
    Processor que maneja errores gracefully y continúa procesando
    """
    
    def __init__(self):
        self.successful = []
        self.failed = []
        self.error_summary = defaultdict(int)
    
    def process_batch(self, items):
        """
        Procesa batch de items, continúa aunque algunos fallen
        """
        for i, item in enumerate(items):
            try:
                result = self._process_single_item(item)
                self.successful.append((i, result))
            except ValidationError as e:
                self._handle_error(i, item, e, "validation")
            except ProcessingError as e:
                self._handle_error(i, item, e, "processing")
            except Exception as e:
                self._handle_error(i, item, e, "unexpected")
    
    def _handle_error(self, index, item, exception, category):
        """Maneja error individual sin stop processing"""
        # TODO: Log error, update statistics, maybe attempt recovery
        pass
    
    def get_error_report(self):
        """Genera reporte de errores para analysis"""
        # TODO: Usar comprehensions para crear reporte
        pass
```

---

# **DÍA 6: Context Managers y Advanced Args/Kwargs**

## **Primera Hora: Context Managers Deep Dive**

### **0:00-0:15 - Context Manager Fundamentals**
```python
# Built-in context managers que ya conoces
with open('file.txt', 'r') as file:
    content = file.read()
# File se cierra automáticamente

# Lock context manager para threading
import threading
lock = threading.Lock()

with lock:
    # Critical section
    shared_resource += 1
# Lock se libera automáticamente

# Exception handling en context managers
try:
    with open('nonexistent.txt') as file:
        content = file.read()
except FileNotFoundError:
    print("File not found, but file handle cleaned up properly")
```

### **0:15-0:40 - Creating Custom Context Managers**

#### **Method 1: Class-based Context Managers**
```python
class DatabaseConnection:
    """
    Context manager para database connections
    """
    
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connection = None
        self.transaction = None
    
    def __enter__(self):
        """Setup: ejecuta al entrar al with block"""
        print(f"Connecting to {self.connection_string}")
        self.connection = self._create_connection()
        self.transaction = self.connection.begin_transaction()
        return self.connection
    
    def __exit__(self, exc_type, exc_value, traceback):
        """Cleanup: ejecuta al salir del with block"""
        try:
            if exc_type is None:
                # No exception occurred
                self.transaction.commit()
                print("Transaction committed successfully")
            else:
                # Exception occurred
                self.transaction.rollback()
                print(f"Transaction rolled back due to {exc_type.__name__}")
                
        finally:
            if self.connection:
                self.connection.close()
                print("Database connection closed")
        
        # Return False to propagate exception, True to suppress
        return False
    
    def _create_connection(self):
        # TODO: Simular database connection
        return MockDatabaseConnection()

# Uso
try:
    with DatabaseConnection("postgresql://localhost/mydb") as conn:
        conn.execute("INSERT INTO users (name) VALUES ('John')")
        # Si hay exception aquí, rollback automático
        conn.execute("INVALID SQL")  # Esto causará rollback
except Exception as e:
    print(f"Database operation failed: {e}")
```

#### **Method 2: contextlib para Context Managers**
```python
from contextlib import contextmanager
import tempfile
import os

@contextmanager
def temporary_file(content="", suffix=".tmp"):
    """
    Context manager para archivos temporales
    """
    # Setup phase
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix=suffix, delete=False)
    try:
        temp_file.write(content)
        temp_file.flush()
        temp_file.close()
        
        # Yield the resource
        yield temp_file.name
        
    finally:
        # Cleanup phase - ALWAYS executes
        try:
            os.unlink(temp_file.name)
            print(f"Temporary file {temp_file.name} cleaned up")
        except OSError:
            print(f"Warning: Could not delete {temp_file.name}")

# Uso
with temporary_file(content="Hello World", suffix=".txt") as filename:
    with open(filename, 'r') as f:
        print(f.read())  # File se limpia automáticamente

@contextmanager
def timer_context(operation_name):
    """Context manager para timing operations"""
    start_time = time.time()
    try:
        print(f"Starting {operation_name}...")
        yield start_time
    finally:
        end_time = time.time()
        print(f"{operation_name} completed in {end_time - start_time:.4f}s")

# Uso
with timer_context("Data processing"):
    # Operación a medir
    result = sum(x**2 for x in range(100000))
```

#### **Context Managers for Resource Management**
```python
@contextmanager
def managed_resources(*resources):
    """
    Maneja múltiples recursos con cleanup garantizado
    """
    acquired_resources = []
    try:
        # Acquire all resources
        for resource in resources:
            acquired = resource.acquire()
            acquired_resources.append(acquired)
        
        yield acquired_resources
            
    finally:
        # Release in reverse order
        for resource in reversed(acquired_resources):
            try:
                resource.release()
            except Exception as e:
                print(f"Error releasing resource: {e}")

class ConnectionPool:
    """Ejemplo de resource que necesita management"""
    def __init__(self, name):
        self.name = name
    
    def acquire(self):
        print(f"Acquiring {self.name}")
        return self
    
    def release(self):
        print(f"Releasing {self.name}")

# TODO: Uso con múltiples recursos
```

### **0:40-1:00 - Args/Kwargs Advanced Patterns**

```python
def function_signature_mastery():
    """
    Demuestra todos los patrones de argumentos
    """
    
    def complex_function(req_arg, 
                        req_arg2,
                        opt_arg="default",
                        *args,
                        kw_only_arg,
                        kw_only_opt="default",
                        **kwargs):
        """
        Función que demuestra todos los tipos de argumentos
        """
        return {
            'required': [req_arg, req_arg2],
            'optional': opt_arg,
            'varargs': args,
            'keyword_only': kw_only_arg,
            'keyword_optional': kw_only_opt,
            'extra_kwargs': kwargs
        }
    
    # TODO: Ejemplos de llamadas válidas e inválidas
    
def argument_unpacking_mastery():
    """
    Patrones avanzados de unpacking
    """
    
    # Unpacking en function calls
    def api_call(method, url, headers=None, **request_kwargs):
        # TODO: Implementar
        pass
    
    # Data preparation
    request_data = {
        'method': 'POST',
        'url': 'https://api.example.com/users',
        'headers': {'Content-Type': 'application/json'},
        'timeout': 30,
        'retries': 3
    }
    
    # Elegant unpacking
    response = api_call(**request_data)
    
    # Advanced unpacking patterns
    def merge_configs(*config_dicts, **override_kwargs):
        """Merge múltiples configs con overrides"""
        # TODO: Usar dict comprehensions + args/kwargs
        pass

def decorator_with_args_kwargs():
    """
    Decorador que acepta argumentos flexibles
    """
    def flexible_decorator(*dec_args, **dec_kwargs):
        """
        Decorador que puede usarse con o sin argumentos
        @flexible_decorator
        @flexible_decorator(timeout=30)
        @flexible_decorator(retries=3, timeout=30)
        """
        def actual_decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # TODO: Usar dec_args y dec_kwargs en lógica
                print(f"Decorator args: {dec_args}")
                print(f"Decorator kwargs: {dec_kwargs}")
                return func(*args, **kwargs)
            return wrapper
        
        # Handle different usage patterns
        if len(dec_args) == 1 and callable(dec_args[0]) and not dec_kwargs:
            # Used as @flexible_decorator (without parentheses)
            return actual_decorator(dec_args[0])
        else:
            # Used as @flexible_decorator(...) (with arguments)
            return actual_decorator
    
    return flexible_decorator
```

---

## **Segunda Hora: Proyecto Integrador + LeetCode**

### **1:00-1:30 - Proyecto: Robust Data Pipeline**

```python
class RobustDataPipeline:
    """
    Pipeline de datos que combina todos los conceptos de días 5-6
    """
    
    def __init__(self, name, error_policy='continue'):
        self.name = name
        self.error_policy = error_policy  # 'continue', 'stop', 'retry'
        self.metrics = {
            'processed': 0,
            'errors': 0,
            'retries': 0
        }
        self.error_log = []
    
    @contextmanager
    def pipeline_context(self):
        """Context manager para el pipeline completo"""
        start_time = time.time()
        try:
            print(f"Starting pipeline: {self.name}")
            yield self
        except Exception as e:
            print(f"Pipeline {self.name} failed: {e}")
            raise
        finally:
            duration = time.time() - start_time
            print(f"Pipeline {self.name} completed in {duration:.2f}s")
            print(f"Metrics: {self.metrics}")
    
    def process_data_source(self, source_config, *transformations, **processing_kwargs):
        """
        Procesa data source con transformaciones flexibles
        """
        try:
            # TODO: Implementar usando todos los conceptos:
            # 1. Context managers para resources
            # 2. Exception handling robusto
            # 3. Generators para memory efficiency
            # 4. Args/kwargs para flexibilidad
            
            with self._get_data_source(source_config) as data_source:
                # Generator pipeline
                processed_data = self._apply_transformations(
                    data_source, 
                    transformations, 
                    **processing_kwargs
                )
                
                # Lazy evaluation hasta que se necesite
                return list(processed_data)  # Materialize generator
                
        except Exception as e:
            self._handle_pipeline_error(e)
            if self.error_policy == 'stop':
                raise
            return []
    
    @contextmanager
    def _get_data_source(self, config):
        """Context manager para data sources"""
        # TODO: Implementar context manager para diferentes sources
        pass
    
    def _apply_transformations(self, data_source, transformations, **kwargs):
        """
        Generator que aplica transformaciones con error handling
        """
        for item in data_source:
            try:
                # Apply all transformations in sequence
                result = item
                for transform in transformations:
                    result = transform(result, **kwargs)
                yield result
                self.metrics['processed'] += 1
                
            except Exception as e:
                self._handle_item_error(item, e)
                if self.error_policy == 'continue':
                    continue
                elif self.error_policy == 'stop':
                    raise
    
    def _handle_pipeline_error(self, error):
        """Maneja errores a nivel pipeline"""
        # TODO: Logging, metrics update, recovery logic
        pass
    
    def _handle_item_error(self, item, error):
        """Maneja errores a nivel item individual"""
        # TODO: Error categorization, logging, retry logic
        pass

# Usage example
def test_robust_pipeline():
    # Transformations que pueden fallar
    def validate_item(item, min_value=0):
        if item < min_value:
            raise ValueError(f"Item {item} below minimum {min_value}")
        return item
    
    def transform_item(item, multiplier=2):
        if item > 1000:
            raise OverflowError(f"Item {item} too large")
        return item * multiplier
    
    # Test con data que tiene errores
    test_data = list(range(-5, 1005, 10))  # Incluye valores que fallarán
    
    with RobustDataPipeline("test_pipeline").pipeline_context() as pipeline:
        result = pipeline.process_data_source(
            {'type': 'list', 'data': test_data},
            validate_item,
            transform_item,
            min_value=0,
            multiplier=3
        )
        print(f"Successfully processed {len(result)} items")
```

### **1:30-1:50 - LeetCode Integration**

#### **Problem 1: Implement strStr() con Error Handling**
```python
def str_str_robust(haystack, needle):
    """
    LeetCode #28: Implement strStr()
    Encuentra primera ocurrencia de needle en haystack
    Con robust input validation
    """
    try:
        # TODO: Input validation
        if not isinstance(haystack, str) or not isinstance(needle, str):
            raise TypeError("Both arguments must be strings")
        
        if not needle:  # Empty needle
            return 0
        
        # TODO: Implementar búsqueda eficiente
        # Bonus: implementar KMP algorithm approach
        
    except TypeError as e:
        print(f"Type error: {e}")
        return -1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return -1

@contextmanager
def string_processing_context(string_data):
    """Context manager para string processing con metrics"""
    start_time = time.time()
    operations_count = 0
    
    try:
        yield lambda: operations_count  # Yield counter function
    finally:
        end_time = time.time()
        print(f"String processing: {operations_count} operations in {end_time-start_time:.4f}s")
```

#### **Problem 2: Plus One con Overflow Handling**
```python
def plus_one_robust(digits):
    """
    LeetCode #66: Plus One
    Con overflow detection y memory management
    """
    try:
        # TODO: Implementar con validation
        if not digits or not all(isinstance(d, int) and 0 <= d <= 9 for d in digits):
            raise ValueError("Invalid digit array")
        
        # TODO: Implementar algoritmo usando comprehensions
        # Handle carry propagation elegantemente
        
    except ValueError as e:
        print(f"Validation error: {e}")
        return []
    except MemoryError:
        print("Result too large for memory")
        return []

@contextmanager
def array_processing_session(max_memory_mb=100):
    """Context manager que monitorea memory usage"""
    import psutil
    process = psutil.Process()
    initial_memory = process.memory_info().rss / 1024 / 1024
    
    try:
        yield
    finally:
        final_memory = process.memory_info().rss / 1024 / 1024
        memory_used = final_memory - initial_memory
        print(f"Memory used: {memory_used:.2f} MB")
        
        if memory_used > max_memory_mb:
            print(f"Warning: Memory usage exceeded {max_memory_mb} MB")
```

### **1:50-2:00 - Integration Challenge**

```python
def day5_6_integration_challenge():
    """
    Challenge que combina exception handling + context managers + args/kwargs
    """
    
    class SmartFileProcessor:
        """
        Procesador que usa todos los conceptos de días 5-6
        """
        
        @contextmanager
        def processing_session(self, *files, **config):
            """
            Context manager que maneja múltiples archivos
            """
            opened_files = []
            try:
                # TODO: Open múltiples files con error handling
                for filename in files:
                    try:
                        file_obj = open(filename, 'r', **config)
                        opened_files.append(file_obj)
                    except OSError as e:
                        # Handle individual file errors
                        self._log_file_error(filename, e)
                        if config.get('strict_mode', False):
                            raise
                
                yield opened_files
                
            finally:
                # Cleanup: close all opened files
                for file_obj in opened_files:
                    try:
                        file_obj.close()
                    except Exception as e:
                        print(f"Error closing file: {e}")
        
        def process_files_robust(self, *filenames, **processing_options):
            """
            Procesa múltiples archivos con handling robusto
            """
            try:
                with self.processing_session(*filenames, **processing_options) as files:
                    # TODO: Process usando generators + comprehensions
                    results = []
                    for file_obj in files:
                        try:
                            # Process single file
                            result = self._process_single_file(file_obj, **processing_options)
                            results.append(result)
                        except Exception as e:
                            self._handle_file_processing_error(file_obj.name, e)
                            if not processing_options.get('continue_on_error', True):
                                raise
                    
                    return results
                    
            except Exception as e:
                self._handle_batch_processing_error(e)
                raise
        
        def _process_single_file(self, file_obj, **options):
            """Process individual file con options flexibles"""
            # TODO: Implementar usando args/kwargs patterns
            pass
        
        def _log_file_error(self, filename, error):
            # TODO: Error logging
            pass
        
        def _handle_file_processing_error(self, filename, error):
            # TODO: Error handling específico
            pass
        
        def _handle_batch_processing_error(self, error):
            # TODO: Batch error handling
            pass

# Test the complete system
def test_integration():
    processor = SmartFileProcessor()
    
    # TODO: Test con diferentes scenarios:
    # - Files que existen vs no existen
    # - Different processing options
    # - Error recovery scenarios
    
    test_scenarios = [
        # Scenario 1: All files exist
        {
            'files': ['data1.txt', 'data2.txt'],
            'options': {'continue_on_error': True, 'encoding': 'utf-8'}
        },
        # Scenario 2: Some files missing
        {
            'files': ['existing.txt', 'missing.txt'],
            'options': {'strict_mode': False, 'continue_on_error': True}
        },
        # Scenario 3: Strict mode with errors
        {
            'files': ['corrupted.txt'],
            'options': {'strict_mode': True, 'continue_on_error': False}
        }
    ]
    
    for i, scenario in enumerate(test_scenarios):
        print(f"\n--- Test Scenario {i+1} ---")
        try:
            result = processor.process_files_robust(
                *scenario['files'], 
                **scenario['options']
            )
            print(f"Success: {len(result)} files processed")
        except Exception as e:
            print(f"Scenario failed as expected: {e}")

# Run integration test
test_integration()
```

---

## **Advanced LeetCode Problems with Exception Handling**

### **Problem 3: Longest Common Prefix (Robust Implementation)**
```python
def longest_common_prefix_robust(strs):
    """
    LeetCode #14: Longest Common Prefix
    Con comprehensive input validation y error handling
    """
    try:
        # Input validation
        if not isinstance(strs, list):
            raise TypeError("Input must be a list")
        
        if not strs:
            return ""
        
        if not all(isinstance(s, str) for s in strs):
            raise ValueError("All elements must be strings")
        
        # Edge cases
        if any(s == "" for s in strs):
            return ""
        
        # Main algorithm usando zip + comprehensions
        min_length = min(len(s) for s in strs)
        
        for i in range(min_length):
            chars_at_i = [s[i] for s in strs]
            if len(set(chars_at_i)) != 1:  # Not all same
                return strs[0][:i]
        
        return strs[0][:min_length]
        
    except (TypeError, ValueError) as e:
        print(f"Input error in longest_common_prefix: {e}")
        return ""
    except Exception as e:
        print(f"Unexpected error: {e}")
        return ""

@contextmanager
def string_analysis_context(strings):
    """Context manager para análisis de strings con metrics"""
    analysis_data = {
        'total_chars': sum(len(s) for s in strings),
        'unique_chars': len(set(''.join(strings))),
        'avg_length': sum(len(s) for s in strings) / len(strings) if strings else 0
    }
    
    print(f"Starting analysis of {len(strings)} strings")
    print(f"Total characters: {analysis_data['total_chars']}")
    
    try:
        yield analysis_data
    finally:
        print("String analysis completed")
        print(f"Analysis summary: {analysis_data}")
```

### **Problem 4: Roman to Integer con Context Management**
```python
def roman_to_int_robust(s):
    """
    LeetCode #13: Roman to Integer
    Con validation y context management para conversión
    """
    
    @contextmanager
    def roman_conversion_context(roman_string):
        """Context manager para validar y preparar conversión romana"""
        valid_chars = set('IVXLCDM')
        
        # Validation
        if not isinstance(roman_string, str):
            raise TypeError("Roman numeral must be string")
        
        if not roman_string:
            raise ValueError("Roman numeral cannot be empty")
        
        invalid_chars = set(roman_string) - valid_chars
        if invalid_chars:
            raise ValueError(f"Invalid Roman characters: {invalid_chars}")
        
        print(f"Converting Roman numeral: {roman_string}")
        try:
            yield roman_string.upper()
        finally:
            print("Roman conversion completed")
    
    # Roman values mapping
    roman_values = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50,
        'C': 100, 'D': 500, 'M': 1000
    }
    
    try:
        with roman_conversion_context(s) as clean_roman:
            # TODO: Implementar conversion algorithm
            # Usar comprehensions y exception handling
            total = 0
            for i, char in enumerate(clean_roman):
                value = roman_values[char]
                
                # Look ahead para subtractive notation
                if (i + 1 < len(clean_roman) and 
                    roman_values[clean_roman[i + 1]] > value):
                    total -= value
                else:
                    total += value
            
            return total
            
    except (TypeError, ValueError) as e:
        print(f"Validation error: {e}")
        return 0
    except KeyError as e:
        print(f"Invalid Roman character: {e}")
        return 0
    except Exception as e:
        print(f"Conversion error: {e}")
        return 0
```

### **1:30-1:45 - Custom Context Managers for Common Patterns**

```python
# Context managers útiles para entrevistas
@contextmanager
def suppressed_exceptions(*exception_types, default_return=None):
    """
    Context manager que supprime excepciones específicas
    """
    try:
        yield
    except exception_types as e:
        print(f"Suppressed {type(e).__name__}: {e}")
        return default_return

@contextmanager
def performance_monitor(operation_name, max_time_seconds=10):
    """
    Context manager que monitorea performance y alerta si es lento
    """
    start_time = time.time()
    start_memory = psutil.Process().memory_info().rss
    
    try:
        yield
    finally:
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss
        
        duration = end_time - start_time
        memory_delta = (end_memory - start_memory) / 1024 / 1024  # MB
        
        print(f"{operation_name}:")
        print(f"  Time: {duration:.4f}s")
        print(f"  Memory: {memory_delta:+.2f} MB")
        
        if duration > max_time_seconds:
            print(f"  ⚠️  SLOW: Exceeded {max_time_seconds}s threshold")

@contextmanager
def transaction_simulator(auto_commit=True):
    """
    Simula database transaction con rollback automático
    """
    operations = []
    
    class Transaction:
        def execute(self, operation, *args, **kwargs):
            operations.append((operation, args, kwargs))
            print(f"Executing: {operation} with {args}, {kwargs}")
    
    transaction = Transaction()
    
    try:
        yield transaction
        
        if auto_commit:
            print(f"✅ Transaction committed: {len(operations)} operations")
        
    except Exception as e:
        print(f"❌ Transaction rolled back due to: {e}")
        operations.clear()
        raise

# Usage examples
def demonstrate_context_managers():
    # Example 1: Suppressed exceptions
    with suppressed_exceptions(FileNotFoundError, default_return=[]):
        with open('might_not_exist.txt') as f:
            data = f.readlines()
    
    # Example 2: Performance monitoring
    with performance_monitor("Heavy computation", max_time_seconds=1):
        result = sum(x**2 for x in range(100000))
    
    # Example 3: Transaction simulation
    try:
        with transaction_simulator() as txn:
            txn.execute("INSERT", table="users", data={"name": "John"})
            txn.execute("UPDATE", table="profiles", user_id=123)
            # Si hay exception aquí, rollback automático
            
    except Exception as e:
        print(f"Transaction failed: {e}")
```

### **1:45-2:00 - Advanced Args/Kwargs Patterns**

```python
class FlexibleAPI:
    """
    API class que demuestra advanced args/kwargs patterns
    """
    
    def __init__(self, base_config=None, **default_kwargs):
        self.base_config = base_config or {}
        self.default_kwargs = default_kwargs
    
    def make_request(self, endpoint, *path_segments, method='GET', **request_kwargs):
        """
        Flexible API request method
        
        Examples:
        api.make_request('users')
        api.make_request('users', 123, 'posts', method='GET')
        api.make_request('users', method='POST', data={'name': 'John'})
        """
        
        # Build full URL from segments
        full_path = '/'.join([endpoint] + [str(seg) for seg in path_segments])
        
        # Merge configurations: base < defaults < request_kwargs
        final_config = {**self.base_config, **self.default_kwargs, **request_kwargs}
        
        print(f"{method} {full_path}")
        print(f"Config: {final_config}")
        
        # TODO: Implement actual request logic
        return self._simulate_request(method, full_path, final_config)
    
    def batch_operation(self, operation_name, items, *operation_args, 
                       batch_size=100, parallel=False, **operation_kwargs):
        """
        Ejecuta operación en batch con args/kwargs flexibles
        """
        try:
            with self._batch_context(operation_name, len(items)) as context:
                
                # Process in batches
                for i in range(0, len(items), batch_size):
                    batch = items[i:i + batch_size]
                    
                    try:
                        if parallel:
                            results = self._process_parallel(
                                batch, operation_name, 
                                *operation_args, **operation_kwargs
                            )
                        else:
                            results = [
                                self._execute_operation(
                                    item, operation_name,
                                    *operation_args, **operation_kwargs
                                )
                                for item in batch
                            ]
                        
                        context['processed'] += len(results)
                        context['results'].extend(results)
                        
                    except Exception as e:
                        context['errors'].append((i, str(e)))
                        if not operation_kwargs.get('continue_on_error', True):
                            raise
                
                return context['results']
                
        except Exception as e:
            print(f"Batch operation {operation_name} failed: {e}")
            raise
    
    @contextmanager
    def _batch_context(self, operation_name, total_items):
        """Context manager para batch processing"""
        context = {
            'operation': operation_name,
            'total_items': total_items,
            'processed': 0,
            'errors': [],
            'results': []
        }
        
        start_time = time.time()
        print(f"Starting batch operation: {operation_name} ({total_items} items)")
        
        try:
            yield context
        finally:
            duration = time.time() - start_time
            success_rate = (context['processed'] / total_items * 100) if total_items > 0 else 0
            
            print(f"Batch completed: {context['processed']}/{total_items} items ({success_rate:.1f}%)")
            print(f"Duration: {duration:.2f}s")
            print(f"Errors: {len(context['errors'])}")
    
    def _execute_operation(self, item, operation_name, *args, **kwargs):
        """Execute single operation con flexible args"""
        # TODO: Implement operation dispatch
        operations = {
            'validate': lambda x, *a, **k: self._validate_item(x, *a, **k),
            'transform': lambda x, *a, **k: self._transform_item(x, *a, **k),
            'enrich': lambda x, *a, **k: self._enrich_item(x, *a, **k)
        }
        
        if operation_name not in operations:
            raise ValueError(f"Unknown operation: {operation_name}")
        
        return operations[operation_name](item, *args, **kwargs)
    
    def _validate_item(self, item, *validators, **validation_kwargs):
        """Validate item usando multiple validators"""
        # TODO: Apply all validators with error accumulation
        pass
    
    def _transform_item(self, item, *transformers, **transform_kwargs):
        """Transform item using function composition"""
        # TODO: Apply transformations in sequence
        pass
    
    def _enrich_item(self, item, *enrichers, **enrich_kwargs):
        """Enrich item con additional data"""
        # TODO: Add enrichment data
        pass

# Usage demonstration
def demonstrate_flexible_api():
    api = FlexibleAPI(
        base_config={'timeout': 30},
        default_user_agent='MyApp/1.0'
    )
    
    # Different calling patterns
    api.make_request('users', 123)
    api.make_request('users', 123, 'posts', method='POST', data={'title': 'Hello'})
    
    # Batch operations
    items = list(range(1000))
    results = api.batch_operation(
        'validate',
        items,
        lambda x: x > 0,  # Validator function
        lambda x: x < 1000,  # Another validator
        batch_size=50,
        parallel=False,
        continue_on_error=True,
        min_value=0,
        max_value=999
    )
```

---

## **Assessment y Checkpoint Días 5-6**

### **Skills Validation:**

#### **Exception Handling Mastery Check:**
```python
def exception_handling_interview_question():
    """
    Pregunta típica de entrevista sobre exception handling
    """
    
    # "Implementa una función que procese una lista de URLs,
    # haga requests a cada una, y retorne los resultados exitosos
    # mientras maneja gracefully todos los posibles errores"
    
    def fetch_urls_robust(urls, *request_args, timeout=10, max_retries=2, **request_kwargs):
        """
        Robust URL fetcher con comprehensive error handling
        """
        
        results = {
            'successful': [],
            'failed': [],
            'errors': defaultdict(int)
        }
        
        for url in urls:
            try:
                # TODO: Implementar con proper exception hierarchy
                with timeout_context(timeout):
                    response = make_request_with_retry(
                        url, 
                        max_retries,
                        *request_args,
                        **request_kwargs
                    )
                    results['successful'].append({
                        'url': url,
                        'data': response,
                        'attempt': attempt + 1
                    })
                    
            except TimeoutError:
                # TODO: Handle timeout
                pass
            except ConnectionError:
                # TODO: Handle connection issues
                pass
            except HTTPError as e:
                # TODO: Handle HTTP errors
                pass
            except Exception as e:
                # TODO: Handle unexpected errors
                pass
        
        return results
    
    @contextmanager
    def timeout_context(timeout_seconds):
        """Context manager para timeout handling"""
        # TODO: Implement timeout logic
        yield
    
    def make_request_with_retry(url, max_retries, *args, **kwargs):
        """Request con retry logic y backoff"""
        # TODO: Implement request + retry logic
        pass

# Test the implementation
test_urls = [
    'https://httpbin.org/json',     # Should work
    'https://httpbin.org/status/404', # Should fail with 404
    'https://invalid-url-12345.com',  # Should fail with connection error
    'https://httpbin.org/delay/15'    # Should timeout
]

# results = fetch_urls_robust(test_urls, timeout=5, max_retries=2)
```

#### **Context Manager Mastery Check:**
```python
def context_manager_interview_question():
    """
    "Implementa un context manager para database connection pooling
    que maneje connections, transactions, y cleanup automático"
    """
    
    class ConnectionPool:
        def __init__(self, max_connections=10):
            self.max_connections = max_connections
            self.active_connections = []
            self.available_connections = []
        
        @contextmanager
        def get_connection(self, auto_commit=True):
            """
            Context manager que maneja connection lifecycle
            """
            connection = None
            try:
                # TODO: Acquire connection from pool
                connection = self._acquire_connection()
                
                # Start transaction
                if auto_commit:
                    connection.begin_transaction()
                
                yield connection
                
                # Commit if no exceptions
                if auto_commit and connection.in_transaction():
                    connection.commit()
                    
            except Exception as e:
                # Rollback on any exception
                if connection and connection.in_transaction():
                    try:
                        connection.rollback()
                        print(f"Transaction rolled back due to: {e}")
                    except Exception as rollback_error:
                        print(f"Rollback failed: {rollback_error}")
                raise
            finally:
                # Always return connection to pool
                if connection:
                    self._release_connection(connection)
        
        def _acquire_connection(self):
            # TODO: Pool management logic
            pass
        
        def _release_connection(self, connection):
            # TODO: Return to pool logic
            pass
    
    # Usage demonstration
    pool = ConnectionPool(max_connections=5)
    
    try:
        with pool.get_connection() as conn:
            conn.execute("INSERT INTO users (name) VALUES ('Alice')")
            conn.execute("UPDATE profiles SET updated_at = NOW()")
            # Auto-commit on successful completion
            
    except DatabaseError as e:
        print(f"Database operation failed: {e}")
        # Transaction already rolled back by context manager
```

---

## **Final Integration Project: Exception-Safe File Processing System**

```python
class ProductionFileProcessor:
    """
    Production-ready file processor que demuestra todos los conceptos
    """
    
    def __init__(self, config=None):
        self.config = config or {}
        self.processing_stats = {
            'files_processed': 0,
            'errors_encountered': 0,
            'bytes_processed': 0,
            'processing_time': 0.0
        }
        self.error_details = []
    
    @contextmanager
    def processing_session(self, session_name, **session_config):
        """
        Master context manager para processing sessions
        """
        session_start = time.time()
        session_config = {**self.config, **session_config}
        
        print(f"=== Starting Processing Session: {session_name} ===")
        print(f"Session config: {session_config}")
        
        try:
            # Setup session resources
            with self._setup_session_resources(session_config) as resources:
                yield resources, session_config
                
        except Exception as e:
            print(f"Session {session_name} failed with error: {e}")
            if session_config.get('raise_on_session_error', True):
                raise
        finally:
            session_duration = time.time() - session_start
            self.processing_stats['processing_time'] += session_duration
            print(f"=== Session {session_name} completed in {session_duration:.2f}s ===")
            self._print_session_summary()
    
    @contextmanager
    def _setup_session_resources(self, config):
        """Setup y cleanup de recursos de sesión"""
        resources = {
            'temp_dir': None,
            'log_file': None,
            'connections': []
        }
        
        try:
            # Setup temporary directory
            if config.get('use_temp_dir', False):
                resources['temp_dir'] = tempfile.mkdtemp()
            
            # Setup logging
            if config.get('log_to_file', False):
                resources['log_file'] = open(f"processing_{int(time.time())}.log", 'w')
            
            yield resources
            
        finally:
            # Cleanup resources
            if resources['temp_dir']:
                shutil.rmtree(resources['temp_dir'], ignore_errors=True)
            
            if resources['log_file']:
                resources['log_file'].close()
            
            for conn in resources['connections']:
                try:
                    conn.close()
                except:
                    pass
    
    def process_files_safely(self, file_patterns, *processors, **processing_options):
        """
        Procesa archivos usando patterns + processors flexibles
        """
        session_name = processing_options.get('session_name', 'default')
        
        try:
            with self.processing_session(session_name, **processing_options) as (resources, config):
                
                # Find files matching patterns
                all_files = []
                for pattern in file_patterns:
                    try:
                        matching_files = glob.glob(pattern)
                        all_files.extend(matching_files)
                    except Exception as e:
                        self._log_error(f"Pattern matching failed for {pattern}: {e}")
                
                if not all_files:
                    print("⚠️  No files found matching patterns")
                    return []
                
                print(f"Found {len(all_files)} files to process")
                
                # Process each file
                results = []
                for filepath in all_files:
                    try:
                        with self._file_processing_context(filepath, config) as file_context:
                            # Apply all processors in sequence
                            file_result = filepath
                            for processor in processors:
                                file_result = processor(
                                    file_result, 
                                    context=file_context,
                                    **processing_options
                                )
                            
                            results.append(file_result)
                            self.processing_stats['files_processed'] += 1
                            
                    except Exception as e:
                        self._handle_file_error(filepath, e, config)
                        if not config.get('continue_on_file_error', True):
                            raise
                
                return results
                
        except Exception as e:
            print(f"Session processing failed: {e}")
            if processing_options.get('raise_on_failure', False):
                raise
            return []
    
    @contextmanager
    def _file_processing_context(self, filepath, config):
        """Context manager para processing de archivo individual"""
        file_start_time = time.time()
        file_size = 0
        
        try:
            # Get file info
            file_stats = os.stat(filepath)
            file_size = file_stats.st_size
            
            print(f"  Processing: {filepath} ({file_size} bytes)")
            
            # Create file context
            file_context = {
                'filepath': filepath,
                'size': file_size,
                'start_time': file_start_time,
                'config': config
            }
            
            yield file_context
            
        except OSError as e:
            raise FileProcessingError(f"Cannot access file {filepath}: {e}")
        finally:
            file_duration = time.time() - file_start_time
            self.processing_stats['bytes_processed'] += file_size
            print(f"    ✅ Completed {filepath} in {file_duration:.3f}s")
    
    def _handle_file_error(self, filepath, error, config):
        """Handle individual file processing errors"""
        error_entry = {
            'filepath': filepath,
            'error_type': type(error).__name__,
            'error_message': str(error),
            'timestamp': time.time()
        }
        
        self.error_details.append(error_entry)
        self.processing_stats['errors_encountered'] += 1
        
        # Log based on config
        if config.get('verbose_errors', False):
            print(f"    ❌ Error processing {filepath}: {error}")
        else:
            print(f"    ❌ Error processing {filepath}")
    
    def _log_error(self, message):
        """Central error logging"""
        print(f"ERROR: {message}")
        self.error_details.append({
            'message': message,
            'timestamp': time.time(),
            'type': 'system'
        })
    
    def _print_session_summary(self):
        """Print comprehensive session summary"""
        stats = self.processing_stats
        print(f"\n📊 Processing Summary:")
        print(f"   Files processed: {stats['files_processed']}")
        print(f"   Errors encountered: {stats['errors_encountered']}")
        print(f"   Bytes processed: {stats['bytes_processed']:,}")
        print(f"   Total time: {stats['processing_time']:.2f}s")
        
        if stats['files_processed'] > 0:
            avg_time = stats['processing_time'] / stats['files_processed']
            print(f"   Avg time per file: {avg_time:.3f}s")

# File processors para usar con el sistema
def json_validator(filepath, context=None, **kwargs):
    """Validates JSON file structure"""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # TODO: Add validation logic based on kwargs
        schema = kwargs.get('schema', {})
        if schema:
            validate_against_schema(data, schema)
        
        return {'filepath': filepath, 'valid': True, 'data': data}
        
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON in {filepath}: {e}")
    except Exception as e:
        raise ProcessingError(f"JSON processing failed: {e}")

def csv_transformer(filepath, context=None, **kwargs):
    """Transforms CSV file data"""
    try:
        transformations = kwargs.get('transformations', [])
        
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            transformed_data = []
            
            for row in reader:
                try:
                    # Apply transformations
                    transformed_row = row
                    for transform_func in transformations:
                        transformed_row = transform_func(transformed_row)
                    
                    transformed_data.append(transformed_row)
                    
                except Exception as e:
                    if not kwargs.get('skip_invalid_rows', True):
                        raise
                    print(f"Skipping invalid row: {e}")
            
            return {
                'filepath': filepath, 
                'transformed_data': transformed_data,
                'row_count': len(transformed_data)
            }
            
    except Exception as e:
        raise ProcessingError(f"CSV transformation failed: {e}")

# Custom exceptions
class FileProcessingError(Exception):
    pass

class ValidationError(FileProcessingError):
    pass

class ProcessingError(FileProcessingError):
    pass

# Usage example
def main_processing_example():
    """
    Ejemplo completo que demuestra el sistema en acción
    """
    processor = ProductionFileProcessor({
        'verbose_errors': True,
        'use_temp_dir': True,
        'log_to_file': True
    })
    
    # Define transformations para CSV
    def uppercase_name(row):
        row['name'] = row.get('name', '').upper()
        return row
    
    def add_processing_timestamp(row):
        row['processed_at'] = time.time()
        return row
    
    try:
        # Process JSON files
        json_results = processor.process_files_safely(
            ['data/*.json'],  # File patterns
            json_validator,   # Processor function
            session_name='json_validation',
            schema={'required_fields': ['id', 'name']},
            continue_on_file_error=True
        )
        
        # Process CSV files con transformations
        csv_results = processor.process_files_safely(
            ['data/*.csv'],
            csv_transformer,
            session_name='csv_transformation',
            transformations=[uppercase_name, add_processing_timestamp],
            skip_invalid_rows=True,
            continue_on_file_error=True
        )
        
        print(f"\n🎉 Processing completed!")
        print(f"JSON files processed: {len(json_results)}")
        print(f"CSsV files procesed: {len(csv_results)}")
        
    except Exception as e:
        print(f"💥 Processing pipeline failed: {e}")
        raise

if __name__ == "__main__":
    main_processing_example()
```

---

## **Learning Objectives Checklist**

### **Día 5: Exception Handling**
- [ ] Implemento exception hierarchy personalizada para dominio específico
- [ ] Uso EAFP vs LBYL apropiadamente
- [ ] Manejo múltiples tipos de excepciones en single try block
- [ ] Creo exception chaining para better debugging
- [ ] Implemento retry logic robusto con backoff

### **Día 6: Context Managers**
- [ ] Creo context managers con `__enter__`/`__exit__`
- [ ] Uso `@contextmanager` decorator efectivamente
- [ ] Manejo resource cleanup en presence de exceptions
- [ ] Combino context managers con exception handling
- [ ] Implemento context managers para common patterns (timing, logging, etc.)

### **Args/Kwargs Mastery:**
- [ ] Uso todos los tipos de argumentos (*args, **kwargs, keyword-only)
- [ ] Implemento function signatures flexibles para APIs
- [ ] Combino args/kwargs con decorators y context managers
- [ ] Manejo argument unpacking elegantemente

---

## **Interview Simulation Questions**

### **Technical Deep Dive:**
1. **"Explica la diferencia entre `except Exception` y `except BaseException`"**
2. **"¿Cuándo usarías un context manager vs un try/finally block?"**
3. **"Implementa un decorador que sea también un context manager"**
4. **"¿Cómo manejarías exceptions en un generator?"**

### **Code Review Scenarios:**
```python
# Código problemático para review
def bad_exception_handling(data):
    try:
        result = []
        for item in data:
            try:
                processed = expensive_operation(item)
                result.append(processed)
            except ArithmeticError as e:
                pass  # Swallow all exceptions
            except MemoryError as e:
                pass  # Swallow all exceptions
        return result
    except Exception as e:
        print("Something went wrong")
        raise e

# TODO: Identifica problems y propón mejoras
```

### **System Design Integration:**
- "Diseña error handling strategy para microservices architecture"
- "¿Cómo implementarías circuit breaker pattern usando context managers?"
- "Explica error propagation en distributed systems"

---

## **Preparación para Días 7+ (Algoritmos)**

### **Conceptos que aplicarás:**
- Exception handling en algoritmos recursivos
- Context managers para timing y profiling de algoritmos
- Args/kwargs para algoritmos configurables
- Custom exceptions para algorithm edge cases

### **Pre-work para Semana 2:**
```python
# Practice problems que combinan días 5-6 con algoritmos básicos
def algorithm_with_robust_handling():
    """
    Ejemplos de cómo aplicar exception handling a algoritmos
    """
    
    def binary_search_robust(arr, target, *search_args, **search_kwargs):
        """
        Binary search con comprehensive error handling
        """
        try:
            # Validation
            if not isinstance(arr, (list, tuple)):
                raise TypeError("Array must be list or tuple")
            
            if not arr:
                return -1
            
            # Check if sorted (requirement for binary search)
            if not all(arr[i] <= arr[i+1] for i in range(len(arr)-1)):
                if search_kwargs.get('auto_sort', False):
                    arr = sorted(arr)
                else:
                    raise ValueError("Array must be sorted for binary search")
            
            # Main algorithm
            left, right = 0, len(arr) - 1
            
            with timer_context("Binary Search"):
                while left <= right:
                    mid = (left + right) // 2
                    
                    try:
                        if arr[mid] == target:
                            return mid
                        elif arr[mid] < target:
                            left = mid + 1
                        else:
                            right = mid - 1
                    except (IndexError, TypeError) as e:
                        raise AlgorithmError(f"Search failed at index {mid}: {e}")
                
                return -1  # Not found
                
        except (TypeError, ValueError) as e:
            print(f"Input validation failed: {e}")
            if search_kwargs.get('raise_on_invalid_input', True):
                raise
            return -1
        except AlgorithmError as e:
            print(f"Algorithm execution failed: {e}")
            raise

class AlgorithmError(Exception):
    """Custom exception para algorithm failures"""
    pass

# TODO: Implementar más algoritmos con robust handling
```

---

## **Homework y Extended Practice**

### **Daily Practice Routine:**
```python
def daily_practice_session():
    """
    Rutina diaria para reforzar conceptos días 5-6
    """
    
    # 1. Exception handling drill (10min)
    exception_scenarios = [
        "File not found",
        "Network timeout", 
        "Invalid JSON",
        "Memory overflow",
        "Permission denied"
    ]
    
    # TODO: Para cada scenario, escribir robust handler
    
    # 2. Context manager creation (10min)
    context_manager_challenges = [
        "Database transaction manager",
        "Temporary directory manager", 
        "Performance profiler",
        "Resource lock manager",
        "Logging context manager"
    ]
    
    # TODO: Implementar uno diferente cada día
    
    # 3. Args/kwargs flexibility drill (10min)
    def create_flexible_function_signature():
        """
        Practice creating functions con maximum flexibility
        """
        # TODO: Crear función que pueda llamarse de múltiples formas
        pass

# Schedule: 30min extra practice cada día
```

### **Advanced Challenges (Opcional):**

#### **Challenge 1: Exception-Safe Recursive Algorithms**
```python
def fibonacci_robust(n, memo=None, max_recursion_depth=1000):
    """
    Fibonacci con protection contra stack overflow y memoization
    """
    import sys
    
    if memo is None:
        memo = {}
    
    try:
        # Validation
        if not isinstance(n, int) or n < 0:
            raise ValueError("n must be non-negative integer")
        
        if sys.getrecursionlimit() - len(inspect.stack()) < 100:
            raise RecursionError(f"Approaching recursion limit at n={n}")
        
        # Base cases
        if n in memo:
            return memo[n]
        
        if n <= 1:
            return n
        
        # Recursive case con memoization
        result = fibonacci_robust(n-1, memo, max_recursion_depth) + \
                fibonacci_robust(n-2, memo, max_recursion_depth)
        
        memo[n] = result
        return result
        
    except (ValueError, RecursionError) as e:
        print(f"Fibonacci calculation failed: {e}")
        raise
    except Exception as e:
        raise AlgorithmError(f"Unexpected error in fibonacci({n}): {e}")

# TODO: Test con different values, including edge cases
```

#### **Challenge 2: Multi-threaded Context Manager**
```python
import threading
from contextlib import contextmanager

class ThreadSafeProcessor:
    """
    Processor que maneja concurrency con context managers
    """
    
    def __init__(self):
        self._lock = threading.RLock()
        self._processing_count = 0
        self._results = []
    
    @contextmanager
    def thread_safe_processing(self, thread_id, max_concurrent=5):
        """
        Context manager para processing thread-safe
        """
        acquired = False
        try:
            # Acquire lock con timeout
            acquired = self._lock.acquire(timeout=10)
            if not acquired:
                raise TimeoutError(f"Could not acquire lock for thread {thread_id}")
            
            # Check concurrent processing limit
            if self._processing_count >= max_concurrent:
                raise ResourceError(f"Too many concurrent processes ({self._processing_count})")
            
            self._processing_count += 1
            print(f"Thread {thread_id} started processing ({self._processing_count} active)")
            
            yield thread_id
            
        except Exception as e:
            print(f"Thread {thread_id} encountered error: {e}")
            raise
        finally:
            if acquired:
                self._processing_count -= 1
                self._lock.release()
                print(f"Thread {thread_id} finished ({self._processing_count} active)")

class ResourceError(Exception):
    pass

# TODO: Test con multiple threads
```

---

## **Métricas de Éxito Días 5-6**

### **Technical Mastery Indicators:**
- Escribes exception handling que es específico y útil (no genérico)
- Creas context managers que manejan recursos apropiadamente
- Usas args/kwargs para crear APIs flexibles y elegantes
- Combinas todos los conceptos en solutions robustas

### **Interview Readiness:**
- Puedes explicar cuándo usar cada tipo de exception handling
- Demuestras understanding de resource management
- Justificas design decisions en error handling
- Implementas robust solutions que no crash en edge cases

### **Code Quality Benchmarks:**
```python
def assess_code_quality():
    """
    Self-assessment checklist para días 5-6
    """
    
    quality_checklist = {
        'Exception Handling': [
            "Uso excepciones específicas, no genéricas",
            "Manejo chain exceptions apropiadamente", 
            "Implemento retry logic con backoff",
            "Log errors útilmente sin exponer detalles internos",
            "Recovery strategies donde apropiado"
        ],
        'Context Managers': [
            "Recursos se limpian siempre, incluso con exceptions",
            "Context managers son reusables", 
            "Manejo __exit__ correctamente con exception info",
            "Uso @contextmanager para casos simples",
            "Combino context managers effectively"
        ],
        'Args/Kwargs': [
            "Function signatures son flexibles pero claras",
            "Uso keyword-only arguments donde apropiado",
            "Validation de arguments es robusta",
            "Unpacking patterns son elegantes",
            "Documentation explica argument expectations"
        ]
    }
    
    # TODO: Self-evaluate each item 1-5 scale
    return quality_checklist
```

### **Real-world Application:**
Al final de días 5-6, deberías poder:
- Escribir código production-ready que maneja errores gracefully
- Crear APIs flexibles que pueden evolucionar sin breaking changes
- Manejar recursos de sistema (files, connections, memory) responsablemente
- Debug y troubleshoot problemas complejos usando exception information

### **Momentum hacia Semana 2:**
Los conceptos de días 5-6 son fundamentales para todo lo que viene:
- **Algoritmos robustos** que manejan edge cases
- **Database operations** con proper transaction handling  
- **Web APIs** con comprehensive error responses
- **Concurrent programming** con resource management

**¡Excelente foundation construida!** Ahora tienes las herramientas para escribir código Python profesional y robusto. 🚀

---

## **Tomorrow Preview: Semana 2 - Algoritmos y Estructuras de Datos**

La próxima semana aplicarás todos estos conceptos de robustez y elegancia a algoritmos fundamentales. Cada algoritmo que implementes tendrá:
- Exception handling apropiado
- Performance monitoring con context managers  
- Flexible interfaces usando args/kwargs
- Comprehensive testing y validation

**¡Preparado para el siguiente nivel!** 💪