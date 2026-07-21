# Changelog

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
