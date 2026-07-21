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
