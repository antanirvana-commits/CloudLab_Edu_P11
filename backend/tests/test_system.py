def test_system_status_admin_only(client, admin_headers, dosen_headers):
    ok = client.get("/api/system/status", headers=admin_headers)
    assert ok.status_code == 200
    assert ok.json()["database"] in {"connected", "error"}
    denied = client.get("/api/system/status", headers=dosen_headers)
    assert denied.status_code == 403

def test_failure_demo_is_disabled_by_default(client, admin_headers):
    r = client.get("/api/system/demo/failure", headers=admin_headers)
    assert r.status_code == 403
