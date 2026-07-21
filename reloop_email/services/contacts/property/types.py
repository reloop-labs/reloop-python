from __future__ import annotations
from typing import List, Optional, TypedDict
class ContactProperty(TypedDict,total=False): object:str; id:str; propertyName:str; propertyType:str; defaultValue:Optional[str]; createdAt:str; updatedAt:str
class ContactPropertyResponse(ContactProperty,total=False): event:str
class CreatePropertyParams(TypedDict,total=False): name:str; type:str; fallbackValue:str
class UpdatePropertyParams(TypedDict,total=False): fallbackValue:Optional[str]
class ListPropertiesParams(TypedDict,total=False): page:int; limit:int; search:str; type:str
class PropertyListResponse(TypedDict,total=False): object:str; properties:List[ContactProperty]; total:int; page:int; limit:int; event:str
class DeletePropertyResponse(TypedDict,total=False): object:str; success:bool; id:str; name:str; event:str
