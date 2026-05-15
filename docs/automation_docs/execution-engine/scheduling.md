# Scheduling

## Scheduler Types

### FIFO Scheduler
First in, first out - simple but may cause priority inversion.

### Priority Scheduler
Higher priority tasks execute first.

### Deadline Scheduler
Tasks with earlier deadlines execute first.

## Scheduling Algorithm

```python
class TaskScheduler:
    def __init__(self):
        self.ready_queue = []
        self.running = set()
        self.max_concurrent = 4
    
    def schedule(self):
        # Sort by priority then time
        self.ready_queue.sort(key=lambda t: (-t.priority, t.created_at))
        
        while self.ready_queue and len(self.running) < self.max_concurrent:
            task = self.ready_queue.pop(0)
            self.running.add(task)
            self.execute_async(task)
    
    def task_completed(self, task, result):
        self.running.remove(task)
        
        # Handle dependencies
        for dependent in task.dependents:
            if dependent.all_dependencies_met():
                self.ready_queue.append(dependent)
        
        self.schedule()  # Check for more work
```

## Time-Based Triggers

- Schedule task at specific time
- Schedule task after delay
- Schedule task periodically

## Resource Scheduling

Track and limit:
- Concurrent tasks
- Token usage
- API rate limits
- Compute resources