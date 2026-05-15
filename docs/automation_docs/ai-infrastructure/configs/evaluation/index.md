# Evaluation Config

Evaluation settings.

## Example Configuration

```yaml
evaluation:
  enabled: true
  
  metrics:
    - success_rate
    - quality_score
    - token_efficiency
    - latency
  
  thresholds:
    min_success_rate: 0.8
    max_latency_ms: 5000
    max_cost_per_task: 1.00
```

## Quality Gates

```yaml
quality_gates:
  code_review:
    require_approval: true
    min_approvals: 1
  
  testing:
    require_tests: true
    min_coverage: 0.8
  
  linting:
    require_pass: true
    allowed_warnings: 0
```