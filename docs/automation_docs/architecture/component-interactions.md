# Component Interactions

## Agent Communication

### Direct Delegation
One agent calls another directly for specific subtask.

### Message Queue
Agents communicate via async message passing.

### Shared Memory
Agents share context via shared memory system.

## Component Contracts

### Router → Planner
- Input: User task
- Output: Task classification (simple/complex)

### Planner → Agents
- Input: Task breakdown
- Output: Ordered subtask list

### Coder → Reviewer
- Input: Generated code
- Output: Review feedback

### Reviewer → Fixer (if needed)
- Input: Review feedback
- Output: Fixed code

## Error Propagation
- Agents report failures up the chain
- Planner handles retry logic
- Router handles escalation to higher model