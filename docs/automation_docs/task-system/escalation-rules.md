# Escalation Rules

## When to Escalate

### Automatic Escalation
- Max retries exceeded
- Unknown error type
- Resource exhausted
- Security concern

### Manual Escalation
- Human requests review
- Agent uncertain about solution
- Safety boundaries approached

## Escalation Levels

| Level | Action |
|-------|--------|
| 1 | Retry with same model |
| 2 | Retry with stronger model |
| 3 | Switch to reasoning model |
| 4 | Hand to human operator |

## Escalation Criteria

```python
ESCALATION_RULES = [
    # Code quality issues
    {"condition": "lint_errors > 10", "level": 2},
    {"condition": "test_failures > 5", "level": 2},
    
    # Security concerns
    {"condition": "security_risk_detected", "level": 4},
    
    # Complexity
    {"condition": "task_complexity > 8", "level": 3},
    
    # Repeated failures
    {"condition": "same_error_3_times", "level": 3},
]
```

## Human Notification

When escalated to human:
- Send notification with task details
- Include error history
- Provide context for decision
- Set timeout for response