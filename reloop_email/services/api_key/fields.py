from __future__ import annotations

from reloop_email.services.api_key.errors import ReloopValidationError

NAME_MIN = 1
NAME_MAX = 255


def require_api_key_id(id_value: object, field: str = "id") -> str:
    if not isinstance(id_value, str) or len(id_value.strip()) == 0:
        raise ReloopValidationError(
            f"API key {field} is required and must be a non-empty string.",
            field,
        )
    return id_value.strip()


def require_api_key_name(name: object, field: str = "name") -> str:
    if not isinstance(name, str):
        raise ReloopValidationError(
            f"API key {field} is required and must be a string.",
            field,
        )
    trimmed = name.strip()
    if len(trimmed) < NAME_MIN:
        raise ReloopValidationError(
            f"API key {field} must be at least {NAME_MIN} character.",
            field,
        )
    if len(trimmed) > NAME_MAX:
        raise ReloopValidationError(
            f"API key {field} must be at most {NAME_MAX} characters.",
            field,
        )
    return trimmed
