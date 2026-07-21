from __future__ import annotations
from typing import Optional
from reloop_email.client import ReloopClient
from ._ops import *
class ChannelService:
 def __init__(self,client:ReloopClient):self._client=client
 def create(self,params:dict):return create_channel(self._client,params)
 def list(self,params:Optional[dict]=None):return list_channels(self._client,params)
 def get(self,id:str):return get_channel(self._client,id)
 def update(self,id:str,params:dict):return update_channel(self._client,id,params)
 def delete(self,id:str):return delete_channel(self._client,id)
 def add_contact(self,id:str,params:dict):return add_contact_to_channel(self._client,id,params)
 def update_subscription(self,id:str,params:dict):return update_channel_subscription(self._client,id,params)
