# Swarm Patterns

Multiple agents working in parallel on related tasks.

## What is Agent Swarm

A swarm is a group of agents that:
- Work on different parts of a task simultaneously
- Coordinate their efforts
- Combine results at the end

## When to Use Swarm

| Scenario | Benefit |
|----------|---------|
| Multiple independent files | Process in parallel |
| Large codebase analysis | Divide and conquer |
| Multiple test cases | Run simultaneously |
| Search/retrieval tasks | Parallel queries |

## Swarm Pattern: Divide and Conquer

```
                    ┌─────────────┐
                    │  Coordinator│
                    └──────┬──────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
    ┌─────────┐       ┌─────────┐       ┌─────────┐
    │ Agent A │       │ Agent B │       │ Agent C │
    │ File 1  │       │ File 2  │       │ File 3  │
    └────┬────┘       └────┬────┘       └────┬────┘
         │                 │                 │
         └─────────────────┼─────────────────┘
                           ▼
                    ┌─────────────┐
                    │  Aggregator │
                    │  Combine    │
                    │  Results    │
                    └─────────────┘
```

## Implementation

```python
class AgentSwarm:
    def __init__(self, agents, coordinator=None):
        self.agents = agents
        self.coordinator = coordinator
    
    async def execute_parallel(self, task):
        # Divide task
        subtasks = self.coordinator.divide(task)
        
        # Execute in parallel
        results = await asyncio.gather(
            *[agent.execute(subtask) for subtask, agent in zip(subtasks, self.agents)]
        )
        
        # Combine results
        combined = self.coordinator.combine(results)
        return combined
```

## Example: Analyze Multiple Files

```python
async def analyze_codebase(files):
    swarm = AgentSwarm(agents=[
        CodeAnalyzer() for _ in range(4)
    ])
    
    results = await swarm.execute_parallel(ScanFiles(files))
    
    # Aggregate findings
    all_issues = []
    for result in results:
        all_issues.extend(result.issues)
    
    return aggregate_issues(all_issues)
```

## Swarm vs Sequential

| Approach | Time | Complexity | Use When |
|----------|------|------------|----------|
| Sequential | High | Low | Tasks must be ordered |
| Swarm | Low | High | Independent subtasks |

## Best Practices

1. **Divide evenly** - Split work for equal load
2. **Minimize dependencies** - Independent tasks work best
3. **Handle partial failures** - What if one agent fails?
4. **Aggregate correctly** - Combine results properly