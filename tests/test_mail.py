from __future__ import annotations

import unittest
from unittest.mock import MagicMock

from reloop_email.services.mail import MailService


class MailServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.http = MagicMock()
        self.service = MailService(self.http)

    def test_send_posts_snake_case_body(self) -> None:
        self.http.request.return_value = {
            "success": True,
            "messageId": "msg_123456789",
            "status": "sent",
            "timestamp": "2026-01-01T00:00:00.000Z",
            "id": "log_123456789",
        }

        result = self.service.send(
            from_="Reloop <hello@send.example.com>",
            to="user@example.com",
            subject="Welcome to Reloop",
            html="<p>Thanks for signing up.</p>",
            text="Thanks for signing up.",
            reply_to="support@example.com",
            tags=[{"name": "campaign", "value": "welcome"}],
        )

        self.http.request.assert_called_once_with(
            "POST",
            "/api/mail/v1/send",
            json={
                "from": "Reloop <hello@send.example.com>",
                "to": "user@example.com",
                "subject": "Welcome to Reloop",
                "html": "<p>Thanks for signing up.</p>",
                "text": "Thanks for signing up.",
                "reply_to": "support@example.com",
                "tags": [{"name": "campaign", "value": "welcome"}],
            },
        )
        self.assertTrue(result.success)
        self.assertEqual(result.message_id, "msg_123456789")
        self.assertEqual(result.id, "log_123456789")

    def test_send_supports_template_variables(self) -> None:
        self.http.request.return_value = {
            "success": True,
            "messageId": "msg_1",
            "status": "sent",
            "timestamp": "2026-01-01T00:00:00.000Z",
            "id": "log_1",
        }

        self.service.send(
            from_="hello@send.example.com",
            to=["user@example.com", "admin@example.com"],
            subject="Your weekly digest",
            template={
                "id": "tpl_123456789",
                "variables": {"first_name": "Ada"},
            },
        )

        self.http.request.assert_called_once_with(
            "POST",
            "/api/mail/v1/send",
            json={
                "from": "hello@send.example.com",
                "to": ["user@example.com", "admin@example.com"],
                "subject": "Your weekly digest",
                "template": {
                    "id": "tpl_123456789",
                    "variables": {"first_name": "Ada"},
                },
            },
        )


if __name__ == "__main__":
    unittest.main()
