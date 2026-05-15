# Dependency Graph

## Definition

Tasks form a directed acyclic graph (DAG):
- Nodes = tasks
- Edges = dependencies

## Types of Dependencies

### Finish-to-Start
Task B cannot start until Task A finishes:
```
A ──→ B
```

### Start-to-Start
Task B cannot start until Task A starts:
```
A
│
B
```

### Finish-to-Finish
Task B cannot finish until Task A finishes:
```
A
│
B
```

## Graph Management

### Cycle Detection
Before adding dependency, check for cycles:
```
A → B → C → A  # INVALID
```

### Topological Sorting
Order tasks for execution:
```python
def topological_sort(tasks):
    # Kahn's algorithm
    in_degree = {t: 0 for t in tasks}
    for t in tasks:
        for dep in t.depends_on:
            in_degree[t] += 1
    
    queue = [t for t in tasks if in_degree[t] == 0]
    while queue:
        task = queue.pop(0)
        yield task
        for dependent in task.blocks:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
```

## Parallel Execution

Tasks with no dependencies can run in parallel:
- Reduce total execution time
- Optimize resource usage
- Handle via task queue