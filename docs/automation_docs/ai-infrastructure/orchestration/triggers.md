# Triggers

Automation trigger conditions.

## Trigger Types

| Trigger | Condition |
|---------|-----------|
| schedule | Time-based |
| event | On specific event |
| webhook | HTTP request |
| manual | Human triggered |

## Trigger Definition

```python
class Trigger:
    condition: callable
    action: callable
    enabled: bool
    
trigger = Trigger(
    condition=lambda: failed_tasks > 5,
    action=alert_oncall,
    enabled=True
)
```

## Examples

### On Task Failure
```python
trigger = Trigger(
    condition=lambda task: task.status == "failed",
    action=lambda t: escalate(t),
    enabled=True
)
```

### On Token Threshold
```python
trigger = Trigger(
    condition=lambda: daily_tokens > 0.9 * limit,
    action=alert_team,
    enabled=True
)
```

### Scheduled
```python
trigger = Trigger(
    schedule="0 2 * * *",  # 2 AM daily
    action=daily_reports,
    enabled=True
)
```