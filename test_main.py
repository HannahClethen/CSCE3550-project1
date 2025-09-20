from fastapi.testclient import TestClient
from main import app
import jwt

client = TestClient(app)


def test_jwks_returns_unexpired_keys():
    res = client.get("/jwks")
    assert res.status_code == 200
    keys = res.json().get("keys", [])
    assert isinstance(keys, list)
    for key in keys:
        assert "kid" in key
        assert "n" in key
        assert "e" in key

def test_auth_returns_jwt():
    res = client.post("/auth")
    assert res.status_code == 200
    token = res.json()["token"]
    headers = jwt.get_unverified_header(token)
    assert "kid" in headers

def test_auth_with_expired_param():
    # First wait for key to expire
    import time
    time.sleep(61)  # Wait for key TTL to expire
    res = client.post("/auth?expired=true")
    assert res.status_code == 200
    token = res.json()["token"]
    headers = jwt.get_unverified_header(token)
    assert "kid" in headers
