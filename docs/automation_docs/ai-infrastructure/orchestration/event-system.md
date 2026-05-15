# Event System

Event-driven architecture.

## Event Types

| Event | Description |
|-------|-------------|
| task.created | New task added |
| task.completed | Task finished |
| task.failed | Task failed |
| agent.registered | Agent joined |
| agent.unregistered | Agent left |

## Event Flow

```
Event → Event Bus → Handlers → Actions
```

## Implementation

```python
class EventBus:
    def __init__(self):
        self.handlers = defaultdict(list)
    
    def subscribe(self, event_type, handler):
        self.handlers[event_type].append(handler)
    
    def publish(self, event):
        for handler in self.handlers[event.type]:
            handler(event)

# Example
event_bus.publish(Event(
    type="task.completed",
    data={"task_id": "123", "result": {...}}
))
```

## Handler Examples

```python
@event_handler("task.completed")
def on_task_complete(event):
    notify_user(event.data)
    update_metrics(event.data)
    cleanup_workspace(event.data)
```