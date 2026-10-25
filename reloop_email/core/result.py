from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Generic, Optional, TypeVar, Union

T = TypeVar("T")


@dataclass
class ReloopApiErrorBody:
    message: Optional[str] = None
    why: Optional[str] = None
    fix: Optional[str] = None
    link: Optional[str] = None
    # Deprecated: the API returns `fix`. Kept as an alias of `fix`.
    tip: Optional[str] = None
    extra: Optional[dict[str, Any]] = None

    @classmethod
    def from_mapping(cls, data: Any) -> ReloopApiErrorBody:
        if not isinstance(data, dict):
            return cls()
        known = {"message", "why", "fix", "tip", "link"}
        extra = {k: v for k, v in data.items() if k not in known}
        raw_fix = data.get("fix", data.get("tip"))
        fix = raw_fix if isinstance(raw_fix, str) else None
        return cls(
            message=data.get("message") if isinstance(data.get("message"), str) else None,
            why=data.get("why") if isinstance(data.get("why"), str) else None,
            fix=fix,
            tip=fix,
            link=data.get("link") if isinstance(data.get("link"), str) else None,
            extra=extra or None,
        )


class ReloopApiError(Exception):
    def __init__(
        self,
        status: int,
        status_text: str,
        body: Optional[Union[ReloopApiErrorBody, dict[str, Any]]] = None,
    ) -> None:
        if isinstance(body, ReloopApiErrorBody):
            parsed = body
        elif isinstance(body, dict):
            parsed = ReloopApiErrorBody.from_mapping(body)
        else:
            parsed = ReloopApiErrorBody()

        message = (
            parsed.message
            if isinstance(parsed.message, str)
            else f"Reloop API Error: {status} {status_text}"
        )
        super().__init__(message)
        self.status = status
        self.status_text = status_text
        self.body = parsed


@dataclass(frozen=True)
class ReloopResult(Generic[T]):
    response: Optional[T]
    error: Optional[ReloopApiError]


def ok(response: T) -> ReloopResult[T]:
    return ReloopResult(response=response, error=None)


def err(error: ReloopApiError) -> ReloopResult[T]:
    return ReloopResult(response=None, error=error)
