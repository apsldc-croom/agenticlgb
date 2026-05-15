# Context Window Matters

Large context models useful for:
- Long codebases
- RAG systems
- Large documents
- Full repositories

## But Larger Context =:
- Higher costs
- Increased latency

## Best Practice
- Retrieve only relevant chunks
- Avoid dumping entire projects
- Use 128K context only when truly needed

## Common Mistake
Sending entire codebase when only 50 lines are relevant.