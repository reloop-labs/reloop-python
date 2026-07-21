from __future__ import annotations

from typing import Any, cast

from reloop_email.client import ReloopClient
from reloop_email.core.result import ReloopResult
from reloop_email.services.mail.errors import ReloopValidationError
from reloop_email.services.mail.fields import require_mail_string, require_recipient
from reloop_email.services.mail.paths import mail_send_path
from reloop_email.services.mail.result import EmailResult, to_email_result
from reloop_email.services.mail.types import SendMailParams, SendMailResponse


def validate_send_params(params: object) -> SendMailParams:
    if params is None or not isinstance(params, dict):
        raise ReloopValidationError(
            "send params are required and must be an object.",
            "params",
        )
    raw = cast(dict[str, Any], params)
    body: dict[str, Any] = dict(raw)
    body["from"] = require_mail_string(raw.get("from"), "from")
    body["to"] = require_recipient(raw.get("to"), "to")
    body["subject"] = require_mail_string(raw.get("subject"), "subject")
    return cast(SendMailParams, body)


def send_email(client: ReloopClient, params: SendMailParams) -> EmailResult:
    body = validate_send_params(params)
    result = client.fetch(mail_send_path(), method="POST", json=cast(dict[str, Any], body))
    typed = ReloopResult[SendMailResponse](response=result.response, error=result.error)
    return to_email_result(typed)
