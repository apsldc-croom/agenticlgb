# Workflow Engine

## Workflow Definition

```python
class Workflow:
    name: str
    phases: list[Phase]
    transitions: dict  # phase -> next phase
    error_handlers: dict  # phase -> handler
```

## Workflow Types

### Sequential
```
Phase A → Phase B → Phase C
```

### Parallel
```
     → Phase A →
     → Phase B →  → Merge
     → Phase C →
```

### Conditional
```
Phase A → {Phase B if cond, Phase C if not}
```

## Workflow Execution

```python
class WorkflowEngine:
    def execute(self, workflow, initial_context):
        context = initial_context
        current_phase = workflow.phases[0]
        
        while current_phase:
            result = execute_phase(current_phase, context)
            
            if result.success:
                next_phase = workflow.transitions.get(current_phase)
                if next_phase:
                    current_phase = next_phase
                else:
                    break
            else:
                handler = workflow.error_handlers.get(current_phase)
                if handler:
                    context = handler(result.error, context)
                else:
                    raise WorkflowError(f"Failed at {current_phase}")
        
        return context
```

## Workflow State

- Current phase
- Phase results
- Context accumulated
- Execution history