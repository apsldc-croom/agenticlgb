# Regression Tests

Preventing regression in AI outputs.

## Test Categories

### Output Regression
```python
def test_output_regression(task, expected_output):
    current = run_task(task)
    if current != expected_output:
        # Check if change is acceptable
        if is_acceptable_change(current, expected_output):
            update_expected(current)
        else:
            fail_regression(task)
```

### Quality Regression
```python
def test_quality_regression():
    current = measure_quality()
    previous = get_previous_quality()
    
    if current < previous * 0.9:
        alert("Quality regression detected")
```

### Performance Regression
```python
def test_performance_regression():
    current_latency = measure_latency()
    baseline = get_baseline()
    
    if current_latency > baseline * 1.5:
        alert("Performance regression")
```

## Test Execution

```yaml
regression:
  run_on: [commit, daily, release]
  save_results: true
  alert_on_fail: true