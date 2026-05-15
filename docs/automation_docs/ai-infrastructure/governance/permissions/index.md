# Permissions

Access control and permissions.

## Permission Types

| Permission | Description |
|------------|-------------|
| read | Read data |
| write | Modify data |
| execute | Run actions |
| admin | Administrative |

## Role-Based Access

```yaml
roles:
  developer:
    permissions:
      - read: tasks
      - write: own_tasks
      - execute: run_tests
  
  reviewer:
    permissions:
      - read: all_tasks
      - write: reviews
      - execute: approve
  
  admin:
    permissions:
      - read: all
      - write: all
      - execute: all
      - admin: system
```

## Permission Check

```python
def check_permission(user, action, resource):
    role = get_role(user)
    return action in role.permissions
```