"""Script to create a RunPod template."""

import json
import os
import random
import string
import sys
from typing import Any, Optional

import runpod
from dotenv import load_dotenv


DEFAULT_CONTAINER_DISK_IN_GB = 10
DEFAULT_VOLUME_IN_GB = 0
DEFAULT_VOLUME_MOUNT_PATH = "/workspace"
DEFAULT_PORTS = ""
DEFAULT_TEMPLATE_ENV: dict[str, str] = {}


def generate_random_name(prefix: str = "template") -> str:
    """Generate a random unique name for the template."""
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{prefix}-{suffix}"


def load_api_key() -> Optional[str]:
    """Load and validate API key from .env file."""
    load_dotenv()
    api_key = os.getenv("RUNPOD_API_KEY")
    if not api_key:
        return None
    return api_key


def load_template_config() -> dict[str, Any]:
    """Load template configuration from .env file."""
    load_dotenv()

    config: dict[str, Any] = {}

    image_name = os.getenv("IMAGE_NAME")
    if image_name:
        config["image_name"] = image_name

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

    template_env = os.getenv("TEMPLATE_ENV")
    if template_env:
        try:
            config["env"] = json.loads(template_env)
        except json.JSONDecodeError:
            config["env"] = DEFAULT_TEMPLATE_ENV
    else:
        config["env"] = DEFAULT_TEMPLATE_ENV

    return config


def create_template(name: Optional[str] = None) -> dict[str, Any]:
    """Create a RunPod template with configuration from .env file.

    Args:
        name: Optional name for the template. If not provided, a random
            unique name will be generated.

    Returns:
        The created template object containing an ID.

    Raises:
        ValueError: If the API key or required configuration is not set.
        Exception: If template creation fails.
    """
    api_key = load_api_key()
    if not api_key:
        raise ValueError(
            "RUNPOD_API_KEY not found in .env file. "
            "Please create a .env file with your API key (see .env.example)"
        )

    runpod.api_key = api_key

    config = load_template_config()

    if not config.get("image_name"):
        raise ValueError(
            "IMAGE_NAME not found in .env file. "
            "Please configure your template settings (see .env.example)"
        )

    template_name = name if name else generate_random_name("demo-template")

    template_args: dict[str, Any] = {
        "name": template_name,
        "image_name": config["image_name"],
        "container_disk_in_gb": config["container_disk_in_gb"],
    }

    if config.get("volume_in_gb", 0) > 0:
        template_args["volume_in_gb"] = config["volume_in_gb"]
        template_args["volume_mount_path"] = config["volume_mount_path"]

    if config.get("ports"):
        template_args["ports"] = config["ports"]

    if config.get("env"):
        template_args["env"] = config["env"]

    try:
        template: dict[str, Any] = runpod.create_template(**template_args)
    except Exception as e:
        raise Exception(f"Failed to create template: {e}") from e

    return template


def main() -> int:
    """Main entry point for creating a template."""
    try:
        template = create_template()
        print("Template created successfully!")
        print(f"Template ID: {template.get('id')}")
        print(f"Template Name: {template.get('name')}")
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
