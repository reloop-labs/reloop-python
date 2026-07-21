from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, Optional, TypeVar
from reloop_email.core.result import ReloopApiError, ReloopResult
T=TypeVar("T")
@dataclass(frozen=True)
class PropertyResult(Generic[T]): property: Optional[T]; property_error: Optional[ReloopApiError]
@dataclass(frozen=True)
class PropertyListResult: properties: Optional[dict]; property_error: Optional[ReloopApiError]
def to_property_result(r:ReloopResult[T])->PropertyResult[T]: return PropertyResult(None,r.error) if r.error else PropertyResult(r.response,None)
def to_property_list_result(r:ReloopResult[dict])->PropertyListResult: return PropertyListResult(None,r.error) if r.error else PropertyListResult(r.response,None)
