# Data Flow

## Input Flow

```
User Input
    │
    ▼
Request Parser
    │
    ▼
Task Classifier
    │
    ▼
Context Builder (RAG + Memory)
    │
    ▼
LLM Request
```

## Output Flow

```
LLM Response
    │
    ▼
Output Validator
    │
    ▼
Result Formatter
    │
    ▼
Memory Update
    │
    ▼
User Response
```

## Data Storage

| Data Type | Storage | Purpose |
|-----------|---------|---------|
| Task State | Database | Track task progress |
| Conversation | Memory | Context for current session |
| Project Knowledge | Vector DB | Long-term context |
| Code Artifacts | File System | Generated code |
| Metrics | Time-series DB | Monitoring |