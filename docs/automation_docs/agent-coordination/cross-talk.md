# Cross-Talk

Direct agent-to-agent communication.

## What is Cross-Talk

Cross-talk is when agents communicate directly with each other, not just through a central coordinator.

## Types of Cross-Talk

### 1. Request-Response
```
Agent A ──► "Need your output" ──► Agent B
                                      │
Agent A ◄── "Here it is" ◄───────────┘
```

### 2. Broadcast
```
Agent A ──► "I found something" ──► All Agents
                                  (subscribe)
```

### 3. Pub-Sub
```
Agent A (publisher)
    │
    ▼
Message Broker
    │
    ▼ (filtered)
Agent B, Agent D (subscribers)
```

## When Cross-Talk Happens

| Scenario | Communication |
|----------|---------------|
| Coder needs context from Planner | Request-Response |
| Found bug affects others | Broadcast |
| Result needed by multiple | Pub-Sub |

## Implementation

### Direct Communication
```python
class Agent:
    async def ask_other(self, other_agent, question):
        response = await other_agent.process(question)
        return response
```

### Via Message Bus
```python
class MessageBus:
    async def send_to(self, receiver, message):
        await self.queue.put((receiver, message))
    
    async def subscribe(self, agent, topic):
        self.subscriptions[topic].append(agent)
    
    async def publish(self, topic, message):
        for agent in self.subscriptions[topic]:
            await agent.receive(message)
```

## Cross-Talk Patterns

### Help Request
```python
async def coder_needs_help(coder, context):
    # Ask architect for design guidance
    response = await architect.answer(
        question=f"How should I implement {context.feature}?",
        context=coder.context
    )
    return response
```

### Status Update
```python
async def report_progress(reporter, topic, status):
    await message_bus.publish(
        topic=f"task.{task_id}.status",
        message={"agent": reporter.id, "status": status}
    )
```

## Coordination via Cross-Talk

```
┌────────┐         ┌────────┐
│ Coder  │◄───────►│Reviewer│
└────────┘   cross  └────────┘
    │         talk
    ▼
┌────────┐
│ Tester │ (subscribes to code changes)
└────────┘
```

## Benefits

- **Decentralized** - No single point of failure
- **Fast** - Direct communication
- **Flexible** - Agents can discover each other

## Risks

- **Complexity** - Harder to track
- **Race conditions** - Need synchronization
- **Coupling** - Agents depend on each other

## Best Practices

1. Use message bus for loose coupling
2. Set timeouts for cross-talk
3. Log all cross-talk for debugging
4. Limit cross-talk depth (A→B→C)