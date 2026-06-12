# Reloop Python SDK

The official Python SDK for [Reloop](https://reloop.sh), modeled after the Stripe Python SDK with snake_case parameters and typed resource responses.

## Requirements

- Python 3.9 or higher

## Installation

```bash
pip install reloop
```

## Getting Started

```python
from reloop import Reloop

reloop = Reloop(api_key="re_123456789")
# or
reloop = Reloop.client("re_123456789")
```

## API Keys

```python
reloop = Reloop(api_key="rl_123456789")

reloop.api_keys.list(page=1, limit=10)

reloop.api_keys.create(
    name="Production key",
    enabled=True,
    rate_limit_enabled=True,
)

reloop.api_keys.get("key_123456789")
reloop.api_keys.update("key_123456789", name="Renamed key")
reloop.api_keys.rotate("key_123456789")
reloop.api_keys.disable("key_123456789")
reloop.api_keys.enable("key_123456789")
reloop.api_keys.delete("key_123456789")
```

## Contacts

Manage contacts, custom properties, groups, and channels. Methods accept snake_case keyword arguments and return resource objects with snake_case attributes.

### Create a contact

```python
reloop = Reloop(api_key="re_123456789")

contact = reloop.contacts.create(
    email="steve.wozniak@gmail.com",
    first_name="Steve",
    last_name="Wozniak",
    unsubscribed=False,
)

print(contact.email)
print(contact.first_name)
```

### List and update contacts

```python
contacts = reloop.contacts.list(page=1, limit=10)
print(contacts.contacts, contacts.total)

reloop.contacts.update(
    "cont_123456789",
    first_name="Steve",
    unsubscribed=False,
)
```

### Groups and channels

```python
reloop.contacts.groups.add_contact(
    "grp_123456789",
    contact_id="cont_123456789",
)

reloop.contacts.channels.create(
    name="Product Updates",
    default_subscription="opt_in",
)
```

## Error Handling

```python
from reloop import Reloop, ReloopApiError

reloop = Reloop(api_key="re_123456789")

try:
    reloop.contacts.get("cont_invalid")
except ReloopApiError as error:
    print(error.status_code, error.body)
```

## Context Manager

```python
with Reloop(api_key="re_123456789") as reloop:
    reloop.contacts.list(limit=10)
```
