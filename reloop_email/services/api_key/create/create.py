from __future__ import annotations

from typing import Any, cast

from reloop_email.client import ReloopClient
from reloop_email.core.result import ReloopResult
from reloop_email.services.api_key.errors import ReloopValidationError
from reloop_email.services.api_key.fields import require_api_key_name
from reloop_email.services.api_key.paths import API_KEY_V1
from reloop_email.services.api_key.result import ApiKeyResult, to_api_key_result
from reloop_email.services.api_key.types import ApiKeyWithKey, CreateApiKeyParams


def validate_create_params(params: object) -> CreateApiKeyParams:
    if params is None or not isinstance(params, dict):
        raise ReloopValidationError(
            "create params are required and must be an object.",
            "params",
        )
    raw = cast(dict[str, Any], params)
    return CreateApiKeyParams(name=require_api_key_name(raw.get("name")))


def create_api_key(
    client: ReloopClient,
    params: CreateApiKeyParams,
) -> ApiKeyResult[ApiKeyWithKey]:
    body = validate_create_params(params)
    result = client.fetch(f"{API_KEY_V1}/", method="POST", json=dict(body))
    typed = ReloopResult[ApiKeyWithKey](response=result.response, error=result.error)
    return to_api_key_result(typed)
