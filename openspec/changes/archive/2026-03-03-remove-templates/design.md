## Context

The project demo focuses on the RunPod pod lifecycle (create, wait, list, terminate). Template management features were added but never integrated into the main workflow. The code also contains a misnamed environment variable (`TEMPLATE_ENV`) that controls pod environment variables, not template settings.

## Goals / Non-Goals

**Goals:**
- Remove unused template management code files
- Fix the misnamed `TEMPLATE_ENV` variable to `POD_ENV`
- Ensure all existing scripts continue to work after the change

**Non-Goals:**
- No new pod or template capabilities
- No changes to the pod lifecycle workflow
- No modifications to existing specs

## Decisions

### 1. Delete template management files
**Decision:** Delete the three template files entirely.
**Rationale:** These files are completely unused by `main.py` and provide no value to the demo. The RunPod SDK can be used directly if template management is needed in the future.
**Alternative considered:** Keep files but mark as deprecated. Rejected - adds maintenance burden with no benefit.

### 2. Rename TEMPLATE_ENV to POD_ENV
**Decision:** Rename the environment variable and update all references.
**Rationale:** The current name is misleading. `TEMPLATE_ENV` suggests it configures RunPod templates, but it actually sets environment variables on the pod itself.
**Alternative considered:** Keep the name and add documentation. Rejected - confusing API is worse than a breaking change.

### 3. Import dependency resolution
**Decision:** Update `scripts/list_gpus.py` to import `load_api_key` from `create_pod.py` instead of the deleted `create_template.py`.
**Rationale:** `create_pod.py` already has `load_api_key` - same function, no duplication needed.

## Risks / Trade-offs

| Risk | Impact | Mitigation |
|------|--------|------------|
| Users with `.env` using `TEMPLATE_ENV` | Breakage | Document the rename in CHANGELOG; `POD_ENV` will simply be ignored (pod uses empty env) |
| Someone using template files directly | Breakage | Template files are unused in this demo - unlikely anyone depends on them |

## Migration Plan

1. Update `scripts/list_gpus.py` import
2. Rename `TEMPLATE_ENV` → `POD_ENV` in `create_pod.py`
3. Delete the three template files
4. Run lint/format checks
5. Test that `main.py` and `scripts/list_gpus.py` still work
