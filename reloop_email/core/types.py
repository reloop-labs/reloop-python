from __future__ import annotations

from typing import TypedDict


class ReloopClientOptions(TypedDict, total=False):
    api_key: str
    base_url: str


class ReloopClientOptionsRequired(TypedDict):
    api_key: str
