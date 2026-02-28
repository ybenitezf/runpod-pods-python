## Why

The RunPod Python SDK lacks a built-in function to list official RunPod Docker images. Users need a way to programmatically discover available official images (e.g., PyTorch, TensorFlow) for their pods and endpoints. The SDK provides `create_template` but not `get_templates`, requiring developers to make direct REST API calls.

## What Changes

- Add new script `src/runpod_pods_demo/list_templates.py` that:
  - Calls the RunPod REST API `GET /v1/templates?includeRunpodTemplates=true`
  - Filters results for `isRunpod=True` to get official images
  - Prints a formatted table with Template Name and Docker Image URI
  - Includes error handling for API connection issues

## Capabilities

### New Capabilities
- `list-official-images`: List official RunPod Docker images from templates

## Impact

- New file: `src/runpod_pods_demo/list_templates.py`
- Dependencies: Add `requests` to `pyproject.toml`
- API: Uses existing RunPod REST API endpoint `/v1/templates`
