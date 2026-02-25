"""Main entry point for the RunPod pods demo."""

import sys
from typing import Any, Optional, cast

import runpod

from runpod_pods_demo.create_pod import create_pod, load_api_key
from runpod_pods_demo.terminate_pod import PodNotFoundError, terminate_pod
from runpod_pods_demo.wait_for_pod import (
    PodFailedError,
    PodTimeoutError,
    wait_for_pod_ready,
)


def get_pods() -> list[dict[str, Any]]:
    """Get all RunPod pods."""
    api_key = load_api_key()
    if not api_key:
        raise ValueError(
            "RUNPOD_API_KEY not found in .env file. "
            "Please create a .env file with your API key (see .env.example)"
        )

    runpod.api_key = api_key
    pods: list[dict[str, Any]] = cast(list[dict[str, Any]], runpod.get_pods())
    return pods


def main() -> int:
    """Run the complete pod lifecycle demo.

    Creates a pod, waits for it to be ready, lists all pods,
    and terminates the created pod.
    """
    print("=" * 60)
    print("RunPod Pod Lifecycle Demo")
    print("=" * 60)

    pod_id: Optional[str] = None

    # Step 1: Create a pod
    print("\n[1/4] Creating pod...")
    try:
        pod = create_pod()
        pod_id = pod.get("id")
        if not pod_id:
            raise ValueError("Pod creation did not return a pod ID")
        print(f"  Pod created with ID: {pod_id}")
        print(f"  Pod Name: {pod.get('name')}")
        print(f"  Status: {pod.get('status')}")
    except Exception as e:
        print(f"  Error creating pod: {e}", file=sys.stderr)
        return 1

    # Step 2: Wait for pod to be ready
    print("\n[2/4] Waiting for pod to reach RUNNING state...")
    try:
        running_pod = wait_for_pod_ready(pod_id)  # type: ignore[arg-type]
        print("  Pod is now RUNNING!")
        print(f"  Pod ID: {running_pod.get('id')}")
    except PodTimeoutError as e:
        print(f"  Timeout waiting for pod: {e}")
        print("  Cleaning up (terminating pod)...")
        try:
            terminate_pod(pod_id)  # type: ignore[arg-type]
            print("  Pod terminated.")
        except Exception as cleanup_error:
            print(
                f"  Warning: Failed to terminate pod during cleanup: {cleanup_error}",
                file=sys.stderr,
            )
        return 1
    except PodFailedError as e:
        print(f"  Pod failed to start: {e}")
        print("  Cleaning up (terminating pod)...")
        try:
            terminate_pod(pod_id)  # type: ignore[arg-type]
            print("  Pod terminated.")
        except Exception as cleanup_error:
            print(
                f"  Warning: Failed to terminate pod during cleanup: {cleanup_error}",
                file=sys.stderr,
            )
        return 1
    except Exception as e:
        print(f"  Error waiting for pod: {e}", file=sys.stderr)
        if pod_id:
            print("  Cleaning up (terminating pod)...")
            try:
                terminate_pod(pod_id)
                print("  Pod terminated.")
            except Exception as cleanup_error:
                print(
                    f"  Warning: Failed to terminate pod during cleanup: {cleanup_error}",
                    file=sys.stderr,
                )
        return 1

    # Step 3: List all pods
    print("\n[3/4] Listing all pods...")
    try:
        pods = get_pods()
        print(f"  Found {len(pods)} pod(s):")
        for p in pods:
            status = p.get("desiredStatus", p.get("status", "UNKNOWN"))
            print(f"    - {p.get('name')} ({p.get('id')}): {status}")
    except Exception as e:
        print(f"  Warning: Failed to list pods: {e}", file=sys.stderr)

    # Step 4: Terminate the pod
    print(f"\n[4/4] Terminating pod {pod_id}...")
    try:
        terminate_pod(pod_id)  # type: ignore[arg-type]
        print("  Pod terminated successfully!")
    except PodNotFoundError:
        print("  Warning: Pod not found (may have already been terminated)")
    except Exception as e:
        print(f"  Error terminating pod: {e}", file=sys.stderr)
        return 1

    print("\n" + "=" * 60)
    print("Pod lifecycle demo completed successfully!")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
