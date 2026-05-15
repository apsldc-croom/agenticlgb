# Execution Semantics

## Execution Model

### At-Least-Once
Tasks may execute multiple times but guarantee at least one execution.

### Idempotency
Design tasks to be idempotent - running multiple times produces same result.

### Atomicity
Each subtask should be atomic - either fully complete or fully rolled back.

## Execution Guarantees

### No Data Loss
- All state persisted
- Checkpoints saved regularly
- Recovery possible from any point

### Ordered Execution
- Dependencies enforced
- Sequence maintained within each branch

### Timeout Handling
- Each task has max runtime
- Timeout triggers retry/escalation

## Context Passing

```python
def execute_with_context(task, context):
    # Input: context from previous tasks
    modified_context = task.execute(context)
    
    # Output: context for next tasks
    return modified_context
```

## Error Semantics

### Fail Fast
Stop on first error in sequential flow.

### Fail Safe
Continue parallel flows even if one branch fails.

### Compensating Actions
On failure, execute compensating actions to undo partial work.