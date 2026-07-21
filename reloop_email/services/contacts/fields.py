from __future__ import annotations
import re
from typing import Any, Dict, Optional
from reloop_email.services.contacts.errors import ReloopValidationError
def require_contact_id(value:Any,field:str="id")->str:
 if not isinstance(value,str) or not value.strip():raise ReloopValidationError(f"Contact {field} is required and must be a non-empty string.",field)
 return value.strip()
def require_email(value:Any,field:str="email")->str:
 if not isinstance(value,str) or not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+",value.strip()):raise ReloopValidationError(f"Contact {field} must be a valid email address.",field)
 return value.strip()
def optional_status(v:Any,field:str="status")->Optional[str]:
 if v is None:return None
 if v not in ("subscribed","unsubscribed","blocked"):raise ReloopValidationError(f'{field} must be "subscribed", "unsubscribed", or "blocked".',field)
 return v
def optional_string(v:Any,field:str)->Optional[str]:
 if v is None:return None
 if not isinstance(v,str):raise ReloopValidationError(f"{field} must be a string when provided.",field)
 return v
def require_page(v:Any,field:str="page")->int:
 if not isinstance(v,int) or isinstance(v,bool) or v<1:raise ReloopValidationError(f"list {field} must be an integer >= 1.",field)
 return v
def require_limit(v:Any,field:str="limit")->int:
 if not isinstance(v,int) or isinstance(v,bool) or not 1<=v<=100:raise ReloopValidationError(f"list {field} must be an integer between 1 and 100.",field)
 return v
def properties(v:Any,update:bool=False)->Optional[Dict[str,object]]:
 if v is None:return None
 if not isinstance(v,dict):raise ReloopValidationError("properties must be an object when provided.","properties")
 pattern=r"[a-z_]+" if update else r"[a-z0-9_]+"
 for k,val in v.items():
  if not re.fullmatch(pattern,k):raise ReloopValidationError(f"properties keys must match {pattern}.","properties")
  if not isinstance(val,(str,int)) or isinstance(val,bool):raise ReloopValidationError(f"properties.{k} must be a string or number.","properties")
 return v
def membership(raw:dict)->dict:
 out={}
 for k in ("contact_id","email"):
  if k in raw:
   if not isinstance(raw[k],str) or not raw[k].strip():raise ReloopValidationError(f"{k} must be a non-empty string when provided.",k)
   out[k]=raw[k].strip()
 if not out:raise ReloopValidationError("Either contact_id or email is required.","params")
 return out
