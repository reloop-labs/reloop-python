from __future__ import annotations
from typing import Optional
from reloop_email.client import ReloopClient
from reloop_email.services.api_key.errors import ReloopValidationError
from reloop_email.services.contacts._nested import *
from .result import *
BASE="/api/contacts/v1/groups"; MEMBERS="/api/contacts/group"
def _name(r:dict,maxlen:int):
 n=ident(r.get("name"),"Group","name")
 if len(n)>maxlen:raise ReloopValidationError(f"Group name must be at most {maxlen} characters.","name")
 return n
def create_group(c:ReloopClient,params:dict):return fetch(c,BASE+"/create","POST",{"name":_name(obj(params,"create"),50)},to_group_result)
def list_groups(c:ReloopClient,params:Optional[dict]=None):return list_fetch(c,BASE+"/list",params,to_group_list_result)
def get_group(c:ReloopClient,id:str):return fetch(c,BASE+"/"+ident(id,"Group"),"GET",None,to_group_result)
def update_group(c:ReloopClient,id:str,params:dict):return fetch(c,BASE+"/"+ident(id,"Group"),"PATCH",{"name":_name(obj(params,"update"),255)},to_group_result)
def delete_group(c:ReloopClient,id:str):return fetch(c,BASE+"/"+ident(id,"Group"),"DELETE",None,to_group_result)
def list_group_contacts(c:ReloopClient,id:str,params:Optional[dict]=None):return list_fetch(c,BASE+"/"+ident(id,"Group")+"/contacts",params,to_group_contacts_result)
def add_contact_to_group(c:ReloopClient,id:str,params:dict):return fetch(c,MEMBERS+"/"+ident(id,"Group"),"POST",membership(obj(params,"addContact")),to_group_result)
def remove_contact_from_group(c:ReloopClient,id:str,params:dict):return fetch(c,MEMBERS+"/"+ident(id,"Group"),"DELETE",membership(obj(params,"removeContact")),to_group_result)
