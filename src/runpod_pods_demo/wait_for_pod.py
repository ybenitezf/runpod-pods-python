"""Script to wait for a RunPod pod to reach RUNNING state."""

import sys
import time
from typing import Any, cast

import runpod
from runpod_pods_demo.create_pod import load_api_key
from runpod_pods_demo.exceptions import PodTimeoutError, PodFailedError

POLL_INTERVAL_SECONDS = 5
TIMEOUT_SECONDS = 600


def wait_for_pod_ready(
    pod_id: str,
    poll_interval: int = POLL_INTERVAL_SECONDS,
    timeout: int = TIMEOUT_SECONDS,
) -> dict[str, Any]:
    """Wait for a pod to reach RUNNING state.

    Polls the pod status at regular intervals until it reaches RUNNING,
    a terminal failure state, or the timeout is reached.

    Args:
        pod_id: The ID of the pod to wait for.
        poll_interval: How often to check pod status (in seconds).
        timeout: Maximum time to wait (in seconds).

    Returns:
        The pod object with RUNNING status.

    Raises:
        ValueError: If the API key is not configured.
        PodTimeoutError: If the pod doesn't reach RUNNING within timeout.
        PodFailedError: If the pod enters a failed terminal state.
        Exception: If fetching pod status fails.
    """
    api_key = load_api_key()
    if not api_key:
        raise ValueError(
            "RUNPOD_API_KEY not found in .env file. "
            "Please create a .env file with your API key (see .env.example)"
        )

    runpod.api_key = api_key

    start_time = time.time()
    terminal_states = {"EXITED", "FAILED", "DEAD", "TERMINATED", "CANCELLED"}

    while True:
        elapsed = time.time() - start_time
        if elapsed >= timeout:
            raise PodTimeoutError(
                f"Pod '{pod_id}' did not reach RUNNING state within {timeout} seconds"
            )

        try:
            pod: dict[str, Any] = cast(dict[str, Any], runpod.get_pod(pod_id))
        except Exception as e:
            raise Exception(f"Failed to get pod status: {e}") from e

        desired_status = pod.get("desiredStatus", pod.get("status", "UNKNOWN"))
        runtime = pod.get("runtime")

        if desired_status == "RUNNING" and runtime is not None:
            return pod

        if desired_status in terminal_states:
            raise PodFailedError(
                f"Pod '{pod_id}' entered failed state: {desired_status}"
            )

        remaining = int(timeout - elapsed)
        print(f"  Pod status: {desired_status} (waiting, ~{remaining}s remaining)...")

        time.sleep(poll_interval)


def main() -> int:
    """Main entry point for waiting on a pod."""
    if len(sys.argv) < 2:
        print("Usage: python wait_for_pod.py <pod_id>", file=sys.stderr)
        return 1

    pod_id = sys.argv[1]

    try:
        print(f"Waiting for pod {pod_id} to reach RUNNING state...")
        pod = wait_for_pod_ready(pod_id)
        print("Pod is now RUNNING!")
        print(f"Pod ID: {pod.get('id')}")
        print(f"Pod Name: {pod.get('name')}")
        return 0
    except (PodTimeoutError, PodFailedError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
