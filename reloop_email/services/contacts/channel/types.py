from __future__ import annotations
from typing import List, Optional, TypedDict
class ContactChannel(TypedDict,total=False): object:str; id:str; name:str; description:Optional[str]; defaultSubscription:str; visibility:str; createdAt:str; updatedAt:str
class ContactChannelResponse(ContactChannel,total=False): event:str
class CreateChannelParams(TypedDict,total=False): name:str; description:str; defaultSubscription:str; visibility:str
class UpdateChannelParams(TypedDict,total=False): name:str; description:Optional[str]; visibility:str
class ListChannelsParams(TypedDict,total=False): page:int; limit:int
class ChannelListResponse(TypedDict,total=False): object:str; channels:List[ContactChannel]; total:int; page:int; limit:int; event:str
class DeleteChannelResponse(TypedDict,total=False): object:str; success:bool; id:str; name:str; event:str
class AddContactToChannelParams(TypedDict, total=False):
    contact_id: str
    email: str
    subscription: str


class UpdateContactChannelParams(TypedDict, total=False):
    contact_id: str
    email: str
    subscription: str
class AddContactToChannelResponse(TypedDict,total=False): contact:dict; subscriptionId:str; event:str
class UpdateContactChannelResponse(TypedDict,total=False): success:bool; status:str; event:str
