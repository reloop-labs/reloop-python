from __future__ import annotations
CONTACTS_BASE="/api/contacts"
def contact_create_path()->str:return f"{CONTACTS_BASE}/create"
def contact_retrieve_path(id:str)->str:return f"{CONTACTS_BASE}/retrieve/{id}"
def contact_list_path(q:str="")->str:return f"{CONTACTS_BASE}/list{'?' + q if q else ''}"
def contact_by_id(id:str)->str:return f"{CONTACTS_BASE}/{id}"
