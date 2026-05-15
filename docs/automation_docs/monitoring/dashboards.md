# Dashboards

Monitoring dashboards.

## Dashboard Types

### Overview Dashboard
- Total tasks
- Success rate
- Active tasks
- Cost today

### Performance Dashboard
- Latency percentiles
- Task duration
- Model comparison

### Cost Dashboard
- Daily spend
- Cost by model
- Budget status

### Quality Dashboard
- Quality scores
- Failure breakdown
- Review approval rate

## Example Dashboard (Grafana)

```yaml
panels:
  - title: "Task Success Rate"
    type: graph
    targets:
      - expr: "sum(rate(tasks_completed[5m])) / sum(rate(tasks_total[5m]))"
  
  - title: "Latency P95"
    type: graph
    targets:
      - expr: "histogram_quantile(0.95, rate(task_latency_bucket[5m]))"
  
  - title: "Cost Today"
    type: stat
    targets:
      - expr: "sum(cost_total)"
```

## Alerts Configuration

```yaml
alerts:
  - name: High Failure Rate
    condition: failure_rate > 0.1
    severity: warning
  
  - name: Budget Exceeded
    condition: daily_cost > daily_budget
    severity: critical