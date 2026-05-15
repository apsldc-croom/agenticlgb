# Memory Pruning

Cleaning up old/unused memory.

## Pruning Strategies

### Age-Based
Remove old memories:
```python
def prune_by_age(memory, max_age_days=30):
    old_memories = memory.where(
        created_at < now() - max_age_days
    )
    memory.delete(old_memories)
```

### Usage-Based
Remove unused:
```python
def prune_by_usage(memory, min_access_count=3):
    unused = memory.where(
        access_count < min_access_count
    )
    memory.delete(unused)
```

### Relevance-Based
Remove low-relevance:
```python
def prune_by_relevance(memory):
    low_relevance = memory.where(
        relevance_score < 0.2
    )
    memory.delete(low_relevance)
```

## Triggers

- Scheduled (daily/weekly)
- On memory size threshold
- Before new task