from __future__ import annotations

import pytest
import respx
from httpx import Response

from reloop_email import Reloop


def test_constructs_with_api_key_only() -> None:
    reloop = Reloop(api_key="rl_test")
    assert callable(reloop.api_key.create)
    assert callable(reloop.mail.send)
    assert callable(reloop.inbox.mailboxes.list)
    assert callable(reloop.webhook.create)
    reloop.close()


def test_missing_api_key_throws() -> None:
    with pytest.raises(ValueError, match="api_key"):
        Reloop()


def test_empty_api_key_throws() -> None:
    with pytest.raises(ValueError, match="api_key"):
        Reloop(api_key="")


def test_whitespace_api_key_throws() -> None:
    with pytest.raises(ValueError, match="api_key"):
        Reloop(api_key="   ")


def test_key_alias_rejected() -> None:
    with pytest.raises(ValueError, match="api_key"):
        Reloop(key="rl_legacy")  # type: ignore[call-arg]


@respx.mock
def test_base_url_used() -> None:
    respx.post("https://custom.example/api/mail/v1/send").mock(
        return_value=Response(
            200,
            json={
                "success": True,
                "messageId": "msg_1",
                "status": "sent",
                "timestamp": "2026-01-01T00:00:00.000Z",
                "id": "log_1",
            },
        )
    )
    reloop = Reloop(api_key="rl_test", base_url="https://custom.example")
    reloop.mail.send({"from": "a@b.com", "to": "c@d.com", "subject": "Hi"})
    reloop.close()


@respx.mock
def test_url_alias_does_not_set_base() -> None:
    route = respx.post("https://reloop.sh/api/mail/v1/send").mock(
        return_value=Response(
            200,
            json={
                "success": True,
                "messageId": "msg_1",
                "status": "sent",
                "timestamp": "2026-01-01T00:00:00.000Z",
                "id": "log_1",
            },
        )
    )
    with pytest.raises(ValueError, match="api_key"):
        Reloop(api_key="rl_test", url="https://should-not-be-used.example")  # type: ignore[call-arg]
    assert not route.called


def test_credential_not_public() -> None:
    reloop = Reloop(api_key="rl_secret_value")
    assert reloop.api_key != "rl_secret_value"
    assert not isinstance(reloop.api_key, str)
    assert callable(reloop.api_key.create)
    for name in vars(reloop):
        assert getattr(reloop, name) != "rl_secret_value"
    reloop.close()
