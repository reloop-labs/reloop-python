from __future__ import annotations
CHANNELS_V1="/api/contacts/v1/channels"
def channel_create_path()->str:return f"{CHANNELS_V1}/create"
def channel_list_path(q:str="")->str:return f"{CHANNELS_V1}/list{'?' + q if q else ''}"
def channel_by_id(id:str)->str:return f"{CHANNELS_V1}/{id}"
