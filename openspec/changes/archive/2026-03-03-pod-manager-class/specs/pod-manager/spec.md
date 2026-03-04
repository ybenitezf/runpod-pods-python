# PodManager Module Specification

## Overview

The PodManager module provides a class-based interface for programmatic management of RunPod pods. It encapsulates pod creation, listing, and termination with an internal registry tracking pods created by the manager instance.

---

## Pod Dataclass

### Requirement: Represent pod information in structured format

The system SHALL provide a `Pod` dataclass to represent RunPod pod data in a structured, typed manner.

#### Scenario: Pod dataclass contains essential fields
- **WHEN** a Pod is created
- **THEN** it contains: id, name, status, gpu_count, gpu_type, image_name
- **AND** it contains optional fields: created_at, uptime_seconds, container_disk_gb, volume_gb, volume_mount_path, ports, env_vars, runtime_info, raw_data

#### Scenario: Pod dataclass field mapping
- **WHEN** a Pod is created from RunPod API response
- **THEN** API field names are mapped to Pod fields (e.g., `desiredStatus` → `status`)
- **AND** snake_case conversion is applied (e.g., `gpuCount` → `gpu_count`)
- **AND** nested fields are extracted (e.g., `runtime.uptimeInSeconds` → `uptime_seconds`)

#### Scenario: Pod stores raw API response
- **WHEN** a Pod is created from RunPod API response
- **THEN** the complete API response is stored in `raw_data` field
- **AND** future enhancements can access unmapped fields via `raw_data`

---

## PodManager Class

### Requirement: Initialize with API credentials

The system SHALL initialize a PodManager instance with a RunPod API key.

#### Scenario: Successful initialization
- **WHEN** PodManager is created with valid API key
- **THEN** the instance is ready to create, list, and terminate pods

#### Scenario: Missing API key
- **WHEN** PodManager is created without API key
- **THEN** the instance initializes but creation operations will fail with appropriate error

#### Implementation Notes
- Caller must provide API key (no automatic `.env` loading in class)
- Empty in-memory registry is initialized

---

### Requirement: Create pod and block until ready

The system SHALL create a RunPod pod and return only when the pod reaches RUNNING state.

#### Scenario: Successful pod creation
- **WHEN** caller invokes `create_pod()` with valid configuration
- **THEN** the RunPod API is called to initiate creation
- **AND** the system polls pod status at regular intervals
- **AND** the function blocks until pod reaches RUNNING state
- **AND** the pod is added to internal registry
- **AND** a Pod object is returned to the caller

#### Scenario: Pod creation fails
- **WHEN** RunPod API returns an error during creation
- **THEN** an exception is raised immediately
- **AND** the pod is not added to registry

#### Scenario: Pod fails to start
- **WHEN** the pod transitions to a terminal failure state (FAILED, EXITED, etc.)
- **THEN** a `PodFailedError` is raised
- **AND** the pod is not added to registry
- **AND** caller can manually terminate if needed

#### Scenario: Pod creation times out
- **WHEN** the pod does not reach RUNNING state within the timeout period
- **THEN** a `PodTimeoutError` is raised
- **AND** the pod is not added to registry
- **AND** the pod may still be running in RunPod (caller should terminate manually)

#### Scenario: Configurable wait parameters
- **WHEN** caller invokes `create_pod(poll_interval=X, timeout=Y)`
- **THEN** the system polls every X seconds
- **AND** waits maximum Y seconds before timing out
- **AND** defaults are provided (poll_interval=5, timeout=600)

#### Implementation Notes
- `create_pod()` is a blocking, synchronous operation
- Internally calls `_wait_for_pod_ready()` (private method)
- Caller provides all pod configuration parameters (no defaults from environment)
- See pod-lifecycle spec for detailed pod readiness criteria

---

### Requirement: List pods created by manager instance

The system SHALL return a list of pods created by this PodManager instance.

#### Scenario: List with pods in registry
- **WHEN** caller invokes `list_pods()`
- **THEN** a list of Pod objects is returned
- **AND** the list contains only pods created by this instance
- **AND** the list reflects current state of internal registry

#### Scenario: List with empty registry
- **WHEN** no pods have been created by this instance
- **THEN** an empty list is returned

#### Scenario: List does not fetch from API
- **WHEN** caller invokes `list_pods()`
- **THEN** data is read from internal registry
- **AND** no RunPod API call is made
- **AND** pods are not refreshed from RunPod

#### Implementation Notes
- Simple operation: return `list(self._pods_created.values())`
- No filtering or sorting (can be added in v2)
- Only includes successfully created pods (those in registry)

---

### Requirement: Terminate pod and remove from registry

The system SHALL terminate a RunPod pod and remove it from the internal registry.

#### Scenario: Successful pod termination
- **WHEN** caller invokes `terminate_pod(pod_id)` with valid pod ID
- **THEN** the RunPod API is called to terminate the pod
- **AND** the pod is removed from internal registry
- **AND** success is returned to the caller

#### Scenario: Pod not in registry
- **WHEN** caller invokes `terminate_pod()` with pod_id not in registry
- **THEN** a `PodNotFoundError` is raised
- **AND** no API call is made
- **AND** no registry modification occurs

#### Scenario: API termination fails
- **WHEN** the RunPod API returns an error
- **THEN** an exception is raised
- **AND** the pod is not removed from registry
- **AND** caller may retry or investigate

#### Implementation Notes
- Registry-based termination: only manages pods this instance created
- Cannot terminate pods created by other instances or externally
- If pod was terminated externally, caller must call `terminate_pod()` to remove from registry

---

## Error Handling

### Custom Exceptions

```python
class PodNotFoundError(Exception):
    """Raised when pod does not exist in registry or RunPod account."""

class PodTimeoutError(Exception):
    """Raised when pod does not reach RUNNING within timeout period."""

class PodFailedError(Exception):
    """Raised when pod enters a terminal failure state."""
```

### Exception Usage

| Method | Exception | When Raised |
|--------|-----------|-------------|
| `create_pod()` | `ValueError` | API key not configured |
| `create_pod()` | `PodTimeoutError` | Pod doesn't reach RUNNING in time |
| `create_pod()` | `PodFailedError` | Pod enters failed state |
| `create_pod()` | `Exception` | API call fails |
| `list_pods()` | (none) | Always succeeds |
| `terminate_pod()` | `PodNotFoundError` | Pod not in registry |
| `terminate_pod()` | `Exception` | API call fails |

---

## Internal Implementation

### Private Methods

#### `_get_pod_from_api(pod_id: str) -> dict`
- Fetch current pod details from RunPod API
- Return raw API response dict
- Raise exception on API error

#### `_pod_dict_to_dataclass(pod_dict: dict) -> Pod`
- Convert RunPod API response to Pod dataclass
- Handle field name mappings and type conversions
- Extract nested fields
- Store raw response in `raw_data`

#### `_wait_for_pod_ready(pod_id: str, poll_interval: int, timeout: int) -> dict`
- Poll pod status at regular intervals
- Return raw dict when pod reaches RUNNING
- Raise `PodTimeoutError` on timeout
- Raise `PodFailedError` if terminal state reached
- This is the core polling logic (reused from wait_for_pod.py)

---

## Usage Example

```python
from runpod_pods_demo.pod_manager import PodManager

# Initialize manager
pm = PodManager(api_key="your-api-key")

# Create pod (blocks until RUNNING)
pod = pm.create_pod(
    name="my-pod",
    gpu_type_id="NVIDIA A40",
    image_name="pytorch/pytorch:latest",
    gpu_count=1,
)

# List created pods
pods = pm.list_pods()
print(f"Created {len(pods)} pods")

# Terminate pod
success = pm.terminate_pod(pod.id)
if success:
    print("Pod terminated")
```

---

## Future Enhancements

- Add `get_pod(pod_id)` to fetch individual pod status
- Add `refresh_pod_status(pod_id)` to update pod from API
- Add filtering to `list_pods(status=, gpu_type=, ...)`
- Persist registry to JSON file (cross-session state)
- Support async operations
