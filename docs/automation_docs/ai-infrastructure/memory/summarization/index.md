# Summarization

Strategies for compressing context.

## Methods

### Extractive
Extract key sentences/phrases:
```python
def extractive_summarize(text):
    # Score sentences by importance
    scores = score_sentences(text)
    # Select top sentences
    return select_top(scores, ratio=0.3)
```

### Abstractive
Generate new summary:
```python
def abstractive_summarize(text):
    prompt = f"Summarize this conversation concisely:\n{text}"
    return llm.generate(prompt)
```

### Hybrid
Combine both approaches.

## When to Summarize

- Token count exceeds threshold (e.g., 8000)
- After N messages (e.g., 10)
- Before complex task
- End of session

## Summary Format

```python
conversation_summary = {
    "overview": "User working on Django auth",
    "decisions": ["Use JWT", "Add refresh tokens"],
    "remaining": "Fix token expiry issue",
    "key_files": ["auth/views.py", "auth/models.py"]
}
```