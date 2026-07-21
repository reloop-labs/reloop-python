from __future__ import annotations
from typing import Any, Optional, cast
from urllib.parse import urlencode
from reloop_email.client import ReloopClient
from reloop_email.core.result import ReloopResult
from reloop_email.services.contacts.errors import ReloopValidationError
from reloop_email.services.contacts.fields import *
from reloop_email.services.contacts.paths import *
from reloop_email.services.contacts.result import *
from reloop_email.services.contacts.types import *
def _obj(p:object,label:str)->dict:
 if not isinstance(p,dict):raise ReloopValidationError(f"{label} params are required and must be an object.","params")
 return p
def _res(c:ReloopClient,path:str,method:str,body:Optional[dict]=None)->ContactResult[Any]:
 r=c.fetch(path,method=method,json=body);return to_contact_result(ReloopResult(response=r.response,error=r.error))
def create_contact(c:ReloopClient,params:CreateContactParams)->ContactResult[ContactResponse]:
 raw=_obj(params,"create");body={"email":require_email(raw.get("email"))}
 for key in ("firstName","lastName"): 
  if key in raw:body[key]=optional_string(raw[key],key)
 if "status" in raw:body["status"]=optional_status(raw["status"])
 if "properties" in raw:body["properties"]=properties(raw["properties"])
 if "groupIds" in raw:
  if not isinstance(raw["groupIds"],list) or any(not isinstance(x,str) or not x.strip() for x in raw["groupIds"]):raise ReloopValidationError("groupIds must be an array of non-empty strings.","groupIds")
  body["groupIds"]=[x.strip() for x in raw["groupIds"]]
 if "channels" in raw:
  if not isinstance(raw["channels"],list):raise ReloopValidationError("channels must be an array when provided.","channels")
  body["channels"]=raw["channels"]
 return _res(c,contact_create_path(),"POST",body)
def list_contacts(c:ReloopClient,params:Optional[ListContactsParams]=None)->ContactListResult:
 q={}
 if params is not None:
  if not isinstance(params,dict):raise ReloopValidationError("list params must be an object when provided.","params")
  if "page" in params:q["page"]=str(require_page(params["page"]))
  if "limit" in params:q["limit"]=str(require_limit(params["limit"]))
  if "search" in params:
   if not isinstance(params["search"],str):raise ReloopValidationError("list search must be a string when provided.","search")
   if params["search"]:q["search"]=params["search"]
  if "status" in params:q["status"]=cast(str,optional_status(params["status"]))
 r=c.fetch(contact_list_path(urlencode(q)),method="GET");return to_contact_list_result(ReloopResult(response=r.response,error=r.error))
def get_contact(c:ReloopClient,id:str)->ContactResult[Contact]:return _res(c,contact_retrieve_path(require_contact_id(id)),"GET")
def delete_contact(c:ReloopClient,id:str)->ContactResult[DeleteContactResponse]:return _res(c,contact_by_id(require_contact_id(id)),"DELETE")
def update_contact(c:ReloopClient,id:str,params:UpdateContactParams)->ContactResult[ContactResponse]:
 raw=_obj(params,"update");body={}
 if "email" in raw:body["email"]=require_email(raw["email"])
 for k in ("firstName","lastName"):
  if k in raw:body[k]=optional_string(raw[k],k)
 if "status" in raw:body["status"]=optional_status(raw["status"])
 if "properties" in raw:body["properties"]=properties(raw["properties"],True)
 if not body:raise ReloopValidationError("update requires at least one of email, firstName, lastName, status, or properties.","params")
 return _res(c,contact_by_id(require_contact_id(id)),"PATCH",body)
