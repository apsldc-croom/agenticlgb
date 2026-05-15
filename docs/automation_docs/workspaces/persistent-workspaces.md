# Persistent Workspaces

Long-lived project workspaces.

## Use Cases

- Ongoing development
- Large refactoring
- Multi-session tasks

## Characteristics

- Survives between tasks
- Maintains state
- Shared across sessions

## Implementation

```python
class PersistentWorkspace:
    def __init__(self, project_id):
        self.project_id = project_id
        self.path = f"/workspaces/{project_id}"
        self.load_or_create()
    
    def load_or_create(self):
        if os.path.exists(self.path):
            self.load()
        else:
            self.create()
    
    def create(self):
        # Clone repo or create new
        git.clone(project_url, self.path)
    
    def save(self):
        # Commit changes
        git.add(".")
        git.commit(f"Task {task_id} complete")
    
    def cleanup(self):
        # Archive instead of delete
        archive(self.path, f"/archives/{project_id}.tar.gz")
```

## Cleanup Policy

```yaml
persistent:
  max_age_days: 30
  max_size_gb: 10
  cleanup_on_archive: true