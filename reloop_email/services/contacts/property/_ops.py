from __future__ import annotations
from typing import Optional
from reloop_email.client import ReloopClient
from reloop_email.services.api_key.errors import ReloopValidationError
from reloop_email.services.contacts._nested import *
from .result import *
BASE="/api/contacts/v1/properties"
def create_property(c:ReloopClient,params:dict):
 r=obj(params,"create"); name=ident(r.get("name"),"Property","name"); typ=r.get("type")
 if typ not in ("string","number"):raise ReloopValidationError('Property type must be "string" or "number".',"type")
 b={"name":name,"type":typ}
 if "fallbackValue" in r:
  if not isinstance(r["fallbackValue"],str):raise ReloopValidationError("Property fallbackValue must be a string when provided.","fallbackValue")
  b["fallbackValue"]=r["fallbackValue"]
 return fetch(c,BASE+"/create","POST",b,to_property_result)
def list_properties(c:ReloopClient,params:Optional[dict]=None):
 if isinstance(params,dict) and "type" in params and params["type"] not in ("string","number"):raise ReloopValidationError('Property type must be "string" or "number".',"type")
 return list_fetch(c,BASE+"/list",params,to_property_list_result)
def update_property(c:ReloopClient,id:str,params:dict):
 r=obj(params,"update")
 if "fallbackValue" not in r or (r["fallbackValue"] is not None and not isinstance(r["fallbackValue"],str)):raise ReloopValidationError("Property fallbackValue must be a string or null.","fallbackValue")
 return fetch(c,BASE+"/"+ident(id,"Property"),"PATCH",{"fallbackValue":r["fallbackValue"]},to_property_result)
def delete_property(c:ReloopClient,id:str):return fetch(c,BASE+"/"+ident(id,"Property"),"DELETE",None,to_property_result)
