# Prompt Templates

Reusable prompt skeletons.

## Composition Pattern

Avoid giant prompts. Instead:

```python
final_prompt = (
    system_prompt
    + domain_prompt
    + task_prompt
    + formatting_prompt
)
```

This scales much better.