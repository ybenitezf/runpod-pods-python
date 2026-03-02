## Why

The current demo creates pods directly without configuration flexibility. Adding configuration support allows users to customize pod creation through environment variables, making the demo more useful and demonstrating how to pass various configuration options to the RunPod API.

## What Changes

- Add new script `list_gpus.py` to list available GPU types with their details for user evaluation
- Add new module `create_pod.py` with enhanced configuration support:
  - Container disk size
  - Volume configuration (size and mount path)
  - Port configuration
  - Environment variables
- Update `.env.example` with all available configuration options
- Update `main.py` to:
  1. Load configuration from .env
  2. Create pod with all configuration options
  3. Wait for pod ready
  4. **Pause for user verification** (user can check RunPod console)
  5. Terminate pod

## Capabilities

### New Capabilities
- `pod-config`: Support for customizable pod creation through environment variables

### Modified Capabilities
- `pod-lifecycle`: Enhanced to support additional pod configuration options

## Impact

- New files: `scripts/list_gpus.py`
- Modified files: `src/runpod_pods_demo/create_pod.py`, `main.py`, `.env.example`, `README.md`
- Dependencies: None (uses existing runpod library)
