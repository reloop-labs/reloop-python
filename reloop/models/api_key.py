from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    id: str
    name: Optional[str] = None
    image: Optional[str] = None
    email: str

class ApiKey(BaseModel):
    id: str
    name: Optional[str] = None
    start: Optional[str] = None
    prefix: Optional[str] = None
    organizationId: str
    userId: str
    refillInterval: Optional[int] = None
    refillAmount: Optional[int] = None
    lastRefillAt: Optional[str] = None
    enabled: bool
    rateLimitEnabled: bool
    rateLimitTimeWindow: int
    rateLimitMax: int
    requestCount: int
    remaining: Optional[int] = None
    lastRequest: Optional[str] = None
    expiresAt: Optional[str] = None
    createdAt: str
    updatedAt: str
    permissions: Optional[str] = None
    metadata: Optional[str] = None
    createdBy: Optional[User] = None
    object: str = "api_key"
    event: str

    model_config = ConfigDict(populate_by_name=True)

class ApiKeyWithKey(BaseModel):
    id: str
    name: Optional[str] = None
    key: str
    enabled: bool
    createdAt: str
    updatedAt: str
    permissions: Optional[str] = None
    object: str = "api_key"
    event: str

class ApiKeyListResponse(BaseModel):
    object: str = "api_key"
    apiKeys: List[ApiKey]
    total: int
    page: int
    limit: int
    event: str

class ApiKeyListParams(BaseModel):
    page: Optional[int] = None
    limit: Optional[int] = None
    enabled: Optional[bool] = None
    userId: Optional[str] = None
    q: Optional[str] = None

class DeleteApiKeyResponse(BaseModel):
    id: str
    message: str
    object: str = "api_key"
    event: str

class CreateApiKeyParams(BaseModel):
    name: str

class UpdateApiKeyParams(BaseModel):
    name: str
