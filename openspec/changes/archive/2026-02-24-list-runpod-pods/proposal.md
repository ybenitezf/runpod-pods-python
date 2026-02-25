## Why

This project needs a simple script to list all RunPod pods for the user. Without this, there's no way to see what pods exist in the account or their current status.

## What Changes

- Add a script that uses the RunPod Python SDK to fetch and display all pods
- Load API key from `.env` file using `python-dotenv`
- Display pods in a formatted table with name, ID, status, uptime, and GPU type

## Capabilities

### New Capabilities
- `list-pods`: Display all RunPod pods in a formatted table showing name, ID, status, uptime, and GPU type

### Modified Capabilities
- None

## Impact

- New file: `src/runpod_pods_demo/__init__.py` (package init)
- New file: `src/runpod_pods_demo/list_pods.py` (main script)
- New file: `.env.example` (template for API key)
