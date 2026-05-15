# Message Bus

Asynchronous messaging for agent communication.

## What is a Message Bus

A message bus is an asynchronous communication system:
- Agents send messages without waiting
- Messages are queued and delivered later
- Decouples sender from receiver

## Message Bus vs Direct Call

| Direct Call | Message Bus |
|--------------|-------------|
| Synchronous | Asynchronous |
| Tightly coupled | Loosely coupled |
| Immediate response | Queued |
| Fails if receiver down | Tolerates failures |

## Implementation

```python
import asyncio
from dataclasses import dataclass
from typing import Dict, List, Callable

@dataclass
class Message:
    id: str
    sender: str
    topic: str
    payload: dict
    timestamp: datetime

class MessageBus:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.queue: asyncio.Queue = asyncio.Queue()
    
    async def subscribe(self, topic: str, handler: Callable):
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(handler)
    
    async def publish(self, message: Message):
        await self.queue.put(message)
    
    async def start(self):
        while True:
            message = await self.queue.get()
            await self._deliver(message)
    
    async def _deliver(self, message: Message):
        handlers = self.subscribers.get(message.topic, [])
        for handler in handlers:
            try:
                await handler(message)
            except Exception as e:
                log.error(f"Handler failed: {e}")
```

## Message Types

### Task Messages
```python
task_msg = Message(
    id="msg-1",
    sender="planner",
    topic="task.assign",
    payload={
        "task_id": "task-123",
        "type": "coding",
        "priority": 5
    }
)
```

### Result Messages
```python
result_msg = Message(
    id="msg-2",
    sender="coder",
    topic="task.complete",
    payload={
        "task_id": "task-123",
        "result": "generated_code"
    }
)
```

### Status Messages
```python
status_msg = Message(
    id="msg-3",
    sender="reviewer",
    topic="agent.status",
    payload={
        "status": "busy",
        "current_task": "task-456"
    }
)
```

## Pub-Sub Pattern

```python
# Publisher (Coder)
await message_bus.publish(Message(
    sender="coder",
    topic="code.generated",
    payload={"file": "main.py", "code": "..."}
))

# Subscriber (Tester)
await message_bus.subscribe(
    "code.generated",
    handler=lambda msg: create_tests(msg.payload)
)

# Subscriber (Reviewer)
await message_bus.subscribe(
    "code.generated", 
    handler=lambda msg: review_code(msg.payload)
)
```

## Request-Response via Bus

```python
class RequestResponseBus:
    def __init__(self, bus):
        self.bus = bus
        self.pending: Dict[str, asyncio.Future] = {}
    
    async def request(self, receiver, request):
        future = asyncio.get_event_loop().create_future()
        self.pending[request.id] = future
        
        await self.bus.publish(Message(
            sender="me",
            receiver=receiver,
            topic="request",
            payload=request
        ))
        
        return await future
    
    async def respond(self, request_id, response):
        future = self.pending.pop(request_id)
        future.set_result(response)
```

## Message Queue (Redis)

For production, use Redis:

```python
import redis.asyncio as redis

class RedisMessageBus:
    def __init__(self):
        self.redis = redis.Redis()
    
    async def publish(self, channel, message):
        await self.redis.publish(channel, json.dumps(message))
    
    async def subscribe(self, channel):
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(channel)
        async for message in pubsub.listen():
            yield message
```

## Best Practices

1. **Topic naming** - Use clear, hierarchical names (e.g., `task.created`, `agent.status`)
2. **Message size** - Keep messages small
3. **Acknowledge** - Confirm important messages
4. **Timeouts** - Don't wait forever
5. **Dead letters** - Handle undeliverable messages