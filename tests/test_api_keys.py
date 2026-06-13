from __future__ import annotations

import sys
import unittest
from unittest.mock import MagicMock

if "httpx" not in sys.modules:
    sys.modules["httpx"] = MagicMock()

from reloop_email.services.api_keys import ApiKeysService


class ApiKeysServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.http = MagicMock()
        self.service = ApiKeysService(self.http)

    def test_create_posts_to_api_key_create_route(self) -> None:
        self.http.request.return_value = {"id": "key_1", "key": "rl_live_secret"}

        result = self.service.create(name="Production Key")

        self.http.request.assert_called_once_with(
            "POST",
            "/api/api-key/v1/",
            json={"name": "Production Key"},
        )
        self.assertEqual(result.id, "key_1")

    def test_list_passes_query_params(self) -> None:
        self.http.request.return_value = {
            "object": "api_key",
            "api_keys": [],
            "total": 0,
            "page": 1,
            "limit": 10,
            "event": "evt_1",
        }

        self.service.list(page=1, limit=10, enabled=True, q="prod")

        self.http.request.assert_called_once_with(
            "GET",
            "/api/api-key/v1/",
            params={"page": 1, "limit": 10, "enabled": True, "q": "prod"},
        )

    def test_pause_delegates_to_disable(self) -> None:
        self.http.request.return_value = {"id": "key_1", "enabled": False}

        self.service.pause("key_1")

        self.http.request.assert_called_once_with(
            "POST",
            "/api/api-key/v1/disable/key_1",
        )

    def test_rotate_uses_rotate_route(self) -> None:
        self.http.request.return_value = {"id": "key_1", "key": "rl_live_rotated"}

        self.service.rotate("key_1")

        self.http.request.assert_called_once_with(
            "POST",
            "/api/api-key/v1/rotate/key_1",
        )


if __name__ == "__main__":
    unittest.main()
