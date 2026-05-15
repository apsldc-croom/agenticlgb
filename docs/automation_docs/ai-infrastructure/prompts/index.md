# Prompts Folder

Core AI logic storage.

## Structure
```
prompts/
├── system/        # System prompts
├── tasks/         # Task-specific prompts
├── agents/        # Agent prompts
├── evaluators/    # Evaluation prompts
├── templates/     # Prompt templates
└── workflows/     # Workflow prompts
```

## Naming Convention

Use: `<domain>-<task>-<version>.md`

Example:
- `django-api-generator-v3.md`
- `security-review-v2.md`

## Key Principle

Store WHY the prompt exists, not just the prompt itself.

Example:
```md
# Purpose
Generate scalable DRF viewsets.

# Failure Cases
- overengineers serializers
- adds unnecessary abstractions

# Best Models
- Claude Sonnet
- GPT-5

# Notes
Use low temperature.
```