from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session

from app.config.settings import get_settings
from app.database.db import get_db
from app.security.auth import require_roles
from app.models.user import User

router = APIRouter(prefix="/system", tags=["System"])
settings = get_settings()


@router.get("/status")
def system_status(db: Session = Depends(get_db), user: User = Depends(require_roles("admin"))):
    database_status = "connected"
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        database_status = "error"

    overall = "healthy" if database_status == "connected" and not settings.simulate_health_failure else "degraded"
    return {
        "status": overall,
        "service": "cloudlab-backend",
        "database": database_status,
        "environment": settings.app_env,
        "version": settings.app_version,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/config")
def safe_config(user: User = Depends(require_roles("admin"))):
    """Expose only non-secret configuration for classroom inspection."""
    db_url = make_url(settings.database_url)
    return {
        "application": {
            "name": settings.app_name,
            "environment": settings.app_env,
            "version": settings.app_version,
        },
        "database": {
            "driver": db_url.drivername,
            "host": db_url.host or "local-file",
            "database": db_url.database or "-",
        },
        "cors_origins": settings.cors_list,
        "frontend_dir": settings.frontend_dir,
        "feature_flags": {
            "simulate_health_failure": settings.simulate_health_failure,
            "enable_failure_demo": settings.enable_failure_demo,
        },
        "secrets": {
            "app_secret": "configured (masked)",
            "demo_admin_password": "configured (masked)",
            "demo_dosen_password": "configured (masked)",
            "demo_mahasiswa_password": "configured (masked)",
            "database_password": "configured (masked)" if db_url.password else "not used by current database",
        },
        "note": "Nilai secret tidak pernah dikirim oleh endpoint ini.",
    }


@router.get("/architecture")
def architecture(user: User = Depends(require_roles("admin"))):
    return {
        "request_flow": ["route", "schema", "service", "model", "database"],
        "frontend_roles": ["public", "admin", "dosen", "mahasiswa"],
        "controls": ["Pydantic validation", "RBAC", "structured error handling", "environment configuration", "secret masking"],
    }


@router.get("/demo/failure")
def demo_failure(user: User = Depends(require_roles("admin"))):
    if not settings.enable_failure_demo:
        raise HTTPException(status_code=403, detail="Failure demo dinonaktifkan. Set ENABLE_FAILURE_DEMO=true pada staging.")
    raise HTTPException(status_code=500, detail="Simulated deployment failure for CloudLab Edu practicum.")
