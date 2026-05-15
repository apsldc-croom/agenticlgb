# Rollback

## Rollback Strategy

### Automatic Rollback
Undo changes when task fails.

### Manual Rollback
Human decides what to undo.

## Rollback Operations

### File Rollback
- Restore original files
- Remove generated files

### Git Rollback
```python
def rollback_to_commit(commit_sha):
    subprocess.run(["git", "checkout", commit_sha])
    subprocess.run(["git", "reset", "--hard", commit_sha])
```

### State Rollback
- Restore database state
- Clear caches

## Rollback Decision

```python
def should_rollback(task, failure):
    if failure.severity > HIGH_SEVERITY:
        return True
    
    if task.phase == "planning":
        return False  # No changes yet
    
    if can_repair_in_place(failure):
        return False  # Fix instead
    
    return True
```

## Rollback Safety

- Always create backup before rollback
- Test rollback procedure
- Log all rollback actions
- Verify after rollback