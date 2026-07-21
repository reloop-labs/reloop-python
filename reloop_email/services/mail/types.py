from __future__ import annotations

from typing import Any, List, TypedDict, Union

from typing_extensions import NotRequired

# Wire body uses reserved word "from" — functional TypedDict form.
SendMailParams = TypedDict(
    "SendMailParams",
    {
        "from": str,
        "to": Union[str, List[str]],
        "subject": str,
        "cc": NotRequired[Union[str, List[str]]],
        "bcc": NotRequired[Union[str, List[str]]],
        "text": NotRequired[str],
        "html": NotRequired[str],
        "reply_to": NotRequired[Union[str, List[str]]],
        "scheduled_at": NotRequired[str],
        "headers": NotRequired[dict[str, str]],
        "channel_id": NotRequired[str],
        "attachments": NotRequired[List[dict[str, Any]]],
        "tags": NotRequired[List[dict[str, str]]],
        "template": NotRequired[dict[str, Any]],
        "thread_id": NotRequired[str],
    },
)


class SendMailResponse(TypedDict):
    success: bool
    messageId: str
    status: str
    timestamp: str
    id: str
