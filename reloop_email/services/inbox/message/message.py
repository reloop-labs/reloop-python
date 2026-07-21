from __future__ import annotations
from typing import Any, Optional
from reloop_email.client import ReloopClient
from reloop_email.services.api_key.errors import ReloopValidationError
from .fields import require_id,require_string,require_bool,optional_bool,require_int,require_recipients,require_ids
from .result import to_message_result,to_message_list_result
BASE="/api/inbox/v1/messages"
def _obj(v:object,op:str)->dict:
 if not isinstance(v,dict): raise ReloopValidationError(f"{op} params are required and must be an object.","params")
 return v
def _query(p:dict,fields:tuple):
 q={}
 for k in fields:
  if k in p:
   v=p[k]
   if k=="limit": v=require_int(v,k,1,200)
   elif k=="offset": v=require_int(v,k,0)
   elif k in ("isSpam",): v=require_bool(v,k)
   elif not isinstance(v,str): raise ReloopValidationError(f"list {k} must be a string when provided.",k)
   q[k]=v
 return q
def list_messages(client:ReloopClient,params:object=None):
 p={} if params is None else _obj(params,"list");return to_message_list_result(client.fetch(BASE,method="GET",params=_query(p,("mailboxId","limit","offset","q","isSpam"))))
def list_sent_messages(client:ReloopClient,params:object=None):
 p={} if params is None else _obj(params,"listSent");return to_message_list_result(client.fetch(BASE+"/sent",method="GET",params=_query(p,("mailboxId",))))
def get_message(client:ReloopClient,id:object): return to_message_result(client.fetch(BASE+"/"+require_id(id,"Message"),method="GET"))
def get_raw_message(client:ReloopClient,id:object): return to_message_result(client.fetch(BASE+"/"+require_id(id,"Message")+"/raw",method="GET"))
def get_message_attachment(client:ReloopClient,id:object,attachment_id:object): return to_message_result(client.fetch(BASE+"/"+require_id(id,"Message")+"/attachments/"+require_id(attachment_id,"Attachment","attachmentId"),method="GET"))
def batch_messages(client:ReloopClient,params:object):
 p=_obj(params,"batch");return to_message_list_result(client.fetch(BASE+"/batch",method="POST",json={"ids":require_ids(p.get("ids"))}))
def update_message(client:ReloopClient,id:object,params:object):
 p=_obj(params,"update");body={k:require_bool(p[k],k) for k in ("isRead","isStarred","isSpam") if k in p}
 if not body: raise ReloopValidationError("update requires at least one field to change.","params")
 return to_message_result(client.fetch(BASE+"/"+require_id(id,"Message"),method="PATCH",json=body))
def set_message_read(client:ReloopClient,id:object,params:object):
 p=_obj(params,"setRead"); return to_message_result(client.fetch(BASE+"/"+require_id(id,"Message")+"/read",method="PATCH",json={"isRead":require_bool(p.get("isRead"),"isRead")}))
def set_message_star(client:ReloopClient,id:object,params:object):
 p=_obj(params,"setStar"); return to_message_result(client.fetch(BASE+"/"+require_id(id,"Message")+"/star",method="PATCH",json={"isStarred":require_bool(p.get("isStarred"),"isStarred")}))
def delete_message(client:ReloopClient,id:object): return to_message_result(client.fetch(BASE+"/"+require_id(id,"Message"),method="DELETE"))
def send_message(client:ReloopClient,params:object):
 p=_obj(params,"send"); body={"mailboxId":require_string(p.get("mailboxId"),"mailboxId"),"to":require_recipients(p.get("to"),"to"),"subject":require_string(p.get("subject"),"subject")}
 for k in ("text","html","cc","bcc","attachments","scheduledAt","undoWindowSeconds"):
  if k in p: body[k]=p[k]
 return to_message_result(client.fetch(BASE+"/send",method="POST",json=body))
def cancel_pending_message(client:ReloopClient,id:object): return to_message_result(client.fetch(BASE+"/pending/"+require_id(id,"Message")+"/cancel",method="POST"))
def _compose(client,id,params,suffix,forward=False):
 p=_obj(params,suffix); body={k:p[k] for k in ("text","html","cc","bcc","attachments") if k in p}
 if "text" not in body and "html" not in body: raise ReloopValidationError("at least one of text or html is required.","params")
 if forward: body["to"]=require_recipients(p.get("to"),"to")
 return to_message_result(client.fetch(BASE+"/"+require_id(id,"Message")+"/"+suffix,method="POST",json=body))
def reply_to_message(c,id,p): return _compose(c,id,p,"reply")
def reply_all_to_message(c,id,p): return _compose(c,id,p,"reply-all")
def forward_message(c,id,p): return _compose(c,id,p,"forward",True)
class MessageService:
 def __init__(self,client): self._client=client
 def list(self,p=None): return list_messages(self._client,p)
 def list_sent(self,p=None): return list_sent_messages(self._client,p)
 def get(self,id): return get_message(self._client,id)
 def batch(self,p): return batch_messages(self._client,p)
 def get_raw(self,id): return get_raw_message(self._client,id)
 def get_attachment(self,id,attachment_id): return get_message_attachment(self._client,id,attachment_id)
 def update(self,id,p): return update_message(self._client,id,p)
 def set_read(self,id,p): return set_message_read(self._client,id,p)
 def set_star(self,id,p): return set_message_star(self._client,id,p)
 def delete(self,id): return delete_message(self._client,id)
 def send(self,p): return send_message(self._client,p)
 def cancel_pending(self,id): return cancel_pending_message(self._client,id)
 def reply(self,id,p): return reply_to_message(self._client,id,p)
 def reply_all(self,id,p): return reply_all_to_message(self._client,id,p)
 def forward(self,id,p): return forward_message(self._client,id,p)
