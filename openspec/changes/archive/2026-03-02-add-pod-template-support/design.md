## Context

The current demo (`main.py`) creates pods directly using `create_pod()`. This change adds flexible configuration support, allowing users to customize pod creation through environment variables. Configuration includes GPU type, container image, disk sizes, volumes, ports, and environment variables.

## Goals / Non-Goals

**Goals:**
- Add configuration loading from .env file
- Support container disk size, volume, ports, and environment variables
- Provide a GPU listing script for users to evaluate available options
- Keep pod creation simple without template complexity

**Non-Goals:**
- Template creation/deletion (removed from scope)
- Support for serverless endpoints
- Complex GPU selection logic
- Persistent configuration storage

## Decisions

| Decision | Rationale |
|----------|-----------|
| Load config from .env | Keeps configuration external and user-friendly |
| Default GPU in .env | Users can evaluate with list_gpus.py first |
| JSON for env vars in .env | Easy to parse, familiar format |
| Python SDK for pod creation | More reliable than REST API for basic pod creation |

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Default GPU not available in user's region | User can override in .env, list_gpus.py shows available options |
| Invalid configuration | Error messages guide user to fix .env |

## Open Questions

- None at this time
