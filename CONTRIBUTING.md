# Contributing to the Reloop Python SDK

Official PyPI package: **`reloop-email`**.

**License:** [Apache License 2.0](./LICENSE) with additional use restrictions from Reloop Labs.

**API reference:** [reloop.sh/docs](https://reloop.sh/docs)

Implement new API behaviour in the [Node.js SDK](https://github.com/reloop-labs/reloop-node) first, then port here.

---

## Development setup

```bash
git clone git@github.com:reloop-labs/reloop-python.git
cd reloop-python
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
mypy reloop_email
```

Requires **Python 3.9+** (mypy checks as 3.10).

---

## Project layout

```
reloop_email/
  py.typed
  __init__.py            # public exports
  reloop.py              # Reloop facade
  client.py              # ReloopClient → ReloopResult
  core/
    result.py            # ReloopResult, ReloopApiError, ok/err
    types.py
  services/
    mail/
    api_key/
    domain/
    contacts/            # + property, group, channel
    webhook/             # + verify
    inbox/               # + mailbox, message, thread
tests/
  test_init.py
  test_exports.py
  services/...
pyproject.toml
```

---

## Conventions

| Topic | Rule |
|-------|------|
| Wire bodies (mail, domain) | snake_case JSON |
| Wire bodies (contacts, api_key, inbox, webhook) | camelCase as Node/API expect |
| Bad args | raise `ReloopValidationError` before HTTP |
| HTTP / network | named Result (`email_error`, `api_key_error`, …) — no raise |
| Types | TypedDict params/responses; frozen dataclass Results |
| Tests | pytest + respx; assert path/method/headers/body; assert no HTTP on validation |
| Typecheck | `mypy reloop_email` (strict; service overrides for compressed modules) |

---

## Pull request checklist

- [ ] `pytest -q` passes
- [ ] `mypy reloop_email` passes
- [ ] Route tests assert path, method, and JSON body where relevant
- [ ] Version in `pyproject.toml` bumped only for releases
- [ ] No secrets committed

---

## Releasing

Version: **`pyproject.toml`** → `[project] version`.

```bash
# 1. Bump version in pyproject.toml
git commit -am "chore: release v2.0.1"
git push origin main

# 2. Tag (must match pyproject.toml)
git tag v2.0.1
git push origin v2.0.1
```

GitHub Actions publish on tag push.
