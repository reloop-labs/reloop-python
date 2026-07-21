from __future__ import annotations
from reloop_email.services.inbox.mailbox.paths import INBOX_V1
MESSAGES_V1 = INBOX_V1 + "/messages"
def message_list_path(query_string: str = "") -> str: return MESSAGES_V1 + (("?" + query_string) if query_string else "")
def message_list_sent_path(query_string: str = "") -> str: return MESSAGES_V1 + "/sent" + (("?" + query_string) if query_string else "")
def message_batch_path() -> str: return MESSAGES_V1 + "/batch"
def message_send_path() -> str: return MESSAGES_V1 + "/send"
def message_by_id(id: str) -> str: return MESSAGES_V1 + "/" + id
def message_raw_path(id: str) -> str: return message_by_id(id) + "/raw"
def message_attachment_path(id: str, attachment_id: str) -> str: return message_by_id(id) + "/attachments/" + attachment_id
def message_read_path(id: str) -> str: return message_by_id(id) + "/read"
def message_star_path(id: str) -> str: return message_by_id(id) + "/star"
def message_pending_cancel_path(id: str) -> str: return MESSAGES_V1 + "/pending/" + id + "/cancel"
def message_reply_path(id: str) -> str: return message_by_id(id) + "/reply"
def message_reply_all_path(id: str) -> str: return message_by_id(id) + "/reply-all"
def message_forward_path(id: str) -> str: return message_by_id(id) + "/forward"
