# Router Agent

Task routing and model selection.

## Responsibilities

- Classify task complexity
- Select appropriate model
- Route to right agent
- Handle escalations

## Routing Logic

```python
def route(task):
    complexity = assess_complexity(task)
    
    if complexity <= 2:
        return "fast-model", "coder"
    elif complexity <= 5:
        return "balanced-model", "coder"
    elif complexity <= 8:
        return "reasoning-model", "architect"
    else:
        return "advanced", "planner"
```

## Outputs

- Selected model
- Target agent
- Priority
- Estimated cost