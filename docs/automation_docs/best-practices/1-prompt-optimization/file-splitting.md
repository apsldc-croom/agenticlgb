# Split Huge Files into Chunks

## Instead of
```text
Upload entire 2 MB codebase
```

## Do
- Send only relevant files
- Chunk documents
- Retrieve relevant context dynamically (RAG)

## Benefits
- Massively reduces input tokens
- Faster API response times
- Lower costs

## Example
Instead of sending a 10,000 line file, send only the 50 relevant lines related to the issue.