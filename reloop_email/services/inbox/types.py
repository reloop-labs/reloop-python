from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, TypedDict, Union

from typing_extensions import NotRequired

JsonObject = Dict[str, Any]

class InboxSuccessResponse(TypedDict):
    success: bool
    id: NotRequired[str]
    message: NotRequired[str]
    isRead: NotRequired[bool]
    isStarred: NotRequired[bool]
    isSpam: NotRequired[bool]
    isImportant: NotRequired[bool]
    isPinned: NotRequired[bool]
    status: NotRequired[str]
    deletedAt: NotRequired[Optional[str]]

class MessageAttachment(TypedDict):
    id: str
    filename: str
    contentType: str
    size: int
    storagePath: str
    contentDisposition: Optional[str]
    contentId: Optional[str]
    createdAt: str

class AttachmentInput(TypedDict):
    content: NotRequired[str]
    filename: NotRequired[str]
    path: NotRequired[str]
    content_type: NotRequired[str]
    content_id: NotRequired[str]

class SendEmailResponse(TypedDict):
    success: bool
    messageId: str
    status: str
    timestamp: str
    id: str

class PendingSendResponse(TypedDict):
    success: bool
    pending: Literal[True]
    id: str
    sendAt: str
    messageId: str

SendEmailOrPendingResponse = Union[SendEmailResponse, PendingSendResponse]

class ThreadBatchResponse(TypedDict):
    success: bool
    ids: List[str]
    action: str
