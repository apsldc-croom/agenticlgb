# Planner-Reviewer Flow

## Standard Workflow

```
User Request
     │
     ▼
┌──────────┐
│ Planner  │ ─── Decompose task
└──────────┘
     │
     ▼
┌──────────┐
│  Coder   │ ─── Generate code
└──────────┘
     │
     ▼
┌──────────┐
│ Reviewer │ ─── Validate output
└──────────┘
     │
     ▼
  ┌─┴─┐
  ▼   ▼
Pass Fail
  │   │
  ▼   ▼
Done Fixer
```

## Agent Responsibilities

### Planner
- Understand task
- Break into subtasks
- Order tasks
- Identify dependencies

### Coder
- Generate code
- Write tests
- Implement features

### Reviewer
- Check code quality
- Verify correctness
- Suggest improvements

### Fixer
- Address reviewer feedback
- Make corrections
- Re-submit for review

## Flow Variations

### Simple Task
Planner → Coder → Reviewer → Done

### Complex Task
Planner → (Coder → Reviewer) × n → Fixer → Done

### Review Failed
Reviewer → Fixer → Reviewer → Done