# CloudLab Edu v1.2.0 — Pertemuan 10 & 11

CloudLab Edu v1.2.0 menggabungkan praktik **MVP Cloud-Native** dan **Cloud Software Engineering/DevOps** dalam satu aplikasi.

## Perubahan utama v1.2.0
- Login tidak lagi memilih role secara manual.
- Backend menentukan role berdasarkan akun dan token sesi.
- RBAC backend membatasi endpoint Admin, Dosen, dan Mahasiswa.
- Frontend dipisah menjadi `public/`, `admin/`, `dosen/`, dan `mahasiswa/`.
- Sidebar memakai menu bertingkat/flyout agar navigasi tidak menumpuk.
- Setiap role mempunyai Profil sendiri dan dapat mengedit nama/email.
- Mahasiswa mempunyai analytics/progress pribadi melalui `/api/labs/analytics/me`.
- Swagger/OpenAPI dilindungi dan hanya dibuka dari area Admin.
- Tetap mempertahankan testing, Docker, CI/CD, staging, health check, failure simulation, dan rollback.

## Struktur
```text
CloudLab_Edu_P11/
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── models/
│   │   ├── security/
│   │   └── database/
│   └── tests/
├── frontend/
│   ├── public/
│   ├── admin/
│   ├── dosen/
│   ├── mahasiswa/
│   └── static/
├── .github/workflows/ci.yml
├── deploy/staging/
├── docker-compose.yml
└── VERSION
```

## Akun demo kelas
| Role | Username | Password |
|---|---|---|
| Admin | `admin` | `Admin@123` |
| Dosen | `dosen` | `Dosen@123` |
| Mahasiswa | `mahasiswa` | `Mhs@12345` |

Password demo dibaca melalui environment variable. Ubah nilainya untuk penggunaan di luar kelas.

## Menjalankan lokal
```powershell
cd "C:\Users\LENOVO\Documents\CloudLab_Edu_P11"
Set-ExecutionPolicy -Scope Process Bypass
.\run.ps1
```
Buka `http://127.0.0.1:8000` lalu login.

## Menjalankan dengan Docker
```powershell
.\run-docker.ps1
```
- Frontend: `http://localhost:8080`
- Backend: `http://localhost:8000`
- Health: `http://localhost:8080/health`

## Staging
```powershell
.\run-staging.ps1
```
Login sebagai Admin, kemudian buka **Monitoring → System Status**.

## Automated tests
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pytest -q
```
Target versi ini: **11 tests passed**.

## RBAC ringkas
- **Admin:** pengguna, monitoring praktikum read-only, system analytics, system status, Swagger, profil.
- **Dosen:** kelola praktikum, submission, penilaian, learning analytics, laporan, profil.
- **Mahasiswa:** cloud lab, praktikum read-only, mengumpulkan tugas, progress/analytics sendiri, profil.

## Alur Pertemuan 10 → 11
```text
MVP modular
→ Database / managed service
→ Environment configuration
→ Validation & error handling
→ Secret management
→ Authentication & RBAC
→ Git/version control
→ Automated testing
→ Docker/containerization
→ CI/CD
→ Staging
→ Failure handling
→ Rollback
```
