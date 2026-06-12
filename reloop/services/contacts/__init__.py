from __future__ import annotations

from typing import Any

from ..._http_client import HTTPClient
from ..._parameters import for_query, for_request
from ..._resource_factory import (
    contact,
    contact_group,
    contact_list,
    contact_property,
    group_list,
    property_list,
)
from .channels import ContactChannelsService
from .groups import ContactGroupsService


class ContactsService:
    """Manage contacts, properties, and groups."""

    def __init__(self, client: HTTPClient) -> None:
        self._client = client
        self.groups = ContactGroupsService(client)
        self.channels = ContactChannelsService(client)

    def create(self, **parameters: Any) -> Any:
        data = self._client.request(
            "POST",
            "/api/contacts/create",
            json=for_request(parameters),
        )
        return contact(data)

    def get(self, contact_id: str) -> Any:
        data = self._client.request("GET", f"/api/contacts/retrieve/{contact_id}")
        return contact(data)

    def list(self, **options: Any) -> Any:
        group_id = options.get("group_id") or options.get("groupId")

        if group_id:
            filtered = {
                key: value
                for key, value in options.items()
                if key not in ("group_id", "groupId")
            }
            return self.groups.list_contacts(group_id, **filtered)

        data = self._client.request(
            "GET",
            "/api/contacts/list",
            params=for_query(options) or None,
        )
        return contact_list(data)

    def update(self, contact_id: str, **parameters: Any) -> Any:
        data = self._client.request(
            "PATCH",
            f"/api/contacts/{contact_id}",
            json=for_request(parameters),
        )
        return contact(data)

    def delete(self, contact_id: str) -> Any:
        data = self._client.request("DELETE", f"/api/contacts/{contact_id}")
        return contact(data)

    def create_property(self, **parameters: Any) -> Any:
        data = self._client.request(
            "POST",
            "/api/contacts/v1/properties/create",
            json=for_request(parameters),
        )
        return contact_property(data)

    def list_properties(self, **options: Any) -> Any:
        data = self._client.request(
            "GET",
            "/api/contacts/v1/properties/list",
            params=for_query(options) or None,
        )
        return property_list(data)

    def update_property(self, property_id: str, **parameters: Any) -> Any:
        data = self._client.request(
            "PATCH",
            f"/api/contacts/v1/properties/{property_id}",
            json=for_request(parameters),
        )
        return contact_property(data)

    def delete_property(self, property_id: str) -> Any:
        data = self._client.request(
            "DELETE",
            f"/api/contacts/v1/properties/{property_id}",
        )
        return contact_property(data)

    def create_group(self, **parameters: Any) -> Any:
        data = self._client.request(
            "POST",
            "/api/contacts/v1/groups/create",
            json=for_request(parameters),
        )
        return contact_group(data)

    def list_groups(self, **options: Any) -> Any:
        data = self._client.request(
            "GET",
            "/api/contacts/v1/groups/list",
            params=for_query(options) or None,
        )
        return group_list(data)

    def get_group(self, group_id: str) -> Any:
        data = self._client.request("GET", f"/api/contacts/v1/groups/{group_id}")
        return contact_group(data)

    def update_group(self, group_id: str, **parameters: Any) -> Any:
        data = self._client.request(
            "PATCH",
            f"/api/contacts/v1/groups/{group_id}",
            json=for_request(parameters),
        )
        return contact_group(data)

    def delete_group(self, group_id: str) -> Any:
        data = self._client.request(
            "DELETE",
            f"/api/contacts/v1/groups/{group_id}",
        )
        return contact_group(data)
