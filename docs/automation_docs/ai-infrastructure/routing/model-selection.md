# Model Selection

Choosing the right LLM.

## Selection Criteria

```python
def select_model(task, available_models):
    # Score each model
    scored = []
    for model in available_models:
        score = 0
        score += capability_match(model, task)
        score += speed_suitability(model, task)
        score += cost_efficiency(model, task)
        score += historical_performance(model, task.type)
        scored.append((model, score))
    
    return max(scored, key=lambda x: x[1])
```

## Selection Factors

| Factor | Weight | Notes |
|--------|--------|-------|
| Capability | 0.4 | Can handle task? |
| Speed | 0.2 | Latency requirements |
| Cost | 0.2 | Budget constraints |
| History | 0.2 | Past success rate |

## Model Categories

```python
MODELS = {
    "fast": ["minimax", "qwen", "haiku"],
    "balanced": ["sonnet", "gpt-4", "gemini-pro"],
    "reasoning": ["opus", "gpt-5", "deepseek-r1"],
    "cheap": ["llama-3-8b", "gemma"]
}
```

## Usage

```python
# Simple task → fast model
if task.complexity < 3:
    return select_from("fast")

# Complex task → balanced
if task.complexity < 7:
    return select_from("balanced")

# Very complex → reasoning
return select_from("reasoning")