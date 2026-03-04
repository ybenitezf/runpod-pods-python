## Why

The project contains unused RunPod template management code (create, delete, list templates) that is not part of the pod lifecycle demo. Additionally, the environment variable `TEMPLATE_ENV` is misnamed - it configures pod environment variables, not template settings. This cleanup reduces confusion and removes dead code.

## What Changes

- Delete `src/runpod_pods_demo/create_template.py` - unused template creation code
- Delete `src/runpod_pods_demo/delete_template.py` - unused template deletion code
- Delete `src/runpod_pods_demo/list_templates.py` - unused template listing code
- Update `scripts/list_gpus.py` import to use `create_pod` module instead of deleted `create_template`
- Rename `TEMPLATE_ENV` environment variable to `POD_ENV` in `create_pod.py` for clarity

## Capabilities

### New Capabilities
- None - this is a cleanup/refactoring change

### Modified Capabilities
- None - existing pod-lifecycle and list-pods capabilities remain unchanged

## Impact

- **Affected Files**:
  - `src/runpod_pods_demo/create_template.py` (deleted)
  - `src/runpod_pods_demo/delete_template.py` (deleted)
  - `src/runpod_pods_demo/list_templates.py` (deleted)
  - `src/runpod_pods_demo/create_pod.py` (renamed TEMPLATE_ENV to POD_ENV)
  - `scripts/list_gpus.py` (updated import)

- **Breaking Changes**:
  - **BREAKING**: Environment variable `TEMPLATE_ENV` renamed to `POD_ENV` - users must update their `.env` files

- **Dependencies**: None affected
- **APIs**: No API changes
