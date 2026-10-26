# Upgrade CloudLab Edu P11 → v1.2.0 RBAC

## Penting
Patch ini mengubah **frontend dan backend sekaligus**. Jangan hanya mengganti `frontend/` pada backend v1.1.0 karena login baru membutuhkan endpoint `/api/auth/*` dan RBAC backend v1.2.0.

## Cara aman
1. Hentikan CloudLab Edu yang sedang berjalan (`Ctrl+C` atau `docker compose down`).
2. Simpan folder v1.1.0 sebagai backup.
3. Ekstrak paket v1.2.0 sebagai folder terpisah.
4. Jalankan `run.ps1` untuk uji lokal.
5. Login dengan akun demo dan cek setiap role.
6. Setelah stabil, gunakan `run-docker.ps1` dan `run-staging.ps1` untuk praktik Pertemuan 11.

## Akun demo
- Admin: `admin` / `Admin@123`
- Dosen: `dosen` / `Dosen@123`
- Mahasiswa: `mahasiswa` / `Mhs@12345`

## Checklist
- Admin dapat membuka System Status dan Swagger.
- Dosen dapat CRUD Praktikum, melihat Submission, memberi Penilaian, dan melihat Analytics.
- Mahasiswa hanya membaca Praktikum, menjalankan Cloud Lab, mengirim Submission, dan melihat Progress sendiri.
- Mahasiswa mendapat HTTP 403 jika mencoba membuat Praktikum.
- Dosen mendapat HTTP 403 jika mencoba membuka endpoint System Status.
- `pytest -q` menghasilkan 11 passed.
