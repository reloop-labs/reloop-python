from __future__ import annotations
WEBHOOK_V1 = "/api/webhook/v1"
def webhook_create_path() -> str: return WEBHOOK_V1 + "/"
def webhook_list_path(query_string: str = "") -> str: return WEBHOOK_V1 + (("?" + query_string) if query_string else "")
def webhook_by_id(id: str) -> str: return WEBHOOK_V1 + "/" + id
def webhook_trigger_path() -> str: return WEBHOOK_V1 + "/trigger"
def webhook_deliveries_path(webhook_id: str, query_string: str = "") -> str: return webhook_by_id(webhook_id) + "/deliveries" + (("?" + query_string) if query_string else "")
def webhook_delivery_retry_path(delivery_id: str) -> str: return "/api/webhook/deliveries/" + delivery_id + "/retry"
