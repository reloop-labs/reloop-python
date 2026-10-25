from __future__ import annotations

from reloop_email.core.result import ReloopApiError, ReloopApiErrorBody


def test_error_body_reads_fix():
    body = ReloopApiErrorBody.from_mapping(
        {"message": "Domain not verified", "why": "No DKIM", "fix": "Verify the domain", "link": "https://reloop.sh/docs"}
    )
    assert body.fix == "Verify the domain"
    assert body.tip == "Verify the domain"  # deprecated alias
    assert body.extra is None


def test_error_body_accepts_legacy_tip():
    body = ReloopApiErrorBody.from_mapping({"message": "x", "tip": "Try again"})
    assert body.fix == "Try again" and body.tip == "Try again"


def test_api_error_exposes_fix():
    err = ReloopApiError(403, "Forbidden", {"message": "Nope", "fix": "Use another key"})
    assert err.body.fix == "Use another key"
