"""PodManager class for managing RunPod pods."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

import runpod

from runpod_pods_demo.exceptions import (
    PodFailedError,
    PodNotFoundError,
    PodTimeoutError,
)


@dataclass
class Pod:
    """Represents a RunPod pod with essential information.

    Attributes:
        id: The unique identifier for the pod.
        name: The user-provided name for the pod.
        status: The desired status of the pod (e.g., RUNNING, CREATING).
        gpu_count: The number of GPUs allocated to the pod.
        gpu_type: The GPU model (e.g., "NVIDIA A40").
        image_name: The Docker image URI used by the pod.
        created_at: When the pod was created (if available).
        uptime_seconds: How long the pod has been running.
        container_disk_gb: Container disk size in GB.
        volume_gb: Volume size in GB.
        volume_mount_path: Volume mount location.
        ports: List of exposed ports.
        env_vars: Environment variables as key-value pairs.
        runtime_info: Full runtime object from API.
        raw_data: Complete API response for unmapped fields.
    """

    id: str
    name: str
    status: str
    gpu_count: int
    gpu_type: str
    image_name: str
    created_at: Optional[datetime] = None
    uptime_seconds: int = 0
    container_disk_gb: Optional[int] = None
    volume_gb: Optional[int] = None
    volume_mount_path: Optional[str] = None
    ports: Optional[list[str]] = None
    env_vars: dict[str, str] = field(default_factory=dict)
    runtime_info: Optional[dict[str, Any]] = None
    raw_data: dict[str, Any] = field(default_factory=dict)


class PodManager:
    """Manages RunPod pods: create, list, and terminate."""

    def __init__(self, api_key: str):
        """Initialize PodManager with API key.

        Args:
            api_key: RunPod API key for authentication.

        Note:
            Caller must provide valid API key. No automatic .env loading.
        """
        self.api_key = api_key
        self._pods_created: dict[str, Pod] = {}

    def _get_pod_from_api(self, pod_id: str) -> dict[str, Any]:
        """Fetch pod details from RunPod API.

        Args:
            pod_id: The ID of the pod to fetch.

        Returns:
            Raw API response dict.

        Raises:
            Exception: If API call fails.
        """
        runpod.api_key = self.api_key
        try:
            pod: dict[str, Any] = runpod.get_pod(pod_id)
            return pod
        except Exception as e:
            raise Exception(f"Failed to get pod status: {e}") from e

    def _pod_dict_to_dataclass(self, pod_dict: dict[str, Any]) -> Pod:
        """Convert API response dict to Pod dataclass.

        Args:
            pod_dict: Raw API response from RunPod.

        Returns:
            Pod dataclass with mapped fields.
        """
        runtime = pod_dict.get("runtime") or {}

        return Pod(
            id=pod_dict.get("id", ""),
            name=pod_dict.get("name", ""),
            status=pod_dict.get("desiredStatus", pod_dict.get("status", "UNKNOWN")),
            gpu_count=pod_dict.get("gpuCount", 0),
            gpu_type=pod_dict.get("gpuTypeId", ""),
            image_name=pod_dict.get("imageName", ""),
            created_at=None,
            uptime_seconds=runtime.get("uptimeInSeconds", 0),
            container_disk_gb=pod_dict.get("containerDiskInGb"),
            volume_gb=pod_dict.get("volumeInGb"),
            volume_mount_path=pod_dict.get("volumeMountPath"),
            ports=pod_dict.get("ports"),
            env_vars=pod_dict.get("env", {}),
            runtime_info=runtime if runtime else None,
            raw_data=pod_dict,
        )

    def _wait_for_pod_ready(
        self,
        pod_id: str,
        poll_interval: int = 5,
        timeout: int = 600,
    ) -> dict[str, Any]:
        """Poll pod status until RUNNING or terminal state.

        Args:
            pod_id: The ID of the pod to wait for.
            poll_interval: How often to check pod status (in seconds).
            timeout: Maximum time to wait (in seconds).

        Returns:
            Raw API response dict when pod reaches RUNNING.

        Raises:
            PodTimeoutError: If pod doesn't reach RUNNING within timeout.
            PodFailedError: If pod enters terminal failure state.
        """
        import time

        start_time = time.time()
        terminal_states = {"EXITED", "FAILED", "DEAD", "TERMINATED", "CANCELLED"}

        while True:
            elapsed = time.time() - start_time
            if elapsed >= timeout:
                raise PodTimeoutError(
                    f"Pod '{pod_id}' did not reach RUNNING state within {timeout} seconds"
                )

            pod_dict = self._get_pod_from_api(pod_id)
            desired_status = pod_dict.get(
                "desiredStatus", pod_dict.get("status", "UNKNOWN")
            )
            runtime = pod_dict.get("runtime")

            if desired_status == "RUNNING" and runtime is not None:
                return pod_dict

            if desired_status in terminal_states:
                raise PodFailedError(
                    f"Pod '{pod_id}' entered failed state: {desired_status}"
                )

            time.sleep(poll_interval)

    def create_pod(
        self,
        name: str,
        gpu_type_id: str,
        image_name: str,
        gpu_count: int = 1,
        container_disk_in_gb: Optional[int] = None,
        volume_in_gb: Optional[int] = None,
        volume_mount_path: Optional[str] = None,
        ports: Optional[str] = None,
        env: Optional[dict[str, str]] = None,
        poll_interval: int = 5,
        timeout: int = 600,
    ) -> Pod:
        """Create a pod and wait for it to reach RUNNING state.

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
            poll_interval: How often to check pod status (in seconds).
            timeout: Maximum time to wait (in seconds).

        Returns:
            Pod object with RUNNING status.

        Raises:
            ValueError: If API key not configured or invalid parameters.
            PodTimeoutError: If pod doesn't reach RUNNING within timeout.
            PodFailedError: If pod enters failed state.
            Exception: If pod creation fails.
        """
        runpod.api_key = self.api_key

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
            pod_args["volume_mount_path"] = volume_mount_path or "/workspace"

        if ports:
            pod_args["ports"] = ports

        if env:
            pod_args["env"] = env

        try:
            created_pod: dict[str, Any] = runpod.create_pod(**pod_args)
        except Exception as e:
            raise Exception(f"Failed to create pod: {e}") from e

        pod_id = created_pod.get("id")
        if not pod_id:
            raise Exception("Pod creation returned no ID")

        ready_pod_dict = self._wait_for_pod_ready(pod_id, poll_interval, timeout)
        pod = self._pod_dict_to_dataclass(ready_pod_dict)
        self._pods_created[pod.id] = pod

        return pod

    def list_pods(self) -> list[Pod]:
        """List pods created by this PodManager instance.

        Returns:
            List of Pod objects created by this instance.
            Returns empty list if no pods created yet.
        """
        return list(self._pods_created.values())

    def terminate_pod(self, pod_id: str) -> bool:
        """Terminate a pod and remove from registry.

        Args:
            pod_id: The ID of the pod to terminate.

        Returns:
            True if termination successful.

        Raises:
            PodNotFoundError: If pod not in registry.
            Exception: If termination fails.
        """
        if pod_id not in self._pods_created:
            raise PodNotFoundError(f"Pod '{pod_id}' not found in registry")

        runpod.api_key = self.api_key

        try:
            runpod.terminate_pod(pod_id)
        except Exception as e:
            error_msg = str(e).lower()
            if "not found" in error_msg or "404" in error_msg:
                del self._pods_created[pod_id]
                raise PodNotFoundError(f"Pod '{pod_id}' not found") from e
            raise Exception(f"Failed to terminate pod: {e}") from e

        del self._pods_created[pod_id]
        return True
