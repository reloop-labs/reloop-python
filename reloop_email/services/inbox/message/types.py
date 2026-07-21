from __future__ import annotations
from typing import Any, List, Optional, TypedDict, Union
from typing_extensions import NotRequired
class Message(TypedDict): id:str; mailboxId:str; organizationId:str; fromEmail:str; fromName:Optional[str]; toEmails:List[str]; subject:Optional[str]; textBody:Optional[str]; htmlBody:Optional[str]; status:str; isRead:bool; isStarred:bool; isSpam:bool; createdAt:str
class MessageRaw(TypedDict): id:str; messageId:Optional[str]; raw:str
class ListMessagesParams(TypedDict): mailboxId:NotRequired[str]; limit:NotRequired[int]; offset:NotRequired[int]; q:NotRequired[str]; isSpam:NotRequired[bool]
class ListSentMessagesParams(TypedDict): mailboxId:NotRequired[str]
class BatchMessagesParams(TypedDict): ids:List[str]
class UpdateMessageParams(TypedDict): isRead:NotRequired[bool]; isStarred:NotRequired[bool]; isSpam:NotRequired[bool]
class SetMessageReadParams(TypedDict): isRead:bool
class SetMessageStarParams(TypedDict): isStarred:bool
class SendMessageParams(TypedDict): mailboxId:str; to:Union[str,List[str]]; subject:str; text:NotRequired[str]; html:NotRequired[str]; cc:NotRequired[Union[str,List[str]]]; bcc:NotRequired[Union[str,List[str]]]; attachments:NotRequired[List[dict]]; scheduledAt:NotRequired[str]; undoWindowSeconds:NotRequired[float]
class ComposeMessageParams(TypedDict): text:NotRequired[str]; html:NotRequired[str]; cc:NotRequired[Union[str,List[str]]]; bcc:NotRequired[Union[str,List[str]]]; attachments:NotRequired[List[dict]]
class ForwardMessageParams(ComposeMessageParams): to:Union[str,List[str]]
