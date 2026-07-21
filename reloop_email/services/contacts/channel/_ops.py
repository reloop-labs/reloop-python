from __future__ import annotations
from typing import Optional
from reloop_email.client import ReloopClient
from reloop_email.services.api_key.errors import ReloopValidationError
from reloop_email.services.contacts._nested import *
from .result import *
BASE="/api/contacts/v1/channels"; MEMBERS="/api/contacts/channel"
def _name(v):return ident(v,"Channel","name")
def _visibility(v):
 if v not in ("private","public"):raise ReloopValidationError('Channel visibility must be "private" or "public".',"visibility")
 return v
def _subscription(v,key="subscription"):
 if v not in ("opt_in","opt_out"):raise ReloopValidationError(f'Channel {key} must be "opt_in" or "opt_out".',key)
 return v
def create_channel(c:ReloopClient,params:dict):
 r=obj(params,"create");b={"name":_name(r.get("name"))}
 if "description" in r:b["description"]=r["description"]
 if "defaultSubscription" in r:b["defaultSubscription"]=_subscription(r["defaultSubscription"],"defaultSubscription")
 if "visibility" in r:b["visibility"]=_visibility(r["visibility"])
 return fetch(c,BASE+"/create","POST",b,to_channel_result)
def list_channels(c:ReloopClient,params:Optional[dict]=None):return list_fetch(c,BASE+"/list",params,to_channel_list_result)
def get_channel(c:ReloopClient,id:str):return fetch(c,BASE+"/"+ident(id,"Channel"),"GET",None,to_channel_result)
def update_channel(c:ReloopClient,id:str,params:dict):
 r=obj(params,"update");b={}
 if "name" in r:b["name"]=_name(r["name"])
 if "description" in r:b["description"]=r["description"]
 if "visibility" in r:b["visibility"]=_visibility(r["visibility"])
 if not b:raise ReloopValidationError("update requires at least one of name, description, or visibility.","params")
 return fetch(c,BASE+"/"+ident(id,"Channel"),"PATCH",b,to_channel_result)
def delete_channel(c:ReloopClient,id:str):return fetch(c,BASE+"/"+ident(id,"Channel"),"DELETE",None,to_channel_result)
def add_contact_to_channel(c:ReloopClient,id:str,params:dict):
 r=obj(params,"addContact");b=membership(r)
 if "subscription" in r:b["subscription"]=_subscription(r["subscription"])
 return fetch(c,MEMBERS+"/"+ident(id,"Channel"),"POST",b,to_channel_result)
def update_channel_subscription(c:ReloopClient,id:str,params:dict):
 r=obj(params,"updateSubscription");b=membership(r);b["subscription"]=_subscription(r.get("subscription"))
 return fetch(c,MEMBERS+"/"+ident(id,"Channel"),"PATCH",b,to_channel_result)
