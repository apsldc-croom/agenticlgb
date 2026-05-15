# Monitor Token Usage

Track:
- Input tokens
- Output tokens
- Cache reads/writes (if supported)
- Cost per request

## Response Fields (example)
```json
{
  "usage": {
    "input_tokens": 1000,
    "output_tokens": 300,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 500
  }
}
```

## Best Practices
- Log token usage per request
- Set alerts for unusual spending
- Track cost per feature
- Monitor cache hit rates
- Calculate cost per user/conversation