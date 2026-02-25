from runpod_pods_demo.list_pods import list_pods


def main() -> int:
    """Main entry point for the application."""
    return list_pods()


if __name__ == "__main__":
    raise SystemExit(main())
