# Sandboxing

Isolating AI execution.

## Sandboxing Methods

| Method | Isolation | Performance |
|--------|-----------|-------------|
| Container | High | Good |
| VM | Very High | Slow |
| Process | Medium | Fast |
| Browser | Medium | Good |

## Container-Based

```python
import docker

def create_sandbox():
    container = docker.client.containers.run(
        "python-sandbox",
        detach=True,
        mem_limit="512m",
        cpu_period=100000,
        network_disabled=True,
        volumes={"/workspace": "/workspace"}
    )
    return container
```

## Restrictions

```yaml
sandbox:
  network: disabled
  filesystem:
    allowed:
      - /workspace
      - /tmp
    denied:
      - /etc
      - /root
  resources:
    memory: 512mb
    cpu: 1 core
    time: 300 seconds
```