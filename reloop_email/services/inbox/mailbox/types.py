from __future__ import annotations
from typing import Optional, TypedDict
from typing_extensions import NotRequired
class Mailbox(TypedDict):
 id:str; email:str; quota:str; status:str; displayName:Optional[str]; createdAt:str
class MailboxDetail(Mailbox): domainId:str; updatedAt:str
class CreateMailboxResponse(TypedDict): id:str; email:str; status:str
class CreateMailboxParams(TypedDict): domainId:str; email:str; password:NotRequired[str]; quota:NotRequired[str]; displayName:NotRequired[str]
class UpdateMailboxParams(TypedDict): displayName:NotRequired[str]; status:NotRequired[str]; quota:NotRequired[str]
