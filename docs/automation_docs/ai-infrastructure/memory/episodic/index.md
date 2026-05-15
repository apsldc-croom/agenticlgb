# Episodic Memory

Stores sequences of events/actions for learning from past.

## Purpose

- Track what worked/failed
- Learn from execution history
- Pattern recognition

## Structure

```python
episode = {
    "id": "uuid",
    "task": "fix auth bug",
    "actions": [
        {"agent": "planner", "output": "breakdown"},
        {"agent": "coder", "output": "code v1"},
        {"agent": "reviewer", "output": "failed review"},
        {"agent": "fixer", "output": "code v2"},
        {"agent": "reviewer", "output": "approved"}
    ],
    "outcome": "success",
    "duration": 120,
    "tokens": 5000
}
```

## Use Cases

- What prompts worked for similar tasks?
- Which model performed best?
- How many retries typically needed?

## Storage

- Time-series database
- Indexed by task type, outcome