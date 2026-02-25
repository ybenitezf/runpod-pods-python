# AGENTS.md - Developer Guidelines for runpod-pods-demo

## Project Overview

- **Language**: Python 3.12
- **Package Manager**: uv
- **Virtual Environment**: .venv (managed by uv)
- **Project Type**: RunPod Python API Demo

---

## Build / Lint / Test Commands

### Running the Application

```bash
uv run python main.py
# Or: source .venv/bin/activate && python main.py
```

### Installing Dependencies

```bash
uv add <package>          # Add dependency
uv sync                   # Install all from pyproject.toml
uv sync --dev            # Install dev dependencies
```

### Running Tests

This project does not include tests.

### Code Quality Tools

```bash
uv run ruff format    # Format code
uv run ruff check     # Lint
uv run ruff check --fix  # Lint with auto-fix
uv run ruff format && uv run ruff check  # All checks
```

### Adding New Tools

```bash
uv add --dev ruff    # Add ruff
```

---

## Code Style Guidelines

### General Principles
- Follow PEP 8 style guide
- Keep functions small and focused (single responsibility)
- Write docstrings for all public functions and classes
- Use type hints everywhere possible

### Naming Conventions
- **Variables/functions**: `snake_case` (e.g., `get_pod_status`)
- **Classes**: `PascalCase` (e.g., `PodManager`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_RETRIES`)
- **Private methods**: Prefix with underscore (e.g., `_internal_method`)
- **File names**: `snake_case.py`

### Imports
Group imports in order: 1) Standard library, 2) Third-party, 3) Local. Sort alphabetically.

```python
import os
from typing import Any, Optional

import requests
from dotenv import load_dotenv

from runpod_pods_demo.client import APIClient
```

### Type Hints
Always use type hints. Use `Optional[X]` instead of `X | None`.

```python
def get_pod(pod_id: str) -> Optional[dict[str, Any]]:
    ...
```

### Error Handling
- Use custom exceptions for domain-specific errors
- Catch specific exceptions, not broad `Exception`
- Use `logging` for errors, not print

```python
class PodNotFoundError(Exception):
    pass

def get_pod(pod_id: str) -> dict[str, Any]:
    try:
        response = api.get(f"/pods/{pod_id}")
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            raise PodNotFoundError(f"Pod '{pod_id}' not found") from e
        raise
```

### Formatting
- Max line length: 88 characters (ruff default)
- 4 spaces for indentation
- Use trailing commas in multi-line structures

### Docstrings
Use Google-style docstrings:

```python
def create_pod(name: str, image: str, **kwargs) -> Pod:
    """Create a new RunPod pod.

    Args:
        name: The name of the pod.
        image: Docker image to use.
        **kwargs: Additional configuration options.

    Returns:
        The created Pod object.

    Raises:
        PodCreationError: If pod creation fails.
    """
```

### Configuration
- Use environment variables for secrets (API keys)
- Use `.env` files for local development (add to `.gitignore`)
- Create a `config.py` module for settings

---

## Project Structure

```
runpod-pods-demo/
├── .venv/              # Virtual environment
├── .gitignore
├── .python-version    # Python version (3.12)
├── pyproject.toml     # Project configuration
├── uv.lock            # Locked dependencies
├── main.py            # Entry point
├── README.md
├── src/               # Source code (create as needed)
│   └── runpod_pods_demo/
│       ├── __init__.py
│       └── ...
```

---

## Documentation

This project demonstrates the RunPod Python library. Use Context7 to get up-to-date documentation:

```bash
# Use context7_query-docs tool with library ID: /runpod/runpod
# Query examples: "how to create a pod", "how to list pods", "how to get pod status"
```

---

## Git Commit Messages

This project uses [Conventional Commits](https://www.conventionalcommits.org/). Format:

```
<type>[optional scope]: <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `chore`: Maintenance, deps, build changes
- `refactor`: Code refactoring

**Examples:**
```
feat: add pod listing function
fix: handle API timeout gracefully
docs: update README with setup instructions
chore: upgrade runpod library version
feat(auth)!: change API token format
BREAKING CHANGE: the auth module now requires tokens to be JWT
```

---

## Notes
- Use `uv` for package management - avoid `pip` directly
- Always use `uv run` to execute commands
- Keep venv synchronized with `uv sync`
