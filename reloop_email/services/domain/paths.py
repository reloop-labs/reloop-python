from __future__ import annotations
DOMAIN_V1 = "/api/domain/v1"
def domain_create_path() -> str: return f"{DOMAIN_V1}/create"
def domain_list_path(query: str = "") -> str: return f"{DOMAIN_V1}/list{'?' + query if query else ''}"
def domain_by_id(domain_id: str) -> str: return f"{DOMAIN_V1}/{domain_id}"
def domain_verify_path(domain_id: str) -> str: return f"{DOMAIN_V1}/verify/{domain_id}"
