# Reloop Python SDK

Official Python SDK for the [Reloop](https://reloop.sh) email API. Package name on PyPI: **`reloop-email`**.

**Version 2.0** is a breaking rewrite aligned with the [Node.js SDK](https://github.com/reloop-labs/reloop-node): typed params, named Result objects for HTTP errors, and `ReloopValidationError` for bad client input.

## Install

```bash
pip install reloop-email
```

Requires Python 3.9+.

## Quick start

```python
from reloop_email import Reloop

with Reloop(api_key="rl_...") as reloop:
    result = reloop.mail.send({
        "from": "hello@send.example.com",
        "to": "user@example.com",
        "subject": "Welcome",
        "html": "<p>Thanks for signing up.</p>",
    })

    if result.email_error:
        print(result.email_error.status, result.email_error.body.message)
    else:
        print(result.response["messageId"])
```

## Error model

| Kind | Behavior |
|------|----------|
| Invalid arguments | Raises `ReloopValidationError` (no HTTP call) |
| API / network failure | Returns a named Result (`email_error`, `api_key_error`, `domain_error`, …) — does not raise |

## Resources

```text
Reloop
├── api_key      # create, list, get, update, delete, rotate, enable, disable
├── mail         # send
├── contacts     # CRUD + .properties / .groups / .channels
├── domain       # create, list, get, update, delete, verify
├── webhook      # CRUD, pause/enable/disable, trigger, deliveries, verify
└── inbox
    ├── mailboxes
    ├── messages
    └── threads
```

Webhook signature verification (local, no HTTP):

```python
from reloop_email import verify_webhook, WEBHOOK_SIGNATURE_HEADER

event = verify_webhook({
    "payload": raw_body,
    "headers": {WEBHOOK_SIGNATURE_HEADER: signature_header},
    "secret": "whsec_...",
})
```

## Docs

- API reference: [reloop.sh/docs](https://reloop.sh/docs)
- Contributing / local development: [CONTRIBUTING.md](./CONTRIBUTING.md)

## Breaking changes from 1.x

- HTTP failures no longer raise `ReloopApiError` from service methods; they return named `*_error` fields.
- Dynamic Stripe-style `Resource` objects are gone; responses are typed dicts / dataclasses.
- `api_keys` → `api_key`; contacts nesting matches Node (`contacts.properties`, etc.).
- Removed: `domain.get_nameservers`, `domain.forward_dns`, `api_keys.pause`.
- `ReloopClient` is no longer a public constructable export.

## License

Apache License 2.0 with additional use restrictions from Reloop Labs. See [LICENSE](./LICENSE).
