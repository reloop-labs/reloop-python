from __future__ import annotations
from typing import Optional
from reloop_email.client import ReloopClient
from reloop_email.services.domain._ops import *
from reloop_email.services.domain.result import DomainListResult, DomainResult
from reloop_email.services.domain.types import *
class DomainService:
 def __init__(self,client:ReloopClient)->None: self._client=client
 def create(self,params:CreateDomainParams)->DomainResult[Domain]: return create_domain(self._client,params)
 def list(self,params:Optional[ListDomainsParams]=None)->DomainListResult: return list_domains(self._client,params)
 def get(self,id:str)->DomainResult[Domain]: return get_domain(self._client,id)
 def update(self,id:str,params:UpdateDomainParams)->DomainResult[Domain]: return update_domain(self._client,id,params)
 def delete(self,id:str)->DomainResult[Domain]: return delete_domain(self._client,id)
 def verify(self,id:str)->DomainResult[DomainStatusResponse]: return verify_domain(self._client,id)
