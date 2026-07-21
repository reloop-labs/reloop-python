from __future__ import annotations
from typing import Any, Optional
from urllib.parse import urlencode
from reloop_email.client import ReloopClient
from reloop_email.core.result import ReloopResult
from reloop_email.services.api_key.errors import ReloopValidationError
def obj(x:object,label:str)->dict:
 if not isinstance(x,dict):raise ReloopValidationError(f"{label} params are required and must be an object.","params")
 return x
def ident(x:Any,label:str,id:str="id")->str:
 if not isinstance(x,str) or not x.strip():raise ReloopValidationError(f"{label} {id} is required and must be a non-empty string.",id)
 return x.strip()
def page(v:Any,key:str)->int:
 if not isinstance(v,int) or isinstance(v,bool) or v<1:raise ReloopValidationError(f"list {key} must be an integer >= 1.",key)
 return v
def limit(v:Any,key:str)->int:
 if not isinstance(v,int) or isinstance(v,bool) or not 1<=v<=100:raise ReloopValidationError(f"list {key} must be an integer between 1 and 100.",key)
 return v
def membership(raw:dict)->dict:
 out={}
 for k in ("contact_id","email"):
  if k in raw:out[k]=ident(raw[k],"",k)
 if not out:raise ReloopValidationError("Either contact_id or email is required.","params")
 return out
def fetch(c:ReloopClient,path:str,method:str,body:Optional[dict], convert):
 r=c.fetch(path,method=method,json=body);return convert(ReloopResult(response=r.response,error=r.error))
def list_fetch(c:ReloopClient,path:str,q:Optional[dict],convert):
 query={}
 if q is not None:
  if not isinstance(q,dict):raise ReloopValidationError("list params must be an object when provided.","params")
  if "page" in q:query["page"]=str(page(q["page"],"page"))
  if "limit" in q:query["limit"]=str(limit(q["limit"],"limit"))
  for k in ("search","type","status"):
   if k in q:
    if not isinstance(q[k],str):raise ReloopValidationError(f"list {k} must be a string when provided.",k)
    if q[k]:query[k]=q[k]
 return fetch(c,path + ("?"+urlencode(query) if query else ""),"GET",None,convert)
