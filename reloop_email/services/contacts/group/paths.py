from __future__ import annotations
GROUPS_V1="/api/contacts/v1/groups"
def group_create_path()->str:return f"{GROUPS_V1}/create"
def group_list_path(q:str="")->str:return f"{GROUPS_V1}/list{'?' + q if q else ''}"
def group_by_id(id:str)->str:return f"{GROUPS_V1}/{id}"
