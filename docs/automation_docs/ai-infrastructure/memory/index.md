# Memory

Long-term context management.

## Overview

Memory system stores context to avoid sending full history every request.

## Sections
- [Short-Term](./short-term/) - Session context
- [Long-Term](./long-term/) - Project knowledge
- [Episodic](./episodic/) - Event sequences
- [Semantic](./semantic/) - Structured knowledge
- [Summarization](./summarization/) - Compression strategies
- [Retrieval](./retrieval/) - Memory retrieval
- [Pruning](./pruning/) - Memory cleanup
- [Lifecycle](./memory-lifecycle/) - Memory management

## Memory Types

| Type | Purpose | Retention |
|------|---------|-----------|
| Short-term | Current task context | Session |
| Long-term | Project knowledge | Until deleted |
| Episodic | Past events | Configurable |
| Semantic | Facts and rules | Permanent |