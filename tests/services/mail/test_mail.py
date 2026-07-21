from __future__ import annotations

import pytest
import respx
from httpx import Response

from reloop_email import Reloop, ReloopValidationError

BASE_URL = "https://reloop.sh"
TEST_API_KEY = "rl_test"


def create_client(**options: object) -> Reloop:
    return Reloop(api_key=TEST_API_KEY, base_url=str(options.get("base_url", BASE_URL)))


@respx.mock
def test_send_post_snake_case_body() -> None:
    payload = {
        "success": True,
        "messageId": "msg_123456789",
        "status": "sent",
        "timestamp": "2026-01-01T00:00:00.000Z",
        "id": "log_123456789",
    }
    route = respx.post(f"{BASE_URL}/api/mail/v1/send").mock(
        return_value=Response(200, json=payload)
    )
    result = create_client().mail.send(
        {
            "from": "Reloop <hello@send.example.com>",
            "to": "user@example.com",
            "subject": "Welcome to Reloop",
            "html": "<p>Thanks for signing up.</p>",
            "text": "Thanks for signing up.",
            "reply_to": "support@example.com",
            "tags": [{"name": "campaign", "value": "welcome"}],
        }
    )
    assert result.email_error is None
    assert result.response == payload
    assert route.called
    request = route.calls[0].request
    assert request.headers["x-api-key"] == TEST_API_KEY
    assert request.headers["content-type"] == "application/json"
    assert request.read()  # body present


@respx.mock
def test_send_returns_email_error_without_throwing() -> None:
    respx.post(f"{BASE_URL}/api/mail/v1/send").mock(
        return_value=Response(
            400,
            json={"message": "Invalid from address", "why": "Domain not verified"},
        )
    )
    result = create_client().mail.send(
        {"from": "bad@example.com", "to": "user@example.com", "subject": "Hello"}
    )
    assert result.response is None
    assert result.email_error is not None
    assert result.email_error.status == 400
    assert result.email_error.body.message == "Invalid from address"


@respx.mock
def test_send_empty_from_throws_before_fetch() -> None:
    route = respx.post(f"{BASE_URL}/api/mail/v1/send").mock(
        return_value=Response(200, json={})
    )
    with pytest.raises(ReloopValidationError):
        create_client().mail.send(
            {"from": "", "to": "user@example.com", "subject": "Hello"}
        )
    assert not route.called


def test_mail_surface() -> None:
    reloop = create_client()
    assert callable(reloop.mail.send)
    assert not hasattr(reloop.mail, "list")
