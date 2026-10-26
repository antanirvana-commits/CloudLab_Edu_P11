# Simulasi Failure & Rollback — CloudLab Edu

## Deployment staging stabil
```powershell
Copy-Item deploy\staging\.env.staging.example deploy\staging\.env
cd deploy\staging
docker compose --env-file .env -f docker-compose.staging.yml up -d --build
```
Buka `http://localhost:8080/system-status.html` sebagai Admin.

## Simulasi health failure
```powershell
Copy-Item .env.broken.example .env -Force
docker compose --env-file .env -f docker-compose.staging.yml up -d --build
```
Backend akan mengembalikan HTTP 503 pada `/health`, sehingga container menjadi `unhealthy`.

## Rollback konfigurasi ke versi stabil
```powershell
Copy-Item .env.staging.example .env -Force
docker compose --env-file .env -f docker-compose.staging.yml up -d --build
```

## Rollback berbasis Git
```powershell
git log --oneline
git revert <commit-yang-bermasalah>
git push
```
Untuk pembelajaran, `git revert` lebih aman daripada menghapus histori commit.
