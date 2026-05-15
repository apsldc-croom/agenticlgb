# Deployment Architecture

## Recommended Setup (Initial)

```
┌─────────────────────────────────────────┐
│              User Access                │
└─────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│         Application Server              │
│   (Flask/FastAPI + Agent System)        │
└─────────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
┌──────────────┐      ┌──────────────┐
│  API Server  │      │  Queue       │
│  (LLM Calls) │      │  (Task Mgmt) │
└──────────────┘      └──────────────┘
        │                     │
        ▼                     ▼
┌──────────────┐      ┌──────────────┐
│  Workspace   │      │  Database    │
│  (Ephemeral) │      │  (SQLite/PG) │
└──────────────┘      └──────────────┘
```

## Scaling Considerations

### Phase 1: Single Instance
- All components on one server
- SQLite for storage
- Good for low usage

### Phase 2: Separate Services
- API and workers separate
- Task queue (Redis/RabbitMQ)
- PostgreSQL for data

### Phase 3: Distributed
- Multiple worker instances
- Vector DB for memory
- Container orchestration