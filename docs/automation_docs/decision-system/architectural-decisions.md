# Architectural Decisions

Major architectural choices.

## Decision Format

```markdown
# ADR-001: Use PostgreSQL for task storage

## Status
Accepted

## Context
Need persistent storage for task state.

## Decision
Use PostgreSQL instead of SQLite for:
- Better concurrency
- Production-ready
- Easier scaling

## Consequences
- Need migration scripts
- More complex setup
- Better reliability
```

## Decision Categories

| Category | Examples |
|----------|----------|
| Storage | Database selection |
| Infrastructure | Deployment approach |
| Integration | API choices |
| Security | Auth approach |

## Tracking

```python
def record_decision(adr):
    store.save({
        "id": adr.id,
        "title": adr.title,
        "status": adr.status,
        "decided_at": now(),
        "decided_by": system,
        "rationale": adr.rationale
    })
```

## Review

- Review quarterly
- Re-evaluate when context changes
- Document superseded decisions