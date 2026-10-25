from __future__ import annotations
import hashlib
import hmac
import json
import time
import pytest
import respx
import httpx
from reloop_email.client import ReloopClient
from reloop_email.services.api_key.errors import ReloopValidationError
from reloop_email.services.webhook.verify.verify import verify_webhook
from reloop_email.services.webhook.types import WebhookSignatureVerificationError
from reloop_email.services.webhook.webhook import WebhookService

@respx.mock
def test_create_webhook_happy_path():
    route=respx.post("https://example.test/api/webhook/v1/").mock(return_value=httpx.Response(200,json={"id":"wh_1"}))
    with ReloopClient("key",base_url="https://example.test") as client:
        result=WebhookService(client).create({"description":"events","url":"https://hook.test","events":["email.sent"]})
    assert route.called and result.webhook == {"id":"wh_1"} and result.webhook_error is None

@respx.mock
def test_create_webhook_api_error():
    respx.post("https://example.test/api/webhook/v1/").mock(return_value=httpx.Response(422,json={"message":"bad"}))
    with ReloopClient("key",base_url="https://example.test") as client:
        result=WebhookService(client).create({"description":"x","url":"u","events":[]})
    assert result.webhook is None and result.webhook_error is not None and result.webhook_error.status == 422

def test_verify_webhook_and_invalid_signature():
    timestamp=str(int(time.time())); body=json.dumps({"id":"evt_1","event":"email.sent","payload":{"id":"m_1"},"timestamp":1})
    signature=hmac.new(b"secret",f"{timestamp}.{body}".encode(),hashlib.sha256).hexdigest()
    assert verify_webhook({"payload":body,"headers":{"X-Webhook-Signature":f"t={timestamp},v1={signature}"},"secret":"secret"})["id"] == "evt_1"
    with pytest.raises(WebhookSignatureVerificationError):
        verify_webhook({"payload":body,"headers":{"x-webhook-signature":f"t={timestamp},v1=nope"},"secret":"secret"})

def test_create_webhook_validation():
    with ReloopClient("key",base_url="https://example.test") as client:
        with pytest.raises(ReloopValidationError): WebhookService(client).create(None)


def _sign(secret: bytes, timestamp: str, body: bytes) -> str:
    digest = hmac.new(secret, f"{timestamp}.".encode() + body, hashlib.sha256).hexdigest()
    return f"t={timestamp},v1={digest}"


PRODUCTION_BODY = json.dumps(
    {
        "id": "whev_01abc",
        "type": "email.received",
        "created_at": "2026-10-26T12:00:00.000Z",
        "data": {"email_id": "in_1", "subject": "Hello"},
    }
)


def test_verify_webhook_production_delivery():
    from reloop_email import WEBHOOK_SIGNATURE_HEADER

    timestamp = str(int(time.time()))
    event = verify_webhook(
        {
            "payload": PRODUCTION_BODY.encode(),
            "headers": {
                "reloop-signature": _sign(b"secret", timestamp, PRODUCTION_BODY.encode()),
                "reloop-timestamp": timestamp,
                "reloop-id": "whev_01abc",
            },
            "secret": "secret",
        }
    )
    assert WEBHOOK_SIGNATURE_HEADER == "Reloop-Signature"
    assert event["id"] == "whev_01abc"
    assert event["type"] == "email.received"
    assert event["created_at"] == "2026-10-26T12:00:00.000Z"
    assert event["data"] == {"email_id": "in_1", "subject": "Hello"}
    assert event["event"] == event["type"] and event["payload"] == event["data"]


def test_verify_webhook_rejects_tampered_production_body():
    timestamp = str(int(time.time()))
    header = _sign(b"secret", timestamp, PRODUCTION_BODY.encode())
    with pytest.raises(WebhookSignatureVerificationError):
        verify_webhook(
            {
                "payload": PRODUCTION_BODY.replace("Hello", "Hacked"),
                "headers": {"Reloop-Signature": header},
                "secret": "secret",
            }
        )


def test_verify_webhook_signs_raw_bytes():
    body = json.dumps({"id": "whev_2", "type": "email.received", "created_at": "2026-10-26T12:00:00Z", "data": {"subject": "Grüße"}}, ensure_ascii=False).encode("utf-8")
    timestamp = str(int(time.time()))
    event = verify_webhook({"payload": body, "headers": {"Reloop-Signature": _sign(b"secret", timestamp, body)}, "secret": "secret"})
    assert event["data"]["subject"] == "Grüße"


def test_verify_webhook_missing_header_names_reloop_signature():
    with pytest.raises(WebhookSignatureVerificationError, match="Reloop-Signature"):
        verify_webhook({"payload": PRODUCTION_BODY, "headers": {}, "secret": "secret"})


def test_construct_event_uses_reloop_signature():
    timestamp = str(int(time.time()))
    header = _sign(b"secret", timestamp, PRODUCTION_BODY.encode())
    event = WebhookService.construct_event(PRODUCTION_BODY, header, "secret")
    assert event["type"] == "email.received"
