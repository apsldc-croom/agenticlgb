# Use Temperature Wisely

## Effect
High temperature:
- More verbose
- More tokens
- More randomness

## For Production
```json
{
  "temperature": 0.2
}
```

## Guidelines
| Temperature | Use Case |
|-------------|----------|
| 0.0–0.2 | Factual, code, deterministic tasks |
| 0.5–0.7 | Creative writing, brainstorming |
| 0.8–1.0 | Exploration, diverse outputs |

For cost optimization, use lower temperature in production.