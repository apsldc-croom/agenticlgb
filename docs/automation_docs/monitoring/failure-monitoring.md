# Failure Monitoring

Error and failure tracking.

## Failure Categories

| Category | Examples |
|----------|----------|
| API | Timeout, rate limit |
| Code | Generation failure |
| Quality | Linting failed |
| Validation | Invalid output |

## Tracking

```python
def track_failure(task, error):
    task.error_type = classify_error(error)
    task.error_message = error.message
    task.stack_trace = error.stack_trace
    
    store.failures.save(task)
    alert_if_needed(task)
```

## Failure Rate

```json
{
  "period": "2024-01-15",
  "total_tasks": 100,
  "failures": 5,
  "rate": 0.05,
  "by_type": {
    "api": 2,
    "code": 2,
    "validation": 1
  }
}
```

## Alerts

```yaml
alerts:
  failure_rate:
    warn: 0.10
    critical: 0.20
    
  specific_failure:
    - rate_limit
    - auth_failure