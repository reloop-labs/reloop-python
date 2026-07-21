from __future__ import annotations
INBOX_V1 = "/api/inbox/v1"
MAILBOXES_V1 = INBOX_V1 + "/mailboxes"
def mailbox_list_path() -> str: return MAILBOXES_V1 + "/list"
def mailbox_create_path() -> str: return MAILBOXES_V1 + "/create"
def mailbox_by_id(id: str) -> str: return MAILBOXES_V1 + "/" + id
