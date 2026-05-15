# Pipelines

Workflow pipeline definitions.

## Pipeline Definition

```python
class Pipeline:
    name: str
    stages: list[Stage]
    
class Stage:
    name: str
    action: callable
    on_success: str  # Next stage
    on_failure: str  # Failure handler
```

## Pipeline Types

### Sequential
```python
pipeline = Pipeline([
    Stage("validate", validate, "execute", "rollback"),
    Stage("execute", execute, "test", "rollback"),
    Stage("test", test, "deploy", "rollback"),
    Stage("deploy", deploy, "done", "rollback")
])
```

### Parallel
```python
pipeline = Pipeline([
    Stage("build", build, "merge"),
    Stage("test_unit", test_unit, "merge"),
    Stage("test_integration", test_int, "merge"),
    Stage("merge", merge, "deploy")
])
```

## Execution

```python
def execute_pipeline(pipeline, context):
    current = pipeline.stages[0]
    while current:
        result = current.action(context)
        if result.success:
            current = pipeline.get_stage(current.on_success)
        else:
            current = pipeline.get_stage(current.on_failure)
```