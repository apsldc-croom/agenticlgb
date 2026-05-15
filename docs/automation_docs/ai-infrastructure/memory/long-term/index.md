# Long-Term Memory

Persistent knowledge storage for project information.

## Purpose

- Project architecture
- Coding standards
- Team conventions
- Past decisions

## Storage

- Vector database for semantic search
- Structured storage for facts

## Data Types

```python
long_term_memory = {
    "architecture": {
        "backend": "Django REST Framework",
        "database": "PostgreSQL",
        "cache": "Redis"
    },
    "standards": {
        "naming": "snake_case",
        "testing": "pytest",
        "linting": "ruff"
    },
    "team": {
        "reviewer": "required",
        "commits": "conventional"
    }
}
```

## Retrieval

Search by semantic similarity:
```python
def retrieve_project_context(query):
    results = vector_db.search(query, top_k=5)
    return combine_results(results)
```