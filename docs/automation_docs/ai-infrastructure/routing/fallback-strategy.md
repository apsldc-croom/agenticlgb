# Fallback Strategy

What to do when primary fails.

## Fallback Chain

```python
FALLBACK_CHAIN = [
    # Primary → Fallback 1 → Fallback 2 → Final
    ("sonnet", "haiku", None),        # Quality → fast
    ("gpt-5", "gpt-4", "sonnet"),     # Try weaker if expensive fails
    ("opus", "sonnet", "haiku"),      # Step down
]
```

## Fallback Logic

```python
def execute_with_fallback(task):
    for model in get_fallback_chain(task):
        try:
            result = model.execute(task)
            return Success(result)
        except Exception as e:
            log(f"Model {model} failed: {e}")
            continue
    
    return Failure("All models failed")
```

## Fallback Triggers

| Trigger | Action |
|---------|--------|
| Timeout | Try next model |
| Rate limit | Wait, then retry |
| Error | Try fallback model |
| Low confidence | Try smarter model |

## Fallback Metrics

- Fallback rate per model
- Cost impact of fallbacks
- Success rate after fallback