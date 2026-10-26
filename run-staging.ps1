$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$stage = Join-Path $root "deploy\staging"
Set-Location $stage
if (!(Test-Path ".env")) { Copy-Item ".env.staging.example" ".env" }
docker compose --env-file .env -f docker-compose.staging.yml up -d --build
Write-Host "CloudLab Edu STAGING aktif" -ForegroundColor Green
Write-Host "Frontend : http://localhost:8080"
Write-Host "Login Admin lalu buka Monitoring > System Status"
