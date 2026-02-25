"""Script to list all RunPod pods."""

import os
import sys
from typing import Any, Optional, cast

import runpod
from dotenv import load_dotenv


def format_uptime(seconds: int) -> str:
    """Convert uptime in seconds to human-readable format."""
    if seconds < 60:
        return f"{seconds}s"
    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes}m"
    hours = minutes // 60
    remaining_minutes = minutes % 60
    if remaining_minutes == 0:
        return f"{hours}h"
    return f"{hours}h {remaining_minutes}m"


def get_gpu_type(pod: dict[str, Any]) -> str:
    """Extract GPU type from pod data."""
    gpu_count = pod.get("gpuCount", 0)
    gpu_type = pod.get("gpuTypeId", "N/A")
    if gpu_count > 0:
        return f"{gpu_count}x {gpu_type}"
    return "CPU"


def print_pods_table(pods: list[dict[str, Any]]) -> None:
    """Print pods in a formatted table."""
    if not pods:
        print("No pods found.")
        return

    name_width = max(len(p.get("name", "N/A")) for p in pods)
    name_width = max(name_width, 8)

    id_width = max(len(p.get("id", "N/A")) for p in pods)
    id_width = max(id_width, 10)

    status_width = max(len(p.get("status", "N/A")) for p in pods)
    status_width = max(status_width, 10)

    header = (
        f"{'NAME':<{name_width}} "
        f"{'ID':<{id_width}} "
        f"{'STATUS':<{status_width}} "
        f"{'UPTIME':<8} "
        f"{'GPU':<15}"
    )
    separator = "-" * len(header)

    print(header)
    print(separator)

    for pod in pods:
        uptime_seconds = pod.get("runtime", {}).get("uptimeInSeconds", 0)
        uptime = format_uptime(uptime_seconds) if uptime_seconds else "N/A"
        status = pod.get("status", "N/A")

        print(
            f"{pod.get('name', 'N/A'):<{name_width}} "
            f"{pod.get('id', 'N/A'):<{id_width}} "
            f"{status:<{status_width}} "
            f"{uptime:<8} "
            f"{get_gpu_type(pod):<15}"
        )


def load_api_key() -> Optional[str]:
    """Load and validate API key from .env file."""
    load_dotenv()
    api_key = os.getenv("RUNPOD_API_KEY")
    if not api_key:
        return None
    return api_key


def list_pods() -> int:
    """List all RunPod pods."""
    api_key = load_api_key()
    if not api_key:
        print("Error: RUNPOD_API_KEY not found in .env file.", file=sys.stderr)
        print(
            "Please create a .env file with your API key (see .env.example)",
            file=sys.stderr,
        )
        return 1

    runpod.api_key = api_key

    try:
        pods: list[dict[str, Any]] = cast(list[dict[str, Any]], runpod.get_pods())
    except Exception as e:
        print(f"Error fetching pods: {e}", file=sys.stderr)
        return 1

    print_pods_table(pods)
    return 0


if __name__ == "__main__":
    sys.exit(list_pods())
