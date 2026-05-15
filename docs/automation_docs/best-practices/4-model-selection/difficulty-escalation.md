# Difficulty Escalation - Try Cheap First

Important optimization strategy.

## Workflow
1. Try cheap model first
2. Detect failure/confidence
3. Escalate only if needed

## Example
```
MiniMax -> failed
then Claude Sonnet
```

## Implementation Ideas
- Check if response contains error keywords
- Validate output format
- Use confidence scores if available
- Set timeout thresholds

## Benefit
Most requests are cheap, only hard ones escalate to expensive models.