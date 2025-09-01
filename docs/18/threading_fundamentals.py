"""
THREADING EN PYTHON - FUNDAMENTOS Y SINCRONIZACIÓN
==================================================

Threading es ideal para I/O-bound tasks debido al GIL.
Esta implementación cubre TODOS los conceptos que aparecen en entrevistas:
- Thread creation y lifecycle
- Synchronization primitives (Lock, RLock, Semaphore, Condition)
- Producer-Consumer pattern
- Thread-safe data structures
- Deadlock prevention

¡Entiende estos patrones y brillarás en entrevistas senior!
"""

import threading
import time
import queue
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock, RLock, Semaphore, Condition, Event

# ========================
# BÁSICOS DE THREADING
# ========================

def basic_thread_example():
    """Ejemplo básico de creación de threads"""
    
    def worker(name, duration):
        print(f"Worker {name} starting...")
        time.sleep(duration)  # Simular I/O work
        print(f"Worker {name} finished after {duration}s")
        return f"Result from {name}"
    
    print("=== BASIC THREADING ===")
    
    # Método 1: Usando Thread class
    threads = []
    for i in range(3):
        t = threading.Thread(target=worker, args=(f"T{i}", i + 1))
        threads.append(t)
        t.start()
    
    # Esperar que todos terminen
    for t in threads:
        t.join()
    
    print("All threads completed\n")

def thread_with_return_value():
    """Threads que retornan valores usando ThreadPoolExecutor"""
    
    def cpu_bound_task(n):
        """Simular task CPU-intensive"""
        result = 0
        for i in range(n * 1000000):
            result += i
        return f"Task {n}: {result}"
    
    print("=== THREADS WITH RETURN VALUES ===")
    
    # ThreadPoolExecutor maneja thread pool automáticamente
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Submit tasks
        futures = []
        for i in range(5):
            future = executor.submit(cpu_bound_task, i + 1)
            futures.append(future)
        
        # Recoger resultados
        for future in as_completed(futures):
            result = future.result()
            print(f"   {result}")
    
    print()

# ========================
# SYNCHRONIZATION PRIMITIVES
# ========================

class ThreadSafeCounter:
    """Contador thread-safe usando Lock"""
    
    def __init__(self):
        self._value = 0
        self._lock = Lock()
    
    def increment(self):
        with self._lock:  # Context manager automáticamente acquire/release
            temp = self._value
            time.sleep(0.0001)  # Simular race condition
            self._value = temp + 1
    
    def decrement(self):
        with self._lock:
            temp = self._value
            time.sleep(0.0001)
            self._value = temp - 1
    
    @property
    def value(self):
        with self._lock:
            return self._value

def demonstrate_race_condition():
    """Demostrar race condition y su solución"""
    
    print("=== RACE CONDITION DEMONSTRATION ===")
    
    # Contador SIN protección
    unsafe_counter = 0
    
    def unsafe_increment():
        nonlocal unsafe_counter
        for _ in range(1000):
            temp = unsafe_counter
            time.sleep(0.000001)  # Simular context switch
            unsafe_counter = temp + 1
    
    # Test unsafe counter
    threads = []
    for _ in range(5):
        t = threading.Thread(target=unsafe_increment)
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print(f"Unsafe counter final value: {unsafe_counter} (expected: 5000)")
    
    # Test safe counter
    safe_counter = ThreadSafeCounter()
    
    def safe_increment():
        for _ in range(1000):
            safe_counter.increment()
    
    threads = []
    for _ in range(5):
        t = threading.Thread(target=safe_increment)
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print(f"Safe counter final value: {safe_counter.value} (expected: 5000)\n")

class BankAccount:
    """Cuenta bancaria thread-safe con RLock"""
    
    def __init__(self, initial_balance=0):
        self.balance = initial_balance
        self._lock = RLock()  # Reentrant Lock
    
    def deposit(self, amount):
        with self._lock:
            print(f"Depositing {amount}")
            self.balance += amount
            print(f"New balance: {self.balance}")
    
    def withdraw(self, amount):
        with self._lock:
            if self.balance >= amount:
                print(f"Withdrawing {amount}")
                self.balance -= amount
                print(f"New balance: {self.balance}")
                return True
            else:
                print(f"Insufficient funds for withdrawal of {amount}")
                return False
    
    def transfer(self, other_account, amount):
        """Transfer entre cuentas - demuestra RLock utility"""
        with self._lock:
            if self.withdraw(amount):
                other_account.deposit(amount)
                return True
            return False
    
    def get_balance(self):
        with self._lock:
            return self.balance

# ========================
# PRODUCER-CONSUMER PATTERN
# ========================

class ProducerConsumer:
    """Implementación clásica Producer-Consumer"""
    
    def __init__(self, max_items=10):
        self.buffer = queue.Queue(maxsize=max_items)
        self.is_producing = True
    
    def producer(self, producer_id):
        """Producer que genera items"""
        for i in range(5):
            if not self.is_producing:
                break
            
            item = f"Item-{producer_id}-{i}"
            self.buffer.put(item)
            print(f"Producer {producer_id} produced: {item}")
            time.sleep(random.uniform(0.1, 0.5))
        
        print(f"Producer {producer_id} finished")
    
    def consumer(self, consumer_id):
        """Consumer que procesa items"""
        while self.is_producing or not self.buffer.empty():
            try:
                # Timeout para evitar bloqueo infinito
                item = self.buffer.get(timeout=1)
                print(f"Consumer {consumer_id} consumed: {item}")
                
                # Simular processing time
                time.sleep(random.uniform(0.2, 0.7))
                self.buffer.task_done()
                
            except queue.Empty:
                continue
        
        print(f"Consumer {consumer_id} finished")
    
    def run_simulation(self):
        """Ejecutar simulación completa"""
        print("=== PRODUCER-CONSUMER PATTERN ===")
        
        threads = []
        
        # Crear producers
        for i in range(2):
            t = threading.Thread(target=self.producer, args=(i,))
            threads.append(t)
            t.start()
        
        # Crear consumers
        for i in range(3):
            t = threading.Thread(target=self.consumer, args=(i,))
            threads.append(t)
            t.start()
        
        # Esperar que producers terminen
        time.sleep(3)
        self.is_producing = False
        
        # Esperar que todos los threads terminen
        for t in threads:
            t.join()
        
        print("Producer-Consumer simulation completed\n")

# ========================
# SYNCHRONIZATION AVANZADA
# ========================

class BoundedBuffer:
    """Buffer limitado usando Condition variable"""
    
    def __init__(self, capacity):
        self.capacity = capacity
        self.buffer = []
        self.condition = Condition()
    
    def put(self, item):
        with self.condition:
            # Esperar hasta que haya espacio
            while len(self.buffer) >= self.capacity:
                print(f"Buffer full, producer waiting...")
                self.condition.wait()
            
            self.buffer.append(item)
            print(f"Produced: {item}, buffer size: {len(self.buffer)}")
            
            # Notificar a consumers esperando
            self.condition.notify_all()
    
    def get(self):
        with self.condition:
            # Esperar hasta que haya items
            while len(self.buffer) == 0:
                print(f"Buffer empty, consumer waiting...")
                self.condition.wait()
            
            item = self.buffer.pop(0)
            print(f"Consumed: {item}, buffer size: {len(self.buffer)}")
            
            # Notificar a producers esperando
            self.condition.notify_all()
            return item

class Semaphore_Example:
    """Ejemplo de Semaphore para limitar recursos"""
    
    def __init__(self, max_connections=3):
        self.semaphore = Semaphore(max_connections)
        self.active_connections = 0
        self.lock = Lock()
    
    def connect(self, client_id):
        """Simular conexión limitada por semaphore"""
        print(f"Client {client_id} attempting to connect...")
        
        with self.semaphore:  # Acquire semaphore
            with self.lock:
                self.active_connections += 1
                print(f"Client {client_id} connected! Active: {self.active_connections}")
            
            # Simular trabajo
            time.sleep(random.uniform(1, 3))
            
            with self.lock:
                self.active_connections -= 1
                print(f"Client {client_id} disconnected. Active: {self.active_connections}")

# ========================
# DEADLOCK PREVENTION
# ========================

class DeadlockDemo:
    """Demostración de deadlock y su prevención"""
    
    def __init__(self):
        self.lock1 = Lock()
        self.lock2 = Lock()
    
    def task_a(self):
        """Task que adquiere locks en orden lock1 → lock2"""
        print("Task A: Acquiring lock1...")
        with self.lock1:
            print("Task A: Got lock1, sleeping...")
            time.sleep(0.5)
            
            print("Task A: Acquiring lock2...")
            with self.lock2:
                print("Task A: Got both locks!")
    
    def task_b_deadlock(self):
        """Task que causa deadlock (orden contrario)"""
        print("Task B: Acquiring lock2...")
        with self.lock2:
            print("Task B: Got lock2, sleeping...")
            time.sleep(0.5)
            
            print("Task B: Acquiring lock1...")
            with self.lock1:
                print("Task B: Got both locks!")
    
    def task_b_safe(self):
        """Task segura (mismo orden de locks)"""
        print("Task B (safe): Acquiring lock1...")
        with self.lock1:
            print("Task B (safe): Got lock1, sleeping...")
            time.sleep(0.5)
            
            print("Task B (safe): Acquiring lock2...")
            with self.lock2:
                print("Task B (safe): Got both locks!")
    
    def demonstrate_deadlock(self):
        """¡CUIDADO! Esto puede causar deadlock real"""
        print("=== DEADLOCK DEMONSTRATION ===")
        print("WARNING: This might hang! Press Ctrl+C if needed")
        
        t1 = threading.Thread(target=self.task_a)
        t2 = threading.Thread(target=self.task_b_deadlock)
        
        t1.start()
        t2.start()
        
        # Timeout para evitar hang indefinido
        t1.join(timeout=2)
        t2.join(timeout=2)
        
        if t1.is_alive() or t2.is_alive():
            print("DEADLOCK DETECTED! Threads are stuck")
        else:
            print("No deadlock occurred")
    
    def demonstrate_safe_locking(self):
        """Demostrar locking seguro"""
        print("\n=== SAFE LOCKING ===")
        
        t1 = threading.Thread(target=self.task_a)
        t2 = threading.Thread(target=self.task_b_safe)
        
        t1.start()
        t2.start()
        
        t1.join()
        t2.join()
        
        print("Safe locking completed successfully\n")

# ========================
# THREAD-SAFE DATA STRUCTURES
# ========================

class ThreadSafeDict:
    """Dictionary thread-safe usando RLock"""
    
    def __init__(self):
        self._dict = {}
        self._lock = RLock()
    
    def __setitem__(self, key, value):
        with self._lock:
            self._dict[key] = value
    
    def __getitem__(self, key):
        with self._lock:
            return self._dict[key]
    
    def __delitem__(self, key):
        with self._lock:
            del self._dict[key]
    
    def __contains__(self, key):
        with self._lock:
            return key in self._dict
    
    def get(self, key, default=None):
        with self._lock:
            return self._dict.get(key, default)
    
    def setdefault(self, key, default):
        with self._lock:
            return self._dict.setdefault(key, default)
    
    def pop(self, key, default=None):
        with self._lock:
            return self._dict.pop(key, default)
    
    def keys(self):
        with self._lock:
            return list(self._dict.keys())
    
    def values(self):
        with self._lock:
            return list(self._dict.values())
    
    def items(self):
        with self._lock:
            return list(self._dict.items())
    
    def __len__(self):
        with self._lock:
            return len(self._dict)
    
    def __str__(self):
        with self._lock:
            return str(self._dict)

class ThreadSafeList:
    """Lista thread-safe con operaciones atómicas"""
    
    def __init__(self):
        self._list = []
        self._lock = Lock()
    
    def append(self, item):
        with self._lock:
            self._list.append(item)
    
    def pop(self, index=-1):
        with self._lock:
            if self._list:
                return self._list.pop(index)
            raise IndexError("pop from empty list")
    
    def __getitem__(self, index):
        with self._lock:
            return self._list[index]
    
    def __setitem__(self, index, value):
        with self._lock:
            self._list[index] = value
    
    def __len__(self):
        with self._lock:
            return len(self._list)
    
    def extend(self, items):
        with self._lock:
            self._list.extend(items)
    
    def safe_iterate(self):
        """Iteración segura - retorna copia"""
        with self._lock:
            return self._list[:]

# ========================
# PATRONES AVANZADOS
# ========================

class WorkerPool:
    """Pool de workers con queue de tareas"""
    
    def __init__(self, num_workers=3):
        self.num_workers = num_workers
        self.task_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.workers = []
        self.shutdown_event = Event()
    
    def worker(self, worker_id):
        """Worker que procesa tareas de la queue"""
        print(f"Worker {worker_id} starting...")
        
        while not self.shutdown_event.is_set():
            try:
                # Get task con timeout
                task_func, args, kwargs = self.task_queue.get(timeout=1)
                
                print(f"Worker {worker_id} processing task...")
                
                try:
                    result = task_func(*args, **kwargs)
                    self.result_queue.put(('success', result))
                except Exception as e:
                    self.result_queue.put(('error', str(e)))
                finally:
                    self.task_queue.task_done()
                    
            except queue.Empty:
                continue
        
        print(f"Worker {worker_id} shutting down...")
    
    def start(self):
        """Iniciar todos los workers"""
        for i in range(self.num_workers):
            worker = threading.Thread(target=self.worker, args=(i,))
            worker.daemon = True  # Die when main program exits
            self.workers.append(worker)
            worker.start()
    
    def submit_task(self, func, *args, **kwargs):
        """Enviar tarea al pool"""
        self.task_queue.put((func, args, kwargs))
    
    def get_result(self, timeout=None):
        """Obtener resultado de tarea completada"""
        return self.result_queue.get(timeout=timeout)
    
    def shutdown(self):
        """Shutdown graceful del pool"""
        print("Shutting down worker pool...")
        
        # Wait for all tasks to complete
        self.task_queue.join()
        
        # Signal workers to shutdown
        self.shutdown_event.set()
        
        # Wait for workers to finish
        for worker in self.workers:
            worker.join(timeout=2)

class RateLimiter:
    """Rate limiter thread-safe usando sliding window"""
    
    def __init__(self, max_requests, window_size):
        self.max_requests = max_requests
        self.window_size = window_size
        self.requests = []
        self.lock = Lock()
    
    def is_allowed(self):
        """Verificar si request está permitido"""
        current_time = time.time()
        
        with self.lock:
            # Remover requests fuera del window
            self.requests = [req_time for req_time in self.requests 
                           if current_time - req_time < self.window_size]
            
            # Verificar si podemos agregar nueva request
            if len(self.requests) < self.max_requests:
                self.requests.append(current_time)
                return True
            
            return False

# ========================
# PERFORMANCE TESTING
# ========================

def io_bound_task(task_id, duration=1):
    """Simular I/O-bound task (file read, network call)"""
    print(f"I/O Task {task_id} starting...")
    time.sleep(duration)  # Simular I/O wait
    print(f"I/O Task {task_id} completed")
    return f"Result-{task_id}"

def cpu_bound_task(task_id, size=1000000):
    """Simular CPU-bound task"""
    print(f"CPU Task {task_id} starting...")
    result = 0
    for i in range(size):
        result += i * i
    print(f"CPU Task {task_id} completed")
    return result

def compare_threading_performance():
    """Comparar performance para different workloads"""
    print("=== THREADING PERFORMANCE COMPARISON ===")
    
    # Test I/O-bound tasks
    print("\n1. I/O-BOUND TASKS:")
    
    # Sequential
    start = time.time()
    for i in range(5):
        io_bound_task(i, 0.5)
    sequential_time = time.time() - start
    
    # Threaded
    start = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(io_bound_task, i, 0.5) for i in range(5)]
        for future in as_completed(futures):
            future.result()
    threaded_time = time.time() - start
    
    print(f"Sequential I/O: {sequential_time:.2f}s")
    print(f"Threaded I/O: {threaded_time:.2f}s")
    print(f"Speedup: {sequential_time/threaded_time:.1f}x")
    
    # Test CPU-bound tasks (threading será PEOR debido al GIL)
    print("\n2. CPU-BOUND TASKS:")
    
    # Sequential
    start = time.time()
    for i in range(3):
        cpu_bound_task(i, 500000)
    sequential_cpu_time = time.time() - start
    
    # Threaded (será más lento por GIL contention)
    start = time.time()
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(cpu_bound_task, i, 500000) for i in range(3)]
        for future in as_completed(futures):
            future.result()
    threaded_cpu_time = time.time() - start
    
    print(f"Sequential CPU: {sequential_cpu_time:.2f}s")
    print(f"Threaded CPU: {threaded_cpu_time:.2f}s")
    print(f"Threading overhead: {threaded_cpu_time/sequential_cpu_time:.1f}x slower")
    print("(This is why we need multiprocessing for CPU-bound tasks!)\n")

# ========================
# TESTING FRAMEWORK
# ========================

def test_thread_safety():
    """Test thread safety mechanisms"""
    print("=== TESTING THREAD SAFETY ===")
    
    # Test thread-safe counter
    demonstrate_race_condition()
    
    # Test bank account transfers
    print("=== BANK ACCOUNT TRANSFERS ===")
    account1 = BankAccount(1000)
    account2 = BankAccount(500)
    
    def random_transfer():
        for _ in range(5):
            if random.choice([True, False]):
                account1.transfer(account2, 50)
            else:
                account2.transfer(account1, 30)
            time.sleep(0.1)
    
    threads = []
    for i in range(3):
        t = threading.Thread(target=random_transfer)
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print(f"Final balances: Account1: {account1.get_balance()}, Account2: {account2.get_balance()}")
    print(f"Total money: {account1.get_balance() + account2.get_balance()}\n")

def test_advanced_patterns():
    """Test patrones avanzados"""
    
    # Test Producer-Consumer
    pc = ProducerConsumer()
    pc.run_simulation()
    
    # Test Worker Pool
    print("=== WORKER POOL PATTERN ===")
    
    def sample_task(x, y):
        time.sleep(0.5)
        return x * y
    
    pool = WorkerPool(num_workers=2)
    pool.start()
    
    # Submit tasks
    for i in range(5):
        pool.submit_task(sample_task, i, i + 1)
    
    # Collect results
    results = []
    for _ in range(5):
        try:
            status, result = pool.get_result(timeout=3)
            results.append((status, result))
            print(f"   Got result: {status} - {result}")
        except queue.Empty:
            print("   Timeout waiting for result")
    
    pool.shutdown()
    print()

def test_rate_limiter():
    """Test rate limiter"""
    print("=== RATE LIMITER TEST ===")
    
    # Max 3 requests per 2 seconds
    limiter = RateLimiter(max_requests=3, window_size=2)
    
    def make_request(client_id):
        for i in range(5):
            if limiter.is_allowed():
                print(f"Client {client_id} - Request {i}: ALLOWED")
            else:
                print(f"Client {client_id} - Request {i}: RATE LIMITED")
            time.sleep(0.3)
    
    # Múltiples clients haciendo requests
    threads = []
    for client_id in range(2):
        t = threading.Thread(target=make_request, args=(client_id,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print()

if __name__ == "__main__":
    basic_thread_example()
    thread_with_return_value()
    test_thread_safety()
    test_advanced_patterns()
    test_rate_limiter()
    compare_threading_performance()
    
    # Deadlock demo (comentado por seguridad)
    deadlock_demo = DeadlockDemo()
    deadlock_demo.demonstrate_safe_locking()
    print("Deadlock demonstration skipped for safety")
