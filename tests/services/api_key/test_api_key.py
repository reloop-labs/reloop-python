from __future__ import annotations

import pytest
import respx
from httpx import Response

from reloop_email import Reloop, ReloopValidationError

BASE_URL = "https://reloop.sh"
TEST_API_KEY = "rl_test"


def create_client() -> Reloop:
    return Reloop(api_key=TEST_API_KEY, base_url=BASE_URL)


@respx.mock
def test_create_api_key() -> None:
    payload = {
        "id": "key_1",
        "name": "Prod",
        "key": "rl_secret",
        "enabled": True,
        "createdAt": "2026-01-01T00:00:00.000Z",
        "updatedAt": "2026-01-01T00:00:00.000Z",
        "permissions": None,
        "object": "api_key",
        "event": "created",
    }
    route = respx.post(f"{BASE_URL}/api/api-key/v1/").mock(
        return_value=Response(200, json=payload)
    )
    result = create_client().api_key.create({"name": "  Prod  "})
    assert result.api_key_error is None
    assert result.api_key == payload
    assert route.called
    assert b'"name":"Prod"' in route.calls[0].request.content


@respx.mock
def test_create_api_error() -> None:
    respx.post(f"{BASE_URL}/api/api-key/v1/").mock(
        return_value=Response(400, json={"message": "bad"})
    )
    result = create_client().api_key.create({"name": "x"})
    assert result.api_key is None
    assert result.api_key_error is not None
    assert result.api_key_error.status == 400


@respx.mock
def test_create_validation_no_fetch() -> None:
    route = respx.post(f"{BASE_URL}/api/api-key/v1/").mock(
        return_value=Response(200, json={})
    )
    with pytest.raises(ReloopValidationError):
        create_client().api_key.create({"name": ""})
    assert not route.called


def test_api_key_surface() -> None:
    svc = create_client().api_key
    for name in ("create", "list", "get", "update", "delete", "rotate", "enable", "disable"):
        assert callable(getattr(svc, name))
    assert not hasattr(svc, "pause")
