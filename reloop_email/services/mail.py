from __future__ import annotations

from typing import Any

from .._http_client import HTTPClient
from .._parameters import for_snake_request
from .._resource_factory import send_mail


class MailService:
    """Send transactional email."""

    def __init__(self, client: HTTPClient) -> None:
        self._client = client

    def send(self, **parameters: Any) -> Any:
        if "from_" in parameters:
            parameters["from"] = parameters.pop("from_")

        data = self._client.request(
            "POST",
            "/api/mail/v1/send",
            json=for_snake_request(parameters),
        )
        return send_mail(data)
