## Context

The current demo project (`runpod-pods-demo`) uses the RunPod Python library to list pods. The demo is a learning tool showing how to use the RunPod API. Currently it only demonstrates reading data (get_pods). The proposal extends this to demonstrate the full pod lifecycle.

**Current State:**
- `main.py` → `list_pods()` → `runpod.get_pods()`
- Uses `python-dotenv` for API key loading
- No error handling for API failures

**Constraints:**
- Must use the runpod-python library
- API key must be loaded from .env file
- Should follow existing code patterns (type hints, docstrings, error handling)

## Goals / Non-Goals

**Goals:**
- Create a pod with A40 GPU and PyTorch image
- Poll until pod status is RUNNING
- List all pods (reuse existing functionality)
- Terminate the created pod for cleanup

**Non-Goals:**
- Serverless endpoints (only persistent pods)
- Network volumes or persistent storage
- Custom container registries
- Automated scaling or multiple pod management

## Decisions

### Decision 1: Reuse existing API key loading vs create new module

**Choice:** Reuse the `load_api_key()` function from `list_pods.py`

**Rationale:** Maintains consistency across the codebase. The function is already tested and handles .env loading correctly.

### Decision 2: Polling strategy for pod readiness

**Choice:** Simple polling with fixed interval (5 seconds) and timeout (10 minutes)

**Rationale:**
- Simpler than async/await for a demo
- Matches common patterns in RunPod examples
- Timeout prevents infinite waiting if pod creation fails

**Alternative considered:** Use threading/event-based waiting
- Rejected: Adds complexity, unnecessary for demo

### Decision 2.1: Pod readiness detection

**Choice:** Check both `desiredStatus` and `runtime` field

**Implementation:**
- RunPod API returns `desiredStatus` field (not `status`) to indicate target state
- Pod is truly ready only when BOTH conditions are true:
  - `desiredStatus == "RUNNING"`
  - `runtime` is not null (container is initialized)

**Rationale:** 
- `desiredStatus` indicates the target state but container may still be initializing
- When `runtime` is null, the container is still starting up even if desiredStatus is RUNNING
- This ensures the pod is fully ready to serve requests before proceeding

### Decision 3: Error

**Choice:** handling approach Fail fast with clear error messages at each step

**Rationale:**
- Demo should be easy to understand
- Each step (create, wait, list, terminate) should have explicit error handling
- No retry logic to keep demo simple

### Decision 4: Pod configuration defaults

**Choice:** Use sensible defaults with explicit parameters

- GPU: NVIDIA A40
- Image: pytorch/pytorch:latest
- GPU Count: 1
- Ports: None (not needed for demo)
- Environment: None (not needed for demo)
- Volume: Default (container disk only)

**Rationale:** Simplest configuration that still demonstrates the API

## Risks / Trade-offs

**[Risk] Pod creation may fail due to GPU availability**
→ **Mitigation:** Display clear error message if A40 unavailable. User can modify GPU type in code if needed.

**[Risk] Polling may hang indefinitely if pod gets stuck**
→ **Mitigation:** Implement 10-minute timeout with clear error message

**[Risk] API key may be invalid**
→ **Mitigation:** Reuse existing validation from list_pods.py

**[Risk] Termination may fail if pod already terminated**
→ **Mitigation:** Catch and handle exception gracefully

## Open Questions

1. Should we add a "stop" (not terminate) step to show cost-saving mode?
   - Current scope: terminate only
   - Can be added as future enhancement

2. Should we show the pod IP or SSH info?
   - Current scope: just show it's running
   - Not needed for basic demo
