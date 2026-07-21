from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Generic, Optional, TypeVar

from reloop_email.core.result import ReloopApiError, ReloopResult

T = TypeVar("T")


@dataclass(frozen=True)
class MessageResult(Generic[T]):
    message: Optional[T]
    message_error: Optional[ReloopApiError]


@dataclass(frozen=True)
class MessageListResult:
    messages: Optional[list[Any]]
    message_error: Optional[ReloopApiError]


def to_message_result(result: ReloopResult[T]) -> MessageResult[T]:
    return MessageResult(None, result.error) if result.error else MessageResult(result.response, None)


def to_message_list_result(result: ReloopResult[Any]) -> MessageListResult:
    return (
        MessageListResult(None, result.error)
        if result.error
        else MessageListResult(result.response, None)
    )
