## Context

The RunPod Python SDK (v1.8.1) does not expose a function to list templates. The REST API at `https://rest.runpod.io/v1/templates` supports this with query parameters to filter for official RunPod images.

## Goals / Non-Goals

**Goals:**
- Create a script that lists official RunPod Docker images
- Use REST API directly since SDK lacks `get_templates()`
- Match existing code patterns in the project

**Non-Goals:**
- Modifying the SDK (out of scope for this demo project)
- Caching or storing results
- Listing public/community templates

## Decisions

1. **Direct REST API over SDK** - The SDK uses GraphQL for most operations but templates are REST-only. Using `requests` library (already a dependency) is simpler than extending the SDK.

2. **Bearer Token Auth** - Use `Authorization: Bearer <api_key>` header matching RunPod REST API conventions.

3. **Error Handling** - Use try/except with `requests.RequestException` to catch connection issues, matching the pattern in `list_pods.py`.

4. **Output Format** - Table format similar to `list_pods.py` for consistency:
   - Columns: Template Name, Docker Image URI

## Risks / Trade-offs

- [Risk] SDK version changes → Mitigation: REST API is stable, unlikely to break
- [Risk] API rate limiting → Mitigation: This is a read-only operation, low frequency
