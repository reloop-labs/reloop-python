from __future__ import annotations
import pytest
import respx
import httpx
from reloop_email.client import ReloopClient
from reloop_email.services.api_key.errors import ReloopValidationError
from reloop_email.services.inbox.inbox import InboxService

@respx.mock
def test_list_mailboxes_happy_and_api_error():
    respx.get("https://example.test/api/inbox/v1/mailboxes/list").mock(return_value=httpx.Response(200,json=[{"id":"mb_1"}]))
    with ReloopClient("key",base_url="https://example.test") as client:
        result=InboxService(client).mailboxes.list()
    assert result.mailboxes == [{"id":"mb_1"}] and result.mailbox_error is None
    respx.get("https://example.test/api/inbox/v1/mailboxes/list").mock(return_value=httpx.Response(500,json={"message":"bad"}))
    with ReloopClient("key",base_url="https://example.test") as client:
        result=InboxService(client).mailboxes.list()
    assert result.mailboxes is None and result.mailbox_error is not None

@respx.mock
def test_send_message_happy_path():
    route=respx.post("https://example.test/api/inbox/v1/messages/send").mock(return_value=httpx.Response(200,json={"id":"msg_1","success":True}))
    with ReloopClient("key",base_url="https://example.test") as client:
        result=InboxService(client).messages.send({"mailboxId":"mb_1","to":"to@example.test","subject":"Hi","text":"Hello"})
    assert route.called and result.message == {"id":"msg_1","success":True} and result.message_error is None

def test_send_message_validation():
    with ReloopClient("key",base_url="https://example.test") as client:
        with pytest.raises(ReloopValidationError): InboxService(client).messages.send({"mailboxId":"mb_1","to":[],"subject":"Hi"})
