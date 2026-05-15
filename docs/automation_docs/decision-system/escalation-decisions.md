# Escalation Decisions

Escalation path decisions.

## Decision Recording

```python
@dataclass
class EscalationDecision:
    task_id: str
    current_level: int
    escalated_to: int
    reason: str
    action_taken: str
    outcome: str
```

## Escalation Triggers

```python
ESCALATION_TRIGGERS = {
    "max_retries": {
        "level": 4,
        "action": "notify_human"
    },
    "unknown_error": {
        "level": 3,
        "action": "switch_to_reasoning"
    },
    "quality_issue": {
        "level": 2,
        "action": "retry_stronger_model"
    }
}
```

## Example

```
Task: Fix authentication bug
Level 1: Retry with same model → Failed
Level 2: Retry with stronger model → Failed
Level 3: Switch to reasoning model → Success

Decision: Escalate to level 3
Reason: Standard retries failed
Action: Use deepseek-r1
Outcome: success
```

## Analysis

- Track escalation frequency
- Identify patterns
- Optimize thresholds