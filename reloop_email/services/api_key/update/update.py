from __future__ import annotations

from typing import Any, cast

from reloop_email.client import ReloopClient
from reloop_email.core.result import ReloopResult
from reloop_email.services.api_key.errors import ReloopValidationError
from reloop_email.services.api_key.fields import require_api_key_id, require_api_key_name
from reloop_email.services.api_key.paths import api_key_by_id
from reloop_email.services.api_key.result import ApiKeyResult, to_api_key_result
from reloop_email.services.api_key.types import ApiKey, UpdateApiKeyParams


def validate_update_params(params: object) -> UpdateApiKeyParams:
    if params is None or not isinstance(params, dict):
        raise ReloopValidationError(
            "update params are required and must be an object.",
            "params",
        )
    raw = cast(dict[str, Any], params)
    return UpdateApiKeyParams(name=require_api_key_name(raw.get("name")))


def update_api_key(
    client: ReloopClient,
    key_id: str,
    params: UpdateApiKeyParams,
) -> ApiKeyResult[ApiKey]:
    resolved = require_api_key_id(key_id)
    body = validate_update_params(params)
    result = client.fetch(api_key_by_id(resolved), method="PATCH", json=dict(body))
    typed = ReloopResult[ApiKey](response=result.response, error=result.error)
    return to_api_key_result(typed)
