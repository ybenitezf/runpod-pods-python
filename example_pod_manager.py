"""Example script demonstrating PodManager usage."""

import os
from dotenv import load_dotenv
from runpod_pods_demo import (
    PodManager,
    PodNotFoundError,
    PodTimeoutError,
    PodFailedError,
)


def main() -> int:
    """Demonstrate PodManager workflow: create, list, terminate."""
    load_dotenv()
    api_key = os.getenv("RUNPOD_API_KEY")
    if not api_key:
        print("Error: RUNPOD_API_KEY not found in .env file")
        return 1

    pm = PodManager(api_key=api_key)

    print("=== Creating Pod ===")
    try:
        pod = pm.create_pod(
            name="demo-pod",
            gpu_type_id="NVIDIA A40",
            image_name="pytorch/pytorch:latest",
            gpu_count=1,
        )
        print(f"Pod created: {pod.id}")
        print(f"  Name: {pod.name}")
        print(f"  Status: {pod.status}")
        print(f"  GPU: {pod.gpu_count}x {pod.gpu_type}")
    except PodTimeoutError as e:
        print(f"Timeout: {e}")
        return 1
    except PodFailedError as e:
        print(f"Pod failed: {e}")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1

    print("\n=== Listing Pods ===")
    pods = pm.list_pods()
    print(f"Pods created by this manager: {len(pods)}")
    for p in pods:
        print(f"  - {p.id}: {p.name} ({p.status})")

    print("\n=== Terminating Pod ===")
    try:
        success = pm.terminate_pod(pod.id)
        if success:
            print(f"Pod {pod.id} terminated successfully")
    except PodNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Error terminating pod: {e}")
        return 1

    print("\n=== Final Pod List ===")
    pods = pm.list_pods()
    print(f"Pods in registry: {len(pods)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
