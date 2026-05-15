# Semantic Memory

Structured facts and knowledge.

## Purpose

- Store facts about project
- Encode rules and constraints
- Knowledge graph

## Structure

```python
semantic_memory = {
    "facts": [
        {"subject": "project", "predicate": "uses", "object": "Django"},
        {"subject": "API", "predicate": "returns", "object": "JSON"},
        {"subject": "auth", "predicate": "uses", "object": "JWT"}
    ],
    "rules": [
        "all endpoints require authentication",
        "responses must include request_id",
        "errors must follow RFC 7807"
    ],
    "constraints": {
        "max_response_time": "200ms",
        "max_file_size": "10MB"
    }
}
```

## Querying

```python
def query_knowledge(subject, predicate):
    return semantic_graph.query(subject, predicate)
```