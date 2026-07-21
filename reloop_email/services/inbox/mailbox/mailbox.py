from __future__ import annotations
from typing import Any, Mapping, Optional
from reloop_email.client import ReloopClient
from reloop_email.services.api_key.errors import ReloopValidationError
from .fields import require_id, require_string, optional_string
from .result import to_mailbox_result,to_mailbox_list_result
BASE="/api/inbox/v1/mailboxes"
def _object(params: object, op:str)->dict:
 if not isinstance(params,dict): raise ReloopValidationError(f"{op} params are required and must be an object.","params")
 return params
def create_mailbox(client:ReloopClient,params:object):
 p=_object(params,"create"); body={"domainId":require_string(p.get("domainId"),"domainId"),"email":require_string(p.get("email"),"email")}
 for k in ("password","quota","displayName"):
  if k in p: body[k]=optional_string(p[k],k)
 return to_mailbox_result(client.fetch(BASE+"/create",method="POST",json=body))
def list_mailboxes(client:ReloopClient): return to_mailbox_list_result(client.fetch(BASE+"/list",method="GET"))
def get_mailbox(client:ReloopClient,id:object): return to_mailbox_result(client.fetch(BASE+"/"+require_id(id,"Mailbox"),method="GET"))
def update_mailbox(client:ReloopClient,id:object,params:object):
 p=_object(params,"update"); body={k:p[k] for k in ("displayName","quota","status") if k in p}
 if not body: raise ReloopValidationError("update requires at least one of displayName, status, or quota.","params")
 if "status" in body and body["status"] not in ("active","disabled"): raise ReloopValidationError('status must be "active" or "disabled".',"status")
 if any(not isinstance(v,str) for k,v in body.items() if k != "status"): raise ReloopValidationError("update values must be strings when provided.","params")
 return to_mailbox_result(client.fetch(BASE+"/"+require_id(id,"Mailbox"),method="PATCH",json=body))
def delete_mailbox(client:ReloopClient,id:object): return to_mailbox_result(client.fetch(BASE+"/"+require_id(id,"Mailbox"),method="DELETE"))
class MailboxService:
 def __init__(self,client:ReloopClient): self._client=client
 def list(self): return list_mailboxes(self._client)
 def get(self,id:object): return get_mailbox(self._client,id)
 def create(self,params:object): return create_mailbox(self._client,params)
 def update(self,id:object,params:object): return update_mailbox(self._client,id,params)
 def delete(self,id:object): return delete_mailbox(self._client,id)
