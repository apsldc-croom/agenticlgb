# Control Output Size (max_tokens)

Always set reasonable output limits.

## Example
```json
{
  "max_tokens": 300
}
```

Without limits, models may generate long explanations unnecessarily.

## Typical Ranges
| Use Case | max_tokens |
|----------|------------|
| Short answer | 100–300 |
| Code fix | 300–800 |
| Long article | 2000+ |

## Key Point
Always set a reasonable output limit to avoid unnecessary token generation and costs.