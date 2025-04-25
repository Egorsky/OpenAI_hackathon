from fastapi.testclient import TestClient
from back_app import app

client = TestClient(app)

def test_echo():
    payload = {"msg": "pytest"}
    r = client.post("/api/echo", json=payload)
    assert r.status_code == 200, f"Expected status code 200, got {r.status_code}"
    assert r.json() == {"received": payload}, f"Expected {payload}, got {r.json()}"
