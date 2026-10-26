from fastapi.testclient import TestClient

from app.main import app
from app.database.db import SessionLocal
from app.models.user import User


def test_login_survives_legacy_invalid_email():
    with SessionLocal() as db:
        user = db.query(User).filter(User.username == "mahasiswa").first()
        assert user is not None
        old_email = user.email
        user.email = "legacy-invalid-email"
        db.commit()

    try:
        client = TestClient(app, raise_server_exceptions=False)
        response = client.post(
            "/api/auth/login",
            json={"username": "mahasiswa", "password": "Mhs@12345"},
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["user"]["username"] == "mahasiswa"
        assert data["user"]["email"] == "legacy-invalid-email"
    finally:
        with SessionLocal() as db:
            user = db.query(User).filter(User.username == "mahasiswa").first()
            user.email = old_email
            db.commit()
