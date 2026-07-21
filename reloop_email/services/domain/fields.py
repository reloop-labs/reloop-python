from __future__ import annotations
import re
from typing import Any, Optional
from reloop_email.services.domain.errors import ReloopValidationError
DOMAIN_PATTERN = re.compile(r"^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}$")
def require_domain_id(value: Any, field: str="id") -> str:
 if not isinstance(value,str) or not value.strip(): raise ReloopValidationError(f"Domain {field} is required and must be a non-empty string.",field)
 return value.strip()
def require_domain_name(value: Any, field: str="domain") -> str:
 if not isinstance(value,str): raise ReloopValidationError(f"Domain {field} is required and must be a string.",field)
 value=value.strip().lower()
 if len(value)<4: raise ReloopValidationError(f"Domain {field} must be at least 4 characters.",field)
 if len(value)>255: raise ReloopValidationError(f"Domain {field} must be at most 255 characters.",field)
 if not DOMAIN_PATTERN.fullmatch(value): raise ReloopValidationError(f"Domain {field} must be a valid domain name.",field)
 return value
def optional_boolean(value: Any, field: str) -> Optional[bool]:
 if value is None: return None
 if not isinstance(value,bool): raise ReloopValidationError(f"{field} must be a boolean when provided.",field)
 return value
def optional_tls(value: Any, field: str="tls") -> Optional[str]:
 if value is None: return None
 if value not in ("opportunistic","enforced"): raise ReloopValidationError(f'{field} must be "opportunistic" or "enforced".',field)
 return value
def require_page(value: Any, field: str="page") -> int:
 if not isinstance(value,int) or isinstance(value,bool) or value<1: raise ReloopValidationError("list %s must be an integer >= 1."%field,field)
 return value
def require_limit(value: Any, field: str="limit") -> int:
 if not isinstance(value,int) or isinstance(value,bool) or not 1<=value<=100: raise ReloopValidationError("list %s must be an integer between 1 and 100."%field,field)
 return value
