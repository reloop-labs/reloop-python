from __future__ import annotations

import hashlib
import hmac
import json
import math
import time
from datetime import datetime, timezone
from typing import Any, Mapping, Optional

from reloop_email.services.webhook.types import WebhookSignatureVerificationError

# Reloop signs every delivery with `Reloop-Signature: t=<unix>,v1=<hex>`.
WEBHOOK_SIGNATURE_HEADER = "Reloop-Signature"
WEBHOOK_TIMESTAMP_HEADER = "Reloop-Timestamp"
WEBHOOK_ID_HEADER = "Reloop-Id"

# Header name used before 2.0.1. Still accepted as a fallback.
_LEGACY_SIGNATURE_HEADER = "x-webhook-signature"


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

    signature = _header(headers, WEBHOOK_SIGNATURE_HEADER) or _header(
        headers, _LEGACY_SIGNATURE_HEADER
    )
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
            f"Invalid {WEBHOOK_SIGNATURE_HEADER} header: expected t= and v1= values"
        )

    try:
        ts = float(timestamp)
    except (TypeError, ValueError) as exc:
        raise WebhookSignatureVerificationError(
            f"Invalid timestamp in {WEBHOOK_SIGNATURE_HEADER} header"
        ) from exc
    if not math.isfinite(ts):
        raise WebhookSignatureVerificationError(
            f"Invalid timestamp in {WEBHOOK_SIGNATURE_HEADER} header"
        )
    if abs(math.floor(time.time()) - ts) > tolerance:
        raise WebhookSignatureVerificationError(
            f"Timestamp outside tolerance: allowed drift is {tolerance} seconds"
        )

    # Sign the exact bytes received; decoding first would corrupt non-UTF-8 bodies.
    if isinstance(payload, (bytes, bytearray)):
        raw_bytes = bytes(payload)
    elif isinstance(payload, str):
        raw_bytes = payload.encode("utf-8")
    else:
        raise WebhookSignatureVerificationError("Webhook payload is not valid JSON")

    expected = hmac.new(
        str(secret).encode(),
        f"{timestamp}.".encode() + raw_bytes,
        hashlib.sha256,
    ).hexdigest()

    if not any(_valid_signature(expected, s) for s in sigs):
        raise WebhookSignatureVerificationError("Webhook signature verification failed")

    try:
        event = json.loads(raw_bytes)
    except Exception as exc:
        raise WebhookSignatureVerificationError(
            "Webhook payload is not valid JSON"
        ) from exc
    if not isinstance(event, dict):
        raise WebhookSignatureVerificationError("Webhook payload must be a JSON object")

    return _normalize_event(event)


def _normalize_event(event: dict[str, Any]) -> dict[str, Any]:
    """Accept the production envelope {id, type, created_at, data} and the
    legacy {id, event, payload, timestamp} shape; return both key sets."""
    event_id = event.get("id")
    if not isinstance(event_id, str) or not event_id:
        raise WebhookSignatureVerificationError(
            "Webhook payload missing required field: id"
        )

    event_type = event.get("type", event.get("event"))
    if not isinstance(event_type, str) or not event_type:
        raise WebhookSignatureVerificationError(
            "Webhook payload missing required field: type"
        )

    data = event.get("data", event.get("payload"))
    if not isinstance(data, dict):
        raise WebhookSignatureVerificationError(
            "Webhook payload missing required field: data"
        )

    created_at = event.get("created_at")
    legacy_ts = event.get("timestamp")
    if isinstance(created_at, str) and created_at:
        try:
            timestamp = datetime.fromisoformat(
                created_at.replace("Z", "+00:00")
            ).timestamp()
        except ValueError as exc:
            raise WebhookSignatureVerificationError(
                "Webhook payload has an invalid created_at"
            ) from exc
    elif isinstance(legacy_ts, (int, float)) and not isinstance(legacy_ts, bool):
        timestamp = float(legacy_ts)
        created_at = (
            datetime.fromtimestamp(timestamp, tz=timezone.utc)
            .isoformat(timespec="milliseconds")
            .replace("+00:00", "Z")
        )
    else:
        raise WebhookSignatureVerificationError(
            "Webhook payload missing required field: created_at"
        )

    return {
        "id": event_id,
        "type": event_type,
        "created_at": created_at,
        "data": data,
        # Deprecated aliases kept for callers of the pre-2.0.1 shape.
        "event": event_type,
        "payload": data,
        "timestamp": timestamp,
    }
