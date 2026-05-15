# Checkpointing

## Why Checkpointing

Save execution state to enable recovery from failures.

## Checkpoint Data

```python
@dataclass
class Checkpoint:
    task_id: str
    phase: str
    context: dict
    artifacts: list[str]
    timestamp: datetime
```

## Checkpoint Strategy

```python
class CheckpointManager:
    def save_checkpoint(self, task):
        checkpoint = Checkpoint(
            task_id=task.id,
            phase=task.current_phase,
            context=task.context,
            artifacts=task.artifacts,
            timestamp=now()
        )
        self.db.save(checkpoint)
    
    def restore_checkpoint(self, task_id):
        return self.db.get_latest(task_id)
```

## When to Checkpoint

- After each phase
- Before risky operations
- At regular intervals
- Before escalation

## Checkpoint Storage

- Database for metadata
- File system for artifacts
- Retain last N checkpoints
- Clean up old checkpoints