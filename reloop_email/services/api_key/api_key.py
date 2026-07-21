from __future__ import annotations

from typing import Optional

from reloop_email.client import ReloopClient
from reloop_email.services.api_key.create.create import create_api_key
from reloop_email.services.api_key.delete.delete import delete_api_key
from reloop_email.services.api_key.disable.disable import disable_api_key
from reloop_email.services.api_key.enable.enable import enable_api_key
from reloop_email.services.api_key.get.get import get_api_key
from reloop_email.services.api_key.list.list import list_api_keys
from reloop_email.services.api_key.result import ApiKeyListResult, ApiKeyResult
from reloop_email.services.api_key.rotate.rotate import rotate_api_key
from reloop_email.services.api_key.types import (
    ApiKey,
    ApiKeyListParams,
    ApiKeyWithKey,
    CreateApiKeyParams,
    DeleteApiKeyResponse,
    UpdateApiKeyParams,
)
from reloop_email.services.api_key.update.update import update_api_key


class ApiKeyService:
    def __init__(self, client: ReloopClient) -> None:
        self._client = client

    def create(self, params: CreateApiKeyParams) -> ApiKeyResult[ApiKeyWithKey]:
        return create_api_key(self._client, params)

    def list(self, params: Optional[ApiKeyListParams] = None) -> ApiKeyListResult:
        return list_api_keys(self._client, params)

    def get(self, key_id: str) -> ApiKeyResult[ApiKey]:
        return get_api_key(self._client, key_id)

    def update(self, key_id: str, params: UpdateApiKeyParams) -> ApiKeyResult[ApiKey]:
        return update_api_key(self._client, key_id, params)

    def delete(self, key_id: str) -> ApiKeyResult[DeleteApiKeyResponse]:
        return delete_api_key(self._client, key_id)

    def rotate(self, key_id: str) -> ApiKeyResult[ApiKeyWithKey]:
        return rotate_api_key(self._client, key_id)

    def enable(self, key_id: str) -> ApiKeyResult[ApiKey]:
        return enable_api_key(self._client, key_id)

    def disable(self, key_id: str) -> ApiKeyResult[ApiKey]:
        return disable_api_key(self._client, key_id)
