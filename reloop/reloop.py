from __future__ import annotations

from typing import Optional

from ._http_client import HTTPClient
from .services.api_keys import ApiKeysService
from .services.contacts import ContactsService


class Reloop:
    """Reloop Python SDK client."""

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = "https://reloop.sh",
    ) -> None:
        self._http = HTTPClient(api_key, base_url)
        self.api_keys = ApiKeysService(self._http)
        self.contacts = ContactsService(self._http)

    @classmethod
    def client(
        cls,
        api_key: str,
        base_url: str = "https://reloop.sh",
    ) -> "Reloop":
        """Create a new Reloop client with the given API key."""
        return cls(api_key, base_url=base_url)

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> "Reloop":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
