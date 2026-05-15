# Approval Gates

Workflow approval checkpoints.

## Gate Types

| Gate | Trigger | Approver |
|------|---------|----------|
| pre_execution | Task start | Optional |
| pre_commit | Before commit | Reviewer |
| pre_deploy | Before deploy | Admin |
| pre_delete | Before delete | Admin |

## Gate Configuration

```yaml
approval_gates:
  pre_commit:
    required: true
    approvers:
      - role: reviewer
      - role: developer
        if: owns_code
    
  pre_deploy:
    required: true
    approvers:
      - role: admin
  
  pre_delete:
    required: true
    approvers:
      - role: admin
    warning: "This action cannot be undone"
```

## Gate Implementation

```python
def check_gate(task, gate_type):
    gate = get_gate(gate_type)
    if not gate.required:
        return True
    
    return get_approval(task, gate)
```