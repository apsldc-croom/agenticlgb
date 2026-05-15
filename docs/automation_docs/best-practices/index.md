# Best Practices

General strategies for using LLMs efficiently across any provider.

## Quick Reference

| Category | Best Practice |
|----------|---------------|
| Prompt Optimization | Keep prompts short, compress code, split files |
| Output Optimization | Set max_tokens, use stop sequences, control temperature |
| Context Management | Use prompt caching, RAG, summarize history |
| Model Selection | Choose model based on reasoning need, not "best available" |
| Provider Selection | Use speed-first providers for latency, hosted APIs for flexibility |
| Monitoring | Track token usage and costs |
| Streaming | Use streaming for faster UX and early stopping |
| Cost Optimization | Use hybrid routing, difficulty escalation, smaller models |

## Key Mindset

> **"How intelligent does this task actually need?"**  
> NOT: "What is the best model available?"

This single mindset saves the most money.

## Biggest Savings

1. **Hybrid routing** - Use different models for different tasks
2. **Difficulty escalation** - Try cheap first, escalate if needed
3. **RAG** - Retrieve only relevant context
4. **Prompt caching** - Reuse repeated prompts
5. **Smaller context** - Send only what's needed
6. **Using smaller models** - Haiku/MiniMax/Qwen for simple tasks
7. **Avoiding unnecessary reasoning** - Skip thinking prompts

These practices can reduce costs by **50–90%** in production.