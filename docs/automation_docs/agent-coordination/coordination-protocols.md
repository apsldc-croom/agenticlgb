# Coordination Protocols

## Standard Protocols

### Request-Acknowledge
```
Agent A: [Request]
Agent B: [Acknowledge]
Agent A: [Task]
Agent B: [Complete] → Agent A: [Acknowledge]
```

### Bidding
```
Coordinator: [Broadcast task]
Agent A: [Bid: can do in 5 min]
Agent B: [Bid: can do in 3 min]
Coordinator: [Award to B]
```

### Contract Net
```
Initiator: [Announce task]
Participants: [Propose]
Initiator: [Select and award]
Participant: [Execute and report]
```

## Protocol Selection

| Scenario | Protocol |
|----------|----------|
| Clear task assignment | Request-Acknowledge |
| Multiple capable agents | Bidding |
| Complex negotiation | Contract Net |
| Parallel work | Barrier |

## Custom Protocols

Define custom protocols for specific needs:

```python
@protocol("code_review")
def code_review_protocol(initiator, code):
    reviewer = select_reviewer(code)
    review = reviewer.review(code)
    return review
```