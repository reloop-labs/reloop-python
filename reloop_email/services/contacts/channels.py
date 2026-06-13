from __future__ import annotations

from typing import Any

from ..._http_client import HTTPClient
from ..._parameters import for_query, for_request
from ..._resource_factory import channel_list, contact_channel


class ContactChannelsService:
    """Manage contact channels."""

    def __init__(self, client: HTTPClient) -> None:
        self._client = client

    def create(self, **parameters: Any) -> Any:
        data = self._client.request(
            "POST",
            "/api/contacts/v1/channels/create",
            json=for_request(parameters),
        )
        return contact_channel(data)

    def list(self, **options: Any) -> Any:
        data = self._client.request(
            "GET",
            "/api/contacts/v1/channels/list",
            params=for_query(options) or None,
        )
        return channel_list(data)

    def get(self, channel_id: str) -> Any:
        data = self._client.request("GET", f"/api/contacts/v1/channels/{channel_id}")
        return contact_channel(data)

    def update(self, channel_id: str, **parameters: Any) -> Any:
        data = self._client.request(
            "PATCH",
            f"/api/contacts/v1/channels/{channel_id}",
            json=for_request(parameters),
        )
        return contact_channel(data)

    def delete(self, channel_id: str) -> Any:
        data = self._client.request(
            "DELETE",
            f"/api/contacts/v1/channels/{channel_id}",
        )
        return contact_channel(data)

    def add_contact(self, channel_id: str, **parameters: Any) -> Any:
        data = self._client.request(
            "POST",
            f"/api/contacts/channel/{channel_id}",
            json=for_request(parameters),
        )
        return contact_channel(data)

    def update_subscription(self, channel_id: str, **parameters: Any) -> Any:
        data = self._client.request(
            "PATCH",
            f"/api/contacts/channel/{channel_id}",
            json=for_request(parameters),
        )
        return contact_channel(data)
