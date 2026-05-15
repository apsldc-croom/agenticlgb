# Agent Pools

Managing groups of agents for parallel work.

## What is an Agent Pool

A pool is a collection of agent instances that can be assigned tasks dynamically.

## Pool Types

### Static Pool
Fixed number of agents, always available:
```python
class StaticPool:
    def __init__(self, agent_class, size=4):
        self.agents = [agent_class() for _ in range(size)]
        self.available = deque(self.agents)
    
    async def get_agent(self):
        while not self.available:
            await asyncio.sleep(0.1)
        return self.available.popleft()
    
    def release(self, agent):
        self.available.append(agent)
```

### Dynamic Pool
Scales based on demand:
```python
class DynamicPool:
    def __init__(self, agent_class, min_size=1, max_size=10):
        self.agent_class = agent_class
        self.min_size = min_size
        self.max_size = max_size
        self.agents = []
    
    async def get_agent(self):
        # Scale up if needed
        if not self.agents and len(self.agents) < self.max_size:
            self.agents.append(self.agent_class())
        
        return self.agents.pop()
```

## Pool Management

### Task Assignment

```python
class PoolManager:
    def __init__(self, pool):
        self.pool = pool
        self.queue = asyncio.Queue()
    
    async def submit(self, task):
        agent = await self.pool.get_agent()
        try:
            result = await agent.execute(task)
        finally:
            self.pool.release(agent)
        return result
```

### Load Balancing

```python
class LoadBalancer:
    def __init__(self, pools):
        self.pools = pools
    
    async def assign(self, task):
        # Send to least loaded pool
        least_loaded = min(self.pools, key=lambda p: p负载)
        return await least_loaded.submit(task)
```

## Specialized Pools

### Coding Pool
```python
coding_pool = AgentPool(
    agent_class=CodingAgent,
    size=4,
    specialized_for=["coding", "refactoring"]
)
```

### Review Pool
```python
review_pool = AgentPool(
    agent_class=ReviewerAgent,
    size=2,
    specialized_for=["code_review", "security"]
)
```

## Pool Metrics

| Metric | Description |
|--------|-------------|
| Utilization | % of agents busy |
| Queue Length | Waiting tasks |
| Wait Time | Time to get agent |
| Throughput | Tasks/minute |

```python
def get_pool_metrics(pool):
    return {
        "total_agents": pool.size,
        "busy": pool.size - len(pool.available),
        "utilization": (pool.size - len(pool.available)) / pool.size,
        "queue_length": pool.queue.qsize()
    }
```

## Auto-Scaling

```python
class AutoScalingPool:
    def __init__(self):
        self.scale_up_threshold = 0.8
        self.scale_down_threshold = 0.2
    
    async def maybe_scale(self, metrics):
        if metrics.utilization > self.scale_up_threshold:
            await self.scale_up()
        elif metrics.utilization < self.scale_down_threshold:
            await self.scale_down()
```