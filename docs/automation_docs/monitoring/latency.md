# Latency

Response time monitoring.

## Latency Metrics

| Metric | Description |
|--------|-------------|
| P50 | Median response time |
| P90 | 90th percentile |
| P99 | 99th percentile |
| Max | Maximum time |

## Measurement

```python
def measure_latency(task):
    start = time.time()
    response = execute(task)
    end = time.time()
    
    task.latency_ms = (end - start) * 1000
    return task.latency_ms
```

## Latency by Task Type

```json
{
  "coding": {
    "p50": 2000,
    "p90": 5000,
    "p99": 10000
  },
  "review": {
    "p50": 1000,
    "p90": 3000,
    "p99": 5000
  }
}
```

## Alerts

```yaml
alerts:
  latency:
    warn: 5000ms
    critical: 10000ms