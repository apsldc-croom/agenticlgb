# Branch Management

Git branch strategy.

## Branch Types

| Branch | Purpose | Who Creates |
|--------|---------|-------------|
| main | Production | System |
| develop | Integration | System |
| feature/* | New features | Agent/Human |
| task/* | Task-specific | Agent |
| fix/* | Bug fixes | Agent |
| review/* | For review | Agent |

## Branch Rules

```yaml
branches:
  protected:
    - main
    - develop
  
  naming:
    feature: "feature/{task-id}-{description}"
    task: "task/{task-id}-{description}"
    fix: "fix/{issue-id}-{description}"
  
  creation:
    from: develop
    auto_delete: true
```

## Branch Operations

```python
def create_task_branch(task_id, description):
    branch_name = f"task/{task_id}-{slugify(description)}"
    git.checkout_new_branch(branch_name)
    return branch_name

def cleanup_branch(branch_name):
    if should_delete(branch_name):
        git.delete_branch(branch_name)
```