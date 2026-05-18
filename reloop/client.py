from typing import Optional, Any
import httpx
from .services.api_key import ApiKeyService

class ReloopError(Exception):
    def __init__(self, message: str, cause: Any = None):
        super().__init__(message)
        self.cause = cause

class ReloopClient:
    def __init__(self, api_key: str, base_url: str = "https://reloop.sh"):
        if not api_key:
            raise ValueError("Reloop SDK requires an api_key.")
        
        self.api_key = api_key
        self.base_url = base_url
        
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        self.http_client = httpx.Client(base_url=self.base_url, headers=headers)
        
        # Initialize services
        self.api_key_service = ApiKeyService(self)

    def fetch(self, method: str, path: str, **kwargs) -> Any:
        try:
            response = self.http_client.request(method, path, **kwargs)
        except httpx.RequestError as e:
            raise ReloopError(f"Reloop Network Error: {e}") from e

        if not response.is_success:
            error_body = {}
            try:
                error_body = response.json()
            except ValueError:
                pass
            raise ReloopError(
                f"Reloop API Error: {response.status_code} {response.reason_phrase}",
                cause=error_body
            )

        if response.status_code == 204:
            return {}

        return response.json()
