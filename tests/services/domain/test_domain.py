import pytest
import respx
from httpx import Response
from reloop_email.services.domain.domain import DomainService
from reloop_email.services.api_key.errors import ReloopValidationError
from tests.helpers import client

@respx.mock
def test_create_domain_happy_path():
    route = respx.post("https://api.test/api/domain/v1/create").mock(return_value=Response(200, json={"id": "d1", "domain": "example.com"}))
    result = DomainService(client()).create({"domain": "Example.COM"})
    assert route.called and result.domain == {"id": "d1", "domain": "example.com"} and result.domain_error is None

@respx.mock
def test_list_domain_api_error():
    respx.get("https://api.test/api/domain/v1/list").mock(return_value=Response(422, json={"message": "bad"}))
    result = DomainService(client()).list()
    assert result.domains is None and result.domain_error is not None

@respx.mock
def test_create_domain_validation_makes_no_request():
    with pytest.raises(ReloopValidationError): DomainService(client()).create({"domain": "bad"})
    assert not respx.calls

@respx.mock
def test_list_domain_validation_makes_no_request():
    with pytest.raises(ReloopValidationError): DomainService(client()).list({"page": 0})
    assert not respx.calls
