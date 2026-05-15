# Retry Strategy

## Retry Policy

```python
RETRY_CONFIG = {
    "max_attempts": 3,
    "initial_delay": 1,      # seconds
    "max_delay": 60,         # seconds
    "backoff_factor": 2,     # exponential backoff
    "jitter": True,          # add randomness
}
```

## Retry Logic

```python
def should_retry(task, attempt):
    if attempt >= config.max_attempts:
        return False
    
    # Don't retry certain errors
    if task.error in NON_RETRYABLE_ERRORS:
        return False
    
    return True

def calculate_delay(attempt):
    delay = config.initial_delay * (config.backoff_factor ** attempt)
    delay = min(delay, config.max_delay)
    if config.jitter:
        delay *= random.uniform(0.5, 1.5)
    return delay
```

## Error Categories

### Retriable
- Network timeout
- Rate limiting
- Temporary service unavailable

### Non-Retriable
- Invalid input
- Authentication failure
- Resource not found

### Conditional
- Code generation failure (retry with different prompt)
- Review failure (retry with different model)

## Retry Tracking

- Record attempt number
- Record error type
- Record delay used
- Analyze for patterns