# Constraints

System constraints and limits.

## Resource Constraints

```yaml
constraints:
  resources:
    max_concurrent_tasks: 10
    max_tokens_per_task: 10000
    max_execution_time_seconds: 600
  
  cost:
    daily_budget: 100.00
    max_cost_per_task: 5.00
  
  data:
    max_file_size_mb: 10
    max_context_length: 128000
```

## Operational Constraints

```yaml
  operations:
    allow_destructive_actions: false
    require_git_branch: true
    auto_backup_before_changes: true
```

## Validation

```python
def validate_constraints(task):
    if task.estimated_tokens > MAX_TOKENS:
        return False, "Exceeds token limit"
    if estimated_cost(task) > MAX_COST:
        return False, "Exceeds cost limit"
    return True, "OK"
```