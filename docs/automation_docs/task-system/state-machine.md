# State Machine

## Task State Machine

```
                    ┌─────────────┐
                    │   created   │
                    └──────┬──────┘
                           │ dependencies_met()
                           ▼
                    ┌─────────────┐
              ┌─────│    ready    │─────┐
              │     └──────┬──────┘     │
              │            │            │
              ▼            ▼            ▼
        ┌─────────┐  ┌─────────┐  ┌─────────┐
        │ running │  │  hold   │  │cancelled│
        └────┬────┘  └─────────┘  └─────────┘
             │
    ┌────────┼────────┐
    ▼        ▼        ▼
┌───────┐ ┌───────┐ ┌───────┐
│completed│ │ failed│ │paused │
└───────┘ └───────┘ └───────┘
    │        │
    ▼        ▼
(retry)  (escalate)
```

## Valid Transitions

```python
TRANSITIONS = {
    "created": ["ready", "cancelled"],
    "ready": ["running", "cancelled"],
    "running": ["completed", "failed", "paused"],
    "paused": ["running", "cancelled"],
    "completed": [],
    "failed": ["ready", "escalated", "cancelled"],
    "escalated": [],
    "cancelled": [],
}
```

## State Persistence

- Save state after each transition
- Store in database for recovery
- Include timestamp and reason