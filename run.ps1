$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location "$root\backend"

if (!(Test-Path ".venv")) { python -m venv .venv }
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
if (!(Test-Path ".env")) { Copy-Item ".env.example" ".env" }

Write-Host "CloudLab Edu v1.2.0 local development" -ForegroundColor Cyan
Write-Host "Platform : http://127.0.0.1:8000"
Write-Host "Health   : http://127.0.0.1:8000/health"
Write-Host "Swagger  : login Admin > Developer > API / Swagger"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
