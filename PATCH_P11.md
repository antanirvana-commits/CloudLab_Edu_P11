# Patch CloudLab Edu v1.2.0 — Role-Based Frontend & RBAC

Patch ini menyempurnakan CloudLab Edu agar konsisten dengan teori Pertemuan 10 dan 11.

1. Login berbasis akun; role tidak dipilih di frontend.
2. Token sesi ditandatangani backend dan role ditentukan server.
3. Endpoint dilindungi dengan Role-Based Access Control.
4. Frontend dipisahkan per role: `public`, `admin`, `dosen`, `mahasiswa`.
5. Navigasi memakai flyout submenu saat hover atau klik.
6. Admin, Dosen, dan Mahasiswa memiliki menu/fungsi berbeda sesuai peruntukannya.
7. Profil per role dapat diedit oleh pemilik akun.
8. Mahasiswa hanya melihat analytics/progress Cloud Lab miliknya sendiri.
9. Swagger/OpenAPI hanya dapat dibuka menggunakan token Admin.
10. Automated test RBAC ditambahkan; total 10 tests lolos.
11. Docker, CI/CD, staging, failure simulation, health check, dan rollback tetap dipertahankan.
