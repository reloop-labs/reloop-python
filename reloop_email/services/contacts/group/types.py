from __future__ import annotations
from typing import List, Optional, TypedDict
class ContactGroup(TypedDict,total=False): object:str; id:str; name:str; createdAt:str; updatedAt:str
class ContactGroupResponse(ContactGroup,total=False): event:str
class CreateGroupParams(TypedDict): name:str
class UpdateGroupParams(TypedDict): name:str
class ListGroupsParams(TypedDict,total=False): page:int; limit:int; search:str
class ListGroupContactsParams(TypedDict,total=False): page:int; limit:int; search:str; status:str
class GroupListResponse(TypedDict,total=False): object:str; groups:List[ContactGroup]; total:int; page:int; limit:int; event:str
class GroupContactListResponse(TypedDict,total=False): object:str; group:dict; contacts:List[dict]; total:int; page:int; limit:int; event:str
class AddContactToGroupParams(TypedDict,total=False): contact_id:str; email:str
class RemoveContactFromGroupParams(AddContactToGroupParams,total=False): pass
class AddContactToGroupResponse(TypedDict,total=False): success:bool; object:str; id:str; event:str
class RemoveContactFromGroupResponse(AddContactToGroupResponse,total=False): pass
class DeleteGroupResponse(AddContactToGroupResponse,total=False): name:str
