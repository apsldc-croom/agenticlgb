# Routing Config

Routing rules and strategies.

## Example Configuration

```yaml
routing:
  default_strategy: complexity
  
  strategies:
    complexity:
      enabled: true
      levels:
        - complexity: 1-2
          model_category: fast
        - complexity: 3-5
          model_category: balanced
        - complexity: 6-10
          model_category: reasoning
    
    cost:
      enabled: true
      max_budget_per_task: 0.50
    
    performance:
      enabled: true
      prefer_model: gpt-4
```

## Fallback Configuration

```yaml
fallback:
  chain:
    - from: claude-opus
      to: claude-sonnet
    - from: gpt-5
      to: gpt-4
  
  retry:
    max_attempts: 3
    backoff_seconds: 5
```