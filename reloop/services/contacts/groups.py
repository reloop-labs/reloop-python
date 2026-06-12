from __future__ import annotations

from typing import Any

from ..._http_client import HTTPClient
from ..._parameters import for_query, for_request
from ..._resource_factory import contact, contact_group


class ContactGroupsService:
    """Manage contact group membership."""

    def __init__(self, client: HTTPClient) -> None:
        self._client = client

    def add_contact(self, group_id: str, **parameters: Any) -> Any:
        data = self._client.request(
            "POST",
            f"/api/contacts/group/{group_id}",
            json=for_request(parameters),
        )
        return contact(data)

    def remove_contact(self, group_id: str, **parameters: Any) -> Any:
        data = self._client.request(
            "DELETE",
            f"/api/contacts/group/{group_id}",
            json=for_request(parameters),
        )
        return contact(data)

    def list_contacts(self, group_id: str, **options: Any) -> Any:
        data = self._client.request(
            "GET",
            f"/api/contacts/v1/groups/{group_id}/contacts",
            params=for_query(options) or None,
        )
        return contact_group(data)
