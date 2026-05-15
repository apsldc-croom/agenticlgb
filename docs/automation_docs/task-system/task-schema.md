# Task Schema

## Task Structure

```yaml
task:
  id: string              # Unique task identifier
  type: string            # Task type (coding, review, etc.)
  status: string          # current status
  priority: integer       # 1-10, higher is more urgent
  description: string     # Human-readable description
  
  # Hierarchy
  parent_id: string|null  # Parent task if subtask
  children: [string]     # Subtask IDs
  
  # Execution
  assigned_agent: string  # Agent handling this task
  created_at: timestamp
  updated_at: timestamp
  started_at: timestamp|null
  completed_at: timestamp|null
  
  # Context
  context: object         # Task-specific context
  artifacts: [string]    # Files/code generated
  
  # Dependencies
  depends_on: [string]   # Task IDs that must complete first
  blocks: [string]       # Tasks waiting on this one
  
  # Results
  result: object|null     # Task output
  error: string|null     # Error message if failed
```

## Task Types

| Type | Description |
|------|-------------|
| coding | Code generation |
| review | Code review |
| testing | Test generation |
| debugging | Bug fixing |
| planning | Task planning |
| documentation | Doc generation |