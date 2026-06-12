from typing import Any, Optional


class ReloopError(Exception):
    """Base exception for all Reloop SDK errors."""


class ReloopApiError(ReloopError):
    """Raised when the Reloop API returns an error response."""

    def __init__(
        self,
        message: str,
        *,
        status_code: Optional[int] = None,
        body: Optional[Any] = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.body = body

    def __repr__(self) -> str:
        return f"ReloopApiError(message={self.args[0]!r}, status_code={self.status_code!r})"


class ReloopNetworkError(ReloopError):
    """Raised when a network error occurs while communicating with Reloop."""
