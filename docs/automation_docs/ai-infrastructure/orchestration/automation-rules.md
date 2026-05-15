# Automation Rules

Automated workflow rules.

## Rule Structure

```python
class AutomationRule:
    name: str
    trigger: Trigger
    condition: callable  # Optional additional condition
    action: callable
    priority: int
```

## Example Rules

### Auto-Retry Rule
```python
auto_retry = AutomationRule(
    name="auto_retry",
    trigger=Trigger(condition=lambda: task.failed),
    condition=lambda t: t.error_type in RETRYABLE,
    action=lambda t: retry(t),
    priority=10
)
```

### Auto-Escalate Rule
```python
auto_escalate = AutomationRule(
    name="auto_escalate",
    trigger=Trigger(condition=lambda: task.retries >= 3),
    action=lambda t: escalate_to_human(t),
    priority=20
)
```

### Auto-Complete Rule
```python
auto_complete = AutomationRule(
    name="auto_complete",
    trigger=Trigger(condition=lambda: all_tests_passed),
    condition=lambda t: t.approval_required == False,
    action=lambda t: mark_complete(t),
    priority=5
)
```

## Rule Execution

```python
def run_automation(event):
    for rule in get_matching_rules(event):
        if rule.condition(event):
            rule.action(event)
```