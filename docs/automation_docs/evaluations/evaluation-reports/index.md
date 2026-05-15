# Evaluation Reports

Analysis and reporting.

## Report Types

### Daily Report
```json
{
  "date": "2024-01-15",
  "tasks_total": 50,
  "tasks_success": 45,
  "success_rate": 0.90,
  "avg_latency_ms": 1500,
  "total_tokens": 500000,
  "total_cost": 15.00
}
```

### Weekly Report
- Success by task type
- Model comparison
- Cost breakdown
- Quality trends

### Incident Report
```json
{
  "incident": "regression_detected",
  "date": "2024-01-15",
  "task": "api_generation",
  "issue": "output_format_changed",
  "impact": "4 tasks failed",
  "resolution": "updated expected output"
}
```

## Report Generation

```python
def generate_report(type, date_range):
    data = collect_metrics(date_range)
    report = format_report(type, data)
    notify(report)
    return report
```