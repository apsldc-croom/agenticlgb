# Short-Term Memory

Session-scoped context that persists during a task.

## Purpose

- Store current task context
- Keep intermediate results
- Track progress

## Characteristics

- Cleared after task completion
- Not persisted to disk
- Available to all agents in session

## Data Stored

```python
short_term_memory = {
    "current_task": task_id,
    "subtasks_completed": [id1, id2],
    "subtasks_pending": [id3, id4],
    "context": {
        "project_path": "/path/to/project",
        "language": "python",
        "framework": "django"
    },
    "intermediate_results": {
        "design": {...},
        "code_generated": {...}
    }
}
```

## Usage

```python
def get_context(agent):
    return short_term_memory.copy()

def update_context(updates):
    short_term_memory.update(updates)
```