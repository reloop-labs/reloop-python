from __future__ import annotations
from reloop_email.client import ReloopClient
from reloop_email.services.api_key.errors import ReloopValidationError
from .fields import require_id,require_bool,require_int,require_ids
from .result import to_thread_result,to_thread_list_result
BASE="/api/inbox/v1/threads"
def _obj(v,op):
 if not isinstance(v,dict): raise ReloopValidationError(f"{op} params are required and must be an object.","params")
 return v
def list_threads(c,params=None):
 p={} if params is None else _obj(params,"list");q={}
 for k in ("mailboxId","folder","q","filter"):
  if k in p:
   if not isinstance(p[k],str): raise ReloopValidationError(f"list {k} must be a string when provided.",k)
   q[k]=p[k]
 for k,lo,hi in (("limit",1,200),("offset",0,None)):
  if k in p:q[k]=require_int(p[k],k,lo,hi)
 if "isPinned" in p:q["isPinned"]=require_bool(p["isPinned"],"isPinned")
 return to_thread_list_result(c.fetch(BASE,method="GET",params=q))
def batch_threads(c,params):
 p=_obj(params,"batch"); action=p.get("action"); valid=("archive","trash","restore","star","unstar","read","unread","important","unimportant","spam","unspam","pin","unpin")
 if action not in valid: raise ReloopValidationError("batch action must be a valid thread batch action.","action")
 return to_thread_result(c.fetch(BASE+"/batch",method="POST",json={"ids":require_ids(p.get("ids")),"action":action}))
def get_thread(c,id): return to_thread_result(c.fetch(BASE+"/"+require_id(id,"Thread"),method="GET"))
def get_thread_attachment(c,id,attachment_id): return to_thread_result(c.fetch(BASE+"/"+require_id(id,"Thread")+"/attachments/"+require_id(attachment_id,"Attachment","attachmentId"),method="GET"))
def update_thread(c,id,params):
 p=_obj(params,"update");body={k:require_bool(p[k],k) for k in ("isRead","isStarred","isImportant","isPinned") if k in p}
 if "status" in p:
  if p["status"] not in ("active","archived","closed","trash"): raise ReloopValidationError('status must be "active", "archived", "closed", or "trash".',"status")
  body["status"]=p["status"]
 if not body: raise ReloopValidationError("update requires at least one field to change.","params")
 return to_thread_result(c.fetch(BASE+"/"+require_id(id,"Thread"),method="PATCH",json=body))
def set_thread_read(c,id,params):
 p=_obj(params,"setRead");return to_thread_result(c.fetch(BASE+"/"+require_id(id,"Thread")+"/read",method="PATCH",json={"isRead":require_bool(p.get("isRead"),"isRead")}))
def set_thread_star(c,id,params):
 p=_obj(params,"setStar");return to_thread_result(c.fetch(BASE+"/"+require_id(id,"Thread")+"/star",method="PATCH",json={"isStarred":require_bool(p.get("isStarred"),"isStarred")}))
def _action(c,id,action): return to_thread_result(c.fetch(BASE+"/"+require_id(id,"Thread")+"/"+action,method="POST"))
def archive_thread(c,id):return _action(c,id,"archive")
def trash_thread(c,id):return _action(c,id,"trash")
def restore_thread(c,id):return _action(c,id,"restore")
def delete_thread(c,id):return to_thread_result(c.fetch(BASE+"/"+require_id(id,"Thread"),method="DELETE"))
class ThreadService:
 def __init__(self,c):self._client=c
 def list(self,p=None):return list_threads(self._client,p)
 def batch(self,p):return batch_threads(self._client,p)
 def get(self,id):return get_thread(self._client,id)
 def get_attachment(self,id,attachment_id):return get_thread_attachment(self._client,id,attachment_id)
 def update(self,id,p):return update_thread(self._client,id,p)
 def set_read(self,id,p):return set_thread_read(self._client,id,p)
 def set_star(self,id,p):return set_thread_star(self._client,id,p)
 def archive(self,id):return archive_thread(self._client,id)
 def trash(self,id):return trash_thread(self._client,id)
 def restore(self,id):return restore_thread(self._client,id)
 def delete(self,id):return delete_thread(self._client,id)
