# Vector Storage

Vector database options.

## Options

| Database | Type | Best For |
|----------|------|----------|
| Pinecone | Managed | Production |
| Weaviate | Open source | Flexibility |
| Chroma | Local | Prototyping |
| Qdrant | Open source | Self-hosted |
| Milvus | Open source | Scale |

## Basic Operations

```python
# Store
vector_db.upsert(
    ids=["doc1", "doc2"],
    embeddings=[emb1, emb2],
    metadata=[{"text": "..."}, {"text": "..."}]
)

# Query
results = vector_db.query(
    vector=query_embedding,
    top_k=5,
    filter={"source": "code"},
    include_metadata=True
)

# Delete
vector_db.delete(ids=["doc1"])
```

## Index Types

- **HNSW**: Fast, memory-intensive
- **IVF**: Slower, memory-efficient
- **PQ**: Compression, accuracy trade-off