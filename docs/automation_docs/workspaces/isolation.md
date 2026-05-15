# Isolation

Resource and process isolation.

## Isolation Levels

### Process Isolation
```python
import subprocess

def run_isolated(command):
    proc = subprocess.run(
        command,
        cwd="/workspace",
        env={**safe_env, "PATH": "/bin"},
        timeout=60,
        capture_output=True
    )
    return proc
```

### Filesystem Isolation
- Separate directories per task
- No access to host filesystem
- Temporary file cleanup

### Network Isolation
- Block outbound network
- Allow only specific endpoints
- Log all connection attempts

## Implementation

```python
class IsolatedWorkspace:
    def __init__(self, task_id):
        self.path = f"/workspaces/{task_id}"
        self._setup_isolation()
    
    def _setup_isolation(self):
        os.makedirs(self.path, mode=0o700)
        os.chroot(self.path)  # If running as root
```