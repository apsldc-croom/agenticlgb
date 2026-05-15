# Avoid Unnecessary "Thinking"

Large reasoning models may generate hidden/internal reasoning tokens.

## Avoid Prompts Like
- "Think deeply"
- "Reason step by step"
- "Extensively analyze"

## Use Instead
```text
Give direct answer with brief reasoning.
```

For coding:
```text
Return optimized code only.
```

## Why It Matters
Thinking/reasoning tokens add to cost without adding value when not needed.