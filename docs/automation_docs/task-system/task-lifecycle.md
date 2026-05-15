# Task Lifecycle

## States

```
created → ready → running → completed
                    ↓
                  failed
                    ↓
               (retry or escalate)
```

## State Transitions

| From | To | Trigger |
|------|-----|---------|
| created | ready | Dependencies satisfied |
| ready | running | Agent assigned |
| running | completed | Task succeeded |
| running | failed | Task failed |
| failed | ready | Retry succeeded |
| failed | escalated | Max retries reached |

## Lifecycle Events

### Created
- Task initialized
- Dependencies recorded
- Added to queue

### Ready
- All dependencies complete
- Waiting for agent assignment

### Running
- Agent actively working
- Progress tracked
- Checkpoints saved

### Completed
- All outputs generated
- Artifacts stored
- Result recorded

### Failed
- Error recorded
- Retry decision made
- Escalation if needed

## Implementation

```python
class TaskState:
    CREATED = "created"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    ESCALATED = "escalated"

def transition(task, new_state):
    validate_transition(task.state, new_state)
    task.state = new_state
    task.updated_at = now()
    emit_event("task_state_changed", task)
```