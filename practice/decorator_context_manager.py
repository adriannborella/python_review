"""
Implementación de un decorador que también funciona como context manager.
Este patrón combina la funcionalidad de decoradores y context managers,
permitiendo usar la misma clase de ambas formas.
"""

import functools
import time
import threading
from contextlib import contextmanager
from typing import Any, Callable, Optional


class TimerDecoratorContextManager:
    """
    Decorador/Context Manager híbrido para timing de operaciones.

    Puede usarse de tres formas:
    1. Como decorador: @TimerDecoratorContextManager()
    2. Como context manager: with TimerDecoratorContextManager("operation"):
    3. Como decorador con parámetros: @TimerDecoratorContextManager(name="my_func")
    """

    def __init__(
        self,
        name: Optional[str] = None,
        log_results: bool = True,
        threshold_warning: float = 1.0,
    ):
        self.name = name
        self.log_results = log_results
        self.threshold_warning = threshold_warning
        self.start_time = None
        self.end_time = None
        self.duration = None

    def __enter__(self):
        """Context manager entrance - start timing"""
        self.start_time = time.time()
        if self.log_results:
            operation_name = self.name or "Operation"
            print(f"🚀 Starting {operation_name}...")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - stop timing and log results"""
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time

        if self.log_results:
            operation_name = self.name or "Operation"
            print(f"✅ {operation_name} completed in {self.duration:.4f}s")

            if self.duration > self.threshold_warning:
                print(
                    f"⚠️  Warning: {operation_name} took longer than {self.threshold_warning}s"
                )

        # Return False to propagate exceptions
        return False

    def __call__(self, func: Callable) -> Callable:
        """
        Decorator functionality - wraps function with timing
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Use the function name if no name was provided
            operation_name = self.name or func.__name__

            # Create a new instance for this specific call
            timer = TimerDecoratorContextManager(
                name=operation_name,
                log_results=self.log_results,
                threshold_warning=self.threshold_warning,
            )

            # Use context manager behavior
            with timer:
                result = func(*args, **kwargs)

            # Store timing info in the function for later access
            if not hasattr(func, "_timing_history"):
                func._timing_history = []
            func._timing_history.append(timer.duration)

            return result

        # Add method to get timing statistics
        def get_timing_stats():
            if not hasattr(wrapper, "_timing_history"):
                return None

            history = wrapper._timing_history
            return {
                "calls": len(history),
                "total_time": sum(history),
                "average_time": sum(history) / len(history),
                "min_time": min(history),
                "max_time": max(history),
            }

        wrapper.get_timing_stats = get_timing_stats
        return wrapper


class ResourceManagerDecoratorContextManager:
    """
    Decorador/Context Manager más avanzado para manejo de recursos.
    Puede manejar múltiples recursos y cleanup automático.
    """

    def __init__(self, *resources, auto_cleanup: bool = True, max_retries: int = 3):
        self.resources = list(resources)
        self.auto_cleanup = auto_cleanup
        self.max_retries = max_retries
        self.acquired_resources = []
        self.lock = threading.RLock()

    def __enter__(self):
        """Acquire all resources"""
        with self.lock:
            try:
                for resource in self.resources:
                    if hasattr(resource, "acquire"):
                        acquired = resource.acquire()
                        self.acquired_resources.append(acquired)
                    else:
                        # Simple resource (like file path)
                        self.acquired_resources.append(resource)

                return self.acquired_resources

            except Exception as e:
                # Cleanup any partially acquired resources
                self._cleanup_resources()
                raise ResourceAcquisitionError(f"Failed to acquire resources: {e}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Release all resources"""
        if self.auto_cleanup:
            self._cleanup_resources()
        return False

    def _cleanup_resources(self):
        """Clean up acquired resources in reverse order"""
        with self.lock:
            for resource in reversed(self.acquired_resources):
                try:
                    if hasattr(resource, "release"):
                        resource.release()
                    elif hasattr(resource, "close"):
                        resource.close()
                except Exception as e:
                    print(f"Warning: Failed to clean up resource {resource}: {e}")

            self.acquired_resources.clear()

    def __call__(self, func: Callable) -> Callable:
        """Decorator functionality"""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create new instance for this call
            manager = ResourceManagerDecoratorContextManager(
                *self.resources,
                auto_cleanup=self.auto_cleanup,
                max_retries=self.max_retries,
            )

            retry_count = 0
            last_exception = None

            while retry_count <= self.max_retries:
                try:
                    with manager as acquired:
                        # Pass acquired resources to the function
                        if acquired:
                            return func(*args, resources=acquired, **kwargs)
                        else:
                            return func(*args, **kwargs)

                except ResourceAcquisitionError as e:
                    last_exception = e
                    retry_count += 1
                    if retry_count <= self.max_retries:
                        wait_time = 2**retry_count  # Exponential backoff
                        print(
                            f"Resource acquisition failed, retrying in {wait_time}s... (attempt {retry_count})"
                        )
                        time.sleep(wait_time)
                    continue
                except Exception as e:
                    # Non-resource errors don't retry
                    raise

            # All retries exhausted
            raise last_exception

        return wrapper


class DatabaseTransactionDecoratorContextManager:
    """
    Ejemplo específico para transacciones de base de datos.
    Combina transaction management con exception handling.
    """

    def __init__(
        self,
        connection_pool=None,
        isolation_level="READ_COMMITTED",
        auto_commit: bool = True,
        rollback_on_error: bool = True,
    ):
        self.connection_pool = connection_pool
        self.isolation_level = isolation_level
        self.auto_commit = auto_commit
        self.rollback_on_error = rollback_on_error
        self.connection = None
        self.transaction = None

    def __enter__(self):
        """Start database transaction"""
        try:
            # Acquire connection from pool
            self.connection = self._get_connection()

            # Start transaction
            self.transaction = self.connection.begin_transaction(
                isolation_level=self.isolation_level
            )

            print(
                f"🔄 Database transaction started (isolation: {self.isolation_level})"
            )
            return self.connection

        except Exception as e:
            self._cleanup_connection()
            raise DatabaseError(f"Failed to start transaction: {e}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Commit or rollback transaction"""
        try:
            if exc_type is None and self.auto_commit:
                # No exception occurred, commit
                if self.transaction:
                    self.transaction.commit()
                    print("✅ Transaction committed successfully")
            else:
                # Exception occurred or auto_commit is False
                if self.transaction and self.rollback_on_error:
                    self.transaction.rollback()
                    if exc_type:
                        print(f"❌ Transaction rolled back due to: {exc_type.__name__}")
                    else:
                        print("🔄 Transaction rolled back (auto_commit disabled)")

        except Exception as cleanup_error:
            print(f"Error during transaction cleanup: {cleanup_error}")
        finally:
            self._cleanup_connection()

        return False  # Don't suppress exceptions

    def __call__(self, func: Callable) -> Callable:
        """Decorator for automatic transaction management"""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            manager = DatabaseTransactionDecoratorContextManager(
                connection_pool=self.connection_pool,
                isolation_level=self.isolation_level,
                auto_commit=self.auto_commit,
                rollback_on_error=self.rollback_on_error,
            )

            with manager as conn:
                # Pass connection to the function
                return func(*args, db_connection=conn, **kwargs)

        return wrapper

    def _get_connection(self):
        """Get connection from pool or create mock connection"""
        if self.connection_pool:
            return self.connection_pool.get_connection()
        else:
            # Mock connection for demonstration
            return MockDatabaseConnection()

    def _cleanup_connection(self):
        """Return connection to pool"""
        if self.connection:
            if self.connection_pool:
                self.connection_pool.return_connection(self.connection)
            else:
                self.connection.close()
            self.connection = None


# Mock classes for demonstration
class MockDatabaseConnection:
    def __init__(self):
        self.in_transaction = False

    def begin_transaction(self, isolation_level="READ_COMMITTED"):
        self.in_transaction = True
        return MockTransaction()

    def close(self):
        self.in_transaction = False
        print("🔌 Database connection closed")


class MockTransaction:
    def commit(self):
        print("💾 Transaction committed to database")

    def rollback(self):
        print("↩️  Transaction rolled back")


# Custom exceptions
class ResourceAcquisitionError(Exception):
    """Raised when resource acquisition fails"""

    pass


class DatabaseError(Exception):
    """Raised when database operations fail"""

    pass


# Usage examples and demonstrations
def demonstrate_timer_decorator_context_manager():
    """Demuestra el uso del TimerDecoratorContextManager"""

    print("=== Timer Decorator/Context Manager Demo ===\n")

    # 1. Como context manager
    print("1. Como Context Manager:")
    with TimerDecoratorContextManager("Manual operation", threshold_warning=0.5):
        time.sleep(0.3)
        result = sum(x**2 for x in range(10000))

    print()

    # 2. Como decorador sin parámetros
    print("2. Como Decorador (sin parámetros):")

    @TimerDecoratorContextManager()
    def slow_function():
        time.sleep(0.2)
        return "Slow operation completed"

    result = slow_function()
    print(f"Result: {result}")

    # 3. Como decorador con parámetros
    print("\n3. Como Decorador (con parámetros):")

    @TimerDecoratorContextManager(name="Fast Math", threshold_warning=0.1)
    def fast_math_operation(n):
        return sum(x**2 for x in range(n))

    result = fast_math_operation(1000)
    print(f"Result: {result}")

    # Mostrar estadísticas de timing
    stats = fast_math_operation.get_timing_stats()
    if stats:
        print(f"Timing stats: {stats}")


def demonstrate_resource_manager():
    """Demuestra el ResourceManagerDecoratorContextManager"""

    print("\n=== Resource Manager Decorator/Context Manager Demo ===\n")

    # Mock resource class
    class MockResource:
        def __init__(self, name):
            self.name = name
            self.acquired = False

        def acquire(self):
            if not self.acquired:
                self.acquired = True
                print(f"📦 Acquired resource: {self.name}")
                return self
            else:
                raise ResourceAcquisitionError(f"Resource {self.name} already acquired")

        def release(self):
            if self.acquired:
                self.acquired = False
                print(f"📤 Released resource: {self.name}")

        def use(self):
            if self.acquired:
                return f"Using {self.name}"
            else:
                raise Exception(f"Resource {self.name} not acquired")

    # Create mock resources
    resource1 = MockResource("Database Connection")
    resource2 = MockResource("File Handle")

    # 1. Como context manager
    print("1. Como Context Manager:")
    try:
        with ResourceManagerDecoratorContextManager(resource1, resource2) as resources:
            for resource in resources:
                if hasattr(resource, "use"):
                    print(f"  {resource.use()}")
    except Exception as e:
        print(f"Error: {e}")

    print()

    # 2. Como decorador
    print("2. Como Decorador:")

    # Reset resources
    resource1.acquired = False
    resource2.acquired = False

    @ResourceManagerDecoratorContextManager(resource1, resource2, max_retries=2)
    def process_with_resources(*args, resources=None, **kwargs):
        if resources:
            results = []
            for resource in resources:
                if hasattr(resource, "use"):
                    results.append(resource.use())
            return results
        return "No resources provided"

    try:
        results = process_with_resources()
        print(f"Processing results: {results}")
    except Exception as e:
        print(f"Processing failed: {e}")


def demonstrate_database_transaction():
    """Demuestra el DatabaseTransactionDecoratorContextManager"""

    print("\n=== Database Transaction Decorator/Context Manager Demo ===\n")

    # 1. Como context manager - successful transaction
    print("1. Como Context Manager (éxito):")
    try:
        with DatabaseTransactionDecoratorContextManager(auto_commit=True) as conn:
            print("  Executing: INSERT INTO users (name) VALUES ('Alice')")
            print("  Executing: UPDATE profiles SET active = true")
            # Simula operaciones exitosas
    except Exception as e:
        print(f"Transaction failed: {e}")

    print()

    # 2. Como context manager - failed transaction
    print("2. Como Context Manager (error):")
    try:
        with DatabaseTransactionDecoratorContextManager(auto_commit=True) as conn:
            print("  Executing: INSERT INTO users (name) VALUES ('Bob')")
            raise Exception("Simulated database error")
    except Exception as e:
        print(f"Expected error caught: {e}")

    print()

    # 3. Como decorador
    print("3. Como Decorador:")

    @DatabaseTransactionDecoratorContextManager(isolation_level="SERIALIZABLE")
    def create_user_with_profile(username, email, db_connection=None, **kwargs):
        print(f"  Creating user: {username}")
        print(f"  Setting email: {email}")
        print(f"  Creating user profile")
        return f"User {username} created successfully"

    try:
        result = create_user_with_profile("charlie", "charlie@example.com")
        print(f"Operation result: {result}")
    except Exception as e:
        print(f"Operation failed: {e}")


# Advanced Pattern: Combinable Decorator/Context Manager
class CombinableDecoratorContextManager:
    """
    Patrón avanzado que permite combinar múltiples decoradores/context managers
    """

    def __init__(self, *managers):
        self.managers = managers
        self.active_managers = []

    def __enter__(self):
        """Enter all managers in order"""
        try:
            for manager in self.managers:
                result = manager.__enter__()
                self.active_managers.append((manager, result))

            # Return results from all managers
            return [result for _, result in self.active_managers]

        except Exception as e:
            # Cleanup any managers that were successfully entered
            self._cleanup_managers()
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit all managers in reverse order"""
        return self._cleanup_managers(exc_type, exc_val, exc_tb)

    def _cleanup_managers(self, exc_type=None, exc_val=None, exc_tb=None):
        """Cleanup managers in reverse order"""
        suppress_exception = False

        for manager, _ in reversed(self.active_managers):
            try:
                result = manager.__exit__(exc_type, exc_val, exc_tb)
                # If any manager wants to suppress the exception
                if result:
                    suppress_exception = True
            except Exception as cleanup_error:
                print(f"Error during cleanup of {manager}: {cleanup_error}")

        self.active_managers.clear()
        return suppress_exception

    def __call__(self, func: Callable) -> Callable:
        """Decorator that applies all managers"""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with CombinableDecoratorContextManager(*self.managers):
                return func(*args, **kwargs)

        return wrapper


def demonstrate_combinable_pattern():
    """Demuestra el patrón combinable avanzado"""

    print("\n=== Combinable Decorator/Context Manager Demo ===\n")

    # Combinar timer + resource manager
    timer = TimerDecoratorContextManager("Combined Operation")

    # Mock resource para demostración
    class SimpleResource:
        def __enter__(self):
            print("🔧 Simple resource acquired")
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            print("🔧 Simple resource released")
            return False

    resource = SimpleResource()

    # Combinar múltiples context managers
    combined = CombinableDecoratorContextManager(timer, resource)

    # Usar como context manager
    print("1. Como Context Manager Combinado:")
    with combined:
        time.sleep(0.1)
        print("  Doing work with combined managers...")

    print()

    # Usar como decorador
    print("2. Como Decorador Combinado:")

    @combined
    def complex_operation():
        time.sleep(0.05)
        return "Complex operation completed"

    result = complex_operation()
    print(f"Result: {result}")


# Función principal para ejecutar todas las demostraciones
def main():
    """Ejecuta todas las demostraciones"""

    print("🎯 DECORADOR QUE ES TAMBIÉN CONTEXT MANAGER")
    print("=" * 60)

    try:
        demonstrate_timer_decorator_context_manager()
        demonstrate_resource_manager()
        demonstrate_database_transaction()
        demonstrate_combinable_pattern()

        print("\n🎉 Todas las demostraciones completadas exitosamente!")

    except Exception as e:
        print(f"\n💥 Error durante la demostración: {e}")
        raise


if __name__ == "__main__":
    main()
