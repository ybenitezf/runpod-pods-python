## Context

A simple CLI script to list all RunPod pods for the user. The script will:
- Load API key from `.env` file via `python-dotenv`
- Use RunPod Python SDK (`runpod.get_pods()`)
- Display results in a formatted table

## Goals / Non-Goals

**Goals:**
- List all pods with name, ID, status, uptime, and GPU type
- Load API key securely from `.env`
- Handle errors gracefully (missing API key, invalid key, network issues)

**Non-Goals:**
- Create, update, or delete pods
- Filter or sort pods
- Interactive prompts

## Decisions

| Decision | Rationale |
|----------|-----------|
| Use RunPod SDK | Simplest approach, well-documented |
| Table output format | Clean, scannable output as requested |
| Fail-fast on missing API key | Clear error message helps user get started |

## Risks / Trade-offs

- **API response structure may vary** → Handle missing fields gracefully with defaults
- **Uptime calculation** → Convert seconds to human-readable format (e.g., "2h 15m")
