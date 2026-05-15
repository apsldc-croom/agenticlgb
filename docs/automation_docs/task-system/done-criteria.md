# Done Criteria

## Definition

A task is "done" when all of its done criteria are met.

## Criteria Types

### Output Criteria
- Required artifacts generated
- Files created/modified
- Tests passing

### Quality Criteria
- Linting passes
- Code review approved
- Tests pass

### Process Criteria
- Documentation updated
- Dependencies resolved
- Changes committed

## Task-Specific Done Criteria

### Coding Task
- [ ] Code written
- [ ] Tests written
- [ ] Tests pass
- [ ] Linting passes
- [ ] Code reviewed

### Review Task
- [ ] All files reviewed
- [ ] Issues logged
- [ ] Approval given or changes requested

### Testing Task
- [ ] Tests written
- [ ] Tests pass
- [ ] Coverage adequate

## Validation

```python
def validate_done_criteria(task):
    for criterion in task.done_criteria:
        if not criterion.is_met():
            return False, f"Missing: {criterion.name}"
    return True, "All criteria met"
```

## Override

Human can mark task done manually if automated checks fail but output is acceptable.