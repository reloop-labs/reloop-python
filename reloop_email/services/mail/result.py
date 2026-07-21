from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from reloop_email.core.result import ReloopApiError, ReloopResult
from reloop_email.services.mail.types import SendMailResponse


@dataclass(frozen=True)
class EmailResult:
    response: Optional[SendMailResponse]
    email_error: Optional[ReloopApiError]


def to_email_result(result: ReloopResult[SendMailResponse]) -> EmailResult:
    if result.error is not None:
        return EmailResult(response=None, email_error=result.error)
    return EmailResult(response=result.response, email_error=None)
