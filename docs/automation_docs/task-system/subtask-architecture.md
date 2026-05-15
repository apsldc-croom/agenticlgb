# Subtask Architecture

## Decomposition Strategy

### Top-Down Decomposition
1. Planner receives main task
2. Breaks into logical subtasks
3. Orders subtasks by dependencies
4. Assigns to appropriate agents

## Subtask Types

### Sequential Subtasks
Must execute in order:
```
A → B → C
```

### Parallel Subtasks
Can execute simultaneously:
```
A
↔
B
```

### Conditional Subtasks
Execute based on previous results:
```
A → {B if success, C if failure}
```

## Subtask Design Principles

1. **Single Responsibility** - Each subtask has one clear purpose
2. **Clear Interface** - Defined input/output for each subtask
3. **Independent** - Minimize coupling between subtasks
4. **Appropriate Size** - Not too small (overhead) or large (hard to track)

## Example

Main Task: "Add user authentication"
- Subtask 1: Design auth architecture
- Subtask 2: Implement user model
- Subtask 3: Create login view
- Subtask 4: Create register view
- Subtask 5: Add token generation
- Subtask 6: Write auth tests