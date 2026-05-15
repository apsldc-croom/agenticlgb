# Reasoning Models Are Slower and More Expensive

Why?

- More internal thinking
- Larger compute
- Longer outputs
- Chain-of-thought generation

## Implications
- Don't use reasoning models for trivial tasks
- Don't ask for "deep analysis" unless necessary
- Set appropriate max_tokens (reasoning models need more room)

## Trade-off
| Factor | Regular Models | Reasoning Models |
|--------|---------------|------------------|
| Speed | Fast | Slow |
| Cost | Low | High |
| Output length | Shorter | Longer |
| Best for | Simple tasks | Complex reasoning |