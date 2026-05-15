# Chunking

Splitting text for embedding.

## Strategies

### Fixed Size
```python
def chunk_fixed(text, chunk_size=500, overlap=50):
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i+chunk_size])
    return chunks
```

### By Paragraph
```python
def chunk_paragraphs(text):
    paragraphs = text.split("\n\n")
    return [p for p in paragraphs if p.strip()]
```

### Semantic
```python
def chunk_semantic(text):
    # Use LLM to identify logical sections
    prompt = f"Split this into logical sections:\n{text}"
    sections = llm.generate(prompt)
    return sections
```

## Best Practices

- Chunk size: 256-1024 tokens
- Include context in each chunk
- Overlap between chunks (10-20%)
- Consider structure (functions, classes)