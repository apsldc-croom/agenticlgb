# Compress Conversation History

Instead of sending full chat history every time, use summaries.

## Instead of
```text
[Full conversation history - 5000 tokens]
```

## Use
```text
Conversation summary:
- User uses Django backend
- JWT auth implemented
- Current issue: refresh token expiry

Current question: [latest question]
```

## Benefits
- Saves huge token costs in chat apps
- Maintains context efficiently
- Reduces API costs by 60–80%

## Implementation
Periodically summarize conversation:
- Every N messages
- When token count exceeds threshold
- Use separate API call for summarization