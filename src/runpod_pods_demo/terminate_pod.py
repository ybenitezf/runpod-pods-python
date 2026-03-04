"""Script to terminate a RunPod pod."""

import sys
from typing import Any, cast

import runpod
from runpod_pods_demo.create_pod import load_api_key
from runpod_pods_demo.exceptions import PodNotFoundError


def terminate_pod(pod_id: str) -> dict[str, Any]:
    """Terminate a RunPod pod.

    Args:
        pod_id: The ID of the pod to terminate.

    Returns:
        The response from the terminate API call.

    Raises:
        ValueError: If the API key is not configured.
        PodNotFoundError: If the pod does not exist.
        Exception: If termination fails.
    """
    api_key = load_api_key()
    if not api_key:
        raise ValueError(
            "RUNPOD_API_KEY not found in .env file. "
            "Please create a .env file with your API key (see .env.example)"
        )

    runpod.api_key = api_key

    try:
        result: dict[str, Any] = cast(dict[str, Any], runpod.terminate_pod(pod_id))
    except Exception as e:
        error_msg = str(e).lower()
        if "not found" in error_msg or "404" in error_msg:
            raise PodNotFoundError(f"Pod '{pod_id}' not found") from e
        raise Exception(f"Failed to terminate pod: {e}") from e

    return result


def main() -> int:
    """Main entry point for terminating a pod."""
    if len(sys.argv) < 2:
        print("Usage: python terminate_pod.py <pod_id>", file=sys.stderr)
        return 1

    pod_id = sys.argv[1]

    try:
        print(f"Terminating pod {pod_id}...")
        terminate_pod(pod_id)
        print("Pod terminated successfully!")
        return 0
    except PodNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
