from datetime import datetime, timedelta, timezone


def test_safe_config_is_admin_only_and_masks_secrets(client, admin_headers, dosen_headers):
    denied = client.get('/api/system/config', headers=dosen_headers)
    assert denied.status_code == 403
    assert denied.json()['error'] == 'FORBIDDEN'

    r = client.get('/api/system/config', headers=admin_headers)
    assert r.status_code == 200
    data = r.json()
    assert data['application']['environment']
    assert data['database']['driver']
    assert 'masked' in data['secrets']['app_secret']
    assert 'Admin@123' not in str(data)
    assert 'cloudlab-demo-secret' not in str(data)


def test_architecture_audit_endpoint(client, admin_headers):
    r = client.get('/api/system/architecture', headers=admin_headers)
    assert r.status_code == 200
    assert r.json()['request_flow'] == ['route', 'schema', 'service', 'model', 'database']


def test_validation_error_has_structured_envelope(client, admin_headers):
    r = client.post('/api/students', headers=admin_headers, json={
        'nim': '12', 'name': 'A', 'email': 'not-an-email'
    })
    assert r.status_code == 422
    data = r.json()
    assert data['error'] == 'VALIDATION_ERROR'
    assert data['path'] == '/api/students'
    assert isinstance(data['detail'], list)
    assert data['timestamp']


def test_not_found_error_has_structured_envelope(client, admin_headers):
    r = client.get('/api/practicums/999999', headers=admin_headers)
    assert r.status_code == 404
    data = r.json()
    assert data['error'] == 'NOT_FOUND'
    assert data['detail'] == 'Praktikum tidak ditemukan.'


def test_conflict_error_has_structured_envelope(client, admin_headers):
    r = client.patch('/api/auth/me', headers=admin_headers, json={
        'full_name': 'Administrator CloudLab',
        'email': 'dosen@cloudlab.example.com'
    })
    assert r.status_code == 409
    data = r.json()
    assert data['error'] == 'CONFLICT'


def test_practicum_update_rejects_past_deadline(client, dosen_headers):
    listing = client.get('/api/practicums', headers=dosen_headers)
    assert listing.status_code == 200
    rows = listing.json()
    if not rows:
        future = (datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=7)).isoformat()
        created = client.post('/api/practicums', headers=dosen_headers, json={
            'title': 'Praktikum Validasi P10',
            'description': 'Praktikum untuk menguji validasi deadline update.',
            'deadline': future,
        })
        assert created.status_code == 201
        pid = created.json()['id']
    else:
        pid = rows[0]['id']

    past = (datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=1)).isoformat()
    r = client.put(f'/api/practicums/{pid}', headers=dosen_headers, json={'deadline': past})
    assert r.status_code == 422
    assert r.json()['error'] == 'VALIDATION_ERROR'
