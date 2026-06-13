from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from reloop_email import Reloop
from reloop_email._parameters import for_snake_request
from reloop_email.services.domain import DomainService


class DomainParametersTest(unittest.TestCase):
    def test_for_snake_request_keeps_snake_case(self) -> None:
        payload = for_snake_request(
            {
                "domain": "send.example.com",
                "click_tracking": True,
                "custom_return_path": "inbound",
                "ignored": None,
            }
        )

        self.assertEqual(
            payload,
            {
                "domain": "send.example.com",
                "click_tracking": True,
                "custom_return_path": "inbound",
            },
        )
        self.assertNotIn("clickTracking", payload)


class DomainServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.http = MagicMock()
        self.service = DomainService(self.http)

    def test_create_posts_snake_case_body(self) -> None:
        self.http.request.return_value = {
            "object": "domain",
            "id": "dom_1",
            "domain": "send.example.com",
            "status": "pending",
            "userVerifiedDomain": False,
            "systemVerified": False,
            "customReturnPath": "inbound",
            "trackingSubdomain": "tracking",
            "isClickTrackingEnabled": True,
            "isOpenTrackingEnabled": False,
            "tls": "opportunistic",
            "isTrackingDomain": False,
            "isSendingEmailEnabled": True,
            "isReceivingEmailEnabled": True,
            "verificationFailedReason": None,
            "dnsRecords": [],
            "lastVerifiedAt": None,
            "createdAt": "2026-01-01T00:00:00.000Z",
            "updatedAt": "2026-01-01T00:00:00.000Z",
        }

        result = self.service.create(
            domain="send.example.com",
            click_tracking=True,
            custom_return_path="inbound",
        )

        self.http.request.assert_called_once_with(
            "POST",
            "/api/domain/v1/create",
            json={
                "domain": "send.example.com",
                "click_tracking": True,
                "custom_return_path": "inbound",
            },
        )
        self.assertEqual(result.id, "dom_1")
        self.assertTrue(result.is_click_tracking_enabled)

    def test_list_builds_query_params(self) -> None:
        self.http.request.return_value = {
            "object": "domain",
            "domains": [],
            "total": 0,
            "page": 2,
            "limit": 5,
            "event": "evt_1",
        }

        self.service.list(page=2, limit=5, status="active", q="example")

        self.http.request.assert_called_once_with(
            "GET",
            "/api/domain/v1/list",
            params={"page": 2, "limit": 5, "status": "active", "q": "example"},
        )

    def test_get_nameservers_uses_nameservers_route(self) -> None:
        self.http.request.return_value = {
            "object": "domain_nameservers",
            "domainId": "dom_1",
            "domain": "send.example.com",
            "nameservers": ["ns1.example.net"],
            "dnsProvider": "cloudflare",
            "event": "evt_1",
        }

        result = self.service.get_nameservers("dom_1")

        self.http.request.assert_called_once_with(
            "GET",
            "/api/domain/v1/nameservers/dom_1",
        )
        self.assertEqual(result.dns_provider, "cloudflare")
        self.assertEqual(result.nameservers, ["ns1.example.net"])

    def test_forward_dns_posts_email(self) -> None:
        self.http.request.return_value = {"success": True}

        result = self.service.forward_dns("dom_1", email="admin@example.com")

        self.http.request.assert_called_once_with(
            "POST",
            "/api/domain/v1/verify/dom_1/forward-dns",
            json={"email": "admin@example.com"},
        )
        self.assertTrue(result.success)


class ReloopDomainIntegrationTest(unittest.TestCase):
    @patch("reloop_email._http_client.httpx.Client")
    def test_reloop_exposes_domain_service(self, client_cls: MagicMock) -> None:
        client = client_cls.return_value
        client.request.return_value = MagicMock(
            status_code=200,
            content=b'{"object":"domain","domains":[],"total":0,"page":1,"limit":10,"event":"evt_1"}',
            json=lambda: {
                "object": "domain",
                "domains": [],
                "total": 0,
                "page": 1,
                "limit": 10,
                "event": "evt_1",
            },
        )

        with Reloop(api_key="rl_test") as reloop:
            result = reloop.domain.list(limit=10)

        self.assertEqual(result.total, 0)


if __name__ == "__main__":
    unittest.main()
