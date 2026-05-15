# Execution Metrics

Task execution metrics.

## Task Metrics

| Metric | Description |
|--------|-------------|
| Total Tasks | Tasks created |
| Completed | Tasks completed |
| Failed | Tasks failed |
| In Progress | Active tasks |

## Success Rate

```python
def calculate_success_rate(tasks):
    completed = [t for t in tasks if t.status == "completed"]
    failed = [t for t in tasks if t.status == "failed"]
    
    return len(completed) / (len(completed) + len(failed))
```

## By Task Type

```json
{
  "coding": {
    "total": 100,
    "success": 90,
    "rate": 0.90
  },
  "review": {
    "total": 50,
    "success": 48,
    "rate": 0.96
  }
}
```

## Metric Collection

```python
def collect_metrics(task):
    return {
        "id": task.id,
        "type": task.type,
        "status": task.status,
        "duration": task.duration,
        "retries": task.retry_count,
        "tokens": task.total_tokens
    }
```