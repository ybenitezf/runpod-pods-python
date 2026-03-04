# Implementation Tasks

## Phase 1: Foundation

- [x] **Create exceptions module**
  - Extract `PodNotFoundError`, `PodTimeoutError`, `PodFailedError` from existing files
  - Create `src/runpod_pods_demo/exceptions.py`
  - Update imports in existing modules

- [x] **Create Pod dataclass**
  - Add `Pod` dataclass to `src/runpod_pods_demo/pod_manager.py`
  - Include all fields with proper type hints
  - Add docstring explaining each field

## Phase 2: Core PodManager Implementation

- [x] **Implement PodManager.__init__()**
  - Accept `api_key: str`
  - Initialize `_pods_created: dict[str, Pod] = {}`

- [x] **Implement PodManager._get_pod_from_api()**
  - Fetch pod details from RunPod API using `runpod.get_pod(pod_id)`
  - Return raw dict response
  - Handle API errors

- [x] **Implement PodManager._pod_dict_to_dataclass()**
  - Convert API response dict to `Pod` dataclass
  - Map API field names to Pod fields (handle camelCase conversions)
  - Extract nested fields (e.g., `runtime.uptimeInSeconds`)
  - Store raw API response in `Pod.raw_data`

- [x] **Implement PodManager._wait_for_pod_ready()**
  - Copy logic from `wait_for_pod.py`
  - Poll pod status at regular intervals
  - Return raw dict when pod reaches RUNNING state
  - Raise `PodTimeoutError` on timeout
  - Raise `PodFailedError` if pod enters terminal state

- [x] **Implement PodManager.create_pod()**
  - Accept all pod configuration parameters
  - Call RunPod API to create pod
  - Call `_wait_for_pod_ready()` internally (blocking)
  - Convert response to `Pod` dataclass using `_pod_dict_to_dataclass()`
  - Add pod to `_pods_created` registry
  - Return `Pod`
  - Handle and propagate exceptions

## Phase 3: Remaining Public Methods

- [x] **Implement PodManager.list_pods()**
  - Return list of Pod objects from `_pods_created`
  - Simple: `return list(self._pods_created.values())`

- [x] **Implement PodManager.terminate_pod()**
  - Check if pod_id exists in `_pods_created`
  - Call RunPod API to terminate
  - Remove from registry on success
  - Return boolean success
  - Raise exceptions on failure

## Phase 4: Integration and Testing

- [x] **Update `__init__.py`**
  - Export `PodManager` and `Pod` classes
  - Export custom exceptions

- [x] **Create example/test script**
  - Demonstrate `PodManager` usage
  - Show: create pod → list pods → terminate pod workflow
  - Include error handling examples

- [x] **Verify backwards compatibility**
  - Confirm old modules still work
  - Run existing `main.py` with old functions

- [x] **Documentation**
  - Add docstrings to all public methods
  - Add type hints throughout
  - Include usage examples in docstrings

## Acceptance Criteria

✅ `PodManager` class exists and can be imported  
✅ `create_pod()` blocks until pod is RUNNING  
✅ `list_pods()` returns pods created by instance  
✅ `terminate_pod()` removes pod from registry  
✅ Pod dataclass properly represents RunPod pod data  
✅ Custom exceptions are properly used and raised  
✅ All public methods have docstrings  
✅ Type hints on all function signatures  
✅ Backwards compatibility maintained (old code still works)  

## Notes

- Keep polling logic from `wait_for_pod.py` (it's already solid)
- API key handling: caller must provide (no `.env` loading in class)
- Registry is in-memory only (no persistence)
- Don't refactor old modules—add new functionality separately
