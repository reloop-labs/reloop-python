from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Generic, Optional, TypeVar

from reloop_email.core.result import ReloopApiError, ReloopResult

T = TypeVar("T")


@dataclass(frozen=True)
class GroupResult(Generic[T]):
    group: Optional[T]
    group_error: Optional[ReloopApiError]


@dataclass(frozen=True)
class GroupListResult:
    groups: Optional[dict[str, Any]]
    group_error: Optional[ReloopApiError]


@dataclass(frozen=True)
class GroupContactsResult:
    contacts: Optional[dict[str, Any]]
    group_error: Optional[ReloopApiError]


def to_group_result(r: ReloopResult[T]) -> GroupResult[T]:
    return GroupResult(None, r.error) if r.error else GroupResult(r.response, None)


def to_group_list_result(r: ReloopResult[dict[str, Any]]) -> GroupListResult:
    return GroupListResult(None, r.error) if r.error else GroupListResult(r.response, None)


def to_group_contacts_result(r: ReloopResult[dict[str, Any]]) -> GroupContactsResult:
    return (
        GroupContactsResult(None, r.error)
        if r.error
        else GroupContactsResult(r.response, None)
    )
