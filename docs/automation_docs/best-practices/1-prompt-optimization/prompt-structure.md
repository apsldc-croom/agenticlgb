# Keep Prompts Short but Structured

## Bad
```text
Please carefully analyze this code in deep detail and think step by step...
```

## Better
```text
Analyze bug cause in this code. Return concise fix only.
```

## Tips

- Remove filler words
- Avoid repeated instructions
- Use bullet points
- Use templates

## Example Efficient Prompt

Instead of:
```text
Please analyze this entire Django project thoroughly and explain everything in detail...
```

Use:
```text
Task:
Fix JWT refresh issue.

Context:
- Django REST Framework
- SimpleJWT
- Refresh token expires immediately

Code:
[paste relevant code]

Return:
1. Cause
2. Minimal fix
3. Updated code only
```

## General Principle
Less context = less tokens = lower cost + faster response.