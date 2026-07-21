from reloop_email.client import ReloopClient

def client() -> ReloopClient:
    return ReloopClient("test-key", base_url="https://api.test")
