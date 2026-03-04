"""Script to create a RunPod pod."""

import json
import os
import sys
from typing import Any, Optional, cast

import runpod
from dotenv import load_dotenv


POD_NAME = "pod-lifecycle-demo"
GPU_TYPE_ID = "NVIDIA A40"
IMAGE_NAME = "pytorch/pytorch:latest"
GPU_COUNT = 1
DEFAULT_CONTAINER_DISK_IN_GB = 10
DEFAULT_VOLUME_IN_GB = 0
DEFAULT_VOLUME_MOUNT_PATH = "/workspace"
DEFAULT_PORTS = ""
DEFAULT_POD_ENV: dict[str, str] = {}


def load_api_key() -> Optional[str]:
    """Load and validate API key from .env file."""
    load_dotenv()
    api_key = os.getenv("RUNPOD_API_KEY")
    if not api_key:
        return None
    return api_key


def load_pod_config() -> dict[str, Any]:
    """Load pod configuration from .env file."""
    load_dotenv()

    config: dict[str, Any] = {}

    gpu_type_id = os.getenv("GPU_TYPE_ID")
    if gpu_type_id:
        config["gpu_type_id"] = gpu_type_id

    image_name = os.getenv("IMAGE_NAME")
    if image_name:
        config["image_name"] = image_name

    gpu_count = os.getenv("GPU_COUNT")
    config["gpu_count"] = int(gpu_count) if gpu_count else GPU_COUNT

    container_disk = os.getenv("CONTAINER_DISK_IN_GB")
    config["container_disk_in_gb"] = (
        int(container_disk) if container_disk else DEFAULT_CONTAINER_DISK_IN_GB
    )

    volume_in_gb = os.getenv("VOLUME_IN_GB")
    config["volume_in_gb"] = int(volume_in_gb) if volume_in_gb else DEFAULT_VOLUME_IN_GB

    volume_mount_path = os.getenv("VOLUME_MOUNT_PATH")
    config["volume_mount_path"] = (
        volume_mount_path if volume_mount_path else DEFAULT_VOLUME_MOUNT_PATH
    )

    ports = os.getenv("PORTS")
    config["ports"] = ports if ports else DEFAULT_PORTS

    pod_env = os.getenv("POD_ENV")
    if pod_env:
        try:
            config["env"] = json.loads(pod_env)
        except json.JSONDecodeError:
            config["env"] = DEFAULT_POD_ENV
    else:
        config["env"] = DEFAULT_POD_ENV

    return config


def create_pod(
    name: str = POD_NAME,
    gpu_type_id: str = GPU_TYPE_ID,
    image_name: str = IMAGE_NAME,
    gpu_count: int = GPU_COUNT,
    container_disk_in_gb: Optional[int] = None,
    volume_in_gb: Optional[int] = None,
    volume_mount_path: Optional[str] = None,
    ports: Optional[str] = None,
    env: Optional[dict[str, str]] = None,
) -> dict[str, Any]:
    """Create a RunPod pod with the specified configuration.

    Args:
        name: The name for the pod.
        gpu_type_id: The GPU type ID (e.g., "NVIDIA A40").
        image_name: The Docker image to use.
        gpu_count: The number of GPUs to request.
        container_disk_in_gb: Container disk size in GB.
        volume_in_gb: Volume size in GB.
        volume_mount_path: Volume mount path.
        ports: Ports to expose (e.g., "22/tcp,8888/http").
        env: Environment variables as dict.

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

    pod_args: dict[str, Any] = {
        "name": name,
        "image_name": image_name,
        "gpu_type_id": gpu_type_id,
        "gpu_count": gpu_count,
    }

    if container_disk_in_gb:
        pod_args["container_disk_in_gb"] = container_disk_in_gb

    if volume_in_gb and volume_in_gb > 0:
        pod_args["volume_in_gb"] = volume_in_gb
        pod_args["volume_mount_path"] = volume_mount_path or DEFAULT_VOLUME_MOUNT_PATH

    if ports:
        pod_args["ports"] = ports

    if env:
        pod_args["env"] = env

    try:
        pod: dict[str, Any] = cast(
            dict[str, Any],
            runpod.create_pod(**pod_args),
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
