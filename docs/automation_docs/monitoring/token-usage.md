# Token Usage

Track token consumption.

## Metrics to Track

| Metric | Description |
|--------|-------------|
| Input Tokens | Tokens sent |
| Output Tokens | Tokens received |
| Cache Reads | Reused context |
| Cache Writes | New cached context |

## Usage by Task

```python
def track_token_usage(task, response):
    task.tokens_in = response.usage.input_tokens
    task.tokens_out = response.usage.output_tokens
    task.tokens_cache = response.usage.cache_read_tokens
    
    store.task_tokens.save(task)
```

## Usage by Model

```json
{
  "model": "claude-sonnet",
  "total_input": 1000000,
  "total_output": 500000,
  "total_cache": 200000,
  "cost": 50.00
}
```

## Alerts

```yaml
alerts:
  token_threshold:
    daily: 1000000
    warn_at: 0.8
    critical_at: 0.95