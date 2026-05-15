# Acceptance Tests

User acceptance validation.

## Test Categories

### Functional Acceptance
Does it do what it's supposed to?

```python
def test_functional_acceptance(task, result):
    expected_behavior = task.requirements
    actual_behavior = result.output
    
    for behavior in expected_behavior:
        if not matches(actual_behavior, behavior):
            return fail(f"Missing: {behavior}")
    return pass()
```

### Usability Acceptance
Is it easy to use?

```python
def test_usability(result):
    if result.is_clear:
        score += 1
    if result.has_examples:
        score += 1
    return usability_score(score)
```

### Performance Acceptance
Is it fast enough?

```python
def test_performance(result):
    if result.latency < THRESHOLD:
        return pass()
    return fail(f"Too slow: {result.latency}ms")
```

## Acceptance Criteria

| Category | Criteria |
|----------|----------|
| Functional | Meets requirements |
| Usable | Clear and helpful |
| Reliable | Consistent results |
| Efficient | Acceptable performance |