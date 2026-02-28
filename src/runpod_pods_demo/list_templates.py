"""Script to list official RunPod Docker images from templates."""

import os
import sys
from typing import Any, Optional

import requests
from dotenv import load_dotenv

RUNPOD_API_BASE = "https://rest.runpod.io"


def load_api_key() -> Optional[str]:
    """Load and validate API key from .env file."""
    load_dotenv()
    api_key = os.getenv("RUNPOD_API_KEY")
    if not api_key:
        return None
    return api_key


def get_official_images(api_key: str) -> list[dict[str, Any]]:
    """Fetch official RunPod images from templates API."""
    url = f"{RUNPOD_API_BASE}/v1/templates"
    params = {"includeRunpodTemplates": "true"}

    headers = {"Authorization": f"Bearer {api_key}"}

    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()

    if isinstance(data, list):
        templates = data
    else:
        templates = data.get("templates", [])

    official_images = [t for t in templates if t.get("isRunpod", False)]

    return official_images


def print_images_table(images: list[dict[str, Any]]) -> None:
    """Print official images in a formatted table."""
    if not images:
        print("No official RunPod images found.")
        return

    name_width = max(len(i.get("name", "N/A")) for i in images)
    name_width = max(name_width, 12)

    image_width = max(len(i.get("imageName", "N/A")) for i in images)
    image_width = max(image_width, 15)

    header = f"{'TEMPLATE NAME':<{name_width}} {'DOCKER IMAGE'}"
    separator = "-" * len(header)

    print(header)
    print(separator)

    for image in images:
        name = image.get("name", "N/A")
        image_name = image.get("imageName", "N/A")
        print(f"{name:<{name_width}} {image_name}")


def list_official_images() -> int:
    """List all official RunPod Docker images."""
    api_key = load_api_key()
    if not api_key:
        print("Error: RUNPOD_API_KEY not found in .env file.", file=sys.stderr)
        print(
            "Please create a .env file with your API key (see .env.example)",
            file=sys.stderr,
        )
        return 1

    try:
        images = get_official_images(api_key)
    except requests.RequestException as e:
        print(f"Error fetching templates: {e}", file=sys.stderr)
        return 1

    print_images_table(images)
    return 0


if __name__ == "__main__":
    sys.exit(list_official_images())
