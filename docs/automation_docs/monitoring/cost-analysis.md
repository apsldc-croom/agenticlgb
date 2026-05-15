# Cost Analysis

Cost tracking and optimization.

## Cost Metrics

| Metric | Description |
|--------|-------------|
| Total Cost | Overall spend |
| Cost per Task | Average cost |
| Cost per User | User spend |
| Cost by Model | Model breakdown |

## Cost Calculation

```python
def calculate_cost(usage, model_prices):
    input_cost = usage.input_tokens / 1000 * model_prices.input
    output_cost = usage.output_tokens / 1000 * model_prices.output
    return input_cost + output_cost
```

## Cost Breakdown

```json
{
  "period": "2024-01",
  "total": 500.00,
  "by_model": {
    "claude-sonnet": 300.00,
    "gpt-4": 150.00,
    "minimax": 50.00
  },
  "by_task": {
    "coding": 250.00,
    "review": 150.00,
    "planning": 100.00
  }
}
```

## Optimization

- Identify high-cost tasks
- Route to cheaper models
- Optimize context usage
- Set budget limits