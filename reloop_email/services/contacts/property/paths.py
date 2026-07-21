from __future__ import annotations
PROPERTYS_V1="/api/contacts/v1/properties"
def property_create_path()->str:return f"{PROPERTYS_V1}/create"
def property_list_path(q:str="")->str:return f"{PROPERTYS_V1}/list{'?' + q if q else ''}"
def property_by_id(id:str)->str:return f"{PROPERTYS_V1}/{id}"
