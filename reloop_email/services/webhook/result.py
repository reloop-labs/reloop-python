from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Generic, Optional, TypeVar

from reloop_email.core.result import ReloopApiError, ReloopResult

T = TypeVar("T")


@dataclass(frozen=True)
class WebhookResult(Generic[T]):
    webhook: Optional[T]
    webhook_error: Optional[ReloopApiError]


@dataclass(frozen=True)
class WebhookListResult:
    webhooks: Optional[dict[str, Any]]
    webhook_error: Optional[ReloopApiError]


@dataclass(frozen=True)
class WebhookDeliveryListResult:
    deliveries: Optional[dict[str, Any]]
    webhook_error: Optional[ReloopApiError]


def to_webhook_result(r: ReloopResult[T]) -> WebhookResult[T]:
    return WebhookResult(None, r.error) if r.error else WebhookResult(r.response, None)


def to_webhook_list_result(r: ReloopResult[Any]) -> WebhookListResult:
    return WebhookListResult(None, r.error) if r.error else WebhookListResult(r.response, None)


def to_webhook_delivery_list_result(r: ReloopResult[Any]) -> WebhookDeliveryListResult:
    return (
        WebhookDeliveryListResult(None, r.error)
        if r.error
        else WebhookDeliveryListResult(r.response, None)
    )
