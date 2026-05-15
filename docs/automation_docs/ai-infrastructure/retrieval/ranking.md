# Ranking

Scoring and ordering retrieved results.

## Ranking Methods

### Similarity Score
```python
def rank_by_similarity(results):
    return sorted(results, key=lambda r: r.score, reverse=True)
```

### Reciprocal Rank Fusion
```python
def reciprocal_rank_fusion(results_lists, k=60):
    scores = {}
    for results in results_lists:
        for i, r in enumerate(results):
            scores[r.id] = scores.get(r.id, 0) + 1 / (k + i + 1)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)
```

### Learning to Rank
```python
def rerank_with_model(query, results, reranker):
    pairs = [(query, r.text) for r in results]
    scores = reranker.predict(pairs)
    for r, s in zip(results, scores):
        r.final_score = s
    return sorted(results, key=lambda r: r.final_score, reverse=True)
```

## Multi-Factor Ranking

```python
def rank_final(results, query):
    for r in results:
        r.score = (
            0.4 * r.similarity +
            0.3 * r.freshness +
            0.2 * r.relevance +
            0.1 * r.authority
        )
    return sorted(results, key=lambda r: r.score)