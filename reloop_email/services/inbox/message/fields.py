from __future__ import annotations
from typing import Any, List, Optional
from reloop_email.services.api_key.errors import ReloopValidationError
def require_id(value: object, label: str, field: str="id") -> str:
    if not isinstance(value,str) or not value.strip(): raise ReloopValidationError(f"{label} {field} is required and must be a non-empty string.",field)
    return value.strip()
def require_string(value: object, field: str) -> str:
    if not isinstance(value,str) or not value.strip(): raise ReloopValidationError(f"{field} is required and must be a non-empty string.",field)
    return value.strip()
def optional_string(value: object, field: str):
    if value is None: return None
    if not isinstance(value,str): raise ReloopValidationError(f"{field} must be a string when provided.",field)
    return value
def require_bool(value: object, field: str) -> bool:
    if not isinstance(value,bool): raise ReloopValidationError(f"{field} is required and must be a boolean.",field)
    return value
def optional_bool(value: object, field: str):
    if value is None: return None
    if not isinstance(value,bool): raise ReloopValidationError(f"{field} must be a boolean when provided.",field)
    return value
def require_int(
    value: object, field: str, minimum: int, maximum: Optional[int] = None
) -> int:
    if not isinstance(value,int) or isinstance(value,bool) or value < minimum or (maximum is not None and value > maximum):
        msg=f"list {field} must be an integer >= {minimum}." if maximum is None else f"list {field} must be an integer between {minimum} and {maximum}."
        raise ReloopValidationError(msg,field)
    return value
def require_recipients(value: object, field: str):
    if isinstance(value,str): return require_string(value,field)
    if isinstance(value,list) and value: return [require_string(v,f"{field}[{i}]") for i,v in enumerate(value)]
    raise ReloopValidationError(f"{field} is required and must be a string or array of strings.",field)
def require_ids(value: object, field: str="ids") -> List[str]:
    if not isinstance(value,list) or not value or len(value)>100: raise ReloopValidationError(f"{field} is required and must be a non-empty array.",field)
    return [require_string(v,f"{field}[{i}]") for i,v in enumerate(value)]
