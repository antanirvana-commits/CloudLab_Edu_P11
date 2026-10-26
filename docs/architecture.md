# Arsitektur CloudLab Edu v1.2.0

```text
Browser
  |
  v
Frontend Nginx
  ├── public/
  ├── admin/
  ├── dosen/
  └── mahasiswa/
  |
  | Bearer Token
  v
FastAPI Backend
  ├── Authentication
  ├── RBAC Dependency
  ├── Routes
  ├── Pydantic Schemas / Validation
  ├── Services / Business Logic
  ├── Error Handling
  └── Logging
  |
  v
SQLAlchemy
  |
  v
SQLite (development) / PostgreSQL (Docker & staging)
```

## Hak akses
- Admin: administrasi + monitoring sistem.
- Dosen: pengajaran + penilaian + analytics pembelajaran.
- Mahasiswa: aktivitas belajar dan progress sendiri.

## Configuration & Secret
`.env -> Settings -> APP_SECRET / DATABASE_URL / password demo / CORS`.
File `.env` diabaikan Git. Pada deployment gunakan environment variable/secret manager.

## Deployment
`Frontend (Nginx) → Backend (FastAPI) → PostgreSQL`.
CI menjalankan pytest, build container, lalu staging smoke test.
