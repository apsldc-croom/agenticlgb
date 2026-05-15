# Orchestration Config

Workflow orchestration settings.

## Example Configuration

```yaml
orchestration:
  max_concurrent_tasks: 4
  task_timeout_seconds: 300
  
  pipelines:
    coding:
      stages:
        - plan
        - generate
        - review
        - test
    
    debugging:
      stages:
        - analyze
        - identify
        - fix
        - verify
```

## Event Settings

```yaml
events:
  enabled: true
  handlers:
    - task.completed
    - task.failed
    - agent.error
  notifications:
    slack: false
    email: false
```