# Communication

## Communication Patterns

### Request-Response
```
Agent A → [Request] → Agent B → [Response] → Agent A
```

### Publish-Subscribe
```
Agent A → [Message] → Message Broker
                        ↓
                   Agent B, Agent C
```

### Broadcast
```
Agent A → [Broadcast] → Agent B, C, D
```

## Message Types

| Type | Purpose |
|------|---------|
| task | Assign work |
| result | Return output |
| query | Ask question |
| inform | Notify of event |
| error | Report problem |

## Message Format

```python
@dataclass
class AgentMessage:
    id: str
    sender: str
    receiver: str
    type: MessageType
    payload: dict
    timestamp: datetime
    correlation_id: str  # For tracking
```

## Implementation

```python
class AgentCommunication:
    def send(self, message):
        self.message_bus.publish(
            topic=message.receiver,
            message=message
        )
    
    def receive(self, agent_id):
        return self.message_bus.subscribe(agent_id)
```