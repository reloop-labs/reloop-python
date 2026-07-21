from __future__ import annotations

from typing import List, Optional, TypedDict

from typing_extensions import NotRequired


class ApiKeyCreatedBy(TypedDict):
    id: str
    name: Optional[str]
    image: Optional[str]
    email: str


class ApiKey(TypedDict):
    id: str
    name: Optional[str]
    start: Optional[str]
    prefix: Optional[str]
    refillInterval: Optional[int]
    refillAmount: Optional[int]
    lastRefillAt: Optional[str]
    enabled: bool
    rateLimitEnabled: bool
    rateLimitTimeWindow: int
    rateLimitMax: int
    requestCount: int
    remaining: Optional[int]
    lastRequest: Optional[str]
    expiresAt: Optional[str]
    createdAt: str
    updatedAt: str
    permissions: Optional[str]
    metadata: Optional[str]
    object: str
    event: str
    createdBy: NotRequired[ApiKeyCreatedBy]


class ApiKeyWithKey(TypedDict):
    id: str
    name: Optional[str]
    key: str
    enabled: bool
    createdAt: str
    updatedAt: str
    permissions: Optional[str]
    object: str
    event: str


class ApiKeyListResponse(TypedDict):
    object: str
    apiKeys: List[ApiKey]
    total: int
    page: int
    limit: int
    event: str


class ApiKeyListParams(TypedDict, total=False):
    page: int
    limit: int
    enabled: bool
    userId: str
    q: str


class DeleteApiKeyResponse(TypedDict):
    id: str
    message: str
    object: str
    event: str


class CreateApiKeyParams(TypedDict):
    name: str


class UpdateApiKeyParams(TypedDict):
    name: str
