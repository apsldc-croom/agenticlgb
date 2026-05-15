# Protected Resources

Protected assets that require special handling.

## Protected Resource Types

| Resource | Protection | Access |
|----------|------------|--------|
| Production DB | Full | Admin only |
| Production Config | Full | Admin only |
| Secrets | Full | Admin only |
| Production Code | Read-only | Team |
| Test Code | Write | Developer |

## Configuration

```yaml
protected_resources:
  production_database:
    type: database
    protection: full_block
    approvers: [admin]
  
  production_config:
    type: file
    protection: full_block
    approvers: [admin]
  
  secrets:
    type: file
    protection: full_block
    approvers: [admin]
  
  production_code:
    type: git
    protection: read_only
    approvers: [reviewer]
```

## Access Control

```python
def can_access(resource, user):
    if resource.protection == "full_block":
        return user.role in resource.approvers
    return user.has_permission(resource.type)
```