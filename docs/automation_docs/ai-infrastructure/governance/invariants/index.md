# Invariants

Invariant rules that must always hold.

## Invariant Types

### Safety Invariants
```python
INVARIANTS = [
    "never_delete_production_data",
    "always_backup_before_changes",
    "never_bypass_security_checks",
]
```

### Quality Invariants
```python
QUALITY_INVARIANTS = [
    "all_code_passes_linting",
    "all_tests_pass_before_merge",
    "all_changes_have_review",
]
```

### State Invariants
```python
STATE_INVARIANTS = [
    "task.state in valid_states",
    "task.parent_id exists if has_children",
    "task.created_at <= task.completed_at",
]
```

## Enforcement

```python
def enforce_invariants(task):
    for invariant in INVARIANTS:
        if not invariant.holds(task):
            raise InvariantViolation(invariant, task)
```