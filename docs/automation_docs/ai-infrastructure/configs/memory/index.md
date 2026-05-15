# Memory Config

Memory management settings.

## Example Configuration

```yaml
memory:
  short_term:
    max_items: 100
    ttl_seconds: 3600
  
  long_term:
    enabled: true
    vector_db: pinecone
    index_name: project-memory
    embedding_model: text-embedding-3-small
  
  episodic:
    enabled: true
    retention_days: 30
  
  summarization:
    enabled: true
    trigger_tokens: 6000
    method: abstractive
```

## Retrieval Settings

```yaml
retrieval:
  default_top_k: 5
  max_context_tokens: 8000
  hybrid_search:
    enabled: true
    vector_weight: 0.7
    keyword_weight: 0.3
```