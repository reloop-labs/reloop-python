from __future__ import annotations

from typing import Any, Optional, cast
from urllib.parse import urlencode

from reloop_email.client import ReloopClient
from reloop_email.core.result import ReloopResult
from reloop_email.services.api_key.errors import ReloopValidationError
from reloop_email.services.api_key.paths import api_key_list_path
from reloop_email.services.api_key.result import ApiKeyListResult, to_api_key_list_result
from reloop_email.services.api_key.types import ApiKeyListParams, ApiKeyListResponse

PAGE_MIN = 1
LIMIT_MIN = 1
LIMIT_MAX = 100


def validate_list_params(
    params: Optional[ApiKeyListParams] = None,
) -> Optional[ApiKeyListParams]:
    if params is None:
        return None
    if not isinstance(params, dict):
        raise ReloopValidationError(
            "list params must be an object when provided.",
            "params",
        )
    raw = cast(dict[str, Any], params)
    out: dict[str, Any] = {}

    if "page" in raw and raw["page"] is not None:
        page = raw["page"]
        if not isinstance(page, int) or isinstance(page, bool) or page < PAGE_MIN:
            raise ReloopValidationError(
                f"list page must be an integer >= {PAGE_MIN}.",
                "page",
            )
        out["page"] = page

    if "limit" in raw and raw["limit"] is not None:
        limit = raw["limit"]
        if (
            not isinstance(limit, int)
            or isinstance(limit, bool)
            or limit < LIMIT_MIN
            or limit > LIMIT_MAX
        ):
            raise ReloopValidationError(
                f"list limit must be an integer between {LIMIT_MIN} and {LIMIT_MAX}.",
                "limit",
            )
        out["limit"] = limit

    if "enabled" in raw and raw["enabled"] is not None:
        enabled = raw["enabled"]
        if not isinstance(enabled, bool):
            raise ReloopValidationError(
                "list enabled must be a boolean.",
                "enabled",
            )
        out["enabled"] = enabled

    if "userId" in raw and raw["userId"] is not None:
        user_id = raw["userId"]
        if not isinstance(user_id, str) or len(user_id.strip()) == 0:
            raise ReloopValidationError(
                "list userId must be a non-empty string when provided.",
                "userId",
            )
        out["userId"] = user_id.strip()

    if "q" in raw and raw["q"] is not None:
        q = raw["q"]
        if not isinstance(q, str):
            raise ReloopValidationError(
                "list q must be a string when provided.",
                "q",
            )
        out["q"] = q

    return cast(ApiKeyListParams, out)


def list_api_keys(
    client: ReloopClient,
    params: Optional[ApiKeyListParams] = None,
) -> ApiKeyListResult:
    valid = validate_list_params(params)
    query: dict[str, str] = {}
    if valid is not None:
        if "page" in valid:
            query["page"] = str(valid["page"])
        if "limit" in valid:
            query["limit"] = str(valid["limit"])
        if "enabled" in valid:
            query["enabled"] = "true" if valid["enabled"] else "false"
        if "userId" in valid:
            query["userId"] = valid["userId"]
        if "q" in valid:
            query["q"] = valid["q"]

    path = api_key_list_path(urlencode(query))
    result = client.fetch(path, method="GET")
    typed = ReloopResult[ApiKeyListResponse](response=result.response, error=result.error)
    return to_api_key_list_result(typed)
