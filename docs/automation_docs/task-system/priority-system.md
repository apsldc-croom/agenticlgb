# Priority System

## Priority Levels

| Level | Name | Use Case |
|-------|------|----------|
| 1 | Lowest | Background tasks |
| 2 | Low | Nice-to-have features |
| 3 | Medium | Normal tasks |
| 4 | High | Important features |
| 5 | Urgent | Must complete |
| 6 | Critical | Blocker issues |
| 7-10 | Reserved | System tasks |

## Priority Calculation

### Base Priority
Set by user or derived from parent task.

### Dynamic Adjustment

```python
def calculate_priority(task):
    priority = task.base_priority
    
    # Increase for blocked tasks
    if task.is_blocked:
        priority += 1
    
    # Increase for aging tasks
    age_hours = (now() - task.created_at).hours
    if age_hours > 24:
        priority += 1
    
    # Increase for dependencies
    for dependent in task.dependents:
        if dependent.priority > priority:
            priority = dependent.priority
    
    return min(priority, 10)
```

## Queue Order

Tasks sorted by:
1. Priority (descending)
2. Created time (ascending)

This ensures:
- High priority runs first
- Among same priority, older tasks first