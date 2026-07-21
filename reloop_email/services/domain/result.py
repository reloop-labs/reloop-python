from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, Optional, TypeVar
from reloop_email.core.result import ReloopApiError, ReloopResult
from reloop_email.services.domain.types import DomainListResponse
T = TypeVar("T")
@dataclass(frozen=True)
class DomainResult(Generic[T]):
 domain: Optional[T]
 domain_error: Optional[ReloopApiError]
@dataclass(frozen=True)
class DomainListResult:
 domains: Optional[DomainListResponse]
 domain_error: Optional[ReloopApiError]
def to_domain_result(result: ReloopResult[T]) -> DomainResult[T]: return DomainResult(None, result.error) if result.error else DomainResult(result.response, None)
def to_domain_list_result(result: ReloopResult[DomainListResponse]) -> DomainListResult: return DomainListResult(None, result.error) if result.error else DomainListResult(result.response, None)
