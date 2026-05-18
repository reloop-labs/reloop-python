from typing import Optional, Dict, Any
from ..models.api_key import (
    ApiKey,
    ApiKeyListParams,
    ApiKeyListResponse,
    ApiKeyWithKey,
    CreateApiKeyParams,
    DeleteApiKeyResponse,
    UpdateApiKeyParams,
)

class ApiKeyService:
    def __init__(self, client):
        self.client = client

    def create(self, params: CreateApiKeyParams) -> ApiKeyWithKey:
        response = self.client.fetch("POST", "/api-key/v1/", json=params.model_dump(exclude_none=True))
        return ApiKeyWithKey.model_validate(response)

    def list(self, params: Optional[ApiKeyListParams] = None) -> ApiKeyListResponse:
        query_params: Dict[str, Any] = {}
        if params:
            query_params = {k: v for k, v in params.model_dump(exclude_none=True).items()}
        
        response = self.client.fetch("GET", "/api-key/v1/", params=query_params)
        return ApiKeyListResponse.model_validate(response)

    def get(self, id: str) -> ApiKey:
        response = self.client.fetch("GET", f"/api-key/v1/{id}")
        return ApiKey.model_validate(response)

    def update(self, id: str, params: UpdateApiKeyParams) -> ApiKey:
        response = self.client.fetch("PATCH", f"/api-key/v1/{id}", json=params.model_dump(exclude_none=True))
        return ApiKey.model_validate(response)

    def delete(self, id: str) -> DeleteApiKeyResponse:
        response = self.client.fetch("DELETE", f"/api-key/v1/{id}")
        return DeleteApiKeyResponse.model_validate(response)

    def rotate(self, id: str) -> ApiKeyWithKey:
        response = self.client.fetch("POST", f"/api-key/v1/rotate/{id}")
        return ApiKeyWithKey.model_validate(response)

    def enable(self, id: str) -> ApiKey:
        response = self.client.fetch("POST", f"/api-key/v1/enable/{id}")
        return ApiKey.model_validate(response)

    def disable(self, id: str) -> ApiKey:
        response = self.client.fetch("POST", f"/api-key/v1/disable/{id}")
        return ApiKey.model_validate(response)
