# Memory Lifecycle

Memory management phases.

## Lifecycle Stages

### Creation
- Store new information
- Index for retrieval
- Assign metadata

### Usage
- Read/retrieve
- Update/extend
- Track access

### Maintenance
- Summarize old content
- Prune unused
- Archive important

### Deletion
- Explicit removal
- Auto-pruning
- Expiration

## Implementation

```python
class MemoryManager:
    def create(self, data, memory_type):
        memory = Memory(
            data=data,
            type=memory_type,
            created_at=now()
        )
        return self.store(memory)
    
    def access(self, memory_id):
        memory = self.get(memory_id)
        memory.access_count += 1
        memory.last_accessed = now()
        return memory
    
    def maintain(self):
        self.summarize_old()
        self.prune_unused()
    
    def delete(self, memory_id):
        self.remove(memory_id)
```