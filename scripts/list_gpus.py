"""Script to list available GPU types."""

import sys
from typing import Any, List, cast

import runpod
from dotenv import load_dotenv


def get_gpus() -> List[dict[str, Any]]:
    """Get all available GPU types from RunPod.

    Returns:
        A list of GPU type objects.

    Raises:
        ValueError: If the API key is not configured.
    """
    load_dotenv()
    api_key = runpod.api_key
    if not api_key:
        from runpod_pods_demo.create_pod import load_api_key

        api_key = load_api_key()
        if not api_key:
            raise ValueError(
                "RUNPOD_API_KEY not found in .env file. "
                "Please create a .env file with your API key (see .env.example)"
            )
        runpod.api_key = api_key

    gpus: List[dict[str, Any]] = cast(List[dict[str, Any]], runpod.get_gpus())
    return gpus


def format_gpu_table(gpus: List[dict[str, Any]]) -> str:
    """Format GPU data as a table.

    Args:
        gpus: List of GPU type objects.

    Returns:
        Formatted table string.
    """
    if not gpus:
        return "No GPUs available."

    header = f"{'ID':<25} {'Name':<30} {'Memory (GB)':<12}"
    separator = "-" * len(header)

    rows = [header, separator]

    for gpu in gpus:
        gpu_id = gpu.get("id", "N/A")[:24]
        display_name = gpu.get("displayName", "N/A")[:29]
        memory = gpu.get("memoryInGb", "N/A")
        rows.append(f"{gpu_id:<30} {display_name:<30} {memory:<12}")

    return "\n".join(rows)


def main() -> int:
    """Main entry point for listing GPUs."""
    try:
        gpus = get_gpus()
        print("Available GPU Types:")
        print("=" * 70)
        print(format_gpu_table(gpus))
        print("=" * 70)
        print(f"\nTotal: {len(gpus)} GPU type(s) available")
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
