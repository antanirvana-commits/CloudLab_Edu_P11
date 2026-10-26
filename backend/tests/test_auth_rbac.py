def test_login_roles_are_server_defined(client):
    for username, password, role in [
        ("admin","Admin@123","admin"),
        ("dosen","Dosen@123","dosen"),
        ("mahasiswa","Mhs@12345","mahasiswa"),
    ]:
        r=client.post("/api/auth/login",json={"username":username,"password":password})
        assert r.status_code==200
        assert r.json()["user"]["role"]==role

def test_wrong_password_rejected(client):
    r=client.post("/api/auth/login",json={"username":"admin","password":"password-salah"})
    assert r.status_code==401

def test_dosen_can_manage_practicum_but_not_system(client,dosen_headers):
    r=client.get("/api/practicums",headers=dosen_headers)
    assert r.status_code==200
    r=client.get("/api/system/status",headers=dosen_headers)
    assert r.status_code==403

def test_mahasiswa_analytics_is_own_endpoint(client,mahasiswa_headers):
    r=client.get("/api/labs/analytics/me",headers=mahasiswa_headers)
    assert r.status_code==200
    assert r.json()["student_name"]=="mahasiswa"

def test_swagger_admin_only(client):
    client.cookies.clear()
    denied = client.get("/docs")
    assert denied.status_code == 401
    login = client.post("/api/auth/login", json={"username":"admin","password":"Admin@123"})
    assert login.status_code == 200
    allowed = client.get("/docs")
    assert allowed.status_code == 200
    assert "CloudLab Edu - Admin API Docs" in allowed.text
