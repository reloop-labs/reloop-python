API_KEY_V1 = "/api/api-key/v1"


def api_key_by_id(key_id: str) -> str:
    return f"{API_KEY_V1}/{key_id}"


def api_key_rotate(key_id: str) -> str:
    return f"{API_KEY_V1}/rotate/{key_id}"


def api_key_enable(key_id: str) -> str:
    return f"{API_KEY_V1}/enable/{key_id}"


def api_key_disable(key_id: str) -> str:
    return f"{API_KEY_V1}/disable/{key_id}"


def api_key_list_path(query_string: str) -> str:
    return f"{API_KEY_V1}/{('?' + query_string) if query_string else ''}"
