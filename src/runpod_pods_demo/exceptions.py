"""Custom exceptions for RunPod operations."""


class PodNotFoundError(Exception):
    """Raised when the specified pod does not exist."""

    pass


class PodTimeoutError(Exception):
    """Raised when pod fails to reach RUNNING state within timeout."""

    pass


class PodFailedError(Exception):
    """Raised when pod enters a failed terminal state."""

    pass
