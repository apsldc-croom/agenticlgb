# Stream Responses

Use streaming for:
- Faster UX
- Early stopping
- Reduced wasted generation

## Benefits

1. **Faster perceived response** - First token arrives immediately
2. **Early stopping** - Detect completion, cancel if needed
3. **Token savings** - Stop generation when done

## Implementation (example)
```python
response = client.messages.create(
    model="claude-3-sonnet-20240229",
    max_tokens=500,
    stream=True,
    messages=[{"role": "user", "content": "Hello"}]
)

for chunk in response:
    print(chunk)
```

## When to Use
- Chat interfaces
- Real-time applications
- Long-form generation
- When early feedback matters