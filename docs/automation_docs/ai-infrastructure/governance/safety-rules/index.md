# Safety Rules

Safety guidelines and rules.

## Safety Categories

### Code Safety
```python
SAFETY_RULES = [
    "no_hardcoded_secrets",
    "no_sql_injection_vulnerable_code",
    "no_eval_or_exec",
]
```

### Data Safety
```yaml
  data:
    - no_pii_in_logs
    - encrypt_sensitive_data
    - validate_all_inputs
```

### Execution Safety
```yaml
  execution:
    - timeout_all_long_running
    - sandbox_all_code
    - limit_resource_usage
```

## Safety Checks

```python
def safety_check(code):
    violations = []
    
    if contains_secrets(code):
        violations.append("Hardcoded secrets")
    
    if contains_sql_injection(code):
        violations.append("SQL injection risk")
    
    if contains_dangerous_functions(code):
        violations.append("Dangerous functions")
    
    return violations
```