from __future__ import annotations

from reloop_email.client import ReloopClient
from reloop_email.services.mail.result import EmailResult
from reloop_email.services.mail.send.send import send_email
from reloop_email.services.mail.types import SendMailParams


class MailService:
    def __init__(self, client: ReloopClient) -> None:
        self._client = client

    def send(self, params: SendMailParams) -> EmailResult:
        return send_email(self._client, params)
