from __future__ import annotations

from typing import List, Union

from reloop_email.services.mail.errors import ReloopValidationError


def require_mail_string(value: object, field: str) -> str:
    if not isinstance(value, str) or len(value.strip()) == 0:
        raise ReloopValidationError(
            f"{field} is required and must be a non-empty string.",
            field,
        )
    return value.strip()


def require_recipient(
    value: object,
    field: str = "to",
) -> Union[str, List[str]]:
    if isinstance(value, str):
        return require_mail_string(value, field)
    if isinstance(value, list):
        if len(value) == 0:
            raise ReloopValidationError(
                f"{field} must contain at least one address.",
                field,
            )
        return [
            require_mail_string(entry, f"{field}[{index}]")
            for index, entry in enumerate(value)
        ]
    raise ReloopValidationError(
        f"{field} is required and must be a string or string array.",
        field,
    )
