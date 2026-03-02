# RunPod Pods Python API Demo

This is a demo of how to use the runpod python library

## Setup

```bash
uv sync
```

## Configuration

Copy `.env.example` to `.env` and configure the following:

| Variable | Description | Required |
|----------|-------------|----------|
| `RUNPOD_API_KEY` | Your RunPod API key | Yes |
| `GPU_TYPE_ID` | GPU type (e.g., "NVIDIA A40") | Yes |
| `IMAGE_NAME` | Docker image to use | Yes |
| `CONTAINER_DISK_IN_GB` | Container disk size in GB (default: 10) | No |
| `VOLUME_IN_GB` | Persistent volume size in GB | No |
| `VOLUME_MOUNT_PATH` | Volume mount path (e.g., /workspace) | No |
| `PORTS` | Ports to expose (e.g., 22/tcp,8888/http) | No |
| `TEMPLATE_ENV` | Environment variables as JSON | No |

Run `uv run python scripts/list_gpus.py` to see available GPU types.

## Running

```bash
uv run python main.py
```

## Contributing

This project uses [Conventional Commits](https://www.conventionalcommits.org/) for commit messages.

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
```


