# Reduce Code/Comments Sent

Tokens count:
- comments
- whitespace
- logs
- stack traces
- markdown

## Before Sending Code
- Remove debug logs
- Remove unnecessary comments
- Send minimal reproducing code

## Example

Before:
```python
# This function calculates the total price
# It takes a list of items and returns sum
# Author: John
# Date: 2024-01-15
def calculate_total(items):  # main function
    total = 0
    for item in items:  # loop through items
        total += item['price']
    return total  # return result
```

After:
```python
def calculate_total(items):
    return sum(item['price'] for item in items)
```

## Key Point
Strip everything unnecessary before sending code to API.