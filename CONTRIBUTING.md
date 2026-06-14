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
pip install -e .
python -m unittest discover -s tests -v
```

Requires **Python 3.9+**.

---

## Project layout

```
reloop_email/
  reloop.py              # Reloop client
  client.py              # HTTP layer
  _parameters.py         # for_request / for_snake_request
  _resource.py           # Resource objects (snake_case attrs)
  services/
    mail.py
    domain.py
    api_keys.py
    contacts/
tests/
pyproject.toml           # version + hatch build
```

---

## Conventions

| Topic | Rule |
|-------|------|
| Mail & domain | `for_snake_request()` — snake_case JSON |
| Contacts & API keys | `for_request()` — camelCase JSON |
| Mail sender | Use `from_=` (Python reserves `from`) |
| Responses | `for_response()` → snake_case attributes (`message_id`) |
| Tests | `unittest` + `MagicMock` on `HTTPClient.request` |
| README | Minimal send example + link to docs |

---

## Pull request checklist

- [ ] `python -m unittest discover -s tests -v` passes
- [ ] Route tests assert path, method, and JSON body
- [ ] Version in `pyproject.toml` bumped only for releases
- [ ] No secrets committed

---

## Releasing

Version: **`pyproject.toml`** → `[project] version`.

```bash
# 1. Bump version in pyproject.toml
git commit -am "chore: release v1.9.0"
git push origin main

# 2. Tag (must match pyproject.toml)
git tag v1.9.0
git push origin v1.9.0
```

[`.github/workflows/release.yml`](./.github/workflows/release.yml) creates a GitHub Release with source zip + `dist/*` wheels.

Publish to PyPI: [`.github/workflows/publish.yml`](./.github/workflows/publish.yml) or `hatch publish`.
