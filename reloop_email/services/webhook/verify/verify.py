from __future__ import annotations

import hashlib
import hmac
import json
import math
import time
from typing import Any, Mapping, Optional, Union

from reloop_email.services.webhook.types import WebhookSignatureVerificationError

WEBHOOK_SIGNATURE_HEADER = "x-webhook-signature"
WEBHOOK_TIMESTAMP_HEADER = "x-webhook-timestamp"


def _header(headers: Mapping[str, Any], name: str) -> Optional[Any]:
    lower = name.lower()
    for key, value in headers.items():
        if key.lower() == lower:
            return value
    return None


def _valid_signature(expected: str, received: str) -> bool:
    try:
        expected_bytes = bytes.fromhex(expected)
        received_bytes = bytes.fromhex(received)
        return len(expected_bytes) == len(received_bytes) and hmac.compare_digest(
            expected_bytes, received_bytes
        )
    except (TypeError, ValueError):
        return False


def verify_webhook(params: Mapping[str, Any]) -> dict[str, Any]:
    payload = params.get("payload")
    headers = params.get("headers") or {}
    secret = params.get("secret")
    tolerance = int(params.get("tolerance", 300))

    if not secret:
        raise WebhookSignatureVerificationError("Webhook secret is required")
    if not isinstance(headers, Mapping):
        raise WebhookSignatureVerificationError(
            f"Missing {WEBHOOK_SIGNATURE_HEADER} header"
        )

    signature = _header(headers, WEBHOOK_SIGNATURE_HEADER)
    if not signature:
        raise WebhookSignatureVerificationError(
            f"Missing {WEBHOOK_SIGNATURE_HEADER} header"
        )

    timestamp: Optional[str] = None
    sigs: list[str] = []
    for part in str(signature).split(","):
        key, sep, value = part.strip().partition("=")
        if not sep:
            continue
        if key == "t":
            timestamp = value
        elif key == "v1":
            sigs.append(value)

    if not timestamp or not sigs:
        raise WebhookSignatureVerificationError(
            "Invalid X-Webhook-Signature header: expected t= and v1= values"
        )

    try:
        ts = float(timestamp)
    except (TypeError, ValueError) as exc:
        raise WebhookSignatureVerificationError(
            "Invalid timestamp in X-Webhook-Signature header"
        ) from exc
    if not math.isfinite(ts):
        raise WebhookSignatureVerificationError(
            "Invalid timestamp in X-Webhook-Signature header"
        )
    if abs(math.floor(time.time()) - ts) > tolerance:
        raise WebhookSignatureVerificationError(
            f"Timestamp outside tolerance: allowed drift is {tolerance} seconds"
        )

    if isinstance(payload, bytes):
        raw = payload.decode("utf-8", errors="replace")
    elif isinstance(payload, str):
        raw = payload
    else:
        raise WebhookSignatureVerificationError("Webhook payload is not valid JSON")

    expected = hmac.new(
        str(secret).encode(),
        f"{timestamp}.{raw}".encode(),
        hashlib.sha256,
    ).hexdigest()

    if not any(_valid_signature(expected, s) for s in sigs):
        raise WebhookSignatureVerificationError("Webhook signature verification failed")

    try:
        event = json.loads(raw)
    except Exception as exc:
        raise WebhookSignatureVerificationError(
            "Webhook payload is not valid JSON"
        ) from exc
    if not isinstance(event, dict):
        raise WebhookSignatureVerificationError("Webhook payload must be a JSON object")

    if not isinstance(event.get("id"), str) or not event["id"]:
        raise WebhookSignatureVerificationError(
            "Webhook payload missing required field: id"
        )
    if not isinstance(event.get("event"), str) or not event["event"]:
        raise WebhookSignatureVerificationError(
            "Webhook payload missing required field: event"
        )
    if not isinstance(event.get("timestamp"), (int, float)):
        raise WebhookSignatureVerificationError(
            "Webhook payload missing required field: timestamp"
        )
    if not isinstance(event.get("payload"), dict):
        raise WebhookSignatureVerificationError(
            "Webhook payload missing required field: payload"
        )
    return event
