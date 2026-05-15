# Parallel Execution

Running tasks concurrently for speed.

## Why Parallel Execution

| Sequential | Parallel |
|------------|----------|
| 4 tasks × 10s = 40s | 10s (all at once) |
| Simple to debug | More complex |
| Predictable | Resource management needed |

## Types of Parallelism

### 1. Task Parallelism
Different agents do different things simultaneously:

```
Agent A: Generate code    ─┐
Agent B: Write tests      ─┼─► All at once
Agent C: Update docs      ─┘
```

### 2. Data Parallelism
Same agent works on different data:

```
Coder Agent
    ├─► File 1
    ├─► File 2
    └─► File 3
```

### 3. Pipeline Parallelism
Staggered parallel execution:

```
Stage 1: [A1][A2][A3]
           └─► [B1][B2][B3]
                    └─► [C1][C2][C3]
```

## Implementation

### Async Execution
```python
import asyncio

async def execute_parallel(tasks):
    # Create tasks
    coroutines = [execute_task(t) for t in tasks]
    
    # Run all concurrently
    results = await asyncio.gather(*coroutines, return_exceptions=True)
    
    return results
```

### With Rate Limiting
```python
import asyncio
from asyncio import Semaphore

async def execute_parallel_limited(tasks, max_concurrent=3):
    semaphore = Semaphore(max_concurrent)
    
    async def bounded_task(task):
        async with semaphore:
            return await execute_task(task)
    
    return await asyncio.gather(*[bounded_task(t) for t in tasks])
```

## Parallel Execution Patterns

### Map-Reduce Pattern

```python
async def map_reduce(items, map_fn, reduce_fn):
    # Map phase - parallel
    mapped = await asyncio.gather(*[map_fn(item) for item in items])
    
    # Reduce phase - combine
    result = reduce_fn(mapped)
    return result

# Example
results = await map_reduce(
    files,
    lambda f: analyze_file(f),
    lambda r: combine_results(r)
)
```

### Fan-Out-Fan-In

```python
async def fan_out_fan_in(task):
    # Fan out - spawn subtasks
    subtasks = [SubTask(id=i) for i in range(4)]
    
    # Execute in parallel
    futures = [execute(subtask) for subtask in subtasks]
    
    # Fan in - collect results
    results = await asyncio.gather(*futures)
    
    return combine(results)
```

## Parallel Safety

### Race Conditions

```python
# BAD - Race condition
shared_state += 1  # Multiple threads reading/writing

# GOOD - Use lock
async with lock:
    shared_state += 1
```

### Deadlocks

```python
# Avoid - Circular wait
# Agent A has lock 1, waits for lock 2
# Agent B has lock 2, waits for lock 1

# Solution - Always acquire locks in same order
```

## Performance Tuning

### Concurrency Level

```python
# Too high = resource exhaustion
# Too low = slow execution
optimal = min(
    available_cpu_cores * 4,  # I/O bound
    len(tasks)
)
```

### Batch Size

```python
# Process in batches to manage memory
async def process_large_dataset(items):
    batch_size = 100
    for i in range(0, len(items), batch_size):
        batch = items[i:i+batch_size]
        await process_batch(batch)
```

## Monitoring Parallel Execution

```python
async def execute_with_monitoring(tasks):
    start = time.time()
    
    results = await asyncio.gather(
        *tasks,
        return_exceptions=True
    )
    
    duration = time.time() - start
    success = sum(1 for r in results if not isinstance(r, Exception))
    
    return {
        "total": len(tasks),
        "success": success,
        "failed": len(tasks) - success,
        "duration": duration
    }
```