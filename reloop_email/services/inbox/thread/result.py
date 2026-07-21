from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Generic, Optional, TypeVar

from reloop_email.core.result import ReloopApiError, ReloopResult

T = TypeVar("T")


@dataclass(frozen=True)
class ThreadResult(Generic[T]):
    thread: Optional[T]
    thread_error: Optional[ReloopApiError]


@dataclass(frozen=True)
class ThreadListResult:
    threads: Optional[list[Any]]
    thread_error: Optional[ReloopApiError]


def to_thread_result(result: ReloopResult[T]) -> ThreadResult[T]:
    return ThreadResult(None, result.error) if result.error else ThreadResult(result.response, None)


def to_thread_list_result(result: ReloopResult[Any]) -> ThreadListResult:
    return (
        ThreadListResult(None, result.error)
        if result.error
        else ThreadListResult(result.response, None)
    )
