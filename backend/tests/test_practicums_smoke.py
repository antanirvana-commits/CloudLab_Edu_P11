from fastapi.testclient import TestClient
from app.main import app


def test_practicums_requires_login():
    fresh = TestClient(app)
    fresh.cookies.clear()
    r = fresh.get("/api/practicums")
    assert r.status_code == 401


def test_practicums_student_can_read(client, mahasiswa_headers):
    r = client.get("/api/practicums", headers=mahasiswa_headers)
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_student_cannot_create_practicum(client, mahasiswa_headers):
    r = client.post("/api/practicums", headers=mahasiswa_headers, json={
        "title":"Praktikum Terlarang",
        "description":"Mahasiswa tidak boleh membuat praktikum dari endpoint ini.",
        "deadline":"2030-01-01T00:00:00"
    })
    assert r.status_code == 403
