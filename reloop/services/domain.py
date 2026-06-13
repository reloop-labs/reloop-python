from __future__ import annotations

from typing import Any

from .._http_client import HTTPClient
from .._parameters import for_query, for_snake_request
from .._resource_factory import (
    domain,
    domain_list,
    domain_nameservers,
    domain_status,
    forward_dns_response,
)


class DomainService:
    """Manage sending and receiving domains."""

    def __init__(self, client: HTTPClient) -> None:
        self._client = client

    def create(self, **parameters: Any) -> Any:
        data = self._client.request(
            "POST",
            "/api/domain/v1/create",
            json=for_snake_request(parameters),
        )
        return domain(data)

    def list(self, **options: Any) -> Any:
        data = self._client.request(
            "GET",
            "/api/domain/v1/list",
            params=for_query(options) or None,
        )
        return domain_list(data)

    def get(self, domain_id: str) -> Any:
        data = self._client.request("GET", f"/api/domain/v1/{domain_id}")
        return domain(data)

    def get_nameservers(self, domain_id: str) -> Any:
        data = self._client.request(
            "GET",
            f"/api/domain/v1/nameservers/{domain_id}",
        )
        return domain_nameservers(data)

    def update(self, domain_id: str, **parameters: Any) -> Any:
        data = self._client.request(
            "PATCH",
            f"/api/domain/v1/{domain_id}",
            json=for_snake_request(parameters),
        )
        return domain(data)

    def delete(self, domain_id: str) -> Any:
        data = self._client.request("DELETE", f"/api/domain/v1/{domain_id}")
        return domain(data)

    def verify(self, domain_id: str) -> Any:
        data = self._client.request("POST", f"/api/domain/v1/verify/{domain_id}")
        return domain_status(data)

    def forward_dns(self, domain_id: str, *, email: str) -> Any:
        data = self._client.request(
            "POST",
            f"/api/domain/v1/verify/{domain_id}/forward-dns",
            json={"email": email},
        )
        return forward_dns_response(data)
