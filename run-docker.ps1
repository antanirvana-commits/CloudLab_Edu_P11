$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root
docker compose up -d --build
Write-Host "CloudLab Edu Docker aktif" -ForegroundColor Green
Write-Host "Frontend : http://localhost:8080"
Write-Host "Backend  : http://localhost:8000"
Write-Host "Health   : http://localhost:8080/health"
