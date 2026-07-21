from __future__ import annotations

from typing import Optional


class ReloopValidationError(Exception):
    def __init__(self, message: str, field: Optional[str] = None) -> None:
        super().__init__(message)
        self.field = field

    @property
    def name(self) -> str:
        return "ReloopValidationError"
