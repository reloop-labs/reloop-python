from __future__ import annotations
from typing import Optional
from reloop_email.client import ReloopClient
from ._ops import *
class PropertyService:
 def __init__(self,client:ReloopClient):self._client=client
 def create(self,params:dict):return create_property(self._client,params)
 def list(self,params:Optional[dict]=None):return list_properties(self._client,params)
 def update(self,id:str,params:dict):return update_property(self._client,id,params)
 def delete(self,id:str):return delete_property(self._client,id)
