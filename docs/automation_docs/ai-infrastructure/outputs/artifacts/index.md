# Artifacts

Generated files and outputs.

## Storage

```
artifacts/
├── {task_id}/
│   ├── code/
│   ├── tests/
│   └── docs/
```

## Artifact Types

| Type | Description |
|------|-------------|
| code | Generated source files |
| tests | Test files |
| docs | Documentation |
| config | Configuration files |

## Metadata

```json
{
  "artifact_id": "uuid",
  "task_id": "uuid",
  "type": "code",
  "path": "artifacts/uuid/main.py",
  "created_at": "2024-01-15T10:30:00Z",
  "size": 1024,
  "checksum": "sha256:..."
}
```