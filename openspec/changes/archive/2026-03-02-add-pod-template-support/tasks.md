## 1. Configuration

- [x] 1.1 Update .env.example with pod configuration options
- [x] 1.2 Document config values in README

## 2. GPU Listing Script

- [x] 2.1 Create list_gpus.py script
- [x] 2.2 Display GPU info in table format

## 3. Pod Creation Module

- [x] 3.1 Enhance create_pod.py to support all config options (container_disk, volume, ports, env)
- [x] 3.2 Add load_pod_config() function to read from .env

## 4. Main Flow Integration

- [x] 4.1 Update main.py to load config from .env
- [x] 4.2 Pass all config options to create_pod()
- [x] 4.3 Add pause for user verification after pod is ready
- [x] 4.4 Clean up on pod failure

## 5. Verification

- [x] 5.1 Run main.py and verify full flow works
- [x] 5.2 Run ruff format and ruff check
