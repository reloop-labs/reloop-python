from __future__ import annotations

import re
from typing import Any

REQUEST_KEY_MAP = {
    "first_name": "firstName",
    "last_name": "lastName",
    "group_ids": "groupIds",
    "group_id": "groupId",
    "fallback_value": "fallbackValue",
    "default_subscription": "defaultSubscription",
    "channel_id": "channelId",
    "property_name": "propertyName",
    "property_type": "propertyType",
    "contact_id": "contactId",
    "rate_limit_enabled": "rateLimitEnabled",
    "user_id": "userId",
}


def for_request(parameters: dict[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}

    for key, value in parameters.items():
        if key == "unsubscribed":
            if "status" not in parameters:
                normalized["status"] = "unsubscribed" if value else "subscribed"
            continue

        api_key = REQUEST_KEY_MAP.get(key, _to_camel_case(key))
        normalized[api_key] = _normalize_value(value, is_request=True)

    return {key: value for key, value in normalized.items() if value is not None}


def for_query(options: dict[str, Any]) -> dict[str, Any]:
    return for_request(options)


def for_response(data: dict[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}

    for key, value in data.items():
        normalized[_to_snake_case(key)] = _normalize_value(value, is_request=False)

    return normalized


def _normalize_value(value: Any, *, is_request: bool) -> Any:
    if not isinstance(value, dict):
        return value

    if _is_list(value):
        return [
            _normalize_value(item, is_request=is_request) if isinstance(item, dict) else item
            for item in value
        ]

    return for_request(value) if is_request else for_response(value)


def _is_list(value: dict[str, Any]) -> bool:
    if not value:
        return True
    return list(value.keys()) == list(range(len(value)))


def _to_camel_case(key: str) -> str:
    if key in REQUEST_KEY_MAP:
        return REQUEST_KEY_MAP[key]
    if "_" not in key:
        return key
    parts = key.split("_")
    return parts[0] + "".join(part.capitalize() for part in parts[1:])


def _to_snake_case(key: str) -> str:
    if "_" in key:
        return key
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", key).lower()
