# RAG Strategy

Retrieval-Augmented Generation approach.

## RAG Pipeline

```
Query → Retrieve → Augment → Generate → Output
```

## Implementation

```python
class RAGSystem:
    def __init__(self, vector_db, llm):
        self.vector_db = vector_db
        self.llm = llm
    
    def query(self, user_query, context_window=5):
        # Retrieve
        relevant_docs = self.retrieve(user_query, context_window)
        
        # Augment
        augmented_prompt = self.augment(
            user_query,
            relevant_docs
        )
        
        # Generate
        response = self.llm.generate(augmented_prompt)
        
        return response
    
    def retrieve(self, query, top_k):
        embedding = self.embed(query)
        results = self.vector_db.search(embedding, top_k)
        return results
```

## Best Practices

- Chunk size: 512-1024 tokens
- Top K: 3-10 depending on context limit
- Re-rank results for quality
- Cache frequently queried items