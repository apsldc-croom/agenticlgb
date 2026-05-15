# Escalation Strategy

When and how to escalate.

## Escalation Levels

| Level | Action | Threshold |
|-------|--------|-----------|
| 1 | Retry same model | 1 failure |
| 2 | Try stronger model | 2 failures |
| 3 | Switch to reasoning | 3 failures |
| 4 | Human intervention | Max reached |

## Escalation Triggers

```python
ESCALATION_TRIGGERS = [
    {"condition": "retries >= max_retries", "level": 4},
    {"condition": "security_risk", "level": 4},
    {"condition": "unknown_error", "level": 3},
    {"condition": "timeout", "level": 2},
    {"condition": "quality_score < 0.5", "level": 2},
]
```

## Escalation Implementation

```python
def escalate(task, reason):
    if reason == "max_retries":
        return notify_human(task)
    elif reason == "security":
        return block_and_alert(task)
    elif reason == "quality":
        return try_reasoning_model(task)
    else:
        return try_stronger_model(task)
```

## Escalation Metrics

- Escalation rate
- Escalation by type
- Resolution time after escalation