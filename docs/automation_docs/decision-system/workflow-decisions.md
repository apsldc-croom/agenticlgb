# Workflow Decisions

Workflow and pipeline choices.

## Decision Types

| Type | Example |
|------|---------|
| Pipeline | Use coding pipeline vs debugging |
| Parallel | Run tests in parallel |
| Retry | Retry strategy |
| Fallback | Fallback chain |

## Recording

```python
@dataclass
class WorkflowDecision:
    task_id: str
    workflow_type: str
    steps: list[str]
    reason: str
    outcome: str
```

## Example

```
Task: Add user authentication
Decision: coding-pipeline
Steps: [plan, generate, review, test]
Reason: Standard feature development workflow
Outcome: success
```

## Optimization

- Analyze workflow patterns
- Identify bottlenecks
- Improve success rate