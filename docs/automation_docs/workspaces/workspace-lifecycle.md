# Workspace Lifecycle

Workspace creation to cleanup.

## Lifecycle Stages

```
Create → Initialize → Use → Save → Cleanup
```

## Stage Details

### Create
```python
def create_workspace(task_id):
    path = f"/workspaces/{task_id}"
    os.makedirs(path)
    return Workspace(path)
```

### Initialize
```python
def initialize(workspace):
    # Copy project files
    # Install dependencies
    # Setup git
```

### Use
```python
def use(workspace, task):
    # Execute tasks
    # Run commands
```

### Save
```python
def save(workspace):
    # Commit changes
    # Store artifacts
    # Update metadata
```

### Cleanup
```python
def cleanup(workspace):
    # Remove temp files
    # Stop services
    # Delete workspace
```

## State Transitions

| From | To | Trigger |
|------|-----|---------|
| created | initialized | init() |
| initialized | active | task assigned |
| active | saving | task complete |
| saving | cleaned | cleanup() |