from sqlalchemy import text
from app.database.db import SessionLocal


def test_demo_login_repairs_legacy_corruption(client):
    with SessionLocal() as db:
        db.execute(text(
            "UPDATE users SET full_name='Legacy User', email='legacy-invalid', role='Mahasiswa', "
            "password_salt='ZZ-not-hex', password_hash='bad' WHERE username='mahasiswa'"
        ))
        db.commit()

    response = client.post('/api/auth/login', json={'username': 'mahasiswa', 'password': 'Mhs@12345'})
    assert response.status_code == 200
    payload = response.json()
    assert payload['user']['role'] == 'mahasiswa'
    assert payload['user']['email'] == 'mahasiswa@cloudlab.example.com'
