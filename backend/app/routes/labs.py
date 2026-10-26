from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.services import lab_service
from app.security.auth import require_roles
from app.models.user import User

router = APIRouter(prefix="/labs", tags=["Cloud Labs"])

@router.get("")
def list_labs(user: User = Depends(require_roles("mahasiswa", "dosen", "admin"))):
    return lab_service.get_labs()

@router.get("/analytics/summary")
def analytics(db: Session = Depends(get_db), user: User = Depends(require_roles("dosen", "admin"))):
    return lab_service.analytics(db)

@router.get("/analytics/me")
def my_analytics(db: Session = Depends(get_db), user: User = Depends(require_roles("mahasiswa"))):
    return lab_service.analytics_for_student(db, user.username)

@router.get("/{lab_id}")
def get_lab(lab_id: str, user: User = Depends(require_roles("mahasiswa", "dosen", "admin"))):
    lab = lab_service.get_lab(lab_id)
    if not lab:
        raise HTTPException(status_code=404, detail="Lab tidak ditemukan.")
    return lab

@router.get("/{lab_id}/progress")
def progress(lab_id: str, db: Session = Depends(get_db), user: User = Depends(require_roles("mahasiswa"))):
    return lab_service.score(db, lab_id, user.username)

@router.post("/{lab_id}/events")
def record_event(lab_id: str, payload: dict, db: Session = Depends(get_db), user: User = Depends(require_roles("mahasiswa"))):
    lab = lab_service.get_lab(lab_id)
    if not lab:
        raise HTTPException(status_code=404, detail="Lab tidak ditemukan.")
    event = lab_service.record_event(
        db=db,
        lab_id=lab_id,
        step_id=str(payload.get("step_id","unknown")),
        event_type=str(payload.get("event_type","manual")),
        result=str(payload.get("result","PASS")),
        message=str(payload.get("message","")),
        student_name=user.username,
    )
    return {"id": event.id, "status":"recorded"}
