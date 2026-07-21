from __future__ import annotations
from typing import Optional
from reloop_email.client import ReloopClient
from ._ops import *
from .property.property import PropertyService
from .group.group import GroupService
from .channel.channel import ChannelService
class ContactsService:
 def __init__(self,client:ReloopClient):
  self._client=client;self.properties=PropertyService(client);self.groups=GroupService(client);self.channels=ChannelService(client)
 def create(self,params:dict):return create_contact(self._client,params)
 def get(self,id:str):return get_contact(self._client,id)
 def list(self,params:Optional[dict]=None):return list_contacts(self._client,params)
 def update(self,id:str,params:dict):return update_contact(self._client,id,params)
 def delete(self,id:str):return delete_contact(self._client,id)
