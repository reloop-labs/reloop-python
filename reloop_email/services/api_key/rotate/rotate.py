from __future__ import annotations

from reloop_email.client import ReloopClient
from reloop_email.core.result import ReloopResult
from reloop_email.services.api_key.fields import require_api_key_id
from reloop_email.services.api_key.paths import api_key_rotate
from reloop_email.services.api_key.result import ApiKeyResult, to_api_key_result
from reloop_email.services.api_key.types import ApiKeyWithKey


def rotate_api_key(client: ReloopClient, key_id: str) -> ApiKeyResult[ApiKeyWithKey]:
    resolved = require_api_key_id(key_id)
    result = client.fetch(api_key_rotate(resolved), method="POST")
    typed = ReloopResult[ApiKeyWithKey](response=result.response, error=result.error)
    return to_api_key_result(typed)
