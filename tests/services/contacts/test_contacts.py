import pytest
import respx
from httpx import Response
from reloop_email.services.contacts.contacts import ContactsService
from reloop_email.services.api_key.errors import ReloopValidationError
from tests.helpers import client

@respx.mock
def test_create_contact_happy_path():
    route = respx.post("https://api.test/api/contacts/create").mock(return_value=Response(200, json={"id": "c1", "email": "a@example.com"}))
    result = ContactsService(client()).create({"email": "a@example.com"})
    assert route.called and result.contact == {"id": "c1", "email": "a@example.com"} and result.contact_error is None

@respx.mock
def test_list_contact_api_error():
    respx.get("https://api.test/api/contacts/list").mock(return_value=Response(500, json={"message": "bad"}))
    result = ContactsService(client()).list()
    assert result.contacts is None and result.contact_error is not None

@respx.mock
def test_create_contact_validation_makes_no_request():
    with pytest.raises(ReloopValidationError): ContactsService(client()).create({"email": "bad"})
    assert not respx.calls

@respx.mock
def test_list_contact_validation_makes_no_request():
    with pytest.raises(ReloopValidationError): ContactsService(client()).list({"limit": 101})
    assert not respx.calls
