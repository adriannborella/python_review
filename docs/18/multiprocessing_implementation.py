"""
MULTIPROCESSING EN PYTHON - SUPERANDO EL GIL
============================================

Multiprocessing crea procesos separados, cada uno con su propio GIL.
Ideal para CPU-bound tasks y verdadero paralelismo.

VENTAJAS:
- Verdadero paralelismo (bypass GIL)
- Aislamiento (crash en un proceso no afecta otros)
- Puede usar todos los CPU cores

DESVENTAJAS:  
- Mayor overhead (crear processes es costoso)
- Communication más compleja (IPC)
- Mayor uso de memoria

CUÁNDO USAR:
- CPU-intensive computations
- Scientific computing
- Image/video processing
- Mathematical calculations
"""

import multiprocessing as mp
import time
import os
import random
from multiprocessing import Process, Pool, Queue, Pipe, Value, Array
from multiprocessing import Lock as MPLock, Manager
from concurrent.futures import ProcessPoolExecutor, as_completed

# ========================
# COMPARACIÓN: THREADING VS MULTIPROCESSING
# ========================

def cpu_intensive_task(n):
    """Task que realmente usa CPU"""
    result = 0
    for i in range(n):
        result += i ** 2
    return result

def io_intensive_task(duration):
    """Task que simula I/O"""
    time.sleep(duration)
    return f"Completed after {duration}s"

def compare_threading_vs_multiprocessing():
    """Comparación directa para different workloads"""
    print("=== THREADING VS MULTIPROCESSING COMPARISON ===\n")
    
    # CPU-bound task comparison
    print("1. CPU-BOUND TASKS (calculating squares):")
    
    task_size = 2000000
    num_tasks = 4
    
    # Sequential
    start = time.time()
    results_seq = []
    for i in range(num_tasks):
        result = cpu_intensive_task(task_size)
        results_seq.append(result)
    sequential_time = time.time() - start
    
    # Threading (será lento por GIL)
    start = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(cpu_intensive_task, task_size) for _ in range(num_tasks)]
        results_thread = [f.result() for f in futures]
    threading_time = time.time() - start
    
    # Multiprocessing (será rápido)
    start = time.time()
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(cpu_intensive_task, task_size) for _ in range(num_tasks)]
        results_mp = [f.result() for f in futures]
    multiprocessing_time = time.time() - start
    
    print(f"   Sequential: {sequential_time:.2f}s")
    print(f"   Threading: {threading_time:.2f}s (GIL limited)")
    print(f"   Multiprocessing: {multiprocessing_time:.2f}s")
    print(f"   MP Speedup: {sequential_time/multiprocessing_time:.1f}x")
    
    # I/O-bound task comparison
    print("\n2. I/O-BOUND TASKS (sleep simulation):")
    
    duration = 0.5
    num_tasks = 8
    
    # Sequential
    start = time.time()
    for _ in range(num_tasks):
        io_intensive_task(duration)
    sequential_io_time = time.time() - start
    
    # Threading (será rápido)
    start = time.time()
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(io_intensive_task, duration) for _ in range(num_tasks)]
        results = [f.result() for f in futures]
    threading_io_time = time.time() - start
    
    # Multiprocessing (overhead innecesario)
    start = time.time()
    with ProcessPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(io_intensive_task, duration) for _ in range(num_tasks)]
        results = [f.result() for f in futures]
    mp_io_time = time.time() - start
    
    print(f"   Sequential: {sequential_io_time:.2f}s")
    print(f"   Threading: {threading_io_time:.2f}s")
    print(f"   Multiprocessing: {mp_io_time:.2f}s")
    print(f"   Threading speedup: {sequential_io_time/threading_io_time:.1f}x")
    print(f"   MP overhead: {mp_io_time/threading_io_time:.1f}x slower than threading\n")

# ========================
# INTER-PROCESS COMMUNICATION
# ========================

def demonstrate_queue_communication():
    """Comunicación entre procesos usando Queue"""
    print("=== INTER-PROCESS COMMUNICATION: QUEUE ===")
    
    def producer(q, producer_id):
        """Producer process"""
        for i in range(5):
            item = f"Item-{producer_id}-{i}"
            q.put(item)
            print(f"Producer {producer_id} produced: {item}")
            time.sleep(0.1)
        
        q.put(None)  # Sentinel value
        print(f"Producer {producer_id} finished")
    
    def consumer(q, consumer_id):
        """Consumer process"""
        while True:
            item = q.get()
            if item is None:
                q.put(None)  # Re-add sentinel for other consumers
                break
            
            print(f"Consumer {consumer_id} consumed: {item}")
            time.sleep(0.2)
        
        print(f"Consumer {consumer_id} finished")
    
    # Crear queue compartida
    q = Queue()
    
    # Crear procesos
    processes = []
    
    # Producer process
    p1 = Process(target=producer, args=(q, 1))
    processes.append(p1)
    
    # Consumer processes
    for i in range(2):
        p = Process(target=consumer, args=(q, i))
        processes.append(p)
    
    # Iniciar todos los procesos
    for p in processes:
        p.start()
    
    # Esperar que terminen
    for p in processes:
        p.join()
    
    print("Queue communication demo completed\n")

def demonstrate_pipe_communication():
    """Comunicación usando Pipe (bidireccional)"""
    print("=== INTER-PROCESS COMMUNICATION: PIPE ===")
    
    def sender(conn, name):
        """Proceso que envía mensajes"""
        for i in range(3):
            message = f"Message {i} from {name}"
            conn.send(message)
            print(f"Sent: {message}")
            time.sleep(0.5)
        
        conn.close()
    
    def receiver(conn, name):
        """Proceso que recibe mensajes"""
        while True:
            try:
                message = conn.recv()
                print(f"Received by {name}: {message}")
            except EOFError:
                break
        
        conn.close()
    
    # Crear pipe
    parent_conn, child_conn = Pipe()
    
    # Crear procesos
    p1 = Process(target=sender, args=(child_conn, "Sender"))
    p2 = Process(target=receiver, args=(parent_conn, "Receiver"))
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()
    
    print("Pipe communication demo completed\n")

def demonstrate_shared_memory():
    """Shared memory entre procesos"""
    print("=== SHARED MEMORY DEMONSTRATION ===")
    
    def worker_with_shared_value(shared_val, lock, worker_id):
        """Worker que modifica shared value"""
        for i in range(5):
            with lock:
                temp = shared_val.value
                time.sleep(0.01)  # Simular processing
                shared_val.value = temp + 1
                print(f"Worker {worker_id}: incremented to {shared_val.value}")
    
    def worker_with_shared_array(shared_arr, lock, worker_id):
        """Worker que modifica shared array"""
        with lock:
            for i in range(len(shared_arr)):
                shared_arr[i] += worker_id
            print(f"Worker {worker_id}: modified array")
    
    # Shared Value
    shared_counter = Value('i', 0)  # 'i' = integer
    lock = MPLock()
    
    processes = []
    for i in range(3):
        p = Process(target=worker_with_shared_value, args=(shared_counter, lock, i))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    print(f"Final shared counter value: {shared_counter.value}")
    
    # Shared Array
    shared_array = Array('d', [1.0, 2.0, 3.0, 4.0])  # 'd' = double
    
    processes = []
    for i in range(3):
        p = Process(target=worker_with_shared_array, args=(shared_array, lock, i + 1))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    print(f"Final shared array: {list(shared_array)}\n")

# ========================
# REAL-WORLD EXAMPLES
# ========================

def parallel_file_processing():
    """Procesamiento paralelo de archivos (simulado)"""
    print("=== PARALLEL FILE PROCESSING ===")
    
    def process_file(filename):
        """Simular procesamiento de archivo"""
        print(f"Processing {filename}...")
        
        # Simular lectura y processing
        time.sleep(random.uniform(0.5, 2.0))
        
        # Simular algún resultado
        word_count = random.randint(100, 1000)
        return (filename, word_count)
    
    # Lista de archivos a procesar
    files = [f"file_{i}.txt" for i in range(10)]
    
    print(f"Processing {len(files)} files...")
    
    # Sequential processing
    start = time.time()
    results_seq = []
    for filename in files:
        result = process_file(filename)
        results_seq.append(result)
    sequential_time = time.time() - start
    
    # Parallel processing
    start = time.time()
    with ProcessPoolExecutor(max_workers=4) as executor:
        results_parallel = list(executor.map(process_file, files))
    parallel_time = time.time() - start
    
    print(f"Sequential processing: {sequential_time:.2f}s")
    print(f"Parallel processing: {parallel_time:.2f}s")
    print(f"Speedup: {sequential_time/parallel_time:.1f}x")
    
    # Mostrar algunos resultados
    print("Sample results:")
    for filename, word_count in results_parallel[:3]:
        print(f"   {filename}: {word_count} words")
    
    print()

def monte_carlo_pi_estimation():
    """Estimación de π usando Monte Carlo - perfecto para multiprocessing"""
    print("=== MONTE CARLO PI ESTIMATION ===")
    
    def estimate_pi_chunk(num_points):
        """Estimar π usando chunk de puntos aleatorios"""
        inside_circle = 0
        
        for _ in range(num_points):
            x = random.uniform(-1, 1)
            y = random.uniform(-1, 1)
            
            if x*x + y*y <= 1:
                inside_circle += 1
        
        return inside_circle
    
    total_points = 10000000  # 10 millones
    num_processes = 4
    points_per_process = total_points // num_processes
    
    print(f"Estimating π using {total_points:,} points with {num_processes} processes...")
    
    # Sequential
    start = time.time()
    total_inside = estimate_pi_chunk(total_points)
    pi_estimate_seq = 4 * total_inside / total_points
    sequential_time = time.time() - start
    
    # Parallel
    start = time.time()
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        futures = [executor.submit(estimate_pi_chunk, points_per_process) 
                  for _ in range(num_processes)]
        
        total_inside_parallel = sum(f.result() for f in futures)
    
    pi_estimate_parallel = 4 * total_inside_parallel / total_points
    parallel_time = time.time() - start
    
    print(f"Sequential π estimate: {pi_estimate_seq:.6f} ({sequential_time:.2f}s)")
    print(f"Parallel π estimate: {pi_estimate_parallel:.6f} ({parallel_time:.2f}s)")
    print(f"Actual π: {3.141592653589793:.6f}")
    print(f"Speedup: {sequential_time/parallel_time:.1f}x")
    print(f"Accuracy: {abs(pi_estimate_parallel - 3.141592653589793):.6f} error\n")

# ========================
# ADVANCED MULTIPROCESSING PATTERNS
# ========================

class ParallelMapReduce:
    """Implementación simple de MapReduce pattern"""
    
    def __init__(self, num_workers=None):
        self.num_workers = num_workers or mp.cpu_count()
    
    def map_reduce(self, data, map_func, reduce_func):
        """
        MapReduce implementation
        map_func: función aplicada a cada elemento
        reduce_func: función para combinar resultados
        """
        print(f"MapReduce with {self.num_workers} workers")
        
        # Map phase - distribuir trabajo
        chunk_size = len(data) // self.num_workers
        chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
        
        with ProcessPoolExecutor(max_workers=self.num_workers) as executor:
            # Aplicar map_func a cada chunk
            map_futures = [executor.submit(self._map_chunk, chunk, map_func) 
                          for chunk in chunks]
            
            map_results = [f.result() for f in map_futures]
        
        # Reduce phase - combinar resultados
        final_result = map_results[0]
        for result in map_results[1:]:
            final_result = reduce_func(final_result, result)
        
        return final_result
    
    def _map_chunk(self, chunk, map_func):
        """Aplicar map_func a un chunk de datos"""
        return [map_func(item) for item in chunk]

def word_count_example():
    """Ejemplo de word count usando MapReduce"""
    print("=== MAPREDUCE WORD COUNT ===")
    
    # Simular documentos grandes
    documents = []
    words = ["python", "java", "javascript", "go", "rust", "scala", "kotlin"]
    
    for i in range(1000):
        doc = " ".join(random.choices(words, k=random.randint(10, 50)))
        documents.append(doc)
    
    def map_words(doc):
        """Map function: documento → word counts"""
        word_count = {}
        for word in doc.split():
            word_count[word] = word_count.get(word, 0) + 1
        return word_count
    
    def reduce_counts(count1, count2):
        """Reduce function: combinar word counts"""
        result = count1.copy()
        for word, count in count2.items():
            result[word] = result.get(word, 0) + count
        return result
    
    mr = ParallelMapReduce()
    
    start = time.time()
    word_counts = mr.map_reduce(documents, map_words, reduce_counts)
    parallel_time = time.time() - start
    
    # Sequential comparison
    start = time.time()
    seq_counts = {}
    for doc in documents:
        doc_counts = map_words(doc)
        seq_counts = reduce_counts(seq_counts, doc_counts)
    sequential_time = time.time() - start
    
    print(f"Processed {len(documents)} documents")
    print(f"Sequential: {sequential_time:.3f}s")
    print(f"Parallel: {parallel_time:.3f}s")
    print(f"Speedup: {sequential_time/parallel_time:.1f}x")
    
    # Mostrar top words
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    print("Top 5 words:")
    for word, count in sorted_words[:5]:
        print(f"   {word}: {count}")
    
    print()

class ProcessPool:
    """Custom process pool implementation"""
    
    def __init__(self, num_processes=None):
        self.num_processes = num_processes or mp.cpu_count()
        self.task_queue = Queue()
        self.result_queue = Queue()
        self.processes = []
        self.shutdown_event = mp.Event()
    
    def worker(self, worker_id):
        """Worker process"""
        print(f"Process worker {worker_id} started (PID: {os.getpid()})")
        
        while not self.shutdown_event.is_set():
            try:
                func, args, kwargs = self.task_queue.get(timeout=1)
                
                print(f"Worker {worker_id} processing task...")
                try:
                    result = func(*args, **kwargs)
                    self.result_queue.put(('success', result))
                except Exception as e:
                    self.result_queue.put(('error', str(e)))
                
            except:  # queue.Empty o otras excepciones
                continue
        
        print(f"Worker {worker_id} shutting down")
    
    def start(self):
        """Iniciar pool de procesos"""
        for i in range(self.num_processes):
            p = Process(target=self.worker, args=(i,))
            p.start()
            self.processes.append(p)
        
        print(f"Started {self.num_processes} worker processes")
    
    def submit(self, func, *args, **kwargs):
        """Submit task al pool"""
        self.task_queue.put((func, args, kwargs))
    
    def get_result(self, timeout=None):
        """Get resultado de task completada"""
        return self.result_queue.get(timeout=timeout)
    
    def shutdown(self):
        """Shutdown graceful del pool"""
        print("Shutting down process pool...")
        
        self.shutdown_event.set()
        
        for p in self.processes:
            p.join(timeout=2)
            if p.is_alive():
                print(f"Force terminating process {p.pid}")
                p.terminate()

# ========================
# SYNCHRONIZATION EN MULTIPROCESSING
# ========================

def demonstrate_mp_synchronization():
    """Sincronización en multiprocessing"""
    print("=== MULTIPROCESSING SYNCHRONIZATION ===")
    
    def worker_with_lock(shared_list, lock, worker_id):
        """Worker que modifica lista compartida con lock"""
        for i in range(5):
            with lock:
                shared_list.append(f"Worker-{worker_id}-Item-{i}")
                print(f"Worker {worker_id} added item {i}")
            time.sleep(0.1)
    
    # Usar Manager para shared objects
    with Manager() as manager:
        shared_list = manager.list()
        lock = manager.Lock()
        
        processes = []
        for i in range(3):
            p = Process(target=worker_with_lock, args=(shared_list, lock, i))
            processes.append(p)
            p.start()
        
        for p in processes:
            p.join()
        
        print(f"Final shared list length: {len(shared_list)}")
        print("Sample items:", list(shared_list)[:5])
    
    print()

# ========================
# PRACTICAL APPLICATIONS
# ========================

def parallel_matrix_multiplication():
    """Multiplicación de matrices en paralelo"""
    print("=== PARALLEL MATRIX MULTIPLICATION ===")
    
    def multiply_row(args):
        """Multiplicar una fila de A con matriz B"""
        row_a, matrix_b = args
        result_row = []
        
        for col in range(len(matrix_b[0])):
            dot_product = sum(row_a[i] * matrix_b[i][col] for i in range(len(row_a)))
            result_row.append(dot_product)
        
        return result_row
    
    # Crear matrices de prueba
    size = 200
    matrix_a = [[random.randint(1, 10) for _ in range(size)] for _ in range(size)]
    matrix_b = [[random.randint(1, 10) for _ in range(size)] for _ in range(size)]
    
    print(f"Multiplying {size}x{size} matrices...")
    
    # Sequential
    start = time.time()
    result_seq = []
    for row_a in matrix_a:
        result_row = multiply_row((row_a, matrix_b))
        result_seq.append(result_row)
    sequential_time = time.time() - start
    
    # Parallel
    start = time.time()
    with ProcessPoolExecutor() as executor:
        args_list = [(row_a, matrix_b) for row_a in matrix_a]
        result_parallel = list(executor.map(multiply_row, args_list))
    parallel_time = time.time() - start
    
    print(f"Sequential: {sequential_time:.3f}s")
    print(f"Parallel: {parallel_time:.3f}s")
    print(f"Speedup: {sequential_time/parallel_time:.1f}x")
    print(f"Results match: {result_seq == result_parallel}\n")

def parallel_prime_finder():
    """Encontrar números primos en paralelo"""
    print("=== PARALLEL PRIME FINDER ===")
    
    def is_prime(n):
        """Verificar si n es primo"""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        
        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    def find_primes_in_range(start, end):
        """Encontrar primos en rango dado"""
        primes = []
        for n in range(start, end):
            if is_prime(n):
                primes.append(n)
        return primes
    
    # Buscar primos hasta 50,000
    max_num = 50000
    num_processes = mp.cpu_count()
    chunk_size = max_num // num_processes
    
    print(f"Finding primes up to {max_num:,} using {num_processes} processes...")
    
    # Crear rangos para cada proceso
    ranges = []
    for i in range(num_processes):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < num_processes - 1 else max_num
        ranges.append((start, end))
    
    # Parallel execution
    start_time = time.time()
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        future_to_range = {executor.submit(find_primes_in_range, start, end): (start, end) 
                          for start, end in ranges}
        
        all_primes = []
        for future in as_completed(future_to_range):
            start, end = future_to_range[future]
            primes = future.result()
            all_primes.extend(primes)
            print(f"   Range {start}-{end}: found {len(primes)} primes")
    
    parallel_time = time.time() - start_time
    
    print(f"Total primes found: {len(all_primes)}")
    print(f"Time taken: {parallel_time:.2f}s")
    print(f"Largest prime: {max(all_primes)}")
    print()

# ========================
# PERFORMANCE MONITORING
# ========================

def monitor_system_resources():
    """Monitor del uso de recursos durante multiprocessing"""
    print("=== SYSTEM RESOURCE MONITORING ===")
    
    import psutil
    
    def cpu_intensive_monitored(duration):
        """Task CPU-intensive que podemos monitorear"""
        start_time = time.time()
        result = 0
        
        while time.time() - start_time < duration:
            for i in range(100000):
                result += i ** 2
        
        return result
    
    # Monitor antes de iniciar
    print("System stats before:")
    print(f"   CPU cores: {mp.cpu_count()}")
    print(f"   CPU usage: {psutil.cpu_percent()}%")
    print(f"   Memory usage: {psutil.virtual_memory().percent}%")
    
    # Ejecutar task intensiva
    duration = 2
    num_processes = mp.cpu_count()
    
    print(f"\nRunning {num_processes} CPU-intensive processes for {duration}s...")
    
    start = time.time()
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        futures = [executor.submit(cpu_intensive_monitored, duration) 
                  for _ in range(num_processes)]
        
        # Monitor during execution
        while any(not f.done() for f in futures):
            cpu_usage = psutil.cpu_percent(interval=0.5)
            memory_usage = psutil.virtual_memory().percent
            print(f"   CPU: {cpu_usage:5.1f}%, Memory: {memory_usage:5.1f}%")
        
        results = [f.result() for f in futures]
    
    end_time = time.time()
    
    print(f"\nCompleted in {end_time - start:.2f}s")
    print("System stats after:")
    print(f"   CPU usage: {psutil.cpu_percent()}%")
    print(f"   Memory usage: {psutil.virtual_memory().percent}%")
    print()

# ========================
# BEST PRACTICES
# ========================

class SafeMultiprocessing:
    """Mejores prácticas para multiprocessing seguro"""
    
    @staticmethod
    def safe_process_with_timeout():
        """Procesos con timeout para evitar hang"""
        
        def potentially_hanging_task():
            # Simular task que podría colgarse
            time.sleep(random.uniform(0.5, 3.0))
            return "Task completed"
        
        print("=== SAFE PROCESS WITH TIMEOUT ===")
        
        processes = []
        for i in range(3):
            p = Process(target=potentially_hanging_task)
            p.start()
            processes.append(p)
        
        # Join con timeout
        for i, p in enumerate(processes):
            p.join(timeout=2)  # 2 second timeout
            
            if p.is_alive():
                print(f"Process {i} timed out, terminating...")
                p.terminate()
                p.join()  # Wait for cleanup
            else:
                print(f"Process {i} completed normally")
        
        print()
    
    @staticmethod
    def error_handling_in_processes():
        """Manejo de errores en procesos"""
        
        def task_with_potential_error(x):
            if x == 3:
                raise ValueError(f"Error processing {x}")
            return x ** 2
        
        print("=== ERROR HANDLING IN PROCESSES ===")
        
        inputs = [1, 2, 3, 4, 5]
        
        with ProcessPoolExecutor() as executor:
            future_to_input = {executor.submit(task_with_potential_error, x): x 
                              for x in inputs}
            
            for future in as_completed(future_to_input):
                input_val = future_to_input[future]
                try:
                    result = future.result()
                    print(f"   Input {input_val}: Success → {result}")
                except Exception as e:
                    print(f"   Input {input_val}: Error → {e}")
        
        print()

# ========================
# TESTING FRAMEWORK
# ========================

def comprehensive_test():
    """Test comprehensivo de todos los conceptos"""
    print("=== COMPREHENSIVE MULTIPROCESSING TEST ===\n")
    
    # Basic comparison
    compare_threading_vs_multiprocessing()
    
    # IPC demonstrations
    demonstrate_queue_communication()
    demonstrate_pipe_communication()
    demonstrate_shared_memory()
    
    # Real-world applications
    parallel_file_processing()
    monte_carlo_pi_estimation()
    
    # MapReduce example
    word_count_example()
    
    # Safety and best practices
    SafeMultiprocessing.safe_process_with_timeout()
    SafeMultiprocessing.error_handling_in_processes()
    
    # Resource monitoring (si psutil está disponible)
    try:
        monitor_system_resources()
    except ImportError:
        print("psutil not available, skipping resource monitoring")

if __name__ == "__main__":
    # Note: En algunos sistemas, multiprocessing requiere if __name__ == "__main__"
    comprehensive_test()
