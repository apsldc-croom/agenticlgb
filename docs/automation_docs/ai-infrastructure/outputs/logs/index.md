# Logs

Execution logs for debugging.

## Log Types

| Type | Contents |
|------|----------|
| agent | Agent actions |
| system | System events |
| error | Errors and exceptions |
| audit | Audit trail |

## Log Format

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "logger": "agent.coder",
  "message": "Generated code for task 123",
  "context": {
    "task_id": "123",
    "duration_ms": 1500
  }
}
```

## Log Storage

- Recent logs: Searchable (last 7 days)
- Archive: Compressed (30+ days)
- Retention: Configurable