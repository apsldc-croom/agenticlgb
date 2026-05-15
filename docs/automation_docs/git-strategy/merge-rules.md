# Merge Rules

Merge policies and rules.

## Merge Requirements

```yaml
merge_requirements:
  task_branch:
    - all_tests_pass
    - code_review_approved
    - linting_passed
    - no_conflicts
  
  feature_branch:
    - code_review_required
    - ci_pipeline_passed
    - documentation_updated
```

## Merge Types

### Squash Merge
```python
def squash_merge(source, target):
    git.checkout(target)
    git.merge("--squash", source)
    git.commit(f"Merge {source}")
    git.delete_branch(source)
```

### Rebase Merge
```python
def rebase_merge(source, target):
    git.checkout(source)
    git.rebase(target)
    git.checkout(target)
    git.merge(source, "--ff-only")
```

## Conflict Resolution

```python
def resolve_conflicts(branch):
    conflicts = get_conflicts(branch)
    for conflict in conflicts:
        # Auto-resolve simple conflicts
        if is_simple_conflict(conflict):
            auto_resolve(conflict)
        else:
            flag_for_human(conflict)
```