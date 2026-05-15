# Models Config

Model configurations.

## Example Configuration

```yaml
models:
  claude-sonnet:
    provider: anthropic
    max_tokens: 8000
    temperature: 0.2
    cost_per_1k_input: 0.003
    cost_per_1k_output: 0.015
  
  gpt-4:
    provider: openai
    max_tokens: 8000
    temperature: 0.2
    cost_per_1k_input: 0.01
    cost_per_1k_output: 0.03
  
  minimax:
    provider: openrouter
    max_tokens: 4000
    temperature: 0.1
    cost_per_1k_input: 0.0002
    capability: fast
```

## Model Categories

```yaml
categories:
  fast:
    - minimax
    - qwen
    - haiku
  
  balanced:
    - claude-sonnet
    - gpt-4
    - gemini-pro
  
  reasoning:
    - claude-opus
    - gpt-5
    - deepseek-r1
```