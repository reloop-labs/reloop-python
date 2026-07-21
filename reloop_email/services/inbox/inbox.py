from __future__ import annotations
from reloop_email.client import ReloopClient
from reloop_email.services.inbox.mailbox.mailbox import MailboxService
from reloop_email.services.inbox.message.message import MessageService
from reloop_email.services.inbox.thread.thread import ThreadService
class InboxService:
 def __init__(self, client:ReloopClient)->None:
  self.mailboxes=MailboxService(client); self.messages=MessageService(client); self.threads=ThreadService(client)
