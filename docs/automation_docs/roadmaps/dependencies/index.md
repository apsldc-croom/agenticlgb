# Dependencies

Project dependencies and tracking.

## Technical Dependencies

| Dependency | Purpose | Status |
|------------|---------|--------|
| OpenRouter | LLM access | Required |
| SQLite | Local storage | Optional |
| Redis | Task queue | Optional |
| Vector DB | Memory | Required |

## Internal Dependencies

```
Phase 1 ──► Phase 2 ──► Phase 3 ──► Phase 4
   │            │            │          │
   ▼            ▼            ▼          ▼
Setup       Multi-agent   Memory     Advanced
             System       System     Features
```

## Dependency Tracking

```json
{
  "task_id": "phase-2",
  "depends_on": ["phase-1"],
  "blocked_by": [],
  "blocks": ["phase-3"]
}
```

## External Dependency Risks

- API changes
- Service outages
- Pricing changes