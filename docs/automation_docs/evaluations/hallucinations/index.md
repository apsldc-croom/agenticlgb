# Hallucinations

Hallucination detection and prevention.

## What are Hallucinations

Incorrect or fabricated information presented as fact.

## Detection Methods

### Factual Check
```python
def check_factual(response, known_facts):
    claims = extract_claims(response)
    for claim in claims:
        if not matches_fact(claim, known_facts):
            yield hallucination(claim)
```

### Cross-Reference
```python
def check_cross_ref(response, context):
    for statement in response:
        if not supported_by(statement, context):
            yield hallucination(statement)
```

### Confidence Scoring
```python
def score_confidence(response):
    for segment in response:
        if contains_uncertainty(segment):
            segment.confidence = low
        elif is_factual(segment):
            segment.confidence = high
```

## Prevention Strategies

- Provide sufficient context
- Ask for citations
- Use chain-of-thought
- Validate key claims