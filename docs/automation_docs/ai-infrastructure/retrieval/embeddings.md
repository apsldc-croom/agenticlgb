# Embeddings

Text vectorization for similarity search.

## Embedding Models

| Model | Dimensions | Use Case |
|-------|------------|----------|
| text-embedding-3-small | 1536 | General |
| text-embedding-3-large | 3072 | High precision |
| sentence-transformers | 768 | Local/small |

## Generating Embeddings

```python
def embed_text(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding
```

## Batching

```python
def embed_batch(texts, batch_size=100):
    embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=batch
        )
        embeddings.extend([d.embedding for d in response.data])
    return embeddings
```