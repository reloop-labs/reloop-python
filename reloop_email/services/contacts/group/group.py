from __future__ import annotations
from typing import Optional
from reloop_email.client import ReloopClient
from ._ops import *
class GroupService:
 def __init__(self,client:ReloopClient):self._client=client
 def create(self,params:dict):return create_group(self._client,params)
 def list(self,params:Optional[dict]=None):return list_groups(self._client,params)
 def get(self,id:str):return get_group(self._client,id)
 def update(self,id:str,params:dict):return update_group(self._client,id,params)
 def delete(self,id:str):return delete_group(self._client,id)
 def list_contacts(self,id:str,params:Optional[dict]=None):return list_group_contacts(self._client,id,params)
 def add_contact(self,id:str,params:dict):return add_contact_to_group(self._client,id,params)
 def remove_contact(self,id:str,params:dict):return remove_contact_from_group(self._client,id,params)
