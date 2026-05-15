# Conflict Resolution

## Conflict Types

### Resource Conflict
Two agents need same resource.

### Output Conflict
Two agents produce different results.

### Goal Conflict
Agents have conflicting objectives.

## Resolution Approaches

### Avoidance
Prevent conflicts through planning.

### Detection
Identify conflicts early.

### Resolution
Resolve when detected.

## Resolution Strategies

### Time-Based
- Agent with earlier start time wins
- Or: Agent with higher priority wins

### Capability-Based
- More capable agent wins
- Or: Agent specializing in resource wins

### Negotiation
- Agents discuss and agree
- May involve compromise

## Example: Code Merge Conflict

```python
def resolve_merge_conflict(conflict):
    # Get both versions
    version_a = conflict.version_a
    version_b = conflict.version_b
    
    # Ask third agent to decide
    reviewer = get_reviewer_agent()
    decision = reviewer.decide(version_a, version_b)
    
    return decision
```