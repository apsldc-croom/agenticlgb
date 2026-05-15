# Cleanup

Workspace resource cleanup.

## Cleanup Triggers

| Trigger | Action |
|---------|--------|
| Task complete | Cleanup ephemeral |
| Session end | Save persistent |
| Idle timeout | Archive workspace |
| Disk pressure | Delete old archives |

## Cleanup Tasks

```python
def cleanup_workspace(workspace):
    # Remove temp files
    for f in glob(f"{workspace.path}/tmp/*"):
        os.remove(f)
    
    # Clear caches
    shutil.rmtree(f"{workspace.path}/.cache", ignore_errors=True)
    
    # Close processes
    for proc in workspace.processes:
        proc.terminate()
    
    # Free resources
    workspace.release_resources()
```

## Retention Policy

```yaml
cleanup:
  ephemeral:
    delete_after_hours: 24
  
  persistent:
    archive_after_days: 30
    delete_after_days: 90
  
  artifacts:
    keep_days: 30
    max_size_gb: 5
```

## Implementation

```python
def run_cleanup():
    for workspace in get_idle_workspaces():
        if workspace.idle_hours > MAX_IDLE:
            if workspace.type == "ephemeral":
                workspace.cleanup()
            else:
                workspace.archive()
```