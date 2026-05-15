# Memory Retrieval

How to retrieve relevant context.

## Retrieval Strategies

### Semantic Search
Vector similarity:
```python
def semantic_retrieve(query, memory, top_k=5):
    query_embedding = embed(query)
    results = memory.search(query_embedding, top_k)
    return results
```

### Keyword Search
BM25 or similar:
```python
def keyword_retrieve(query, memory, top_k=5):
    results = memory.bm25.search(query, top_k)
    return results
```

### Hybrid
Combine both:
```python
def hybrid_retrieve(query, memory):
    semantic = semantic_retrieve(query, memory)
    keyword = keyword_retrieve(query, memory)
    return combine(semantic, keyword)
```

## Ranking

Score and rank results:
```python
def rank_results(results, query):
    for result in results:
        result.score = (
            0.7 * semantic_score +
            0.3 * keyword_score
        )
    return sorted(results, key=lambda r: r.score, reverse=True)
```