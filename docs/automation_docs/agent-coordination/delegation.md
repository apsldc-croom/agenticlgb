# Delegation

## Delegation Patterns

### Direct Delegation
Planner assigns specific task to specific agent.

### Pool Delegation
Task added to agent pool, available agent picks up.

### Capability Delegation
Route to agent with required capability.

## Delegation Logic

```python
def delegate(task, agents):
    # Check agent capabilities
    suitable = [a for a in agents if a.can_handle(task.type)]
    
    # Check agent availability
    available = [a for a in suitable if a.is_available()]
    
    if not available:
        # Queue for later
        return None
    
    # Select best agent
    selected = select_best(available, task)
    return selected
```

## Delegation Criteria

- Agent capability match
- Current workload
- Success history with similar tasks
- Performance metrics

## Delegation Patterns

| Pattern | Use Case |
|---------|----------|
| Round-robin | Equal workload |
| Least-loaded | Minimize wait |
| Capability-based | Specialized tasks |
| Performance-based | Optimize success |