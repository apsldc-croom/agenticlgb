# Agents Config

Agent configurations.

## Example Configuration

```yaml
agents:
  planner:
    model: claude-sonnet
    max_retries: 2
    timeout_seconds: 60
    prompts:
      system: prompts/agents/planner/system.md
      task: prompts/agents/planner/task.md
  
  coder:
    model: claude-sonnet
    max_retries: 3
    timeout_seconds: 120
    prompts:
      system: prompts/agents/coder/system.md
      task: prompts/agents/coder/task.md
  
  reviewer:
    model: gpt-4
    max_retries: 2
    timeout_seconds: 60
    prompts:
      system: prompts/agents/reviewer/system.md
```

## Agent Capabilities

```yaml
capabilities:
  coder:
    - code_generation
    - refactoring
    - bug_fixing
  
  reviewer:
    - code_review
    - security_scan
    - testing
```