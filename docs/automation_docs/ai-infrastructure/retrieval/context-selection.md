# Context Selection

Choosing what to retrieve.

## Selection Strategy

```python
def select_context(task, memory):
    # Determine what to retrieve
    if task.type == "coding":
        code_context = memory.search("code", top_k=5)
        return code_context
    
    if task.type == "debugging":
        error_context = memory.search("errors", top_k=3)
        stack_context = memory.search("stack traces", top_k=3)
        return error_context + stack_context
    
    return memory.search(task.description, top_k=3)
```

## Context Budget

Stay within token limits:
```python
def budget_context(task, max_tokens=6000):
    retrieved = retrieve_all(task)
    selected = []
    total_tokens = 0
    
    for item in sorted_by_relevance(retrieved):
        if total_tokens + item.tokens > max_tokens:
            break
        selected.append(item)
        total_tokens += item.tokens
    
    return selected
```

## Relevance Filtering

- Must match task type
- Score above threshold
- Not duplicate existing context