from __future__ import annotations

from typing import Any, Optional

from .._http_client import HTTPClient
from .._parameters import for_query, for_request
from .._resource_factory import api_key, api_key_list


class ApiKeysService:
    """Manage API keys."""

    def __init__(self, client: HTTPClient) -> None:
        self._client = client

    def create(self, **parameters: Any) -> Any:
        data = self._client.request(
            "POST",
            "/api/api-key/v1/",
            json=for_request(parameters),
        )
        return api_key(data)

    def list(self, **options: Any) -> Any:
        data = self._client.request(
            "GET",
            "/api/api-key/v1/",
            params=for_query(options) or None,
        )
        return api_key_list(data)

    def get(self, api_key_id: str) -> Any:
        data = self._client.request("GET", f"/api/api-key/v1/{api_key_id}")
        return api_key(data)

    def update(self, api_key_id: str, **parameters: Any) -> Any:
        data = self._client.request(
            "PATCH",
            f"/api/api-key/v1/{api_key_id}",
            json=for_request(parameters),
        )
        return api_key(data)

    def delete(self, api_key_id: str) -> Any:
        data = self._client.request("DELETE", f"/api/api-key/v1/{api_key_id}")
        return api_key(data)

    def rotate(self, api_key_id: str) -> Any:
        data = self._client.request("POST", f"/api/api-key/v1/rotate/{api_key_id}")
        return api_key(data)

    def enable(self, api_key_id: str) -> Any:
        data = self._client.request("POST", f"/api/api-key/v1/enable/{api_key_id}")
        return api_key(data)

    def disable(self, api_key_id: str) -> Any:
        data = self._client.request("POST", f"/api/api-key/v1/disable/{api_key_id}")
        return api_key(data)
