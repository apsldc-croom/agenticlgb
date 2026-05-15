# Task Queue

## Queue Implementation

### In-Memory Queue (Development)
```python
from collections import deque

class TaskQueue:
    def __init__(self):
        self.queue = deque()
        self.priority_queue = PriorityQueue()
    
    def enqueue(self, task, priority=None):
        if priority:
            self.priority_queue.put((priority, task))
        else:
            self.queue.append(task)
    
    def dequeue(self):
        if not self.priority_queue.empty():
            return self.priority_queue.get()[1]
        if self.queue:
            return self.queue.popleft()
        return None
```

### Redis Queue (Production)
```python
import redis

class RedisTaskQueue:
    def __init__(self):
        self.redis = redis.Redis()
        self.key = "task_queue"
    
    def enqueue(self, task):
        self.redis.zadd(self.key, {json.dumps(task): task.priority})
    
    def dequeue(self):
        result = self.redis.zpopmax(self.key)
        if result:
            return json.loads(result[0])
        return None
```

## Queue Operations

### Enqueue
1. Validate task
2. Check dependencies
3. Add to appropriate queue

### Dequeue
1. Check priority queue first
2. Then check regular queue
3. Return task or None

### Monitoring
- Queue length
- Average wait time
- Tasks by status