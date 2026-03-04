# PodManager Class Design

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│              PodManager                                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  PUBLIC INTERFACE                                       │
│  ┌───────────────────────────────────────────────────┐ │
│  │ create_pod(name, gpu_type_id, image_name, ...)   │ │
│  │   → Blocks until RUNNING                          │ │
│  │   → Adds to _pods_created                         │ │
│  │   → Returns Pod                                   │ │
│  │                                                   │ │
│  │ list_pods() -> List[Pod]                          │ │
│  │   → Returns _pods_created.values()               │ │
│  │                                                   │ │
│  │ terminate_pod(pod_id: str) -> bool                │ │
│  │   → Removes from _pods_created                    │ │
│  │   → Returns success status                        │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  INTERNAL STATE                                         │
│  ├─ api_key: str                                        │
│  └─ _pods_created: Dict[str, Pod]                      │
│                                                         │
│  INTERNAL METHODS                                       │
│  ├─ _wait_for_pod_ready(pod_id, poll, timeout)        │
│  │   └─ Polls until RUNNING or terminal state        │
│  │                                                    │
│  ├─ _get_pod_from_api(pod_id)                         │
│  │   └─ Fetches current pod state from API           │
│  │                                                    │
│  └─ _pod_dict_to_dataclass(pod_dict)                 │
│      └─ Converts API response to Pod                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Pod Dataclass Structure

```python
@dataclass
class Pod:
    id: str                                    # Pod UUID
    name: str                                  # User-provided name
    status: str                                # desiredStatus (RUNNING, etc.)
    gpu_count: int                             # Number of GPUs
    gpu_type: str                              # GPU model (e.g., "NVIDIA A40")
    image_name: str                            # Docker image URI
    created_at: Optional[datetime] = None      # When pod was created
    uptime_seconds: int = 0                    # Runtime duration
    container_disk_gb: Optional[int] = None    # Container disk size
    volume_gb: Optional[int] = None            # Volume size
    volume_mount_path: Optional[str] = None    # Volume mount location
    ports: Optional[list[str]] = None          # Exposed ports
    env_vars: dict[str, str] = ...             # Environment variables
    runtime_info: Optional[dict] = None        # Full runtime object
    raw_data: dict = ...                       # Complete API response
```

## Flow Diagrams

### create_pod() Flow

```
┌──────────────────┐
│  caller invokes  │
│  create_pod()    │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────┐
│ 1. Call RunPod API to create     │
│    Returns pod in CREATING state │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│ 2. Poll pod status in loop       │
│    _wait_for_pod_ready()         │
│    (internal)                    │
└────────┬─────────────────────────┘
         │
    ┌────┴────┐
    │          │
    ▼          ▼
  RUNNING  FAILED/
  state    TIMEOUT
    │          │
    ▼          ▼
  Success   Raise
    │       Exception
    │          │
    ▼          ▼
┌──────────────────────────────────┐
│ 3. Add to _pods_created registry │
│    (only if success)             │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│ 4. Convert to Pod dataclass      │
│    _pod_dict_to_dataclass()      │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────┐
│ Return Pod to    │
│ caller           │
└──────────────────┘
```

### terminate_pod() Flow

```
┌──────────────────┐
│ caller invokes   │
│ terminate_pod()  │
└────────┬─────────┘
         │
         ▼
┌────────────────────────────────────┐
│ 1. Call RunPod API to terminate    │
└────────┬───────────────────────────┘
         │
    ┌────┴────┐
    │          │
    ▼          ▼
 SUCCESS   ERROR
    │          │
    ▼          ▼
┌──────────────────────────────────┐
│ 2. If success: remove from       │
│    _pods_created registry        │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────┐
│ Return success   │
│ or raise error   │
└──────────────────┘
```

## Error Handling Strategy

### Custom Exceptions (reused from existing code)

```python
class PodNotFoundError(Exception):
    """Pod does not exist in RunPod account."""

class PodTimeoutError(Exception):
    """Pod did not reach RUNNING within timeout period."""

class PodFailedError(Exception):
    """Pod entered a failed terminal state."""
```

### Exception Flow

| Scenario | Exception Raised | Recovery |
|----------|-----------------|----------|
| Invalid API key | `ValueError` | Caller must provide valid key |
| Pod not found | `PodNotFoundError` | Pod may have been terminated externally |
| Timeout waiting | `PodTimeoutError` | Caller can retry with longer timeout |
| Pod enters FAILED state | `PodFailedError` | Pod is unrecoverable, termination cleaned up |
| API network error | Generic `Exception` | Caller should implement retry logic |

## Field Mapping: API Response → Pod Dataclass

| API Response Field | Pod Field | Notes |
|--------------------|-----------|-------|
| `id` | `id` | Direct mapping |
| `name` | `name` | Direct mapping |
| `desiredStatus` | `status` | Renamed for clarity |
| `gpuCount` | `gpu_count` | Snake case conversion |
| `gpuTypeId` | `gpu_type` | Renamed, shorter |
| `imageName` | `image_name` | Snake case conversion |
| `containerDiskInGb` | `container_disk_gb` | Snake case conversion |
| `volumeInGb` | `volume_gb` | Renamed, shorter |
| `volumeMountPath` | `volume_mount_path` | Snake case conversion |
| `ports` | `ports` | Direct mapping, may need parsing |
| `env` | `env_vars` | Renamed for clarity |
| `runtime.uptimeInSeconds` | `uptime_seconds` | Extracted from nested object |
| `runtime` | `runtime_info` | Full runtime object |
| Full response | `raw_data` | Store entire API response as backup |

## Implementation Notes

### Initialization
- API key is required (caller must provide)
- No defaults loaded from `.env` (caller's responsibility)
- Registry starts empty

### create_pod() Parameters
- All parameters passed directly to RunPod API
- `poll_interval` and `timeout` control wait behavior (both configurable)
- Sane defaults: poll every 5s, timeout after 10 minutes

### list_pods() Behavior
- Returns pods created by **this instance only**
- Does not fetch from RunPod API (reads internal registry)
- Returns empty list if no pods created yet

### terminate_pod() Behavior
- Only terminates pods in the internal registry
- Cannot terminate pods created by other instances
- Removes pod from registry on success
- Raises `PodNotFoundError` if pod_id not in registry

## File Organization

```
src/runpod_pods_demo/
├── __init__.py
├── pod_manager.py          # NEW: PodManager class + Pod dataclass
├── exceptions.py           # NEW: Custom exceptions (or move existing ones here)
├── create_pod.py           # EXISTING: Keep for backwards compatibility
├── terminate_pod.py        # EXISTING: Keep for backwards compatibility
├── list_pods.py            # EXISTING: Keep for backwards compatibility
└── wait_for_pod.py         # EXISTING: Keep for backwards compatibility
```

### Refactoring Strategy
1. Extract custom exceptions to `exceptions.py`
2. Create new `pod_manager.py` with `Pod` and `PodManager`
3. Keep old modules for backwards compatibility
4. Update `__init__.py` to export new classes
5. Old functions can optionally use PodManager internally
