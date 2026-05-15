# Use System Prompts Carefully

A giant system prompt wastes tokens every request.

## Bad Practice
```text
20-page instructions repeated every API call
```

## Better Approach

- Keep core rules only
- Cache reusable prompts
- Move examples externally

## Best Practice

Structure your system prompt to include only essential instructions:

```text
Role: Code reviewer
Focus: Security and performance
Output: Concise findings only
```

Repeat only what's necessary for each request.