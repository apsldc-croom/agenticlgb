# Rollback Strategy

Reverting changes.

## Rollback Types

| Type | Use Case |
|------|-----------|
| Revert | Undo single commit |
| Reset | Remove commits |
| Checkout | Restore file |

## Revert Commit

```python
def revert_commit(commit_sha):
    git.execute(f"git revert {commit_sha}")
    push_changes(f"Revert {commit_sha}")
```

## Reset to Previous

```python
def reset_to(commit_sha):
    git.execute(f"git reset --hard {commit_sha}")
    push_changes(f"Reset to {commit_sha}")
```

## Emergency Rollback

```yaml
rollback:
  trigger:
    - deployment_failed
    - critical_bug_detected
  
  action:
    - git.reset("--hard", "HEAD~1")
    - notify_team
    - create_incident
```

## Rollback Validation

```python
def validate_rollback(commit):
    if is_production_commit(commit):
        require_approval("admin")
    if has_dependent_commits(commit):
        warn_about_dependent()
    return True
```