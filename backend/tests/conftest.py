import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="session")
def client():
    return TestClient(app)

def login(client, username, password):
    r = client.post("/api/auth/login", json={"username": username, "password": password})
    assert r.status_code == 200, r.text
    return r.json()["access_token"]

@pytest.fixture(scope="session")
def admin_headers(client):
    return {"Authorization": f"Bearer {login(client, 'admin', 'Admin@123')}"}

@pytest.fixture(scope="session")
def dosen_headers(client):
    return {"Authorization": f"Bearer {login(client, 'dosen', 'Dosen@123')}"}

@pytest.fixture(scope="session")
def mahasiswa_headers(client):
    return {"Authorization": f"Bearer {login(client, 'mahasiswa', 'Mhs@12345')}"}
