## Why

The current demo only lists RunPod pods, which demonstrates a read-only capability. To fully showcase the RunPod Python API, we need a comprehensive demo that exercises the full pod lifecycle: creating a pod, waiting for it to be ready, and terminating it. This demonstrates the complete CRUD operations for pod management.

## What Changes

- Add a new `create_pod.py` module that creates a RunPod pod with A40 GPU and PyTorch image
- Add a `wait_for_pod.py` module that polls pod status until it reaches RUNNING state
- Extend `main.py` to run the full lifecycle: create → wait → list → terminate
- Add proper error handling for each step in the lifecycle

## Implementation Notes

During implementation, the following API behaviors were discovered:

- RunPod API uses `desiredStatus` field (not `status`) to indicate the target state
- A pod is truly ready only when BOTH:
  - `desiredStatus == "RUNNING"`
  - `runtime` is not null (container is initialized and running)

## Capabilities

### New Capabilities

- `pod-lifecycle`: Complete pod lifecycle management (create, wait for ready, terminate)
  - Create a pod with specified GPU type and Docker image
  - Poll pod status until it reaches RUNNING state
  - Terminate the created pod to clean up resources

### Modified Capabilities

- (none - list-pods remains unchanged)

## Impact

- **New files**: `src/runpod_pods_demo/create_pod.py`, `src/runpod_pods_demo/wait_for_pod.py`
- **Modified files**: `main.py` to orchestrate the full lifecycle
- **Dependencies**: runpod-python library (already installed), python-dotenv (already installed)
- **API calls**: `create_pod`, `get_pod`, `get_pods`, `terminate_pod`
