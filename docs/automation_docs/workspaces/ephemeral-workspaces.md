# Ephemeral Workspaces

Temporary workspaces for single tasks.

## Use Cases

- One-off code generation
- Single file editing
- Quick debugging sessions

## Characteristics

- Created per task
- Deleted after completion
- No persistent state
- Fast to create

## Implementation

```python
class EphemeralWorkspace:
    def __init__(self, task_id):
        self.task_id = task_id
        self.path = f"/tmp/workspace-{task_id}"
        self.create()
    
    def create(self):
        os.makedirs(self.path, exist_ok=True)
        self.setup_environment()
    
    def cleanup(self):
        shutil.rmtree(self.path)
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.cleanup()

# Usage
with EphemeralWorkspace(task_id) as ws:
    execute_task(ws)
```