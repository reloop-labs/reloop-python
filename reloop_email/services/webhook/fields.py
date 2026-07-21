from __future__ import annotations
from reloop_email.services.api_key.errors import ReloopValidationError
def require_webhook_id(value: object, field: str = "webhookId") -> str:
    if not isinstance(value, str) or not value.strip(): raise ReloopValidationError(f"Webhook {field} is required and must be a non-empty string.", field)
    return value.strip()
def require_delivery_id(value: object, field: str = "deliveryId") -> str:
    if not isinstance(value, str) or not value.strip(): raise ReloopValidationError(f"Webhook delivery {field} is required and must be a non-empty string.", field)
    return value.strip()
def require_page(value: object, field: str = "page") -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1: raise ReloopValidationError("list page must be an integer >= 1.", field)
    return value
def require_limit(value: object, field: str = "limit") -> int:
    if not isinstance(value, int) or isinstance(value, bool) or not 1 <= value <= 100: raise ReloopValidationError("list limit must be an integer between 1 and 100.", field)
    return value
