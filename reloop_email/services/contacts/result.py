from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, Optional, TypeVar
from reloop_email.core.result import ReloopApiError, ReloopResult
from reloop_email.services.contacts.types import ContactListResponse
T=TypeVar("T")
@dataclass(frozen=True)
class ContactResult(Generic[T]): contact: Optional[T]; contact_error: Optional[ReloopApiError]
@dataclass(frozen=True)
class ContactListResult: contacts: Optional[ContactListResponse]; contact_error: Optional[ReloopApiError]
def to_contact_result(result:ReloopResult[T])->ContactResult[T]: return ContactResult(None,result.error) if result.error else ContactResult(result.response,None)
def to_contact_list_result(result:ReloopResult[ContactListResponse])->ContactListResult: return ContactListResult(None,result.error) if result.error else ContactListResult(result.response,None)
