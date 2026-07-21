from __future__ import annotations
from reloop_email.client import ReloopClient
from reloop_email.services.api_key.errors import ReloopValidationError
from .result import to_webhook_result,to_webhook_list_result,to_webhook_delivery_list_result
from .verify.verify import verify_webhook,WEBHOOK_SIGNATURE_HEADER
BASE="/api/webhook/v1"
def _obj(v,op):
 if not isinstance(v,dict):raise ReloopValidationError(f"{op} params are required and must be an object.","params")
 return v
def _id(v,field="webhookId"):
 if not isinstance(v,str) or not v.strip():raise ReloopValidationError(f"Webhook {field} is required and must be a non-empty string.",field)
 return v.strip()
def create_webhook(c,params): return to_webhook_result(c.fetch(BASE+"/",method="POST",json=_obj(params,"create")))
def list_webhooks(c,params=None):
 p={} if params is None else _obj(params,"list");q={}
 for k in ("page","limit"):
  if k in p and (not isinstance(p[k],int) or isinstance(p[k],bool) or p[k]<1 or (k=="limit" and p[k]>100)):raise ReloopValidationError(f"list {k} must be valid.",k)
  if k in p:q[k]=p[k]
 for k in ("status","organizationId","userId"):
  if k in p:
   if not isinstance(p[k],str) or not p[k].strip():raise ReloopValidationError(f"list {k} must be a non-empty string when provided.",k)
   q[k]=p[k].strip()
 if "status" in q and q["status"] not in ("active","paused","disabled","failed"):raise ReloopValidationError("list status must be a valid webhook status.","status")
 return to_webhook_list_result(c.fetch(BASE,method="GET",params=q))
def get_webhook(c,id):return to_webhook_result(c.fetch(BASE+"/"+_id(id),method="GET"))
def update_webhook(c,id,params):
 p=_obj(params,"update"); allowed=("description","name","url","secret","status","customHeaders","rateLimitEnabled","maxRequestsPerMinute","maxRetries","retryBackoffMultiplier","filteringOptions");body={k:p[k] for k in allowed if k in p}
 if not body:raise ReloopValidationError("update requires at least one field to change.","params")
 if "status" in body and body["status"] not in ("active","paused","disabled","failed"):raise ReloopValidationError("update status must be a valid webhook status.","status")
 return to_webhook_result(c.fetch(BASE+"/"+_id(id),method="PATCH",json=body))
def delete_webhook(c,id):return to_webhook_result(c.fetch(BASE+"/"+_id(id),method="DELETE"))
def trigger_webhook(c,params):
 p=_obj(params,"trigger");event=p.get("event");payload=p.get("payload")
 if not isinstance(event,str) or not event.strip():raise ReloopValidationError("trigger event is required and must be a non-empty string.","event")
 if not isinstance(payload,dict):raise ReloopValidationError("trigger payload is required and must be an object.","payload")
 return to_webhook_result(c.fetch(BASE+"/trigger",method="POST",json=p))
def list_webhook_deliveries(c,id,params=None):
 p={} if params is None else _obj(params,"listDeliveries");q={k:p[k] for k in ("page","limit","status") if k in p and p[k] != ""}
 return to_webhook_delivery_list_result(c.fetch(BASE+"/"+_id(id)+"/deliveries",method="GET",params=q))
def retry_webhook_delivery(c,id):
 if not isinstance(id,str) or not id.strip():raise ReloopValidationError("Webhook delivery deliveryId is required and must be a non-empty string.","deliveryId")
 return to_webhook_result(c.fetch("/api/webhook/deliveries/"+id.strip()+"/retry",method="POST"))
class WebhookService:
 def __init__(self, c: ReloopClient) -> None:
  self._client = c
 @staticmethod
 def verify(params: object) -> dict:
  return verify_webhook(params)
 @staticmethod
 def construct_event(payload: object, signature: str, secret: str, tolerance: int = 300) -> dict:
  return verify_webhook({"payload": payload, "headers": {WEBHOOK_SIGNATURE_HEADER: signature}, "secret": secret, "tolerance": tolerance})
 def create(self, p: object):
  return create_webhook(self._client, p)
 def list(self, p: object = None):
  return list_webhooks(self._client, p)
 def get(self, id: object):
  return get_webhook(self._client, id)
 def update(self, id: object, p: object):
  return update_webhook(self._client, id, p)
 def delete(self, id: object):
  return delete_webhook(self._client, id)
 def pause(self, id: object):
  return update_webhook(self._client, id, {"status": "paused"})
 def enable(self, id: object):
  return update_webhook(self._client, id, {"status": "active"})
 def disable(self, id: object):
  return update_webhook(self._client, id, {"status": "disabled"})
 def trigger(self, p: object):
  return trigger_webhook(self._client, p)
 def list_deliveries(self, id: object, p: object = None):
  return list_webhook_deliveries(self._client, id, p)
 def retry_delivery(self, id: object):
  return retry_webhook_delivery(self._client, id)
