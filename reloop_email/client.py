from __future__ import annotations

from typing import Any, Mapping, Optional, TypeVar, Union

import httpx

from .core.result import ReloopApiError, ReloopApiErrorBody, ReloopResult, err, ok

T = TypeVar("T")

DEFAULT_BASE_URL = "https://reloop.sh"


class ReloopClient:
    """Internal HTTP transport. Not part of the public constructable surface."""

    def __init__(self, api_key: str, *, base_url: str = DEFAULT_BASE_URL) -> None:
        key = api_key.strip() if isinstance(api_key, str) else ""
        if not key:
            raise ValueError("Reloop SDK requires an api_key.")
        self._api_key = key
        self._base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self._http = httpx.Client(
            base_url=self._base_url,
            headers={
                "x-api-key": self._api_key,
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            timeout=30.0,
        )

    def fetch(
        self,
        path: str,
        *,
        method: str = "GET",
        json: Optional[Mapping[str, Any]] = None,
        params: Optional[Mapping[str, Union[str, int, float, bool]]] = None,
    ) -> ReloopResult[Any]:
        try:
            response = self._http.request(
                method,
                path,
                json=dict(json) if json is not None else None,
                params=dict(params) if params is not None else None,
            )
        except httpx.RequestError as cause:
            message = str(cause) if str(cause) else "Network request failed"
            return err(ReloopApiError(0, "Network Error", ReloopApiErrorBody(message=message)))

        if response.status_code >= 400:
            body: ReloopApiErrorBody = ReloopApiErrorBody()
            try:
                data = response.json()
                body = ReloopApiErrorBody.from_mapping(data)
            except (ValueError, TypeError):
                pass
            return err(
                ReloopApiError(
                    response.status_code,
                    response.reason_phrase or "",
                    body,
                )
            )

        if response.status_code == 204 or not response.content:
            return ok({})

        try:
            return ok(response.json())
        except (ValueError, TypeError):
            return ok({})

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> ReloopClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
