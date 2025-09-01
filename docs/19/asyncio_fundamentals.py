"""
ASYNCIO - FUNDAMENTOS Y PATTERNS AVANZADOS
==========================================

AsyncIO es la evolución de concurrency en Python:
- Cooperative multitasking con corrutinas
- Event loop para coordinate I/O operations
- Perfecto para network programming y high-concurrency applications

VENTAJAS SOBRE THREADING:
- Menor overhead (no context switching)
- No race conditions (single thread)
- Mejor scaling para I/O-bound (miles de connections)
- Control explícito de when to yield

CUÁNDO USAR:
- Web servers/clients de alta concurrencia
- WebSocket applications
- Real-time data streaming
- Microservices communication
- Chat systems, gaming backends
"""

import asyncio
import aiohttp
import aiofiles
import time
import random
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime
import json

# ========================
# BÁSICOS DE ASYNCIO
# ========================

async def basic_coroutine_example():
    """Ejemplo básico de corrutinas"""
    print("=== BASIC ASYNCIO CONCEPTS ===\n")
    
    async def simple_task(name, delay):
        print(f"Task {name} starting...")
        await asyncio.sleep(delay)  # Non-blocking sleep!
        print(f"Task {name} completed after {delay}s")
        return f"Result from {name}"
    
    # Ejecutar corrutinas secuencialmente
    print("1. SEQUENTIAL EXECUTION:")
    start = time.time()
    
    result1 = await simple_task("A", 1)
    result2 = await simple_task("B", 2)
    result3 = await simple_task("C", 1)
    
    sequential_time = time.time() - start
    print(f"Sequential time: {sequential_time:.2f}s")
    print(f"Results: {[result1, result2, result3]}\n")
    
    # Ejecutar corrutinas concurrentemente
    print("2. CONCURRENT EXECUTION:")
    start = time.time()
    
    # asyncio.gather ejecuta todas las corrutinas concurrentemente
    results = await asyncio.gather(
        simple_task("X", 1),
        simple_task("Y", 2),
        simple_task("Z", 1)
    )
    
    concurrent_time = time.time() - start
    print(f"Concurrent time: {concurrent_time:.2f}s")
    print(f"Speedup: {sequential_time/concurrent_time:.1f}x")
    print(f"Results: {results}\n")

async def advanced_asyncio_patterns():
    """Patterns avanzados de AsyncIO"""
    print("=== ADVANCED ASYNCIO PATTERNS ===\n")
    
    async def task_with_timeout(name, delay):
        """Task que puede timeout"""
        try:
            await asyncio.sleep(delay)
            return f"Task {name} completed"
        except asyncio.CancelledError:
            print(f"Task {name} was cancelled!")
            raise
    
    # 1. Timeout handling
    print("1. TIMEOUT HANDLING:")
    try:
        result = await asyncio.wait_for(task_with_timeout("slow", 3), timeout=2)
        print(f"Result: {result}")
    except asyncio.TimeoutError:
        print("Task timed out after 2 seconds")
    
    # 2. Task cancellation
    print("\n2. TASK CANCELLATION:")
    task = asyncio.create_task(task_with_timeout("cancellable", 5))
    
    await asyncio.sleep(1)  # Let it run for 1 second
    task.cancel()
    
    try:
        await task
    except asyncio.CancelledError:
        print("Task was successfully cancelled")
    
    # 3. Running tasks with different completion strategies
    print("\n3. COMPLETION STRATEGIES:")
    
    tasks = [
        asyncio.create_task(task_with_timeout("fast", 0.5)),
        asyncio.create_task(task_with_timeout("medium", 1.5)),
        asyncio.create_task(task_with_timeout("slow", 2.5))
    ]
    
    # Wait for first completion
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    
    print(f"First completed: {len(done)} task(s)")
    print(f"Still pending: {len(pending)} task(s)")
    
    # Cancel pending tasks
    for task in pending:
        task.cancel()
    
    # Wait for all to finish (including cancellations)
    await asyncio.gather(*pending, return_exceptions=True)
    print()

# ========================
# ASYNCIO CON HTTP REQUESTS
# ========================

class AsyncWebScraper:
    """
    Web scraper asíncrono usando aiohttp
    Demuestra el poder real de AsyncIO para I/O
    """
    
    def __init__(self, max_concurrent=10, rate_limit=0.1):
        self.max_concurrent = max_concurrent
        self.rate_limit = rate_limit
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.session = None
        self.results = []
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def fetch_url(self, url):
        """
        Fetch single URL asíncronamente
        Con rate limiting y error handling
        """
        async with self.semaphore:  # Limit concurrent requests
            
            # Rate limiting
            await asyncio.sleep(self.rate_limit)
            
            try:
                print(f"Fetching {url}...")
                start_time = time.time()
                
                # Simular HTTP request (en real usarías aiohttp)
                response_time = random.uniform(0.1, 2.0)
                await asyncio.sleep(response_time)
                
                # Simular response
                status_code = random.choices([200, 404, 500], weights=[90, 8, 2])[0]
                content_length = random.randint(1000, 100000)
                
                result = {
                    'url': url,
                    'status_code': status_code,
                    'content_length': content_length,
                    'response_time': response_time,
                    'success': status_code == 200
                }
                
                self.results.append(result)
                print(f"✓ {url}: {status_code} ({response_time:.2f}s)")
                return result
                
            except Exception as e:
                print(f"✗ Error fetching {url}: {e}")
                return {'url': url, 'error': str(e), 'success': False}
    
    async def scrape_urls(self, urls):
        """Scrape multiple URLs concurrently"""
        print(f"Scraping {len(urls)} URLs with max {self.max_concurrent} concurrent...")
        
        start_time = time.time()
        
        # Crear tasks para todas las URLs
        tasks = [self.fetch_url(url) for url in urls]
        
        # Ejecutar todas concurrentemente
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        total_time = time.time() - start_time
        
        # Análisis de resultados
        successful = sum(1 for r in results if isinstance(r, dict) and r.get('success'))
        avg_response_time = sum(r.get('response_time', 0) for r in results if isinstance(r, dict)) / len(results)
        
        print(f"\nScraping completed:")
        print(f"   Total time: {total_time:.2f}s")
        print(f"   Successful: {successful}/{len(urls)}")
        print(f"   Average response time: {avg_response_time:.2f}s")
        print(f"   Requests/second: {len(urls)/total_time:.1f}")
        
        return results

# ========================
# ASYNC FILE OPERATIONS
# ========================

class AsyncFileProcessor:
    """
    Procesador de archivos asíncrono
    Demuestra file I/O async + CPU processing
    """
    
    async def read_file_async(self, filename):
        """Read file asíncronamente"""
        print(f"Reading {filename}...")
        
        # Simular file read
        await asyncio.sleep(random.uniform(0.1, 0.5))
        
        # Simular contenido
        lines = [f"Line {i} from {filename}" for i in range(random.randint(10, 100))]
        
        print(f"✓ Read {filename}: {len(lines)} lines")
        return lines
    
    async def process_file_content(self, filename, content):
        """Process file content (potentially CPU-bound)"""
        print(f"Processing {filename}...")
        
        # Simular processing
        await asyncio.sleep(random.uniform(0.2, 1.0))
        
        # Análisis simulado
        word_count = sum(len(line.split()) for line in content)
        char_count = sum(len(line) for line in content)
        
        result = {
            'filename': filename,
            'line_count': len(content),
            'word_count': word_count,
            'char_count': char_count,
            'processed_at': datetime.now().isoformat()
        }
        
        print(f"✓ Processed {filename}: {word_count} words")
        return result
    
    async def write_results_async(self, results, output_file):
        """Write results asíncronamente"""
        print(f"Writing results to {output_file}...")
        
        # Simular write operation
        await asyncio.sleep(0.3)
        
        # En real usarías aiofiles
        print(f"✓ Written {len(results)} results to {output_file}")
        return f"Results saved to {output_file}"
    
    async def process_files_pipeline(self, filenames):
        """Pipeline completo de procesamiento"""
        print("=== ASYNC FILE PROCESSING PIPELINE ===")
        
        start_time = time.time()
        
        # Stage 1: Read all files concurrently
        print("Stage 1: Reading files...")
        read_tasks = [self.read_file_async(filename) for filename in filenames]
        file_contents = await asyncio.gather(*read_tasks)
        
        # Stage 2: Process all contents concurrently
        print("\nStage 2: Processing contents...")
        process_tasks = [
            self.process_file_content(filename, content)
            for filename, content in zip(filenames, file_contents)
        ]
        results = await asyncio.gather(*process_tasks)
        
        # Stage 3: Write results
        print("\nStage 3: Writing results...")
        await self.write_results_async(results, "output.json")
        
        total_time = time.time() - start_time
        print(f"\nPipeline completed in {total_time:.2f}s")
        print(f"Processed {len(filenames)} files")
        
        return results

# ========================
# ASYNC PRODUCER-CONSUMER
# ========================

class AsyncProducerConsumer:
    """
    Producer-Consumer pattern usando AsyncIO
    Más elegante que threading version
    """
    
    def __init__(self, max_queue_size=10):
        self.queue = asyncio.Queue(maxsize=max_queue_size)
        self.stats = {
            'produced': 0,
            'consumed': 0,
            'in_progress': 0
        }
        self.stats_lock = asyncio.Lock()
    
    async def producer(self, producer_id, num_items=10):
        """Async producer"""
        print(f"Producer {producer_id} starting...")
        
        for i in range(num_items):
            item = {
                'id': f"item-{producer_id}-{i}",
                'producer_id': producer_id,
                'data': random.randint(1, 1000),
                'created_at': time.time()
            }
            
            # Put item in queue (blocks if queue is full)
            await self.queue.put(item)
            
            async with self.stats_lock:
                self.stats['produced'] += 1
            
            print(f"Producer {producer_id} produced: {item['id']}")
            
            # Simular variable production rate
            await asyncio.sleep(random.uniform(0.1, 0.5))
        
        print(f"Producer {producer_id} finished")
    
    async def consumer(self, consumer_id):
        """Async consumer"""
        print(f"Consumer {consumer_id} starting...")
        
        while True:
            try:
                # Get item con timeout
                item = await asyncio.wait_for(self.queue.get(), timeout=2.0)
                
                async with self.stats_lock:
                    self.stats['in_progress'] += 1
                
                print(f"Consumer {consumer_id} got: {item['id']}")
                
                # Simular processing
                processing_time = random.uniform(0.2, 1.0)
                await asyncio.sleep(processing_time)
                
                # Mark task as done
                self.queue.task_done()
                
                async with self.stats_lock:
                    self.stats['consumed'] += 1
                    self.stats['in_progress'] -= 1
                
                print(f"Consumer {consumer_id} finished: {item['id']} ({processing_time:.2f}s)")
                
            except asyncio.TimeoutError:
                print(f"Consumer {consumer_id} timeout - assuming shutdown")
                break
            except Exception as e:
                print(f"Consumer {consumer_id} error: {e}")
        
        print(f"Consumer {consumer_id} finished")
    
    async def run_simulation(self, num_producers=2, num_consumers=3, duration=5):
        """Ejecutar simulación completa"""
        print("=== ASYNC PRODUCER-CONSUMER SIMULATION ===")
        
        # Crear producers
        producer_tasks = [
            asyncio.create_task(self.producer(i, 8))
            for i in range(num_producers)
        ]
        
        # Crear consumers
        consumer_tasks = [
            asyncio.create_task(self.consumer(i))
            for i in range(num_consumers)
        ]
        
        # Esperar que producers terminen
        await asyncio.gather(*producer_tasks)
        print("All producers finished")
        
        # Esperar que queue se vacíe
        await self.queue.join()
        print("All items processed")
        
        # Cancel consumers (están en loop infinito)
        for task in consumer_tasks:
            task.cancel()
        
        # Wait for consumers to finish
        await asyncio.gather(*consumer_tasks, return_exceptions=True)
        
        # Mostrar estadísticas
        print(f"\nFinal Statistics:")
        print(f"   Produced: {self.stats['produced']}")
        print(f"   Consumed: {self.stats['consumed']}")
        print(f"   In Progress: {self.stats['in_progress']}")
        print()

# ========================
# ASYNC HTTP CLIENT
# ========================

class AsyncHTTPClient:
    """
    Cliente HTTP asíncrono para APIs
    Ejemplo real de high-performance API consumption
    """
    
    def __init__(self, max_concurrent=20, rate_limit=0.05):
        self.max_concurrent = max_concurrent
        self.rate_limit = rate_limit
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.session = None
        self.request_stats = {
            'total': 0,
            'successful': 0,
            'failed': 0,
            'total_time': 0
        }
    
    async def __aenter__(self):
        """Async context manager"""
        connector = aiohttp.TCPConnector(limit=100, limit_per_host=30)
        timeout = aiohttp.ClientTimeout(total=10)
        self.session = aiohttp.ClientSession(connector=connector, timeout=timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def make_request(self, url, method="GET", **kwargs):
        """
        Make single HTTP request asíncronamente
        Con rate limiting, retries, y error handling
        """
        async with self.semaphore:
            
            await asyncio.sleep(self.rate_limit)  # Rate limiting
            
            start_time = time.time()
            
            try:
                # Simular HTTP request (en real usarías aiohttp)
                response_time = random.uniform(0.1, 2.0)
                await asyncio.sleep(response_time)
                
                # Simular response
                status_code = random.choices([200, 404, 500, 503], weights=[85, 10, 3, 2])[0]
                
                if status_code == 200:
                    # Simular response data
                    data = {
                        'id': random.randint(1, 1000),
                        'name': f"Item from {url}",
                        'value': random.uniform(1, 100)
                    }
                    
                    self.request_stats['successful'] += 1
                    print(f"✓ {method} {url}: {status_code} ({response_time:.2f}s)")
                    
                    return {
                        'url': url,
                        'status_code': status_code,
                        'data': data,
                        'response_time': response_time
                    }
                else:
                    self.request_stats['failed'] += 1
                    print(f"✗ {method} {url}: {status_code}")
                    return {'url': url, 'status_code': status_code, 'error': f"HTTP {status_code}"}
                
            except Exception as e:
                self.request_stats['failed'] += 1
                print(f"✗ {method} {url}: Exception - {e}")
                return {'url': url, 'error': str(e)}
            
            finally:
                self.request_stats['total'] += 1
                self.request_stats['total_time'] += time.time() - start_time
    
    async def batch_requests(self, urls):
        """Hacer múltiples requests en batch"""
        print(f"Making {len(urls)} async HTTP requests...")
        
        start_time = time.time()
        
        # Crear tasks para todas las requests
        tasks = [self.make_request(url) for url in urls]
        
        # Ejecutar con progress reporting
        results = []
        completed = 0
        
        for coro in asyncio.as_completed(tasks):
            result = await coro
            results.append(result)
            completed += 1
            
            if completed % 10 == 0 or completed == len(urls):
                print(f"Progress: {completed}/{len(urls)} requests completed")
        
        total_time = time.time() - start_time
        
        # Statistics
        print(f"\nBatch Request Statistics:")
        print(f"   Total requests: {self.request_stats['total']}")
        print(f"   Successful: {self.request_stats['successful']}")
        print(f"   Failed: {self.request_stats['failed']}")
        print(f"   Success rate: {self.request_stats['successful']/self.request_stats['total']*100:.1f}%")
        print(f"   Total time: {total_time:.2f}s")
        print(f"   Requests/second: {len(urls)/total_time:.1f}")
        print(f"   Average response time: {self.request_stats['total_time']/self.request_stats['total']:.3f}s")
        
        return results

# ========================
# ASYNC DATABASE OPERATIONS
# ========================

class AsyncDatabaseSimulator:
    """
    Simulador de operaciones de database asíncronas
    Patrón común para applications con heavy DB usage
    """
    
    def __init__(self, connection_pool_size=10):
        self.pool_size = connection_pool_size
        self.connection_semaphore = asyncio.Semaphore(connection_pool_size)
        self.query_stats = defaultdict(int)
        self.stats_lock = asyncio.Lock()
    
    async def execute_query(self, query_type, query_data):
        """
        Ejecutar query asíncrona con connection pooling
        """
        async with self.connection_semaphore:
            
            query_id = f"{query_type}_{int(time.time() * 1000000)}"
            print(f"Executing query {query_id}...")
            
            try:
                # Simular different query types
                if query_type == "SELECT":
                    execution_time = random.uniform(0.1, 0.8)
                    await asyncio.sleep(execution_time)
                    
                    # Simular resultset
                    result = {
                        'rows': [{'id': i, 'data': f"row_{i}"} for i in range(random.randint(1, 50))],
                        'execution_time': execution_time
                    }
                    
                elif query_type == "INSERT":
                    execution_time = random.uniform(0.05, 0.3)
                    await asyncio.sleep(execution_time)
                    
                    result = {
                        'inserted_id': random.randint(1000, 9999),
                        'execution_time': execution_time
                    }
                    
                elif query_type == "UPDATE":
                    execution_time = random.uniform(0.1, 0.5)
                    await asyncio.sleep(execution_time)
                    
                    result = {
                        'affected_rows': random.randint(1, 20),
                        'execution_time': execution_time
                    }
                
                else:  # DELETE
                    execution_time = random.uniform(0.1, 0.4)
                    await asyncio.sleep(execution_time)
                    
                    result = {
                        'deleted_rows': random.randint(1, 10),
                        'execution_time': execution_time
                    }
                
                async with self.stats_lock:
                    self.query_stats[query_type] += 1
                    self.query_stats['total_time'] += execution_time
                
                print(f"✓ Query {query_id} completed ({execution_time:.3f}s)")
                return result
                
            except Exception as e:
                async with self.stats_lock:
                    self.query_stats['failed'] += 1
                
                print(f"✗ Query {query_id} failed: {e}")
                raise
    
    async def simulate_database_load(self, num_queries=50):
        """Simular carga realista de database"""
        print("=== ASYNC DATABASE SIMULATION ===")
        
        # Generar queries realistas
        query_types = ['SELECT', 'INSERT', 'UPDATE', 'DELETE']
        query_weights = [60, 25, 10, 5]  # Realistic distribution
        
        queries = []
        for i in range(num_queries):
            query_type = random.choices(query_types, weights=query_weights)[0]
            query_data = {'table': f"table_{random.randint(1, 5)}", 'data': f"data_{i}"}
            queries.append((query_type, query_data))
        
        start_time = time.time()
        
        # Ejecutar todas las queries concurrentemente
        tasks = [self.execute_query(qtype, qdata) for qtype, qdata in queries]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        total_time = time.time() - start_time
        
        # Análisis de performance
        successful = sum(1 for r in results if not isinstance(r, Exception))
        
        print(f"\nDatabase Load Test Results:")
        print(f"   Total queries: {num_queries}")
        print(f"   Successful: {successful}")
        print(f"   Failed: {num_queries - successful}")
        print(f"   Total time: {total_time:.2f}s")
        print(f"   Queries/second: {num_queries/total_time:.1f}")
        
        # Query type breakdown
        async with self.stats_lock:
            total_db_time = self.query_stats['total_time']
            print(f"   Average query time: {total_db_time/successful:.3f}s")
            
            print("   Query type distribution:")
            for qtype in query_types:
                count = self.query_stats[qtype]
                percentage = count / successful * 100 if successful > 0 else 0
                print(f"     {qtype}: {count} ({percentage:.1f}%)")
        
        print()

# ========================
# REAL-TIME DATA STREAMING
# ========================

class AsyncDataStreamer:
    """
    Streaming de datos en tiempo real
    Simula WebSocket connections, chat systems, etc.
    """
    
    def __init__(self):
        self.subscribers = {}
        self.message_stats = defaultdict(int)
        self.stats_lock = asyncio.Lock()
    
    async def data_producer(self, stream_id, rate=1.0):
        """Produce stream de datos"""
        print(f"Data stream {stream_id} starting (rate: {rate}/s)...")
        
        message_count = 0
        while message_count < 20:  # Limitar para demo
            
            # Generar data point
            data_point = {
                'stream_id': stream_id,
                'timestamp': time.time(),
                'value': random.uniform(0, 100),
                'message_id': message_count
            }
            
            # Broadcast a todos los subscribers
            await self.broadcast_to_subscribers(stream_id, data_point)
            
            message_count += 1
            await asyncio.sleep(1.0 / rate)  # Maintain rate
        
        print(f"Data stream {stream_id} finished")
    
    async def broadcast_to_subscribers(self, stream_id, data):
        """Broadcast data a subscribers"""
        if stream_id not in self.subscribers:
            return
        
        # Send to all subscribers concurrently
        tasks = []
        for subscriber_id, queue in self.subscribers[stream_id].items():
            task = asyncio.create_task(self.send_to_subscriber(subscriber_id, queue, data))
            tasks.append(task)
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        
        async with self.stats_lock:
            self.message_stats[f'stream_{stream_id}_messages'] += 1
    
    async def send_to_subscriber(self, subscriber_id, queue, data):
        """Send data a subscriber específico"""
        try:
            await queue.put(data)
            async with self.stats_lock:
                self.message_stats[f'subscriber_{subscriber_id}_received'] += 1
        except Exception as e:
            print(f"Failed to send to subscriber {subscriber_id}: {e}")
    
    async def subscriber(self, subscriber_id, streams_to_follow):
        """Subscriber que recibe data de múltiples streams"""
        print(f"Subscriber {subscriber_id} starting...")
        
        # Crear queue para recibir messages
        message_queue = asyncio.Queue(maxsize=100)
        
        # Subscribe a streams
        for stream_id in streams_to_follow:
            if stream_id not in self.subscribers:
                self.subscribers[stream_id] = {}
            self.subscribers[stream_id][subscriber_id] = message_queue
        
        received_count = 0
        
        try:
            while received_count < 30:  # Limitar para demo
                try:
                    # Wait for messages
                    data = await asyncio.wait_for(message_queue.get(), timeout=3.0)
                    
                    print(f"Subscriber {subscriber_id} received from stream {data['stream_id']}: "
                          f"value={data['value']:.2f}")
                    
                    # Simular processing del message
                    await asyncio.sleep(random.uniform(0.01, 0.1))
                    
                    received_count += 1
                    
                except asyncio.TimeoutError:
                    print(f"Subscriber {subscriber_id} timeout - no more messages")
                    break
        
        finally:
            # Cleanup: remove from subscribers
            for stream_id in streams_to_follow:
                if stream_id in self.subscribers and subscriber_id in self.subscribers[stream_id]:
                    del self.subscribers[stream_id][subscriber_id]
        
        print(f"Subscriber {subscriber_id} finished (received {received_count} messages)")
    
    async def simulate_streaming(self):
        """Simular sistema de streaming completo"""
        print("=== REAL-TIME DATA STREAMING SIMULATION ===")
        
        # Crear multiple data streams
        stream_tasks = [
            asyncio.create_task(self.data_producer("crypto", 2.0)),    # 2 messages/second
            asyncio.create_task(self.data_producer("stocks", 1.5)),    # 1.5 messages/second
            asyncio.create_task(self.data_producer("weather", 0.5))    # 0.5 messages/second
        ]
        
        # Crear subscribers
        subscriber_tasks = [
            asyncio.create_task(self.subscriber("trader_1", ["crypto", "stocks"])),
            asyncio.create_task(self.subscriber("analyst_1", ["stocks", "weather"])),
            asyncio.create_task(self.subscriber("monitor_1", ["crypto", "stocks", "weather"]))
        ]
        
        # Ejecutar streams y subscribers concurrentemente
        all_tasks = stream_tasks + subscriber_tasks
        
        try:
            await asyncio.gather(*all_tasks, return_exceptions=True)
        except Exception as e:
            print(f"Streaming simulation error: {e}")
        
        # Mostrar estadísticas finales
        print(f"\nStreaming Statistics:")
        async with self.stats_lock:
            for key, value in self.message_stats.items():
                print(f"   {key}: {value}")
        print()

# ========================
# PERFORMANCE COMPARISON
# ========================

async def compare_sync_vs_async():
    """Comparación directa: sync vs async I/O"""
    print("=== SYNC VS ASYNC PERFORMANCE COMPARISON ===\n")
    
    def sync_io_task(task_id, delay):
        """Synchronous I/O task"""
        print(f"Sync task {task_id} starting...")
        time.sleep(delay)  # Blocking sleep
        print(f"Sync task {task_id} completed")
        return f"sync_result_{task_id}"
    
    async def async_io_task(task_id, delay):
        """Asynchronous I/O task"""
        print(f"Async task {task_id} starting...")
        await asyncio.sleep(delay)  # Non-blocking sleep
        print(f"Async task {task_id} completed")
        return f"async_result_{task_id}"
    
    num_tasks = 10
    delay_per_task = 0.5
    
    # Synchronous execution
    print("1. SYNCHRONOUS EXECUTION:")
    start = time.time()
    sync_results = []
    for i in range(num_tasks):
        result = sync_io_task(i, delay_per_task)
        sync_results.append(result)
    sync_time = time.time() - start
    
    print(f"Synchronous total time: {sync_time:.2f}s\n")
    
    # Asynchronous execution
    print("2. ASYNCHRONOUS EXECUTION:")
    start = time.time()
    
    async_tasks = [async_io_task(i, delay_per_task) for i in range(num_tasks)]
    async_results = await asyncio.gather(*async_tasks)
    
    async_time = time.time() - start
    
    print(f"Asynchronous total time: {async_time:.2f}s")
    print(f"Speedup: {sync_time/async_time:.1f}x faster")
    print(f"Efficiency: {num_tasks * delay_per_task / async_time:.1f}x theoretical maximum\n")

# ========================
# ASYNC CONTEXT MANAGERS
# ========================

class AsyncResourceManager:
    """
    Async context manager para manejo de recursos
    Patrón importante para database connections, file handles, etc.
    """
    
    def __init__(self, resource_name, setup_time=0.1, cleanup_time=0.05):
        self.resource_name = resource_name
        self.setup_time = setup_time
        self.cleanup_time = cleanup_time
        self.resource = None
    
    async def __aenter__(self):
        """Setup asíncrono del recurso"""
        print(f"Setting up {self.resource_name}...")
        await asyncio.sleep(self.setup_time)
        
        self.resource = {
            'name': self.resource_name,
            'created_at': time.time(),
            'operations': 0
        }
        
        print(f"✓ {self.resource_name} ready")
        return self.resource
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup asíncrono del recurso"""
        if self.resource:
            print(f"Cleaning up {self.resource_name} (performed {self.resource['operations']} operations)...")
            await asyncio.sleep(self.cleanup_time)
            print(f"✓ {self.resource_name} cleaned up")
        
        if exc_type:
            print(f"Exception during {self.resource_name} usage: {exc_val}")
        
        return False  # Don't suppress exceptions

async def demonstrate_async_context_managers():
    """Demostrar async context managers"""
    print("=== ASYNC CONTEXT MANAGERS ===")
    
    async def use_resource(resource_name, operations=3):
        """Usar recurso con async context manager"""
        async with AsyncResourceManager(resource_name) as resource:
            
            for i in range(operations):
                print(f"Performing operation {i+1} on {resource['name']}")
                await asyncio.sleep(0.1)  # Simular work
                resource['operations'] += 1
            
            return f"Completed {operations} operations on {resource['name']}"
    
    # Usar múltiples recursos concurrentemente
    tasks = [
        use_resource("Database Connection", 3),
        use_resource("File Handle", 2),
        use_resource("Network Socket", 4)
    ]
    
    results = await asyncio.gather(*tasks)
    
    for result in results:
        print(f"Result: {result}")
    
    print()

# ========================
# ERROR HANDLING AVANZADO
# ========================

async def robust_async_operations():
    """Manejo robusto de errores en AsyncIO"""
    print("=== ROBUST ASYNC ERROR HANDLING ===")
    
    async def unreliable_task(task_id, failure_rate=0.3):
        """Task que puede fallar aleatoriamente"""
        await asyncio.sleep(random.uniform(0.1, 0.5))
        
        if random.random() < failure_rate:
            raise ValueError(f"Task {task_id} failed randomly")
        
        return f"Task {task_id} succeeded"
    
    async def retry_with_backoff(task_func, max_retries=3, base_delay=0.1):
        """Retry con exponential backoff"""
        for attempt in range(max_retries):
            try:
                result = await task_func()
                return result
            except Exception as e:
                if attempt == max_retries - 1:
                    raise  # Re-raise en último attempt
                
                delay = base_delay * (2 ** attempt)
                print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay:.1f}s...")
                await asyncio.sleep(delay)
    
    # Test retry mechanism
    print("Testing retry mechanism:")
    
    tasks = []
    for i in range(5):
        task_func = lambda task_id=i: unreliable_task(task_id, failure_rate=0.4)
        retry_task = retry_with_backoff(task_func, max_retries=3)
        tasks.append(retry_task)
    
    # Ejecutar con error handling
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    successful = 0
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Task {i}: Failed permanently - {result}")
        else:
            print(f"Task {i}: {result}")
            successful += 1
    
    print(f"Success rate: {successful}/{len(results)} ({successful/len(results)*100:.1f}%)")
    print()

# ========================
# ASYNC GENERATORS
# ========================

async def async_generator_examples():
    """Async generators para streaming data"""
    print("=== ASYNC GENERATORS ===")
    
    async def async_data_stream(stream_name, count=10):
        """Async generator que produce stream de datos"""
        print(f"Starting {stream_name} stream...")
        
        for i in range(count):
            # Simular data generation
            await asyncio.sleep(random.uniform(0.1, 0.3))
            
            data_point = {
                'stream': stream_name,
                'sequence': i,
                'value': random.uniform(0, 100),
                'timestamp': time.time()
            }
            
            print(f"{stream_name}: Generated data point {i}")
            yield data_point
        
        print(f"{stream_name} stream completed")
    
    # Consumir async generator
    print("Consuming async data stream:")
    
    async for data in async_data_stream("sensor_1", 5):
        print(f"Received: {data['stream']} #{data['sequence']} = {data['value']:.2f}")
        
        # Simular processing
        await asyncio.sleep(0.05)
    
    print()

# ========================
# TESTING FRAMEWORK
# ========================

async def comprehensive_asyncio_test():
    """Test comprehensivo de todos los conceptos AsyncIO"""
    print("🚀 COMPREHENSIVE ASYNCIO TEST SUITE 🚀\n")
    
    # Basic concepts
    await basic_coroutine_example()
    await advanced_asyncio_patterns()
    
    # Performance comparison
    await compare_sync_vs_async()
    
    # Context managers
    await demonstrate_async_context_managers()
    
    # Error handling
    await robust_async_operations()
    
    # Generators
    await async_generator_examples()
    
    # Real-world examples
    urls = [f"https://api.example.com/data/{i}" for i in range(20)]
    
    async with AsyncHTTPClient(max_concurrent=5) as client:
        await client.batch_requests(urls[:10])  # Subset para demo
    
    # Database simulation
    db_sim = AsyncDatabaseSimulator(connection_pool_size=5)
    await db_sim.simulate_database_load(30)
    
    # Producer-Consumer
    pc = AsyncProducerConsumer()
    await pc.run_simulation(num_producers=2, num_consumers=3, duration=3)
    
    # Data streaming
    streamer = AsyncDataStreamer()
    
    # Crear streams y subscribers concurrentemente
    stream_task = asyncio.create_task(streamer.data_producer("test_stream", 10))
    subscriber_task = asyncio.create_task(streamer.subscriber("sub_1", ["test_stream"]))
    
    await asyncio.gather(stream_task, subscriber_task, return_exceptions=True)
    
    print("🎉 ALL ASYNCIO TESTS COMPLETED! 🎉")

# Entry point
if __name__ == "__main__":
    # AsyncIO programs need to be run with asyncio.run()
    asyncio.run(comprehensive_asyncio_test())
