from __future__ import annotations
from typing import Dict, List, Literal, Optional, TypedDict
ContactStatus = Literal["subscribed", "unsubscribed", "blocked"]
class ContactChannelInput(TypedDict): channelId: str; subscription: Literal["opt_in", "opt_out"]
class Contact(TypedDict, total=False): object:str; id:str; email:str; firstName:Optional[str]; lastName:Optional[str]; status:ContactStatus; properties:Dict[str, object]; groups:List[dict]; channels:List[dict]; suppressionReason:Optional[str]; suppressedAt:Optional[str]; createdAt:str; updatedAt:str
class ContactResponse(Contact, total=False): event:str
class CreateContactParams(TypedDict, total=False): email:str; firstName:str; lastName:str; status:ContactStatus; properties:Dict[str,object]; groupIds:List[str]; channels:List[ContactChannelInput]
class UpdateContactParams(TypedDict, total=False): email:str; firstName:str; lastName:str; status:ContactStatus; properties:Dict[str,object]
class ListContactsParams(TypedDict, total=False): page:int; limit:int; search:str; status:ContactStatus
class ContactListResponse(TypedDict, total=False): object:str; contacts:List[Contact]; total:int; page:int; limit:int; totalContacts:int; subscribedContacts:int; unsubscribedContacts:int; event:str
class DeleteContactResponse(TypedDict, total=False): success:bool; object:str; id:str; event:str
