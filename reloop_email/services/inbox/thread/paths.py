from __future__ import annotations
from reloop_email.services.inbox.mailbox.paths import INBOX_V1
THREADS_V1 = INBOX_V1 + "/threads"
def thread_list_path(query_string: str = "") -> str: return THREADS_V1 + (("?" + query_string) if query_string else "")
def thread_batch_path() -> str: return THREADS_V1 + "/batch"
def thread_by_id(id: str) -> str: return THREADS_V1 + "/" + id
def thread_attachment_path(id: str, attachment_id: str) -> str: return thread_by_id(id) + "/attachments/" + attachment_id
def thread_read_path(id: str) -> str: return thread_by_id(id) + "/read"
def thread_star_path(id: str) -> str: return thread_by_id(id) + "/star"
def thread_archive_path(id: str) -> str: return thread_by_id(id) + "/archive"
def thread_trash_path(id: str) -> str: return thread_by_id(id) + "/trash"
def thread_restore_path(id: str) -> str: return thread_by_id(id) + "/restore"
