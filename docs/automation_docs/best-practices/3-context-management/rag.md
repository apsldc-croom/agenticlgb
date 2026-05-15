# Use RAG Instead of Full Context

For large apps/docs:
- Store embeddings
- Retrieve only relevant chunks
- Send only top relevant context

## Good Stack
- Pinecone
- Weaviate
- Chroma
- FAISS
- Qdrant

## How RAG Works
1. Index documents into vector database
2. On query, retrieve top K similar chunks
3. Send only relevant chunks to API

## Benefits
- Massive token reduction
- Better answer quality
- Scalable to large knowledge bases

## Example
Instead of sending 10,000 line codebase, send only 5 relevant chunks (~500 tokens).