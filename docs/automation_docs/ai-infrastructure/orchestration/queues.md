# Queues

Task queue implementation.

## Queue Types

### FIFO Queue
```python
queue = deque()
queue.append(task)  # enqueue
task = queue.popleft()  # dequeue
```

### Priority Queue
```python
import heapq

class PriorityQueue:
    def __init__(self):
        self._heap = []
    
    def enqueue(self, task, priority):
        heapq.heappush(self._heap, (priority, task))
    
    def dequeue(self):
        return heapq.heappop(self._heap)[1]
```

### Distributed Queue (Redis)
```python
import redis

class RedisQueue:
    def __init__(self, name):
        self.redis = redis.Redis()
        self.key = f"queue:{name}"
    
    def enqueue(self, task):
        self.redis.lpush(self.key, json.dumps(task))
    
    def dequeue(self):
        return json.loads(self.redis.brpop(self.key)[1])
```

## Queue Operations

- enqueue: Add task
- dequeue: Get next task
- peek: View without removing
- size: Count pending tasks