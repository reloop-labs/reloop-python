from __future__ import annotations
from typing import Any,List,Optional,TypedDict
from typing_extensions import NotRequired
class Thread(TypedDict): id:str; mailboxId:Optional[str]; organizationId:str; subject:Optional[str]; lastMessagePreview:Optional[str]; lastMessageAt:str; status:str; messageCount:int; participants:List[str]; isRead:bool; isStarred:bool; createdAt:str; updatedAt:str
class ThreadDetail(Thread): messages:List[dict]
class ListThreadsParams(TypedDict): mailboxId:NotRequired[str]; limit:NotRequired[int]; offset:NotRequired[int]; folder:NotRequired[str]; q:NotRequired[str]; isPinned:NotRequired[bool]; filter:NotRequired[str]
class BatchThreadsParams(TypedDict): ids:List[str]; action:str
class UpdateThreadParams(TypedDict): isRead:NotRequired[bool]; isStarred:NotRequired[bool]; isImportant:NotRequired[bool]; isPinned:NotRequired[bool]; status:NotRequired[str]
class SetThreadReadParams(TypedDict): isRead:bool
class SetThreadStarParams(TypedDict): isStarred:bool
