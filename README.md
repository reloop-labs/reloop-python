# Reloop Python SDK

## Before you send

You need two things:

1. **API key** — create one in your Reloop account
2. **Verified domain** — add and verify a sending domain; use it in the `from` address

For setup details and the full API reference, see [reloop.sh/docs](https://reloop.sh/docs).

## Send email

```bash
pip install reloop-email
```

```python
from reloop_email import Reloop

reloop = Reloop(api_key="rl_your_api_key_here")

result = reloop.mail.send(
    from_="Reloop <hello@your-verified-domain.com>",
    to="user@example.com",
    subject="Welcome to Reloop",
    html="<p>Thanks for signing up.</p>",
    text="Thanks for signing up.",
)

print(result.message_id, result.id)
```

Use `from_` instead of `from` (`from` is reserved in Python).

More examples and optional fields: [reloop.sh/docs](https://reloop.sh/docs)

## License

Licensed under the [Apache License 2.0](./LICENSE) with additional use restrictions from Reloop Labs (same as the [Reloop project](https://github.com/reloop-labs/reloop/blob/main/LICENSE)).
