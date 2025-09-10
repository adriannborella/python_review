"""
PROBLEMAS DE ENTREVISTA - CONCURRENCIA
======================================

Estos problemas aparecen frecuentemente en entrevistas senior:
- Web Scraping Concurrente (90% probabilidad)
- Producer-Consumer Implementation (85% probabilidad)
- Thread-Safe Cache (75% probabilidad)
- Rate Limiter (70% probabilidad)
- Parallel Processing Design (80% probabilidad)

¡Dominar estos te dará una ventaja enorme sobre otros candidatos!
"""

import threading
import time
import queue
import requests
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from threading import Lock, Semaphore, Event
import multiprocessing as mp
from multiprocessing import Queue as MPQueue, Process
import random
from collections import defaultdict
import json

# ========================
# PROBLEMA 1: Web Scraping Concurrente
# ========================

class ConcurrentWebScraper:
    """
    Web scraper concurrente - problema MUY común en entrevistas
    Demuestra I/O-bound optimization con threading
    """
    
    def __init__(self, max_workers=5, rate_limit=1.0):
        self.max_workers = max_workers
        self.rate_limit = rate_limit  # segundos entre requests
        self.session_lock = Lock()
        self.results = []
        self.results_lock = Lock()
    
    def fetch_url(self, url):
        """
        Fetch single URL con rate limiting
        Simula HTTP request con delay
        """
        # Simular rate limiting
        time.sleep(self.rate_limit)
        
        # Simular HTTP request
        start_time = time.time()
        
        # Simular response time variable
        response_time = random.uniform(0.1, 2.0)
        time.sleep(response_time)
        
        # Simular response data
        response_data = {
            'url': url,
            'status_code': random.choice([200, 200, 200, 404, 500]),  # Mostly 200
            'content_length': random.randint(1000, 50000),
            'response_time': response_time
        }
        
        with self.results_lock:
            self.results.append(response_data)
        
        print(f"Fetched {url}: {response_data['status_code']} ({response_time:.2f}s)")
        return response_data
    
    def scrape_urls_sequential(self, urls):
        """Scraping secuencial para comparación"""
        print("=== SEQUENTIAL SCRAPING ===")
        start = time.time()
        
        results = []
        for url in urls:
            result = self.fetch_url(url)
            results.append(result)
        
        total_time = time.time() - start
        print(f"Sequential scraping: {total_time:.2f}s for {len(urls)} URLs\n")
        return results
    
    def scrape_urls_concurrent(self, urls):
        """Scraping concurrente con ThreadPoolExecutor"""
        print("=== CONCURRENT SCRAPING ===")
        self.results.clear()
        
        start = time.time()
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_url = {executor.submit(self.fetch_url, url): url for url in urls}
            
            concurrent_results = []
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    result = future.result()
                    concurrent_results.append(result)
                except Exception as e:
                    print(f"Error fetching {url}: {e}")
        
        total_time = time.time() - start
        print(f"Concurrent scraping: {total_time:.2f}s for {len(urls)} URLs")
        
        # Análisis de resultados
        successful = sum(1 for r in concurrent_results if r['status_code'] == 200)
        avg_response_time = sum(r['response_time'] for r in concurrent_results) / len(concurrent_results)
        
        print(f"Success rate: {successful}/{len(urls)} ({successful/len(urls)*100:.1f}%)")
        print(f"Average response time: {avg_response_time:.2f}s\n")
        
        return concurrent_results

# ========================
# PROBLEMA 2: Thread-Safe LRU Cache
# ========================

class ThreadSafeLRUCache:
    """
    LRU Cache thread-safe - combinación de patterns
    Muy común en entrevistas de sistemas distribuidos
    """
    
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.access_order = []  # Track access order
        self.lock = threading.RLock()
        self.hit_count = 0
        self.miss_count = 0
    
    def get(self, key):
        """Get con thread safety"""
        with self.lock:
            if key in self.cache:
                # Move to end (most recently used)
                self.access_order.remove(key)
                self.access_order.append(key)
                self.hit_count += 1
                return self.cache[key]
            
            self.miss_count += 1
            return None
    
    def put(self, key, value):
        """Put con eviction policy"""
        with self.lock:
            if key in self.cache:
                # Update existing key
                self.cache[key] = value
                self.access_order.remove(key)
                self.access_order.append(key)
            else:
                # Add new key
                if len(self.cache) >= self.capacity:
                    # Evict least recently used
                    lru_key = self.access_order.pop(0)
                    del self.cache[lru_key]
                
                self.cache[key] = value
                self.access_order.append(key)
    
    def stats(self):
        """Obtener estadísticas del cache"""
        with self.lock:
            total_requests = self.hit_count + self.miss_count
            hit_rate = self.hit_count / total_requests if total_requests > 0 else 0
            
            return {
                'hits': self.hit_count,
                'misses': self.miss_count,
                'hit_rate': hit_rate,
                'size': len(self.cache),
                'capacity': self.capacity
            }
    
    def clear_stats(self):
        """Reset estadísticas"""
        with self.lock:
            self.hit_count = 0
            self.miss_count = 0

def test_thread_safe_cache():
    """Test cache con múltiples threads"""
    print("=== THREAD-SAFE LRU CACHE TEST ===")
    
    cache = ThreadSafeLRUCache(capacity=10)
    
    def cache_worker(worker_id, num_operations=100):
        """Worker que hace operaciones random en cache"""
        for i in range(num_operations):
            operation = random.choice(['get', 'put'])
            key = f"key_{random.randint(1, 20)}"
            
            if operation == 'get':
                result = cache.get(key)
                if result is not None:
                    print(f"Worker {worker_id}: GET {key} → {result}")
            else:
                value = f"value_{worker_id}_{i}"
                cache.put(key, value)
                print(f"Worker {worker_id}: PUT {key} → {value}")
            
            time.sleep(0.01)  # Small delay
    
    # Crear múltiples workers
    threads = []
    for i in range(5):
        t = threading.Thread(target=cache_worker, args=(i, 20))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    # Mostrar estadísticas finales
    stats = cache.stats()
    print(f"\nCache Statistics:")
    for key, value in stats.items():
        if key == 'hit_rate':
            print(f"   {key}: {value:.2%}")
        else:
            print(f"   {key}: {value}")
    print()

# ========================
# PROBLEMA 3: Producer-Consumer con Múltiples Tipos
# ========================

class MultiTypeProducerConsumer:
    """
    Producer-Consumer avanzado con diferentes tipos de tasks
    Común en entrevistas de arquitectura de sistemas
    """
    
    def __init__(self):
        self.high_priority_queue = queue.PriorityQueue()
        self.normal_queue = queue.Queue()
        self.processing_stats = defaultdict(int)
        self.stats_lock = Lock()
        self.shutdown = Event()
    
    def producer(self, producer_id, task_type):
        """Producer que genera diferentes tipos de tasks"""
        for i in range(10):
            if self.shutdown.is_set():
                break
            
            if task_type == "high_priority":
                # Priority queue usa (priority, item)
                task = (1, f"URGENT-{producer_id}-{i}")  # Prioridad 1 (alta)
                self.high_priority_queue.put(task)
            else:
                task = f"NORMAL-{producer_id}-{i}"
                self.normal_queue.put(task)
            
            print(f"Producer {producer_id} created {task_type}: {task}")
            time.sleep(random.uniform(0.1, 0.5))
        
        print(f"Producer {producer_id} ({task_type}) finished")
    
    def smart_consumer(self, consumer_id):
        """Consumer que prioriza high-priority tasks"""
        print(f"Smart Consumer {consumer_id} started")
        
        while not self.shutdown.is_set():
            processed = False
            
            # Primero revisar high priority queue
            try:
                priority, task = self.high_priority_queue.get_nowait()
                self.process_task(task, consumer_id, "HIGH_PRIORITY")
                processed = True
            except queue.Empty:
                pass
            
            # Si no hay high priority, procesar normal
            if not processed:
                try:
                    task = self.normal_queue.get(timeout=0.5)
                    self.process_task(task, consumer_id, "NORMAL")
                    processed = True
                except queue.Empty:
                    pass
            
            if not processed:
                time.sleep(0.1)  # Brief pause si no hay trabajo
        
        print(f"Smart Consumer {consumer_id} finished")
    
    def process_task(self, task, consumer_id, task_type):
        """Procesar task individual"""
        print(f"Consumer {consumer_id} processing {task_type}: {task}")
        
        # Simular processing time (high priority es más rápido)
        if task_type == "HIGH_PRIORITY":
            time.sleep(random.uniform(0.1, 0.3))
        else:
            time.sleep(random.uniform(0.2, 0.8))
        
        with self.stats_lock:
            self.processing_stats[task_type] += 1
        
        print(f"Consumer {consumer_id} completed: {task}")
    
    def run_simulation(self, duration=5):
        """Ejecutar simulación completa"""
        print("=== MULTI-TYPE PRODUCER-CONSUMER ===")
        
        threads = []
        
        # Crear producers
        p1 = threading.Thread(target=self.producer, args=(1, "high_priority"))
        p2 = threading.Thread(target=self.producer, args=(2, "normal"))
        p3 = threading.Thread(target=self.producer, args=(3, "normal"))
        
        threads.extend([p1, p2, p3])
        
        # Crear smart consumers
        for i in range(3):
            c = threading.Thread(target=self.smart_consumer, args=(i,))
            threads.append(c)
        
        # Iniciar todos los threads
        for t in threads:
            t.start()
        
        # Dejar que corran por duration segundos
        time.sleep(duration)
        
        # Shutdown graceful
        self.shutdown.set()
        
        for t in threads:
            t.join(timeout=2)
        
        # Mostrar estadísticas
        print(f"\nProcessing Statistics:")
        with self.stats_lock:
            for task_type, count in self.processing_stats.items():
                print(f"   {task_type}: {count} tasks processed")
        print()

# ========================
# PROBLEMA 4: Parallel Data Processing Pipeline
# ========================

class DataProcessingPipeline:
    """
    Pipeline de procesamiento de datos en paralelo
    Patrón común en entrevistas de data engineering
    """
    
    def __init__(self, num_workers=None):
        self.num_workers = num_workers or mp.cpu_count()
    
    def extract_data(self, source_id):
        """Stage 1: Extract data from source"""
        # Simular extracción de datos
        time.sleep(random.uniform(0.1, 0.5))
        
        data = {
            'source_id': source_id,
            'records': [random.randint(1, 100) for _ in range(random.randint(10, 50))],
            'timestamp': time.time()
        }
        
        print(f"Extracted data from source {source_id}: {len(data['records'])} records")
        return data
    
    def transform_data(self, data):
        """Stage 2: Transform/clean data"""
        # Simular transformación CPU-intensive
        transformed_records = []
        
        for record in data['records']:
            # Simular transformación compleja
            transformed = record ** 2 + random.randint(1, 10)
            transformed_records.append(transformed)
        
        result = {
            'source_id': data['source_id'],
            'transformed_records': transformed_records,
            'original_count': len(data['records']),
            'processed_timestamp': time.time()
        }
        
        print(f"Transformed data from source {data['source_id']}: {len(transformed_records)} records")
        return result
    
    def load_data(self, transformed_data):
        """Stage 3: Load data to destination"""
        # Simular carga a database/storage
        time.sleep(random.uniform(0.2, 0.8))
        
        result = {
            'source_id': transformed_data['source_id'],
            'loaded_count': len(transformed_data['transformed_records']),
            'load_timestamp': time.time(),
            'status': 'success'
        }
        
        print(f"Loaded data from source {transformed_data['source_id']}: {result['loaded_count']} records")
        return result
    
    def process_pipeline_sequential(self, sources):
        """Pipeline secuencial (ETL tradicional)"""
        print("=== SEQUENTIAL PIPELINE ===")
        start = time.time()
        
        results = []
        for source in sources:
            # ETL sequence
            extracted = self.extract_data(source)
            transformed = self.transform_data(extracted)
            loaded = self.load_data(transformed)
            results.append(loaded)
        
        total_time = time.time() - start
        print(f"Sequential pipeline: {total_time:.2f}s\n")
        return results
    
    def process_pipeline_parallel(self, sources):
        """Pipeline paralelo - cada stage en paralelo"""
        print("=== PARALLEL PIPELINE ===")
        start = time.time()
        
        # Stage 1: Parallel extraction (I/O-bound)
        with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            extracted_data = list(executor.map(self.extract_data, sources))
        
        # Stage 2: Parallel transformation (CPU-bound)
        with ProcessPoolExecutor(max_workers=self.num_workers) as executor:
            transformed_data = list(executor.map(self.transform_data, extracted_data))
        
        # Stage 3: Parallel loading (I/O-bound)
        with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            loaded_data = list(executor.map(self.load_data, transformed_data))
        
        total_time = time.time() - start
        print(f"Parallel pipeline: {total_time:.2f}s\n")
        return loaded_data

# ========================
# PROBLEMA 5: Distributed Task Queue
# ========================

class DistributedTaskQueue:
    """
    Sistema de cola de tareas distribuido
    Simula sistemas como Celery/RQ
    """
    
    def __init__(self, num_workers=3):
        self.task_queue = MPQueue()
        self.result_queue = MPQueue()
        self.num_workers = num_workers
        self.workers = []
        self.shutdown_event = mp.Event()
        
        # Task registry
        self.tasks = {
            'cpu_task': self.cpu_intensive_task,
            'io_task': self.io_intensive_task,
            'data_task': self.data_processing_task
        }
    
    def cpu_intensive_task(self, *args):
        """CPU-intensive task"""
        n = args[0] if args else 1000000
        result = sum(i ** 2 for i in range(n))
        return f"CPU task result: {result}"
    
    def io_intensive_task(self, *args):
        """I/O-intensive task"""
        duration = args[0] if args else 1.0
        time.sleep(duration)
        return f"I/O task completed after {duration}s"
    
    def data_processing_task(self, *args):
        """Data processing task"""
        data = args[0] if args else list(range(100))
        processed = [x * 2 + 1 for x in data if x % 2 == 0]
        return f"Processed {len(processed)} items from {len(data)}"
    
    def worker_process(self, worker_id):
        """Worker process que ejecuta tareas"""
        print(f"Worker {worker_id} started (PID: {os.getpid()})")
        
        while not self.shutdown_event.is_set():
            try:
                task_data = self.task_queue.get(timeout=1)
                task_id, task_type, args = task_data
                
                print(f"Worker {worker_id} processing task {task_id} ({task_type})")
                
                try:
                    # Ejecutar task
                    task_func = self.tasks[task_type]
                    result = task_func(*args)
                    
                    # Enviar resultado
                    self.result_queue.put({
                        'task_id': task_id,
                        'worker_id': worker_id,
                        'status': 'success',
                        'result': result,
                        'timestamp': time.time()
                    })
                    
                except Exception as e:
                    self.result_queue.put({
                        'task_id': task_id,
                        'worker_id': worker_id,
                        'status': 'error',
                        'error': str(e),
                        'timestamp': time.time()
                    })
                
            except:  # Timeout o shutdown
                continue
        
        print(f"Worker {worker_id} shutting down")
    
    def start_workers(self):
        """Iniciar worker processes"""
        for i in range(self.num_workers):
            worker = Process(target=self.worker_process, args=(i,))
            worker.start()
            self.workers.append(worker)
        
        print(f"Started {self.num_workers} worker processes")
    
    def submit_task(self, task_type, *args):
        """Submit task a la queue"""
        task_id = f"task_{int(time.time() * 1000000)}"
        self.task_queue.put((task_id, task_type, args))
        return task_id
    
    def get_result(self, timeout=None):
        """Get resultado de task completada"""
        return self.result_queue.get(timeout=timeout)
    
    def shutdown(self):
        """Shutdown graceful"""
        print("Shutting down task queue...")
        self.shutdown_event.set()
        
        for worker in self.workers:
            worker.join(timeout=2)
            if worker.is_alive():
                worker.terminate()

# ========================
# PROBLEMA 6: Concurrent Download Manager
# ========================

class ConcurrentDownloadManager:
    """
    Download manager con concurrency control
    Maneja rate limiting, retries, y progress tracking
    """
    
    def __init__(self, max_concurrent=5, max_retries=3):
        self.max_concurrent = max_concurrent
        self.max_retries = max_retries
        self.semaphore = Semaphore(max_concurrent)
        self.progress_lock = Lock()
        self.download_stats = {
            'completed': 0,
            'failed': 0,
            'bytes_downloaded': 0,
            'total_time': 0
        }
    
    def download_file(self, url, expected_size=None):
        """
        Download single file con retry logic
        Simula download real con chunks y progress
        """
        with self.semaphore:  # Limitar concurrent downloads
            
            for attempt in range(self.max_retries):
                try:
                    print(f"Downloading {url} (attempt {attempt + 1})")
                    
                    # Simular download con chunks
                    downloaded_bytes = 0
                    total_size = expected_size or random.randint(1000000, 10000000)
                    chunk_size = 8192
                    
                    start_time = time.time()
                    
                    while downloaded_bytes < total_size:
                        # Simular chunk download
                        chunk_delay = random.uniform(0.001, 0.01)
                        time.sleep(chunk_delay)
                        
                        current_chunk = min(chunk_size, total_size - downloaded_bytes)
                        downloaded_bytes += current_chunk
                        
                        # Simular network issues ocasionales
                        if random.random() < 0.02:  # 2% chance of failure
                            raise ConnectionError("Network timeout")
                    
                    download_time = time.time() - start_time
                    
                    # Update stats thread-safely
                    with self.progress_lock:
                        self.download_stats['completed'] += 1
                        self.download_stats['bytes_downloaded'] += downloaded_bytes
                        self.download_stats['total_time'] += download_time
                    
                    print(f"✓ Downloaded {url}: {downloaded_bytes:,} bytes in {download_time:.2f}s")
                    return {
                        'url': url,
                        'size': downloaded_bytes,
                        'time': download_time,
                        'success': True
                    }
                
                except Exception as e:
                    print(f"✗ Download {url} failed (attempt {attempt + 1}): {e}")
                    if attempt < self.max_retries - 1:
                        time.sleep(0.5 * (attempt + 1))  # Exponential backoff
            
            # All retries failed
            with self.progress_lock:
                self.download_stats['failed'] += 1
            
            return {
                'url': url,
                'success': False,
                'error': 'Max retries exceeded'
            }
    
    def download_batch(self, urls):
        """Download multiple files concurrently"""
        print(f"=== CONCURRENT DOWNLOAD MANAGER ===")
        print(f"Downloading {len(urls)} files with max {self.max_concurrent} concurrent...")
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=self.max_concurrent * 2) as executor:
            future_to_url = {executor.submit(self.download_file, url): url for url in urls}
            
            results = []
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    print(f"Unexpected error downloading {url}: {e}")
                    results.append({'url': url, 'success': False, 'error': str(e)})
        
        total_time = time.time() - start_time
        
        # Mostrar estadísticas finales
        successful = sum(1 for r in results if r['success'])
        total_bytes = self.download_stats['bytes_downloaded']
        avg_speed = total_bytes / total_time if total_time > 0 else 0
        
        print(f"\nDownload Summary:")
        print(f"   Total files: {len(urls)}")
        print(f"   Successful: {successful}")
        print(f"   Failed: {len(urls) - successful}")
        print(f"   Total bytes: {total_bytes:,}")
        print(f"   Total time: {total_time:.2f}s")
        print(f"   Average speed: {avg_speed/1024/1024:.2f} MB/s")
        print()
        
        return results

# ========================
# PROBLEMA 7: Concurrent Web Server Simulation
# ========================

class ConcurrentWebServer:
    """
    Simulación de web server concurrente
    Evalúa understanding de request handling patterns
    """
    
    def __init__(self, max_connections=100):
        self.max_connections = max_connections
        self.connection_semaphore = Semaphore(max_connections)
        self.request_stats = defaultdict(int)
        self.stats_lock = Lock()
        self.active_connections = 0
        self.connection_lock = Lock()
    
    def handle_request(self, request_id, request_type="GET", complexity="simple"):
        """Handle individual HTTP request"""
        
        with self.connection_semaphore:
            with self.connection_lock:
                self.active_connections += 1
                current_connections = self.active_connections
            
            print(f"Request {request_id} ({request_type}) - Active connections: {current_connections}")
            
            try:
                # Simular different request complexities
                if complexity == "simple":
                    processing_time = random.uniform(0.1, 0.5)
                elif complexity == "medium":
                    processing_time = random.uniform(0.5, 2.0)
                else:  # complex
                    processing_time = random.uniform(2.0, 5.0)
                
                time.sleep(processing_time)
                
                # Simular response codes
                status_code = random.choices(
                    [200, 404, 500, 503],
                    weights=[85, 10, 3, 2]
                )[0]
                
                with self.stats_lock:
                    self.request_stats[f'{request_type}_{status_code}'] += 1
                    self.request_stats['total_requests'] += 1
                    self.request_stats['total_processing_time'] += processing_time
                
                print(f"✓ Request {request_id} completed: {status_code} ({processing_time:.2f}s)")
                
                return {
                    'request_id': request_id,
                    'status_code': status_code,
                    'processing_time': processing_time
                }
                
            finally:
                with self.connection_lock:
                    self.active_connections -= 1
    
    def simulate_traffic(self, duration=10, requests_per_second=10):
        """Simular tráfico web realista"""
        print(f"=== WEB SERVER SIMULATION ===")
        print(f"Simulating {requests_per_second} req/s for {duration}s...")
        
        def request_generator():
            """Generar requests a rate específico"""
            request_id = 0
            end_time = time.time() + duration
            
            while time.time() < end_time:
                # Generar batch de requests
                batch_size = random.poisson(requests_per_second)  # Poisson distribution
                
                futures = []
                with ThreadPoolExecutor(max_workers=50) as executor:
                    for _ in range(batch_size):
                        request_type = random.choices(
                            ['GET', 'POST', 'PUT', 'DELETE'],
                            weights=[70, 20, 8, 2]
                        )[0]
                        
                        complexity = random.choices(
                            ['simple', 'medium', 'complex'],
                            weights=[60, 30, 10]
                        )[0]
                        
                        future = executor.submit(
                            self.handle_request,
                            f"req_{request_id}",
                            request_type,
                            complexity
                        )
                        futures.append(future)
                        request_id += 1
                    
                    # Wait for batch to complete
                    for future in as_completed(futures):
                        try:
                            future.result()
                        except Exception as e:
                            print(f"Request failed: {e}")
                
                # Mantener rate
                time.sleep(1.0)
        
        start_time = time.time()
        request_generator()
        total_simulation_time = time.time() - start_time
        
        # Mostrar estadísticas
        print(f"\nServer Statistics:")
        with self.stats_lock:
            total_reqs = self.request_stats['total_requests']
            avg_processing = self.request_stats['total_processing_time'] / total_reqs if total_reqs > 0 else 0
            
            print(f"   Total requests: {total_reqs}")
            print(f"   Requests/second: {total_reqs/total_simulation_time:.1f}")
            print(f"   Average processing time: {avg_processing:.3f}s")
            
            # Status code breakdown
            status_codes = {}
            for key, value in self.request_stats.items():
                if '_' in key and key != 'total_requests' and key != 'total_processing_time':
                    status_codes[key] = value
            
            print("   Status code distribution:")
            for status, count in sorted(status_codes.items()):
                percentage = count / total_reqs * 100 if total_reqs > 0 else 0
                print(f"     {status}: {count} ({percentage:.1f}%)")
        
        print()

# ========================
# TESTING FRAMEWORK
# ========================

def test_web_scraper():
    """Test concurrent web scraper"""
    scraper = ConcurrentWebScraper(max_workers=3, rate_limit=0.1)
    
    # URLs de prueba
    urls = [f"https://example.com/page_{i}" for i in range(10)]
    
    # Compare sequential vs concurrent
    sequential_results = scraper.scrape_urls_sequential(urls[:5])  # Subset para demo
    concurrent_results = scraper.scrape_urls_concurrent(urls[:5])

def test_data_pipeline():
    """Test data processing pipeline"""
    pipeline = DataProcessingPipeline(num_workers=2)
    
    sources = [f"source_{i}" for i in range(8)]
    
    # Compare sequential vs parallel
    sequential_results = pipeline.process_pipeline_sequential(sources[:4])  # Subset
    parallel_results = pipeline.process_pipeline_parallel(sources[:4])

def test_task_queue():
    """Test distributed task queue"""
    if __name__ == "__main__":  # Required for multiprocessing
        print("=== DISTRIBUTED TASK QUEUE TEST ===")
        
        task_queue = DistributedTaskQueue(num_workers=2)
        task_queue.start_workers()
        
        # Submit various tasks
        tasks = [
            ('cpu_task', 500000),
            ('io_task', 1.0),
            ('data_task', list(range(50))),
            ('cpu_task', 300000),
            ('io_task', 0.5)
        ]
        
        print("Submitting tasks...")
        submitted_tasks = []
        for task_type, *args in tasks:
            task_id = task_queue.submit_task(task_type, *args)
            submitted_tasks.append(task_id)
            print(f"   Submitted {task_id}: {task_type}")
        
        # Collect results
        print("\nCollecting results...")
        for _ in range(len(tasks)):
            try:
                result = task_queue.get_result(timeout=10)
                print(f"   {result['task_id']}: {result['status']} by worker {result['worker_id']}")
                if result['status'] == 'success':
                    print(f"     Result: {result['result'][:50]}...")
            except:
                print("   Timeout waiting for result")
        
        task_queue.shutdown()
        print()

def test_download_manager():
    """Test concurrent download manager"""
    dm = ConcurrentDownloadManager(max_concurrent=3)
    
    # URLs de prueba (simuladas)
    urls = [f"https://example.com/file_{i}.zip" for i in range(8)]
    
    results = dm.download_batch(urls)

def test_web_server():
    """Test web server simulation"""
    server = ConcurrentWebServer(max_connections=20)
    
    # Simular tráfico por 5 segundos
    server.simulate_traffic(duration=5, requests_per_second=8)

# ========================
# PERFORMANCE ANALYSIS
# ========================

def analyze_concurrency_patterns():
    """Análisis de diferentes patrones de concurrencia"""
    print("=== CONCURRENCY PATTERN ANALYSIS ===\n")
    
    def io_bound_workload():
        time.sleep(0.5)
        return "IO completed"
    
    def cpu_bound_workload():
        return sum(i ** 2 for i in range(100000))
    
    workloads = [
        ("I/O-bound", io_bound_workload, 8),
        ("CPU-bound", cpu_bound_workload, 4)
    ]
    
    for workload_name, task_func, num_tasks in workloads:
        print(f"{workload_name} workload ({num_tasks} tasks):")
        
        # Sequential
        start = time.time()
        for _ in range(num_tasks):
            task_func()
        sequential_time = time.time() - start
        
        # Threading
        start = time.time()
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(task_func) for _ in range(num_tasks)]
            for future in as_completed(futures):
                future.result()
        threading_time = time.time() - start
        
        # Multiprocessing
        start = time.time()
        with ProcessPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(task_func) for _ in range(num_tasks)]
            for future in as_completed(futures):
                future.result()
        mp_time = time.time() - start
        
        print(f"   Sequential: {sequential_time:.2f}s")
        print(f"   Threading: {threading_time:.2f}s (speedup: {sequential_time/threading_time:.1f}x)")
        print(f"   Multiprocessing: {mp_time:.2f}s (speedup: {sequential_time/mp_time:.1f}x)")
        print(f"   Best approach: {'Threading' if threading_time < mp_time else 'Multiprocessing'}")
        print()

if __name__ == "__main__":
    test_web_scraper()
    test_thread_safe_cache()
    
    # Producer-Consumer test
    pc = MultiTypeProducerConsumer()
    pc.run_simulation(duration=3)
    
    test_data_pipeline()
    test_download_manager()
    test_web_server()
    
    analyze_concurrency_patterns()
    
if __name__ == "__main__":
    test_web_scraper()
    test_thread_safe_cache()
    
    # Producer-Consumer test
    pc = MultiTypeProducerConsumer()
    pc.run_simulation(duration=3)
    
    test_data_pipeline()
    test_download_manager()
    test_web_server()
    
    analyze_concurrency_patterns()
    
    print("=== ALL CONCURRENCY TESTS COMPLETED ===")

# ========================
# TIPS CRÍTICOS PARA ENTREVISTAS
# ========================

"""
🎯 GUÍA DEFINITIVA: THREADING VS MULTIPROCESSING

CUÁNDO USAR THREADING:
✅ I/O-bound tasks (file reads, network calls, database queries)
✅ Web scraping, API calls, download managers
✅ UI responsiveness (background tasks)
✅ Producer-consumer con I/O
✅ Shared state que necesita sincronización frecuente

CUÁNDO USAR MULTIPROCESSING:
✅ CPU-bound tasks (mathematical calculations, image processing)
✅ Scientific computing, machine learning training
✅ Parallel algorithms (sorting, searching large datasets)
✅ Independent tasks que no necesitan shared state
✅ Fault isolation (crash en un proceso no afecta otros)

CUÁNDO USAR ASYNCIO (próxima semana):
✅ Network I/O intensivo (thousands of connections)
✅ WebSocket servers, chat applications
✅ Microservices communication
✅ Real-time applications

ERRORES COMUNES EN ENTREVISTAS:
❌ Usar threading para CPU-bound tasks
❌ No considerar el GIL
❌ Race conditions (olvidar locks)
❌ Deadlocks (order inconsistente de locks)
❌ No manejar excepciones en threads/processes
❌ Memory leaks en long-running processes

PREGUNTAS TÍPICAS DE ENTREVISTADORES:
1. "¿Por qué Python threading no mejora CPU-bound tasks?"
2. "¿Cómo evitarías deadlocks en este código?"
3. "¿Cuál sería el bottleneck en este sistema?"
4. "¿Cómo escalarías esto para manejar 1M requests/day?"
5. "¿Qué pasa si un worker process crashea?"

RESPUESTAS GANADORAS:
1. Menciona el GIL explícitamente y cuándo/por qué existe
2. Habla de lock ordering, timeouts, y deadlock detection
3. Identifica I/O vs CPU bottlenecks y sus soluciones
4. Discute horizontal scaling, load balancing, caching
5. Explica process isolation, error handling, restart strategies

ARQUITECTURAS REALES QUE DEBES CONOCER:
- Gunicorn: Multiple worker processes para Django/Flask
- Celery: Distributed task queue con Redis/RabbitMQ
- Nginx: Event-driven architecture para high concurrency
- Apache: Process/thread pool models
"""

"""
PROBLEMAS DE ENTREVISTA - CONCURRENCIA
======================================

Estos problemas aparecen frecuentemente en entrevistas senior:
- Web Scraping Concurrente (90% probabilidad)
- Producer-Consumer Implementation (85% probabilidad)
- Thread-Safe Cache (75% probabilidad)
- Rate Limiter (70% probabilidad)
- Parallel Processing Design (80% probabilidad)

¡Dominar estos te dará una ventaja enorme sobre otros candidatos!
"""

import threading
import time
import queue
import requests
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from threading import Lock, Semaphore, Event
import multiprocessing as mp
from multiprocessing import Queue as MPQueue, Process
import random
from collections import defaultdict
import json

# ========================
# PROBLEMA 1: Web Scraping Concurrente
# ========================

class ConcurrentWebScraper:
    """
    Web scraper concurrente - problema MUY común en entrevistas
    Demuestra I/O-bound optimization con threading
    """
    
    def __init__(self, max_workers=5, rate_limit=1.0):
        self.max_workers = max_workers
        self.rate_limit = rate_limit  # segundos entre requests
        self.session_lock = Lock()
        self.results = []
        self.results_lock = Lock()
    
    def fetch_url(self, url):
        """
        Fetch single URL con rate limiting
        Simula HTTP request con delay
        """
        # Simular rate limiting
        time.sleep(self.rate_limit)
        
        # Simular HTTP request
        start_time = time.time()
        
        # Simular response time variable
        response_time = random.uniform(0.1, 2.0)
        time.sleep(response_time)
        
        # Simular response data
        response_data = {
            'url': url,
            'status_code': random.choice([200, 200, 200, 404, 500]),  # Mostly 200
            'content_length': random.randint(1000, 50000),
            'response_time': response_time
        }
        
        with self.results_lock:
            self.results.append(response_data)
        
        print(f"Fetched {url}: {response_data['status_code']} ({response_time:.2f}s)")
        return response_data
    
    def scrape_urls_sequential(self, urls):
        """Scraping secuencial para comparación"""
        print("=== SEQUENTIAL SCRAPING ===")
        start = time.time()
        
        results = []
        for url in urls:
            result = self.fetch_url(url)
            results.append(result)
        
        total_time = time.time() - start
        print(f"Sequential scraping: {total_time:.2f}s for {len(urls)} URLs\n")
        return results
    
    def scrape_urls_concurrent(self, urls):
        """Scraping concurrente con ThreadPoolExecutor"""
        print("=== CONCURRENT SCRAPING ===")
        self.results.clear()
        
        start = time.time()
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_url = {executor.submit(self.fetch_url, url): url for url in urls}
            
            concurrent_results = []
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    result = future.result()
                    concurrent_results.append(result)
                except Exception as e:
                    print(f"Error fetching {url}: {e}")
        
        total_time = time.time() - start
        print(f"Concurrent scraping: {total_time:.2f}s for {len(urls)} URLs")
        
        # Análisis de resultados
        successful = sum(1 for r in concurrent_results if r['status_code'] == 200)
        avg_response_time = sum(r['response_time'] for r in concurrent_results) / len(concurrent_results)
        
        print(f"Success rate: {successful}/{len(urls)} ({successful/len(urls)*100:.1f}%)")
        print(f"Average response time: {avg_response_time:.2f}s\n")
        
        return concurrent_results

# ========================
# PROBLEMA 2: Thread-Safe LRU Cache
# ========================

class ThreadSafeLRUCache:
    """
    LRU Cache thread-safe - combinación de patterns
    Muy común en entrevistas de sistemas distribuidos
    """
    
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.access_order = []  # Track access order
        self.lock = threading.RLock()
        self.hit_count = 0
        self.miss_count = 0
    
    def get(self, key):
        """Get con thread safety"""
        with self.lock: