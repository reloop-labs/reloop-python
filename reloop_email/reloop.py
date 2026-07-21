from __future__ import annotations

from typing import Optional

from reloop_email.client import ReloopClient
from reloop_email.services.api_key.api_key import ApiKeyService
from reloop_email.services.contacts.contacts import ContactsService
from reloop_email.services.domain.domain import DomainService
from reloop_email.services.inbox.inbox import InboxService
from reloop_email.services.mail.mail import MailService
from reloop_email.services.webhook.webhook import WebhookService

DEFAULT_BASE_URL = "https://reloop.sh"


class Reloop:
    """Reloop Python SDK client."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        base_url: str = DEFAULT_BASE_URL,
        **kwargs: object,
    ) -> None:
        # Reject legacy aliases (Node: key/url are not accepted).
        if "key" in kwargs or "url" in kwargs:
            raise ValueError("Reloop SDK requires an api_key.")
        if api_key is None:
            raise ValueError("Reloop SDK requires an api_key.")

        self._client = ReloopClient(api_key, base_url=base_url)
        self.api_key = ApiKeyService(self._client)
        self.contacts = ContactsService(self._client)
        self.domain = DomainService(self._client)
        self.webhook = WebhookService(self._client)
        self.mail = MailService(self._client)
        self.inbox = InboxService(self._client)

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> Reloop:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
