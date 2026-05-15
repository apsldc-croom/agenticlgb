# Shared Memory

## Memory Types

### Working Memory
Shared context for current task.
- Task state
- Intermediate results

### Knowledge Memory
Shared facts and rules.
- Project structure
- Coding standards

### History Memory
Past execution records.
- What worked
- What failed

## Implementation

```python
class SharedMemory:
    def __init__(self):
        self.working = {}
        self.knowledge = {}
        self.history = []
    
    def read(self, key):
        return self.working.get(key) or self.knowledge.get(key)
    
    def write(self, key, value):
        self.working[key] = value
    
    def extend_knowledge(self, facts):
        self.knowledge.update(facts)
    
    def log(self, event):
        self.history.append(event)
```

## Access Control

- Read: Any agent
- Write: Owner or coordinator
- Update: Coordination protocol