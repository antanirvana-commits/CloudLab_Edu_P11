# CloudLab Edu — Role-Based UI

Versi ini memisahkan dashboard berdasarkan role.

## Login demo
Password seluruh role untuk Teaching MVP: `12345678`

- Admin: pilih role **Admin**
- Dosen: pilih role **Dosen**
- Mahasiswa: pilih role **Mahasiswa**

## Dashboard
- Admin -> `/admin-dashboard.html`
  - jumlah mahasiswa/kelompok/praktikum
  - status sistem
  - manajemen pengguna
  - Swagger/API
  - system analytics

- Dosen -> `/dosen-dashboard.html`
  - kelola praktikum
  - submission
  - penilaian
  - learning analytics
  - laporan

- Mahasiswa -> `/mahasiswa-dashboard.html`
  - cloud lab
  - praktikum saya
  - pengumpulan tugas
  - progress dan skor

## Menjalankan
```powershell
cd "C:\Users\LENOVO\Documents\CloudLab_Edu"
Set-ExecutionPolicy -Scope Process Bypass
.\run.ps1
```

Buka:
`http://127.0.0.1:8000`
