# Complexity Routing

Route by task complexity.

## Complexity Levels

| Level | Description | Models |
|-------|-------------|--------|
| 1-2 | Simple (format, extract) | fast |
| 3-5 | Medium (code simple features) | balanced |
| 6-8 | Complex (debug, architect) | reasoning |
| 9-10 | Very complex (multi-phase) | advanced reasoning |

## Assessment

```python
def assess_complexity(task):
    score = 0
    
    # Code generation vs review
    if task.type == "generation":
        score += 2
    
    # Multi-file changes
    if len(task.files) > 3:
        score += 3
    
    # Dependencies
    if len(task.dependencies) > 5:
        score += 2
    
    # Unknown patterns
    if not similar_task_exists(task):
        score += 2
    
    # Security sensitive
    if "security" in task.description.lower():
        score += 2
    
    return min(score, 10)
```

## Routing Logic

```python
def route_by_complexity(task):
    complexity = assess_complexity(task)
    
    if complexity <= 2:
        return "fast"
    elif complexity <= 5:
        return "balanced"
    elif complexity <= 8:
        return "reasoning"
    else:
        return "advanced_reasoning"
```