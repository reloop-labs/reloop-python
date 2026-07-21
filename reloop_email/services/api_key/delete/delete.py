from __future__ import annotations

from reloop_email.client import ReloopClient
from reloop_email.core.result import ReloopResult
from reloop_email.services.api_key.fields import require_api_key_id
from reloop_email.services.api_key.paths import api_key_by_id
from reloop_email.services.api_key.result import ApiKeyResult, to_api_key_result
from reloop_email.services.api_key.types import DeleteApiKeyResponse


def delete_api_key(
    client: ReloopClient,
    key_id: str,
) -> ApiKeyResult[DeleteApiKeyResponse]:
    resolved = require_api_key_id(key_id)
    result = client.fetch(api_key_by_id(resolved), method="DELETE")
    typed = ReloopResult[DeleteApiKeyResponse](response=result.response, error=result.error)
    return to_api_key_result(typed)
