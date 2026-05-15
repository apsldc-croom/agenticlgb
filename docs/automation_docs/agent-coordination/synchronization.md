# Synchronization

## Why Synchronization

Agents may need to coordinate:
- Before parallel execution
- After dependent tasks
- At checkpoints
- On shared resources

## Synchronization Methods

### Barriers
Wait for all agents to reach point:
```
Agent A ──┐
Agent B ──┼──→ [Barrier] ──→ Continue
Agent C ──┘
```

### Locks
Control access to shared resource:
```
with lock:
    # Access shared resource
```

### Semaphores
Limit concurrent access:
```
semaphore.acquire()
# Do work
semaphore.release()
```

## Sync Implementation

```python
class AgentSynchronizer:
    def barrier(self, agents, checkpoint):
        for agent in agents:
            agent.wait_at_checkpoint(checkpoint)
        
        if all_arrived(agents):
            for agent in agents:
                agent.proceed()
    
    def lock(self, resource):
        return LockManager.acquire(resource)
```