"""Script to create a RunPod pod."""

import os
import sys
from typing import Any, Optional, cast

import runpod
from dotenv import load_dotenv


POD_NAME = "pod-lifecycle-demo"
GPU_TYPE_ID = "NVIDIA A40"
IMAGE_NAME = "pytorch/pytorch:latest"
GPU_COUNT = 1


def load_api_key() -> Optional[str]:
    """Load and validate API key from .env file."""
    load_dotenv()
    api_key = os.getenv("RUNPOD_API_KEY")
    if not api_key:
        return None
    return api_key


def create_pod(
    name: str = POD_NAME,
    gpu_type_id: str = GPU_TYPE_ID,
    image_name: str = IMAGE_NAME,
    gpu_count: int = GPU_COUNT,
) -> dict[str, Any]:
    """Create a RunPod pod with the specified GPU and image.

    Args:
        name: The name for the pod.
        gpu_type_id: The GPU type ID (e.g., "NVIDIA A40").
        image_name: The Docker image to use.
        gpu_count: The number of GPUs to request.

    Returns:
        The created pod object containing an ID.

    Raises:
        ValueError: If the API key is not configured.
        Exception: If pod creation fails.
    """
    api_key = load_api_key()
    if not api_key:
        raise ValueError(
            "RUNPOD_API_KEY not found in .env file. "
            "Please create a .env file with your API key (see .env.example)"
        )

    runpod.api_key = api_key

    try:
        pod: dict[str, Any] = cast(
            dict[str, Any],
            runpod.create_pod(
                name=name,
                image_name=image_name,
                gpu_type_id=gpu_type_id,
                gpu_count=gpu_count,
            ),
        )
    except Exception as e:
        raise Exception(f"Failed to create pod: {e}") from e

    return pod


def main() -> int:
    """Main entry point for creating a pod."""
    try:
        pod = create_pod()
        print("Pod created successfully!")
        print(f"Pod ID: {pod.get('id')}")
        print(f"Pod Name: {pod.get('name')}")
        print(f"Status: {pod.get('status')}")
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
