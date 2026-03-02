"""Script to delete a RunPod template using the REST API."""

import sys

import requests

from runpod_pods_demo.create_template import load_api_key


BASE_URL = "https://rest.runpod.io/v1"


def delete_template(template_id: str) -> bool:
    """Delete a RunPod template using the REST API.

    Args:
        template_id: The ID of the template to delete.

    Returns:
        True if deletion was successful, False otherwise.
    """
    api_key = load_api_key()
    if not api_key:
        raise ValueError(
            "RUNPOD_API_KEY not found in .env file. "
            "Please create a .env file with your API key (see .env.example)"
        )

    url = f"{BASE_URL}/templates/{template_id}"

    try:
        response = requests.delete(
            url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=30,
        )
        response.raise_for_status()
        return True
    except requests.HTTPError as e:
        print(
            f"Warning: Failed to delete template '{template_id}': {e}",
            file=sys.stderr,
        )
        return False
    except requests.RequestException as e:
        print(
            f"Warning: Failed to delete template '{template_id}': {e}",
            file=sys.stderr,
        )
        return False


def delete_template_with_warning(template_id: str, template_name: str) -> None:
    """Delete a template and show warning if it fails.

    Args:
        template_id: The ID of the template to delete.
        template_name: The name of the template (for warning message).
    """
    success = delete_template(template_id)
    if not success:
        print(
            "WARNING: Template cleanup failed. Please delete template manually.",
            file=sys.stderr,
        )
        print(f"  Template ID: {template_id}", file=sys.stderr)
        print(f"  Template Name: {template_name}", file=sys.stderr)


def main() -> int:
    """Main entry point for deleting a template."""
    if len(sys.argv) < 2:
        print("Usage: python delete_template.py <template_id>", file=sys.stderr)
        return 1

    template_id = sys.argv[1]

    try:
        success = delete_template(template_id)
        if success:
            print(f"Template {template_id} deleted successfully!")
            return 0
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
