# Changelog

## 2.0.1

- Fix: `verify_webhook` reads the `Reloop-Signature` header that Reloop actually sends (`x-webhook-signature` still works as a fallback). `WEBHOOK_SIGNATURE_HEADER` is now `Reloop-Signature`; `WEBHOOK_TIMESTAMP_HEADER` and new `WEBHOOK_ID_HEADER` are `Reloop-Timestamp` and `Reloop-Id`.
- Fix: verified events use the production envelope `{id, type, created_at, data}`. `event`, `payload` and `timestamp` are still returned as deprecated aliases.
- Fix: the signature is computed over the raw body bytes, so non-UTF-8 bodies verify correctly.
- Fix: `ReloopApiErrorBody` now reads `fix` from API errors. `tip` is kept as a deprecated alias.

## 2.0.0

Breaking rewrite for Node SDK parity:

- Named Result API (`email_error`, `api_key_error`, …) instead of raising on HTTP errors
- `ReloopValidationError` for invalid client input
- Typed params/responses (`TypedDict`) + `py.typed`
- Full surface: `api_key`, `mail`, `contacts` (+ nested), `domain`, `webhook`, `inbox`
- Removed 1.x: `api_keys.pause`, `domain.get_nameservers`, `domain.forward_dns`, public `ReloopClient`
- Tooling: pytest, respx, mypy strict

## 1.8.0

Previous untyped httpx client (mail, domain, api_keys, contacts).
