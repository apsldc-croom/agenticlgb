# AI Infrastructure

Organized system for building scalable AI projects.

## Why This Matters

Without structure:
- Prompts duplicate
- Behavior becomes inconsistent
- Objectives drift
- Debugging becomes impossible
- Models behave differently unexpectedly
- Token costs explode

## Core Principle

Store **behavioral components**, not chat history.

## Structure

| Folder | Purpose |
|--------|---------|
| [prompts](./prompts/) | Core AI logic |
| [outputs](./outputs/) | Responses, logs, artifacts |
| [evaluations](./evaluations/) | Scores, benchmarks |
| [memory](./memory/) | Long-term context |
| [orchestration](./orchestration/) | Workflow controllers |
| [configs](./configs/) | Model routing, settings |
| [routing](./routing/) | Multi-model routing logic |
| [governance](./governance/) | Safety rules, constraints |
| [lifecycle](./lifecycle/) | Prompt creation to deprecation |

## Key Principle

Do NOT tightly couple:
- prompts
- models
- workflows

Keep them modular:
- Same prompt → different models
- Same model → different workflows