# Observability

System observability.

## Three Pillars

### Logs
Structured event records:
```python
logger.info("task_completed", {
    "task_id": task.id,
    "duration": task.duration,
    "model": task.model
})
```

### Metrics
Numeric measurements:
- Task count
- Success rate
- Latency
- Token usage

### Traces
Request flow tracking:
```
Task → Router → Planner → Coder → Reviewer → Done
```

## Implementation

```python
# Logs
logger = logging.getLogger("ai-system")
logger.setLevel("INFO")

# Metrics
from prometheus_client import Counter, Histogram
task_count = Counter('tasks_total', 'Total tasks')

# Traces
from opentelemetry import trace
tracer = trace.get_tracer(__name__)
```

## Correlation

Link logs, metrics, and traces:
```python
with tracer.start_as_current_span("task") as span:
    span.set_attribute("task_id", task.id)
    # Work...
    logger.info("task_complete", {"trace_id": span.context.trace_id})
```