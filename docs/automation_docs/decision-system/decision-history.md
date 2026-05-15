# Decision History

Past decisions for learning.

## History Storage

```python
class DecisionHistory:
    def record(self, decision):
        db.save({
            "type": decision.type,
            "task_id": decision.task_id,
            "decision": decision.to_dict(),
            "timestamp": now()
        })
    
    def query(self, filters):
        return db.query(
            type=filters.type,
            task_id=filters.task_id,
            date_range=filters.date
        )
```

## Queries

### By Task
```python
get_decisions_for_task(task_id)
```

### By Type
```python
get_decisions(type="routing", last_n=100)
```

### By Date
```python
get_decisions(date_range="last_week")
```

## Analysis

### Success Rate by Model
```python
analyze.success_rate_by_model()
```

### Escalation Patterns
```python
analyze.escalation_patterns()
```

### Cost Optimization
```python
analyze.cost_by_routing_strategy()
```

## Retention

- Keep all decisions
- Aggregate for reporting
- Anonymize for sharing