# Cost Routing

Route by cost optimization.

## Cost Factors

```python
COSTS = {
    "minimax": 0.0002,    # per 1K tokens
    "qwen": 0.0003,
    "llama-3-8b": 0.0002,
    "sonnet": 0.003,
    "opus": 0.015,
}
```

## Cost-Based Selection

```python
def route_by_cost(task, budget):
    # Get models under budget
    eligible = [m for m in available_models 
                if estimate_cost(task, m) <= budget]
    
    # Select cheapest that can handle task
    if not eligible:
        return None  # Budget too low
    
    return min(eligible, key=lambda m: m.cost)
```

## Budget Optimization

```python
def optimize_for_budget(tasks, daily_budget):
    remaining = daily_budget
    
    # Sort by priority
    sorted_tasks = sorted(tasks, key=lambda t: -t.priority)
    
    for task in sorted_tasks:
        model = select_affordable_model(task, remaining)
        if model:
            assign(task, model)
            remaining -= estimate_cost(task, model)
```

## Cost Tracking

- Per-task cost
- Daily/weekly/monthly totals
- Per-user costs
- Cost per model