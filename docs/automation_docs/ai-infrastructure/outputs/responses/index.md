# Responses

Raw API responses storage.

## Storage Structure

```
responses/
├── {task_id}/
│   ├── request.json
│   └── response.json
```

## What's Stored

```json
{
  "task_id": "uuid",
  "timestamp": "2024-01-15T10:30:00Z",
  "model": "claude-sonnet",
  "request": {
    "messages": [...],
    "temperature": 0.2,
    "max_tokens": 500
  },
  "response": {
    "content": "...",
    "usage": {
      "input_tokens": 1000,
      "output_tokens": 300
    }
  }
}
```

## Use Cases

- Debugging response issues
- Analyzing model behavior
- Token usage auditing
- Replaying tasks