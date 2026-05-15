# Concurrency

## Concurrency Models

### Thread-Based
Use threads for I/O-bound tasks.

### Async/Await
Use async for I/O-heavy operations.

### Process-Based
Use processes for CPU-intensive tasks.

## Parallel Execution

```python
async def execute_parallel(tasks):
    results = await asyncio.gather(*[execute_async(t) for t in tasks])
    return results

def execute_parallel_threads(tasks):
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(execute, t) for t in tasks]
        return [f.result() for f in futures]
```

## Race Conditions

### Problem
Multiple agents accessing shared state simultaneously.

### Solutions

#### Locking
```python
lock = Lock()
with lock:
    shared_state += 1
```

#### Atomic Operations
```python
counter.increment()  # Thread-safe
```

#### Immutable Data
Pass copies instead of references.

## Coordination

- **Barriers**: Wait for all tasks to complete
- **Semaphores**: Limit concurrent access
- **Channels**: Pass messages between tasks