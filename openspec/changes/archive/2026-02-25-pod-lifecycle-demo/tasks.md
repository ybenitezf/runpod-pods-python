## 1. Create Pod Module

- [x] 1.1 Create `src/runpod_pods_demo/create_pod.py` module
- [x] 1.2 Implement `load_api_key()` function (reuse from list_pods)
- [x] 1.3 Implement `create_pod()` function with A40 GPU and PyTorch image
- [x] 1.4 Add type hints and docstrings following project conventions
- [x] 1.5 Add error handling for API failures

## 2. Wait for Pod Module

- [x] 2.1 Create `src/runpod_pods_demo/wait_for_pod.py` module
- [x] 2.2 Implement `wait_for_pod_ready()` function with polling
- [x] 2.3 Set poll interval to 5 seconds
- [x] 2.4 Set timeout to 10 minutes (600 seconds)
- [x] 2.5 Add TimeoutError exception handling
- [x] 2.6 Add type hints and docstrings

## 3. Terminate Pod Module

- [x] 3.1 Create `src/runpod_pods_demo/terminate_pod.py` module
- [x] 3.2 Implement `terminate_pod()` function
- [x] 3.3 Add error handling for non-existent pods
- [x] 3.4 Add type hints and docstrings

## 4. Update Main Orchestration

- [x] 4.1 Update `main.py` to run full lifecycle
- [x] 4.2 Import new modules (create_pod, wait_for_pod, terminate_pod)
- [x] 4.3 Implement main() to: create → wait → list → terminate
- [x] 4.4 Add cleanup on failure (terminate if create succeeds but wait fails)
- [x] 4.5 Add progress output so user sees what's happening

## 5. Code Quality

- [x] 5.1 Run `ruff format` to format code
- [x] 5.2 Run `ruff check` to lint code
- [x] 5.3 Fix any linting issues

## 6. Testing (Manual)

- [x] 6.1 Run `uv run python main.py` with valid API key
- [x] 6.2 Verify pod is created
- [x] 6.3 Verify wait works (polls until RUNNING with runtime populated)
- [x] 6.4 Verify pods are listed
- [x] 6.5 Verify pod is terminated
- [x] 6.6 Test error handling with invalid API key
