"""Main entry point for the RunPod pods demo."""

import sys
from typing import Any, Optional, cast

import runpod
from dotenv import load_dotenv

from runpod_pods_demo.create_pod import create_pod, load_api_key, load_pod_config
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

    Creates a pod with configuration from .env, waits for it to be ready,
    prompts for user verification, lists all pods, and terminates the pod.
    """
    print("=" * 60)
    print("RunPod Pod Lifecycle Demo")
    print("=" * 60)

    load_dotenv()

    pod_id: Optional[str] = None

    print("\n[1/4] Creating pod...")
    try:
        config = load_pod_config()
        pod = create_pod(
            name="pod-lifecycle-demo",
            gpu_type_id=config.get("gpu_type_id", "NVIDIA A40"),
            image_name=config.get("image_name", "pytorch/pytorch:latest"),
            gpu_count=config.get("gpu_count", 1),
            container_disk_in_gb=config.get("container_disk_in_gb"),
            volume_in_gb=config.get("volume_in_gb"),
            volume_mount_path=config.get("volume_mount_path"),
            ports=config.get("ports"),
            env=config.get("env"),
        )
        pod_id = pod.get("id")
        if not pod_id:
            raise ValueError("Pod creation did not return a pod ID")
        print(f"  Pod created with ID: {pod_id}")
        print(f"  Pod Name: {pod.get('name')}")
        print(f"  Status: {pod.get('status')}")
    except Exception as e:
        print(f"  Error creating pod: {e}", file=sys.stderr)
        return 1

    print("\n[2/4] Waiting for pod to reach RUNNING state...")
    try:
        running_pod = wait_for_pod_ready(pod_id)
        print("  Pod is now RUNNING!")
        print(f"  Pod ID: {running_pod.get('id')}")
    except PodTimeoutError as e:
        print(f"  Timeout waiting for pod: {e}")
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
    except PodFailedError as e:
        print(f"  Pod failed to start: {e}")
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

    print("\n[3/4] User verification...")
    print("  Pod is ready! Please check the RunPod console to verify.")
    print("  Press Enter to continue with termination and cleanup...")
    try:
        input()
    except KeyboardInterrupt:
        print("\n  Aborted by user.")
        print("  Please manually terminate the pod later.")
        return 1

    print("\n[4/4] Terminating pod...")
    try:
        terminate_pod(pod_id)
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
