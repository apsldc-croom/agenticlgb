# Autonomous Commits

Auto-commit rules for AI agents.

## When to Auto-Commit

| Condition | Commit |
|-----------|--------|
| Task complete | Yes |
| Logical unit done | Yes |
| Tests passing | Yes |
| Breakpoint reached | Optional |

## Auto-Commit Configuration

```yaml
autonomous_commits:
  enabled: true
  
  triggers:
    - task_completed
    - tests_passed
    - review_approved
  
  limits:
    max_per_hour: 10
    max_per_task: 5
  
  message_format:
    - type: auto
    - scope: inferred
    - subject: generated
```

## Commit Decision Logic

```python
def should_auto_commit(task, changes):
    if not can_commit():
        return False, "Not allowed"
    
    if not meets_quality_threshold(changes):
        return False, "Quality too low"
    
    if has_sensitive_data(changes):
        return False, "Contains secrets"
    
    if is_task_complete(task):
        return True, "Task complete"
    
    if is_logical_unit(changes):
        return True, "Logical unit done"
    
    return False, "Not enough for commit"
```

## Manual Override

```python
# Agent can request human review
def request_review_for_commit(changes):
    if is_complex_change(changes):
        return request_human_review(changes)
```