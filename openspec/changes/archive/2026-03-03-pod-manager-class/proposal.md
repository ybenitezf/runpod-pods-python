# Pod Manager Class Refactor

## Summary

Refactor scattered pod management functions (`create_pod`, `list_pods`, `terminate_pod`, `wait_for_pod_ready`) into a cohesive `PodManager` class with an internal registry. This provides a clean, reusable module interface for programmatically managing RunPod pods.

## Problem

Current implementation splits pod operations across multiple standalone functions:
- `create_pod.py` - pod creation
- `terminate_pod.py` - pod termination
- `wait_for_pod.py` - wait for pod ready
- `list_pods.py` - list pods
- `main.py` - orchestrates the workflow

This is difficult to:
- Use as a reusable library (must import and call multiple functions)
- Track state (no central place for "pods created by my app")
- Extend (adding features requires modifying multiple files)

## Proposed Solution

Create a `PodManager` class that:
1. **Centralizes pod operations** - single interface for create, list, terminate
2. **Manages pod lifecycle** - `create_pod()` blocks until pod is RUNNING
3. **Tracks created pods** - in-memory registry of pods created by this instance
4. **Uses Pod dataclass** - structured representation instead of raw dicts
5. **Encapsulates complexity** - waiting, polling, error handling are internal

## Design

### Pod Dataclass

```python
@dataclass
class Pod:
    """Represents a RunPod pod with essential information."""
    id: str
    name: str
    status: str                           # desiredStatus from API
    gpu_count: int
    gpu_type: str
    image_name: str
    created_at: Optional[datetime] = None
    uptime_seconds: int = 0
    container_disk_gb: Optional[int] = None
    volume_gb: Optional[int] = None
    volume_mount_path: Optional[str] = None
    ports: Optional[list[str]] = None
    env_vars: dict[str, str] = field(default_factory=dict)
    runtime_info: Optional[dict] = None
    raw_data: dict = field(default_factory=dict)  # Full API response
```

### PodManager Class

```python
class PodManager:
    """Manages RunPod pods: create, list, and terminate."""
    
    def __init__(self, api_key: str):
        """Initialize with API key. Caller must provide credentials."""
        self.api_key = api_key
        self._pods_created: dict[str, Pod] = {}  # Internal registry
    
    def create_pod(
        self,
        name: str,
        gpu_type_id: str,
        image_name: str,
        gpu_count: int = 1,
        container_disk_in_gb: Optional[int] = None,
        volume_in_gb: Optional[int] = None,
        volume_mount_path: Optional[str] = None,
        ports: Optional[str] = None,
        env: Optional[dict[str, str]] = None,
        poll_interval: int = 5,
        timeout: int = 600,
    ) -> Pod:
        """
        Create a pod and wait for it to reach RUNNING state.
        
        Returns only when pod is ready. Adds pod to internal registry.
        
        Raises:
            ValueError: If API key not configured or invalid parameters
            PodCreationError: If pod creation fails
            PodTimeoutError: If pod doesn't reach RUNNING within timeout
            PodFailedError: If pod enters failed state
        """
    
    def list_pods(self) -> list[Pod]:
        """List pods created by this PodManager instance."""
        return list(self._pods_created.values())
    
    def terminate_pod(self, pod_id: str) -> bool:
        """
        Terminate a pod and remove from registry.
        
        Raises:
            PodNotFoundError: If pod not found
            Exception: If termination fails
        """
    
    # Internal methods (private)
    def _wait_for_pod_ready(
        self,
        pod_id: str,
        poll_interval: int,
        timeout: int,
    ) -> dict[str, Any]:
        """Poll pod status until RUNNING or error. Returns raw API response."""
    
    def _get_pod_from_api(self, pod_id: str) -> dict[str, Any]:
        """Fetch pod details from RunPod API."""
    
    def _pod_dict_to_dataclass(self, pod_dict: dict[str, Any]) -> Pod:
        """Convert API response dict to Pod dataclass."""
```

## Implementation Details

### Registry Behavior
- Simple in-memory dict: `pod_id -> Pod`
- Populated only on successful `create_pod()` (after pod reaches RUNNING)
- `list_pods()` returns pods from this registry only
- No persistence across runs (v1 constraint)

### create_pod() Blocking Behavior
- Calls RunPod API to initiate creation
- Internally calls `_wait_for_pod_ready()` (existing logic)
- Blocks until pod reaches RUNNING state
- Adds to registry before returning
- On timeout or failure, removes from registry and raises exception

### Error Handling
- Reuse existing custom exceptions: `PodNotFoundError`, `PodTimeoutError`, `PodFailedError`
- Keep error messages clear and actionable
- Don't catch/suppress errors—let caller decide

### Pod Dataclass Mapping
- Extract known fields from RunPod API response
- Map confusing names: `desiredStatus` → `status`
- Store `raw_data` as fallback for unknown fields
- Calculate `uptime_seconds` from `runtime.uptimeInSeconds`

## Benefits

✅ **Single interface** - one class, three methods  
✅ **Encapsulated state** - internal registry, no external tracking needed  
✅ **Structured data** - Pod dataclass instead of raw dicts  
✅ **Simple semantics** - `create_pod()` blocks, so no async complexity  
✅ **Reusable module** - can be imported and used in other projects  
✅ **Backwards compatible** - old functions still exist for legacy scripts  

## Future Enhancements

- Persist registry to JSON file (cross-session state)
- Add `get_pod(pod_id)` to fetch individual pod details
- Add pod status refresh: `refresh_pod_status(pod_id)`
- Add filtering to `list_pods(status=, gpu_type=, ...)`
- Support async operations if needed
