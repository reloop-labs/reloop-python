from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Generic, Optional, TypeVar

from reloop_email.core.result import ReloopApiError, ReloopResult

T = TypeVar("T")


@dataclass(frozen=True)
class MailboxResult(Generic[T]):
    mailbox: Optional[T]
    mailbox_error: Optional[ReloopApiError]


@dataclass(frozen=True)
class MailboxListResult:
    mailboxes: Optional[list[Any]]
    mailbox_error: Optional[ReloopApiError]


def to_mailbox_result(result: ReloopResult[T]) -> MailboxResult[T]:
    return MailboxResult(None, result.error) if result.error else MailboxResult(result.response, None)


def to_mailbox_list_result(result: ReloopResult[Any]) -> MailboxListResult:
    return (
        MailboxListResult(None, result.error)
        if result.error
        else MailboxListResult(result.response, None)
    )
