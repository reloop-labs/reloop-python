from __future__ import annotations

from typing import Any, Optional

import httpx

from .errors import ReloopApiError, ReloopNetworkError


class HTTPClient:
    """Internal HTTP transport for the Reloop SDK."""

    def __init__(self, api_key: str, base_url: str = "https://reloop.sh") -> None:
        if not api_key:
            raise ValueError("Reloop SDK requires an api_key.")

        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self._http = httpx.Client(
            base_url=self.base_url,
            headers={
                "x-api-key": self.api_key,
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            timeout=30.0,
        )

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        try:
            response = self._http.request(method, path, params=params, json=json)
        except httpx.RequestError as exc:
            raise ReloopNetworkError(f"Reloop network error: {exc}") from exc

        if response.status_code >= 400:
            body: Any = None
            try:
                body = response.json()
            except ValueError:
                body = response.text

            message = response.reason_phrase
            if isinstance(body, dict) and body.get("message"):
                message = str(body["message"])

            raise ReloopApiError(
                f"Reloop API error ({response.status_code}): {message}",
                status_code=response.status_code,
                body=body,
            )

        if response.status_code == 204 or not response.content:
            return {}

        data = response.json()
        if not isinstance(data, dict):
            return {"data": data}
        return data

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> "HTTPClient":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
