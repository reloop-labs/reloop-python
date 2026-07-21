from __future__ import annotations
from typing import Any, Optional, cast
from urllib.parse import urlencode
from reloop_email.client import ReloopClient
from reloop_email.core.result import ReloopResult
from reloop_email.services.domain.errors import ReloopValidationError
from reloop_email.services.domain.fields import *
from reloop_email.services.domain.paths import *
from reloop_email.services.domain.result import *
from reloop_email.services.domain.types import *
def _obj(params: object, label: str) -> dict[str, Any]:
 if not isinstance(params,dict): raise ReloopValidationError(f"{label} params are required and must be an object.","params")
 return cast(dict[str,Any],params)
def _result(client: ReloopClient,path: str,method: str, body: Optional[dict[str,Any]]=None) -> DomainResult[Any]:
 r=client.fetch(path,method=method,json=body); return to_domain_result(ReloopResult(response=r.response,error=r.error))
def create_domain(client: ReloopClient, params: CreateDomainParams) -> DomainResult[Domain]:
 raw=_obj(params,"create"); body={"domain":require_domain_name(raw.get("domain"))}
 for key in ("click_tracking","open_tracking","sending_email","receiving_email"):
  if key in raw: body[key]=optional_boolean(raw[key],key)
 if "tls" in raw: body["tls"]=optional_tls(raw["tls"])
 return _result(client,domain_create_path(),"POST",body)
def list_domains(client: ReloopClient,params: Optional[ListDomainsParams]=None) -> DomainListResult:
 query={}
 if params is not None:
  if not isinstance(params,dict): raise ReloopValidationError("list params must be an object when provided.","params")
  if "page" in params: query["page"]=str(require_page(params["page"]))
  if "limit" in params: query["limit"]=str(require_limit(params["limit"]))
  if "q" in params:
   if not isinstance(params["q"],str): raise ReloopValidationError("list q must be a string when provided.","q")
   if params["q"]: query["q"]=params["q"]
  if "status" in params:
   if params["status"] not in ("pending","verifying","active","suspended","failed"): raise ReloopValidationError("status must be a valid domain status.","status")
   query["status"]=params["status"]
 r=client.fetch(domain_list_path(urlencode(query)),method="GET"); return to_domain_list_result(ReloopResult(response=r.response,error=r.error))
def get_domain(client:ReloopClient,id:str)->DomainResult[Domain]: return _result(client,domain_by_id(require_domain_id(id)),"GET")
def delete_domain(client:ReloopClient,id:str)->DomainResult[Domain]: return _result(client,domain_by_id(require_domain_id(id)),"DELETE")
def verify_domain(client:ReloopClient,id:str)->DomainResult[DomainStatusResponse]: return _result(client,domain_verify_path(require_domain_id(id)),"POST")
def update_domain(client:ReloopClient,id:str,params:UpdateDomainParams)->DomainResult[Domain]:
 raw=_obj(params,"update"); body={}
 for key in ("click_tracking","open_tracking","sending_email","receiving_email"):
  if key in raw: body[key]=optional_boolean(raw[key],key)
 if "tls" in raw: body["tls"]=optional_tls(raw["tls"])
 if not body: raise ReloopValidationError("update requires at least one of click_tracking, open_tracking, sending_email, receiving_email, or tls.","params")
 return _result(client,domain_by_id(require_domain_id(id)),"PATCH",body)
