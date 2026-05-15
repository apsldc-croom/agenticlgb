# Routing Decisions

Model and provider routing choices.

## Decision Recording

```python
@dataclass
class RoutingDecision:
    task_id: str
    selected_model: str
    reason: str
    alternatives_considered: list
    estimated_cost: float
    timestamp: datetime
```

## Decision Logic

```python
def decide_routing(task):
    # Record decision
    decision = RoutingDecision(
        task_id=task.id,
        selected_model=select_model(task),
        reason=explain_reason(task),
        alternatives_considered=get_alternatives(task),
        estimated_cost=estimate(task)
    )
    
    record_decision(decision)
    return decision.model
```

## Analysis

- Track model usage
- Monitor cost efficiency
- Review success by model

## Example

```
Task: Generate API endpoint
Decision: claude-sonnet
Reason: Balanced quality/cost for code generation
Alternatives: haiku (too weak), opus (too expensive)
Est Cost: $0.02
```