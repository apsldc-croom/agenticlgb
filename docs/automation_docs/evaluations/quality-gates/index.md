# Quality Gates

Quality checkpoints in workflow.

## Gate Types

| Gate | Trigger | Action |
|------|---------|--------|
| Pre-Generation | Before generation | Check inputs |
| Post-Generation | After generation | Validate output |
| Pre-Commit | Before commit | Final check |
| Pre-Deploy | Before deploy | Deployment check |

## Gate Implementation

```python
class QualityGate:
    def __init__(self, name, checks):
        self.name = name
        self.checks = checks
    
    def evaluate(self, context):
        results = []
        for check in self.checks:
            result = check.run(context)
            results.append(result)
        
        return all(r.passed for r in results)
```

## Standard Gates

### Code Quality Gate
- Linting passes
- Type checking passes
- No security issues

### Test Quality Gate
- All tests pass
- Coverage above threshold
- No new warnings

### Review Quality Gate
- Reviewer approved
- No critical issues
- Documentation updated