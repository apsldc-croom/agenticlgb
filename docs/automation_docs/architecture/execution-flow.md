# Execution Flow

## Task Execution Pipeline

```
User Request
     │
     ▼
┌────────────┐
│   Router   │ ─── Determine task complexity
└────────────┘
     │
     ▼
┌────────────┐
│  Planner   │ ─── Create execution plan
└────────────┘
     │
     ▼
┌────────────┐
│  Executor  │ ─── Execute subtasks
└────────────┘
     │
     ▼
┌────────────┐
│  Reviewer  │ ─── Validate output
└────────────┘
     │
     ▼
   Result
     │
     ▼
┌────────────┐
│  Monitor   │ ─── Log metrics, handle failures
└────────────┘
```

## Key Flow Patterns

### Simple Task Flow
1. Router → Planner → Coder → Reviewer → Result

### Complex Task Flow
1. Router → Planner → (Architect → Coder → Reviewer) × n → Fixer → Result

### Failed Task Flow
1. Detect failure → Escalate to higher model → Retry → If still failed → Report to human