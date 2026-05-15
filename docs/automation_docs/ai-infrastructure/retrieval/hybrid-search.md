# Hybrid Search

Combining multiple search methods.

## Approach

```python
def hybrid_search(query, vector_db, keyword_index):
    # Semantic search
    semantic = vector_db.search(embed(query), top_k=10)
    
    # Keyword search
    keyword = keyword_index.search(query, top_k=10)
    
    # Combine results
    combined = rrf_fusion([semantic, keyword])
    
    return combined
```

## Benefits

- Keyword: Exact matches
- Vector: Semantic similarity
- Combined: Best of both

## Implementation Options

| Tool | Vector | Keyword |
|------|--------|---------|
| Elasticsearch | ✅ | ✅ |
| Weaviate | ✅ | ✅ |
| Pinecone | ✅ | ❌ |
| Qdrant | ✅ | ✅ |