# CloudLab Edu — Audit Implementasi Pertemuan 10

## Sub-CPMK
Mahasiswa mampu mengembangkan minimum viable product berupa aplikasi/API modular, mengintegrasikannya dengan basis data atau layanan terkelola, serta menerapkan konfigurasi lingkungan, validasi input, error handling, dan pengelolaan secret secara benar.

## 1. MVP dan API modular — TERPENUHI

Alur backend:

`routes → schemas → services → models → database`

Contoh modul mahasiswa:
- Route: `backend/app/routes/students.py`
- Schema: `backend/app/schemas/student.py`
- Service: `backend/app/services/student_service.py`
- Model: `backend/app/models/student.py`
- Database: `backend/app/database/db.py`

Frontend dipisahkan berdasarkan role:
- `frontend/public/`
- `frontend/admin/`
- `frontend/dosen/`
- `frontend/mahasiswa/`
- shared assets di `frontend/static/`

Endpoint audit: `GET /api/system/architecture` (Admin only).

## 2. Database / managed service — TERPENUHI

Development lokal menggunakan SQLite melalui `DATABASE_URL=sqlite:///./practicum.db`.
Container/staging menggunakan PostgreSQL melalui `DATABASE_URL` environment variable.

SQLAlchemy menjadi abstraction layer sehingga service tidak perlu mengubah business logic ketika database berpindah dari SQLite ke PostgreSQL.

## 3. Environment & secret management — TERPENUHI

Konfigurasi berada di `backend/app/config/settings.py` dan dibaca dari environment / `.env`.

File yang boleh dibagikan: `.env.example` dan `backend/.env.example`.
File `.env` diabaikan Git melalui `.gitignore`.

Secret disimpan sebagai `SecretStr` dan tidak diekspos oleh endpoint. Endpoint Admin `GET /api/system/config` hanya menampilkan status `configured (masked)`.

## 4. Input validation — TERPENUHI

Pydantic digunakan untuk validasi request:
- `StudentCreate`: panjang NIM, nama, dan format email.
- `PracticumCreate`: judul, deskripsi, dan deadline masa depan.
- `PracticumUpdate`: deadline masa lalu juga ditolak.
- `LoginRequest` dan `ProfileUpdate`: constraint input dan email.

Input invalid menghasilkan HTTP `422 VALIDATION_ERROR`.

## 5. Error handling — TERPENUHI

CloudLab Edu menggunakan response error terstruktur:

```json
{
  "error": "NOT_FOUND",
  "detail": "Praktikum tidak ditemukan.",
  "path": "/api/practicums/999999",
  "timestamp": "..."
}
```

Skenario utama:
- `401 UNAUTHORIZED` — belum login / token invalid.
- `403 FORBIDDEN` — role tidak memiliki akses.
- `404 NOT_FOUND` — resource tidak ditemukan.
- `409 CONFLICT` — NIM/email duplikat.
- `422 VALIDATION_ERROR` — input tidak valid.
- `500 INTERNAL_SERVER_ERROR` — failure demo staging.
- `503 SERVICE_UNAVAILABLE` — health failure simulation.

## 6. Demonstrasi API — TERPENUHI

Admin → Developer → **API & Validation Lab**.

Halaman tersebut menyediakan demonstrasi real endpoint:
- `201`: membuat mahasiswa valid.
- `422`: mengirim input invalid.
- `404`: meminta praktikum yang tidak ada.
- `409`: mencoba email akun yang sudah dipakai.
- `500`: failure demo ketika staging mengaktifkannya.

Swagger tetap Admin-only melalui `/docs`.

## 7. RBAC — TERPENUHI

Backend menentukan hak akses:
- Admin: administrasi, monitoring, developer tools.
- Dosen: praktikum, submission, penilaian, analytics akademik.
- Mahasiswa: lab, praktikum, submission, progress pribadi.

Role restriction diuji otomatis.

## Hasil automated test

`19 passed`
