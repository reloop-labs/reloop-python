from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

from reloop_email.core.result import ReloopApiError, ReloopResult
from reloop_email.services.api_key.types import ApiKeyListResponse

T = TypeVar("T")


@dataclass(frozen=True)
class ApiKeyResult(Generic[T]):
    api_key: Optional[T]
    api_key_error: Optional[ReloopApiError]


@dataclass(frozen=True)
class ApiKeyListResult:
    api_keys: Optional[ApiKeyListResponse]
    api_key_error: Optional[ReloopApiError]


def to_api_key_result(result: ReloopResult[T]) -> ApiKeyResult[T]:
    if result.error is not None:
        return ApiKeyResult(api_key=None, api_key_error=result.error)
    return ApiKeyResult(api_key=result.response, api_key_error=None)


def to_api_key_list_result(
    result: ReloopResult[ApiKeyListResponse],
) -> ApiKeyListResult:
    if result.error is not None:
        return ApiKeyListResult(api_keys=None, api_key_error=result.error)
    return ApiKeyListResult(api_keys=result.response, api_key_error=None)
