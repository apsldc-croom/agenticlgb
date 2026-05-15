# Provider Selection

Choosing API provider.

## Provider Comparison

| Provider | Models | Cost | Speed | Reliability |
|----------|--------|------|-------|-------------|
| OpenRouter | Many | Variable | Good | Good |
| OpenCode | Many | Low | Good | Good |
| Together | Many | Good | Good | Good |
| Novita | Many | Low | Good | Good |
| Groq | Limited | Low | Excellent | Good |
| Anthropic | Claude | High | Good | Excellent |

## Selection Logic

```python
def select_provider(task, available_providers):
    if requires_specific_model(task):
        return provider_with_model(task.model)
    
    if requires_speed(task):
        return fast_provider()
    
    if budget_constrained(task):
        return cheapest_provider()
    
    return default_provider()
```

## Multi-Provider Setup

```python
PROVIDERS = {
    "primary": {"class": "OpenRouter", "priority": 1},
    "fallback": {"class": "Anthropic", "priority": 2},
    "backup": {"class": "OpenAI", "priority": 3},
}
```