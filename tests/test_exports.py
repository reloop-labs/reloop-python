from __future__ import annotations

import reloop_email as sdk
from reloop_email import Reloop, ReloopApiError, ReloopValidationError, err, ok


def test_reloop_is_public_entry() -> None:
    assert callable(Reloop)
    assert sdk.Reloop is Reloop
    reloop = Reloop(api_key="rl_test")
    assert callable(reloop.api_key.create)
    assert callable(reloop.mail.send)
    reloop.close()


def test_result_helpers_and_errors_exported() -> None:
    assert callable(ok)
    assert callable(err)
    assert callable(ReloopApiError)
    assert callable(ReloopValidationError)

    ok_result = ok({"id": "1"})
    assert ok_result.error is None
    assert ok_result.response == {"id": "1"}

    api_error = ReloopApiError(400, "Bad Request", {"message": "bad"})
    err_result = err(api_error)
    assert err_result.response is None
    assert err_result.error is api_error

    validation = ReloopValidationError("bad name", "name")
    assert validation.field == "name"


def test_reloop_client_not_exported() -> None:
    assert not hasattr(sdk, "ReloopClient")


def test_api_key_service_not_exported() -> None:
    assert not hasattr(sdk, "ApiKeyService")


def test_named_result_fields() -> None:
    assert hasattr(sdk, "EmailResult")
    assert hasattr(sdk, "verify_webhook")
