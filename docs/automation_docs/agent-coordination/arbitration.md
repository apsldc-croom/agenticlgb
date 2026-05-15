# Arbitration

## When Arbitration Needed

- Two agents disagree
- Conflicting outputs
- Resource contention

## Arbitration Strategies

### First-Write-Wins
First agent's decision is final.

### Majority Vote
If multiple agents produce output, use most common.

### External Resolution
Human decides when agents can't agree.

### Hierarchical
Higher-priority agent's decision wins.

## Arbitration Implementation

```python
class Arbitrator:
    def resolve(self, conflict):
        if conflict.type == "output_conflict":
            return self.resolve_output_conflict(conflict)
        elif conflict.type == "resource_conflict":
            return self.resolve_resource_conflict(conflict)
        else:
            return self.escalate(conflict)
    
    def resolve_output_conflict(self, conflict):
        agents = conflict.agents
        outputs = [a.output for a in agents]
        
        # Try to find consensus
        consensus = find_common(outputs)
        if consensus:
            return consensus
        
        # Fall back to ranking
        ranked = rank_by_confidence(agents)
        return ranked[0].output
```