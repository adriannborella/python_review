"""
PROBLEMAS DE ENTREVISTA - ASYNCIO AVANZADO
==========================================

Estos problemas aparecen en entrevistas senior y de arquitectura:
- Async Web Crawler (85% en roles backend)
- Rate-Limited API Client (80% en roles de infrastructure)
- WebSocket Chat Server (70% en roles real-time)
- Async Task Scheduler (75% en roles de systems)
- Circuit Breaker Pattern (60% en roles microservices)

¡Dominar estos te posiciona como senior/staff engineer!
"""

import asyncio
import aiohttp
import time
import random
from typing import List, Dict, Optional, Callable, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict, deque
from enum import Enum
import json
import hashlib

# ========================
# PROBLEMA 1: Async Web Crawler
# ========================

@dataclass
class CrawlResult:
    url: str
    status_code: int
    content_length: int
    response_time: float
    links_found: List[str] = field(default_factory=list)
    error: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)

class AsyncWebCrawler:
    """
    Web crawler asíncrono con rate limiting y depth control
    Problema clásico que evalúa understanding completo de AsyncIO
    """
    
    def __init__(self, max_concurrent=10, max_depth=2, rate_limit=0.1):
        self.max_concurrent = max_concurrent
        self.max_depth = max_depth
        self.rate_limit = rate_limit
        self.semaphore = asyncio.Semaphore(max_concurrent_tasks)
        self.task_queue = asyncio.PriorityQueue()
        self.running_tasks = {}
        self.completed_tasks = {}
        self.failed_tasks = {}
        self.scheduler_running = False
        self.stats = defaultdict(int)
    
    async def schedule_task(self, task_id: str, func: Callable, 
                          delay: float = 0, *args, **kwargs):
        """Schedule task para ejecutar después de delay"""
        schedule_time = time.time() + delay
        
        task = ScheduledTask(
            id=task_id,
            func=func,
            args=args,
            kwargs=kwargs,
            schedule_time=schedule_time
        )
        
        # Priority queue usa (priority, item) - menor priority = mayor precedencia
        await self.task_queue.put((schedule_time, task))
        print(f"Scheduled task {task_id} for {delay:.1f}s from now")
        
        self.stats['scheduled'] += 1
    
    async def execute_task(self, task: ScheduledTask):
        """Execute individual task con error handling"""
        async with self.semaphore:
            task_id = task.id
            print(f"Executing task {task_id}...")
            
            try:
                # Add to running tasks
                self.running_tasks[task_id] = task
                
                start_time = time.time()
                
                # Execute task function
                if asyncio.iscoroutinefunction(task.func):
                    result = await task.func(*task.args, **task.kwargs)
                else:
                    # Run sync function en thread pool
                    loop = asyncio.get_event_loop()
                    result = await loop.run_in_executor(None, task.func, *task.args, **task.kwargs)
                
                execution_time = time.time() - start_time
                
                # Move to completed
                self.completed_tasks[task_id] = {
                    'task': task,
                    'result': result,
                    'execution_time': execution_time,
                    'completed_at': time.time()
                }
                
                self.stats['completed'] += 1
                print(f"✓ Task {task_id} completed ({execution_time:.3f}s)")
                
                return result
                
            except Exception as e:
                print(f"✗ Task {task_id} failed: {e}")
                
                # Retry logic
                if task.retry_count < task.max_retries:
                    task.retry_count += 1
                    retry_delay = 2 ** task.retry_count  # Exponential backoff
                    
                    print(f"Retrying task {task_id} in {retry_delay}s (attempt {task.retry_count})")
                    await self.schedule_task(
                        f"{task_id}_retry_{task.retry_count}",
                        task.func,
                        retry_delay,
                        *task.args,
                        **task.kwargs
                    )
                    self.stats['retries'] += 1
                else:
                    # Max retries exceeded
                    self.failed_tasks[task_id] = {
                        'task': task,
                        'error': str(e),
                        'failed_at': time.time()
                    }
                    self.stats['failed'] += 1
                
                raise
            
            finally:
                # Remove from running tasks
                self.running_tasks.pop(task_id, None)
    
    async def start_scheduler(self):
        """Start task scheduler loop"""
        print("=== ASYNC TASK SCHEDULER STARTED ===")
        self.scheduler_running = True
        
        while self.scheduler_running:
            try:
                # Get next task (blocks hasta que haya una)
                schedule_time, task = await asyncio.wait_for(
                    self.task_queue.get(), timeout=1.0
                )
                
                # Wait hasta que sea tiempo de ejecutar
                current_time = time.time()
                if schedule_time > current_time:
                    wait_time = schedule_time - current_time
                    print(f"Waiting {wait_time:.1f}s before executing {task.id}")
                    await asyncio.sleep(wait_time)
                
                # Execute task asíncronamente
                asyncio.create_task(self.execute_task(task))
                
            except asyncio.TimeoutError:
                # No hay tasks, continuar loop
                continue
            except Exception as e:
                print(f"Scheduler error: {e}")
    
    async def stop_scheduler(self):
        """Stop scheduler gracefully"""
        print("Stopping task scheduler...")
        self.scheduler_running = False
        
        # Wait for running tasks to complete
        if self.running_tasks:
            print(f"Waiting for {len(self.running_tasks)} running tasks to complete...")
            while self.running_tasks:
                await asyncio.sleep(0.1)
    
    def get_stats(self):
        """Get scheduler statistics"""
        return {
            'scheduled': self.stats['scheduled'],
            'completed': self.stats['completed'],
            'failed': self.stats['failed'],
            'retries': self.stats['retries'],
            'running': len(self.running_tasks),
            'queued': self.task_queue.qsize()
        }

async def test_task_scheduler():
    """Test async task scheduler"""
    print("=== TESTING ASYNC TASK SCHEDULER ===")
    
    # Sample tasks
    async def async_task(name, duration):
        print(f"  Running async task {name}...")
        await asyncio.sleep(duration)
        return f"Async task {name} completed"
    
    def sync_task(name, value):
        print(f"  Running sync task {name}...")
        time.sleep(0.5)  # Simular work
        if random.random() < 0.3:  # 30% failure rate
            raise ValueError(f"Task {name} failed")
        return f"Sync task {name}: {value * 2}"
    
    scheduler = AsyncTaskScheduler(max_concurrent_tasks=3)
    
    # Start scheduler en background
    scheduler_task = asyncio.create_task(scheduler.start_scheduler())
    
    # Schedule various tasks
    await scheduler.schedule_task("task_1", async_task, 0, "Alpha", 0.5)
    await scheduler.schedule_task("task_2", sync_task, 1, "Beta", 100)
    await scheduler.schedule_task("task_3", async_task, 2, "Gamma", 1.0)
    await scheduler.schedule_task("task_4", sync_task, 0.5, "Delta", 200)
    await scheduler.schedule_task("task_5", async_task, 3, "Epsilon", 0.3)
    
    # Let scheduler run for a while
    await asyncio.sleep(6)
    
    # Stop scheduler
    await scheduler.stop_scheduler()
    scheduler_task.cancel()
    
    # Print final statistics
    stats = scheduler.get_stats()
    print(f"\nScheduler Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print(f"Completed tasks: {len(scheduler.completed_tasks)}")
    print(f"Failed tasks: {len(scheduler.failed_tasks)}")
    print()

# ========================
# PROBLEMA 5: WebSocket Chat Server
# ========================

@dataclass
class ChatMessage:
    user_id: str
    room_id: str
    content: str
    timestamp: float = field(default_factory=time.time)
    message_id: str = field(default_factory=lambda: str(random.randint(100000, 999999)))

class AsyncChatServer:
    """
    WebSocket chat server simulation
    Maneja múltiples rooms y broadcasting
    """
    
    def __init__(self):
        self.rooms = defaultdict(set)  # room_id -> set of user_ids
        self.user_connections = {}     # user_id -> websocket (simulado)
        self.message_history = defaultdict(list)  # room_id -> messages
        self.stats = {
            'total_connections': 0,
            'active_connections': 0,
            'messages_sent': 0,
            'rooms_created': 0
        }
    
    async def handle_user_connection(self, user_id: str):
        """Handle new user connection"""
        print(f"User {user_id} connected")
        
        # Simular WebSocket connection
        user_queue = asyncio.Queue()
        self.user_connections[user_id] = user_queue
        self.stats['total_connections'] += 1
        self.stats['active_connections'] += 1
        
        try:
            # Simular connection lifecycle
            connection_duration = random.uniform(10, 30)
            await asyncio.sleep(connection_duration)
            
        finally:
            # Cleanup on disconnect
            await self.handle_user_disconnect(user_id)
    
    async def handle_user_disconnect(self, user_id: str):
        """Handle user disconnection"""
        print(f"User {user_id} disconnected")
        
        # Remove from all rooms
        rooms_to_leave = []
        for room_id, users in self.rooms.items():
            if user_id in users:
                rooms_to_leave.append(room_id)
        
        for room_id in rooms_to_leave:
            await self.leave_room(user_id, room_id)
        
        # Remove connection
        self.user_connections.pop(user_id, None)
        self.stats['active_connections'] -= 1
    
    async def join_room(self, user_id: str, room_id: str):
        """User joins chat room"""
        if room_id not in self.rooms:
            self.stats['rooms_created'] += 1
            print(f"Created new room: {room_id}")
        
        self.rooms[room_id].add(user_id)
        print(f"User {user_id} joined room {room_id}")
        
        # Send room history
        if self.message_history[room_id]:
            print(f"Sending {len(self.message_history[room_id])} historical messages to {user_id}")
        
        # Notify other users
        join_message = ChatMessage(
            user_id="system",
            room_id=room_id,
            content=f"{user_id} joined the room"
        )
        await self.broadcast_to_room(room_id, join_message, exclude_user=user_id)
    
    async def leave_room(self, user_id: str, room_id: str):
        """User leaves chat room"""
        if room_id in self.rooms and user_id in self.rooms[room_id]:
            self.rooms[room_id].remove(user_id)
            print(f"User {user_id} left room {room_id}")
            
            # Clean up empty rooms
            if not self.rooms[room_id]:
                del self.rooms[room_id]
                print(f"Room {room_id} deleted (empty)")
            else:
                # Notify remaining users
                leave_message = ChatMessage(
                    user_id="system",
                    room_id=room_id,
                    content=f"{user_id} left the room"
                )
                await self.broadcast_to_room(room_id, leave_message)
    
    async def send_message(self, message: ChatMessage):
        """Send message to room"""
        room_id = message.room_id
        
        # Validar que user está en room
        if message.user_id not in self.rooms.get(room_id, set()):
            print(f"User {message.user_id} not in room {room_id}")
            return False
        
        # Store message in history
        self.message_history[room_id].append(message)
        
        # Keep only last 100 messages per room
        if len(self.message_history[room_id]) > 100:
            self.message_history[room_id] = self.message_history[room_id][-100:]
        
        # Broadcast to room
        await self.broadcast_to_room(room_id, message)
        self.stats['messages_sent'] += 1
        return True
    
    async def broadcast_to_room(self, room_id: str, message: ChatMessage, exclude_user=None):
        """Broadcast message a todos los usuarios en room"""
        if room_id not in self.rooms:
            return
        
        recipients = self.rooms[room_id].copy()
        if exclude_user:
            recipients.discard(exclude_user)
        
        print(f"Broadcasting to room {room_id}: '{message.content}' (to {len(recipients)} users)")
        
        # Send to all connected users in room
        send_tasks = []
        for user_id in recipients:
            if user_id in self.user_connections:
                task = asyncio.create_task(self.send_to_user(user_id, message))
                send_tasks.append(task)
        
        if send_tasks:
            await asyncio.gather(*send_tasks, return_exceptions=True)
    
    async def send_to_user(self, user_id: str, message: ChatMessage):
        """Send message a usuario específico"""
        user_queue = self.user_connections.get(user_id)
        if user_queue:
            await user_queue.put(message)
            # Simular message delivery delay
            await asyncio.sleep(0.01)

async def simulate_chat_server():
    """Simulate chat server con múltiples usuarios y rooms"""
    print("=== WEBSOCKET CHAT SERVER SIMULATION ===")
    
    chat_server = AsyncChatServer()
    
    async def simulate_user(user_id: str, rooms: List[str]):
        """Simulate user behavior"""
        # Connect user
        connection_task = asyncio.create_task(chat_server.handle_user_connection(user_id))
        
        await asyncio.sleep(0.1)  # Connection delay
        
        # Join rooms
        for room_id in rooms:
            await chat_server.join_room(user_id, room_id)
            await asyncio.sleep(0.5)
        
        # Send some messages
        for i in range(random.randint(3, 8)):
            room_id = random.choice(rooms)
            message = ChatMessage(
                user_id=user_id,
                room_id=room_id,
                content=f"Message {i+1} from {user_id} in {room_id}"
            )
            await chat_server.send_message(message)
            await asyncio.sleep(random.uniform(1, 3))
        
        # Leave some rooms randomly
        if len(rooms) > 1 and random.random() < 0.5:
            room_to_leave = random.choice(rooms)
            await chat_server.leave_room(user_id, room_to_leave)
            await asyncio.sleep(1)
        
        # Keep connection alive for a bit more
        await asyncio.sleep(2)
        
        connection_task.cancel()
    
    # Simulate multiple users
    user_tasks = [
        simulate_user("alice", ["general", "tech"]),
        simulate_user("bob", ["general", "random"]),
        simulate_user("charlie", ["tech", "gaming"]),
        simulate_user("diana", ["general", "tech", "gaming"]),
        simulate_user("eve", ["random"])
    ]
    
    # Run simulation
    await asyncio.gather(*user_tasks, return_exceptions=True)
    
    # Print final statistics
    print(f"\n📊 CHAT SERVER STATISTICS:")
    print(f"   Total connections: {chat_server.stats['total_connections']}")
    print(f"   Active connections: {chat_server.stats['active_connections']}")
    print(f"   Messages sent: {chat_server.stats['messages_sent']}")
    print(f"   Rooms created: {chat_server.stats['rooms_created']}")
    print(f"   Active rooms: {len(chat_server.rooms)}")
    
    for room_id, users in chat_server.rooms.items():
        print(f"     Room {room_id}: {len(users)} users")
    print()

# ========================
# PROBLEMA 6: Async Load Balancer
# ========================

@dataclass
class ServerNode:
    id: str
    host: str
    port: int
    current_connections: int = 0
    total_requests: int = 0
    failure_count: int = 0
    last_health_check: float = field(default_factory=time.time)
    is_healthy: bool = True

class AsyncLoadBalancer:
    """
    Load balancer asíncrono con health checking
    Implementa different load balancing algorithms
    """
    
    def __init__(self, algorithm="round_robin"):
        self.servers = []
        self.algorithm = algorithm
        self.current_server_index = 0
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'server_failures': 0
        }
    
    def add_server(self, server: ServerNode):
        """Add server al load balancer"""
        self.servers.append(server)
        print(f"Added server {server.id} ({server.host}:{server.port})")
    
    async def health_check_server(self, server: ServerNode):
        """Check health de servidor específico"""
        try:
            # Simular health check
            await asyncio.sleep(0.1)
            
            # 90% chance of healthy response
            if random.random() < 0.9:
                server.is_healthy = True
                server.failure_count = 0
            else:
                server.failure_count += 1
                if server.failure_count >= 3:
                    server.is_healthy = False
            
            server.last_health_check = time.time()
            
        except Exception as e:
            server.failure_count += 1
            server.is_healthy = False
            print(f"Health check failed for {server.id}: {e}")
    
    async def health_check_all_servers(self):
        """Periodic health check para todos los servers"""
        while True:
            print("Performing health checks...")
            
            health_tasks = [self.health_check_server(server) for server in self.servers]
            await asyncio.gather(*health_tasks, return_exceptions=True)
            
            healthy_servers = sum(1 for s in self.servers if s.is_healthy)
            print(f"Health check completed: {healthy_servers}/{len(self.servers)} servers healthy")
            
            await asyncio.sleep(5)  # Health check every 5 seconds
    
    def select_server(self):
        """Select server basado en load balancing algorithm"""
        healthy_servers = [s for s in self.servers if s.is_healthy]
        
        if not healthy_servers:
            raise Exception("No healthy servers available")
        
        if self.algorithm == "round_robin":
            server = healthy_servers[self.current_server_index % len(healthy_servers)]
            self.current_server_index += 1
            return server
        
        elif self.algorithm == "least_connections":
            return min(healthy_servers, key=lambda s: s.current_connections)
        
        elif self.algorithm == "weighted_round_robin":
            # Simple weighted: prefer servers con fewer failures
            weights = [max(1, 10 - s.failure_count) for s in healthy_servers]
            server = random.choices(healthy_servers, weights=weights)[0]
            return server
        
        else:
            # Default to round robin
            return healthy_servers[self.current_server_index % len(healthy_servers)]
    
    async def forward_request(self, request_data):
        """Forward request a selected server"""
        try:
            server = self.select_server()
            
            print(f"Forwarding request to {server.id}...")
            
            # Track connection
            server.current_connections += 1
            server.total_requests += 1
            self.stats['total_requests'] += 1
            
            try:
                # Simular request processing
                processing_time = random.uniform(0.1, 1.0)
                await asyncio.sleep(processing_time)
                
                # Simular server response
                if random.random() < 0.95:  # 95% success rate
                    response = {
                        'server_id': server.id,
                        'data': f"Response from {server.id}",
                        'processing_time': processing_time
                    }
                    
                    self.stats['successful_requests'] += 1
                    print(f"✓ Request completed by {server.id} ({processing_time:.3f}s)")
                    return response
                else:
                    raise Exception(f"Server {server.id} internal error")
                    
            finally:
                server.current_connections -= 1
                
        except Exception as e:
            self.stats['failed_requests'] += 1
            self.stats['server_failures'] += 1
            print(f"✗ Request failed: {e}")
            raise

async def test_load_balancer():
    """Test load balancer con traffic simulation"""
    print("=== ASYNC LOAD BALANCER TEST ===")
    
    # Create load balancer
    lb = AsyncLoadBalancer(algorithm="least_connections")
    
    # Add servers
    servers = [
        ServerNode("web1", "192.168.1.10", 80),
        ServerNode("web2", "192.168.1.11", 80),
        ServerNode("web3", "192.168.1.12", 80),
        ServerNode("web4", "192.168.1.13", 80)
    ]
    
    for server in servers:
        lb.add_server(server)
    
    # Start health checking
    health_check_task = asyncio.create_task(lb.health_check_all_servers())
    
    # Simulate client requests
    async def generate_requests():
        for i in range(20):
            try:
                request_data = {'request_id': i, 'data': f'request_{i}'}
                await lb.forward_request(request_data)
            except Exception as e:
                print(f"Request {i} failed: {e}")
            
            # Variable request rate
            await asyncio.sleep(random.uniform(0.1, 0.5))
    
    # Run traffic simulation
    await generate_requests()
    
    # Stop health checking
    health_check_task.cancel()
    
    # Print statistics
    print(f"\n⚖️  LOAD BALANCER STATISTICS:")
    print(f"   Algorithm: {lb.algorithm}")
    print(f"   Total requests: {lb.stats['total_requests']}")
    print(f"   Successful: {lb.stats['successful_requests']}")
    print(f"   Failed: {lb.stats['failed_requests']}")
    print(f"   Success rate: {lb.stats['successful_requests']/lb.stats['total_requests']*100:.1f}%")
    
    print(f"\n   Server Statistics:")
    for server in servers:
        print(f"     {server.id}: {server.total_requests} requests, "
              f"{server.current_connections} active, "
              f"healthy: {server.is_healthy}")
    print()

# ========================
# COMPREHENSIVE TEST SUITE
# ========================

async def run_all_asyncio_interview_tests():
    """Run todos los tests de AsyncIO interview problems"""
    print("🎯 ASYNCIO INTERVIEW PROBLEMS - COMPREHENSIVE TEST 🎯\n")
    
    # 1. Web Crawler
    crawler = AsyncWebCrawler(max_concurrent=3, max_depth=2)
    seed_urls = [
        "https://example.com",
        "https://test-site.com",
        "https://demo.org"
    ]
    await crawler.crawl_website(seed_urls)
    
    # 2. Rate-Limited API Client  
    api_client = RateLimitedAPIClient(requests_per_second=8, burst_size=15)
    endpoints = [f"https://api.example.com/data/{i}" for i in range(25)]
    await api_client.batch_api_requests(endpoints)
    
    # 3. Circuit Breaker
    await test_circuit_breaker()
    
    # 4. Task Scheduler
    await test_task_scheduler()
    
    # 5. Chat Server
    await simulate_chat_server()
    
    # 6. Load Balancer
    await test_load_balancer()
    
    print("🏆 ALL ASYNCIO INTERVIEW TESTS COMPLETED! 🏆")
    print("\nKey Patterns Demonstrated:")
    print("✓ Concurrent I/O with rate limiting")
    print("✓ Error handling and retry mechanisms") 
    print("✓ Circuit breaker for fault tolerance")
    print("✓ Task scheduling and priority queues")
    print("✓ Real-time communication patterns")
    print("✓ Load balancing and health checking")

# Run all tests
if __name__ == "__main__":
    asyncio.run(run_all_asyncio_interview_tests())
(max_concurrent)
        
        # State tracking
        self.visited_urls = set()
        self.crawl_queue = asyncio.Queue()
        self.results = []
        self.stats = {
            'pages_crawled': 0,
            'links_discovered': 0,
            'errors': 0,
            'total_time': 0
        }
    
    async def extract_links(self, url, content):
        """
        Extract links from page content (simulado)
        En real usarías BeautifulSoup o similar
        """
        # Simular parsing de HTML y extracción de links
        await asyncio.sleep(0.05)  # Simular parsing time
        
        # Generar links simulados
        base_domain = url.split('/')[2] if len(url.split('/')) > 2 else 'example.com'
        num_links = random.randint(3, 15)
        
        links = []
        for i in range(num_links):
            if random.random() < 0.7:  # 70% internal links
                link = f"https://{base_domain}/page_{random.randint(1, 100)}"
            else:  # 30% external links
                link = f"https://external-{random.randint(1, 10)}.com/page_{i}"
            links.append(link)
        
        return links
    
    async def crawl_page(self, url, depth=0):
        """
        Crawl single page asíncronamente
        Con full error handling y metrics
        """
        if depth > self.max_depth or url in self.visited_urls:
            return None
        
        self.visited_urls.add(url)
        
        async with self.semaphore:
            start_time = time.time()
            
            try:
                print(f"Crawling {url} (depth {depth})...")
                
                # Rate limiting
                await asyncio.sleep(self.rate_limit)
                
                # Simular HTTP request
                response_time = random.uniform(0.1, 2.0)
                await asyncio.sleep(response_time)
                
                # Simular response
                status_code = random.choices([200, 404, 500, 503], weights=[85, 10, 3, 2])[0]
                
                if status_code == 200:
                    content_length = random.randint(1000, 50000)
                    content = f"Simulated content for {url}"
                    
                    # Extract links si no estamos en max depth
                    links = []
                    if depth < self.max_depth:
                        links = await self.extract_links(url, content)
                        self.stats['links_discovered'] += len(links)
                    
                    result = CrawlResult(
                        url=url,
                        status_code=status_code,
                        content_length=content_length,
                        response_time=response_time,
                        links_found=links
                    )
                    
                    # Queue new links para crawling
                    for link in links:
                        if link not in self.visited_urls:
                            await self.crawl_queue.put((link, depth + 1))
                    
                else:
                    result = CrawlResult(
                        url=url,
                        status_code=status_code,
                        content_length=0,
                        response_time=response_time,
                        error=f"HTTP {status_code}"
                    )
                    self.stats['errors'] += 1
                
                self.results.append(result)
                self.stats['pages_crawled'] += 1
                self.stats['total_time'] += response_time
                
                print(f"✓ Crawled {url}: {status_code} ({response_time:.2f}s, {len(result.links_found)} links)")
                return result
                
            except Exception as e:
                error_result = CrawlResult(
                    url=url,
                    status_code=0,
                    content_length=0,
                    response_time=time.time() - start_time,
                    error=str(e)
                )
                
                self.results.append(error_result)
                self.stats['errors'] += 1
                
                print(f"✗ Error crawling {url}: {e}")
                return error_result
    
    async def crawl_website(self, start_urls: List[str]):
        """
        Crawl website completo starting from seed URLs
        Implementa breadth-first crawling strategy
        """
        print(f"=== ASYNC WEB CRAWLER ===")
        print(f"Starting crawl with {len(start_urls)} seed URLs...")
        print(f"Max depth: {self.max_depth}, Max concurrent: {self.max_concurrent}")
        
        # Initialize queue con seed URLs
        for url in start_urls:
            await self.crawl_queue.put((url, 0))
        
        # Worker tasks para process queue
        worker_tasks = []
        for i in range(min(self.max_concurrent, len(start_urls))):
            task = asyncio.create_task(self.crawl_worker(f"worker_{i}"))
            worker_tasks.append(task)
        
        # Esperar que queue se vacíe
        await self.crawl_queue.join()
        
        # Cancel workers
        for task in worker_tasks:
            task.cancel()
        
        await asyncio.gather(*worker_tasks, return_exceptions=True)
        
        # Mostrar resultados finales
        self.print_crawl_summary()
        return self.results
    
    async def crawl_worker(self, worker_id):
        """Worker que procesa URLs de la queue"""
        print(f"Crawl worker {worker_id} started")
        
        try:
            while True:
                url, depth = await self.crawl_queue.get()
                await self.crawl_page(url, depth)
                self.crawl_queue.task_done()
        except asyncio.CancelledError:
            print(f"Crawl worker {worker_id} cancelled")
    
    def print_crawl_summary(self):
        """Imprimir resumen del crawling"""
        print(f"\n📊 CRAWL SUMMARY:")
        print(f"   Pages crawled: {self.stats['pages_crawled']}")
        print(f"   Links discovered: {self.stats['links_discovered']}")
        print(f"   Errors: {self.stats['errors']}")
        print(f"   Average response time: {self.stats['total_time']/max(1, self.stats['pages_crawled']):.3f}s")
        
        # Status code distribution
        status_codes = defaultdict(int)
        for result in self.results:
            status_codes[result.status_code] += 1
        
        print("   Status code distribution:")
        for code, count in sorted(status_codes.items()):
            percentage = count / len(self.results) * 100
            print(f"     {code}: {count} ({percentage:.1f}%)")
        print()

# ========================
# PROBLEMA 2: Rate-Limited API Client
# ========================

class RateLimitedAPIClient:
    """
    Cliente API con rate limiting sofisticado
    Implementa multiple rate limiting strategies
    """
    
    def __init__(self, requests_per_second=10, burst_size=20):
        self.requests_per_second = requests_per_second
        self.burst_size = burst_size
        
        # Token bucket for rate limiting
        self.tokens = burst_size
        self.last_refill = time.time()
        self.rate_lock = asyncio.Lock()
        
        # Statistics
        self.request_stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'rate_limited': 0,
            'errors': 0
        }
    
    async def acquire_rate_limit_token(self):
        """
        Acquire token from rate limiter usando Token Bucket algorithm
        """
        async with self.rate_lock:
            now = time.time()
            time_passed = now - self.last_refill
            
            # Refill tokens based on time passed
            tokens_to_add = time_passed * self.requests_per_second
            self.tokens = min(self.burst_size, self.tokens + tokens_to_add)
            self.last_refill = now
            
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            else:
                # Calculate wait time
                wait_time = (1 - self.tokens) / self.requests_per_second
                await asyncio.sleep(wait_time)
                self.tokens = 0
                return True
    
    async def make_api_request(self, endpoint, method="GET", data=None):
        """
        Make API request con rate limiting y retry logic
        """
        await self.acquire_rate_limit_token()
        
        self.request_stats['total_requests'] += 1
        
        try:
            print(f"Making {method} request to {endpoint}...")
            
            # Simular API request
            start_time = time.time()
            response_time = random.uniform(0.1, 1.0)
            await asyncio.sleep(response_time)
            
            # Simular response codes
            status_code = random.choices([200, 429, 500, 503], weights=[80, 10, 5, 5])[0]
            
            if status_code == 200:
                self.request_stats['successful_requests'] += 1
                
                # Simular response data
                response_data = {
                    'endpoint': endpoint,
                    'data': [{'id': i, 'value': random.randint(1, 100)} for i in range(10)],
                    'timestamp': datetime.now().isoformat()
                }
                
                print(f"✓ {method} {endpoint}: {status_code} ({response_time:.3f}s)")
                return response_data
                
            elif status_code == 429:  # Rate limited por server
                self.request_stats['rate_limited'] += 1
                print(f"⚠ Rate limited by server: {endpoint}")
                
                # Exponential backoff
                backoff_time = random.uniform(1, 3)
                await asyncio.sleep(backoff_time)
                
                # Retry once
                return await self.make_api_request(endpoint, method, data)
            
            else:
                self.request_stats['errors'] += 1
                raise aiohttp.ClientError(f"HTTP {status_code}")
                
        except Exception as e:
            self.request_stats['errors'] += 1
            print(f"✗ Error with {endpoint}: {e}")
            raise
    
    async def batch_api_requests(self, endpoints):
        """Make múltiples API requests efficiently"""
        print(f"=== RATE-LIMITED API CLIENT ===")
        print(f"Making {len(endpoints)} API requests...")
        print(f"Rate limit: {self.requests_per_second} req/s, Burst: {self.burst_size}")
        
        start_time = time.time()
        
        # Crear tasks para todas las requests
        tasks = [self.make_api_request(endpoint) for endpoint in endpoints]
        
        # Ejecutar con progress tracking
        results = []
        completed = 0
        
        for coro in asyncio.as_completed(tasks):
            try:
                result = await coro
                results.append(result)
            except Exception as e:
                results.append({'error': str(e)})
            
            completed += 1
            if completed % 5 == 0:
                print(f"Progress: {completed}/{len(endpoints)} requests completed")
        
        total_time = time.time() - start_time
        
        # Performance metrics
        print(f"\n📈 API CLIENT PERFORMANCE:")
        print(f"   Total time: {total_time:.2f}s")
        print(f"   Actual rate: {len(endpoints)/total_time:.1f} req/s")
        print(f"   Success rate: {self.request_stats['successful_requests']}/{self.request_stats['total_requests']} "
              f"({self.request_stats['successful_requests']/self.request_stats['total_requests']*100:.1f}%)")
        print(f"   Rate limited: {self.request_stats['rate_limited']}")
        print(f"   Errors: {self.request_stats['errors']}")
        print()
        
        return results

# ========================
# PROBLEMA 3: Circuit Breaker Pattern
# ========================

class CircuitState(Enum):
    CLOSED = "closed"        # Normal operation
    OPEN = "open"           # Failing, reject requests
    HALF_OPEN = "half_open" # Testing if service recovered

@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5
    recovery_timeout: float = 10.0
    success_threshold: int = 3

class AsyncCircuitBreaker:
    """
    Circuit Breaker pattern para async operations
    Previene cascade failures en microservices
    """
    
    def __init__(self, config: CircuitBreakerConfig = None):
        self.config = config or CircuitBreakerConfig()
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.lock = asyncio.Lock()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.record_failure()
        else:
            await self.record_success()
        return False
    
    async def call(self, async_func, *args, **kwargs):
        """
        Execute function a través del circuit breaker
        """
        async with self.lock:
            # Check si debemos rechazar request
            if not await self._should_allow_request():
                raise Exception(f"Circuit breaker is {self.state.value}")
        
        # Execute function
        try:
            result = await async_func(*args, **kwargs)
            await self.record_success()
            return result
        except Exception as e:
            await self.record_failure()
            raise
    
    async def _should_allow_request(self):
        """Determinar si permitir request basado en circuit state"""
        now = time.time()
        
        if self.state == CircuitState.CLOSED:
            return True
        
        elif self.state == CircuitState.OPEN:
            # Check si es tiempo de try recovery
            if (self.last_failure_time and 
                now - self.last_failure_time >= self.config.recovery_timeout):
                self.state = CircuitState.HALF_OPEN
                self.success_count = 0
                print("Circuit breaker moved to HALF_OPEN")
                return True
            return False
        
        else:  # HALF_OPEN
            return True
    
    async def record_success(self):
        """Record successful operation"""
        async with self.lock:
            if self.state == CircuitState.HALF_OPEN:
                self.success_count += 1
                if self.success_count >= self.config.success_threshold:
                    self.state = CircuitState.CLOSED
                    self.failure_count = 0
                    print("Circuit breaker moved to CLOSED (recovered)")
            elif self.state == CircuitState.CLOSED:
                self.failure_count = 0  # Reset failure count
    
    async def record_failure(self):
        """Record failed operation"""
        async with self.lock:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if (self.state == CircuitState.CLOSED and 
                self.failure_count >= self.config.failure_threshold):
                self.state = CircuitState.OPEN
                print(f"Circuit breaker OPENED after {self.failure_count} failures")
            
            elif self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.OPEN
                print("Circuit breaker returned to OPEN (recovery failed)")

async def test_circuit_breaker():
    """Test circuit breaker con unreliable service"""
    print("=== CIRCUIT BREAKER PATTERN TEST ===")
    
    # Simular servicio unreliable
    failure_probability = 0.7  # 70% failure rate inicialmente
    
    async def unreliable_service_call(request_id):
        """Simular call a servicio unreliable"""
        await asyncio.sleep(0.1)  # Simular network delay
        
        if random.random() < failure_probability:
            raise Exception(f"Service failure for request {request_id}")
        
        return f"Success response for request {request_id}"
    
    circuit_breaker = AsyncCircuitBreaker(
        CircuitBreakerConfig(failure_threshold=3, recovery_timeout=2.0)
    )
    
    # Test con high failure rate
    print("Testing with 70% failure rate...")
    
    for i in range(15):
        try:
            result = await circuit_breaker.call(unreliable_service_call, i)
            print(f"Request {i}: {result}")
        except Exception as e:
            print(f"Request {i}: {e}")
        
        await asyncio.sleep(0.2)
        
        # Simular service recovery después de algunos requests
        if i == 8:
            failure_probability = 0.1  # Service recovers
            print("--- SERVICE RECOVERED (failure rate now 10%) ---")
    
    print()

# ========================
# PROBLEMA 4: Async Task Scheduler
# ========================

@dataclass
class ScheduledTask:
    id: str
    func: Callable
    args: tuple
    kwargs: dict
    schedule_time: float
    max_retries: int = 3
    retry_count: int = 0

class AsyncTaskScheduler:
    """
    Task scheduler asíncrono con retry logic
    Similar a Celery pero async
    """
    
    def __init__(self, max_concurrent_tasks=5):
        self.max_concurrent = max_concurrent_tasks
        self.semaphore = asyncio.Semaphore