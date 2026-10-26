from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.submission import Submission
from app.models.practicum import Practicum
from app.models.group import Group
from app.schemas.submission import SubmissionCreate

def list_submissions(db: Session):
    return db.query(Submission).order_by(Submission.submitted_at.desc()).all()

def get_submission(db: Session, submission_id: int):
    obj = db.get(Submission, submission_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Submission tidak ditemukan.")
    return obj

def create_submission(db: Session, payload: SubmissionCreate):
    practicum = db.get(Practicum, payload.practicum_id)
    if not practicum:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Praktikum tidak ditemukan.")
    group = db.get(Group, payload.group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kelompok tidak ditemukan.")
    existing = db.query(Submission).filter(
        Submission.practicum_id == payload.practicum_id,
        Submission.group_id == payload.group_id
    ).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Kelompok sudah melakukan submission untuk praktikum ini.")
    status_value = "LATE" if datetime.utcnow() > practicum.deadline else "SUBMITTED"
    obj = Submission(
        practicum_id=payload.practicum_id,
        group_id=payload.group_id,
        repository_url=str(payload.repository_url),
        report_url=str(payload.report_url),
        status=status_value
    )
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

def delete_submission(db: Session, submission_id: int):
    obj = get_submission(db, submission_id)
    db.delete(obj); db.commit()
    return {"message": "Submission berhasil dihapus."}
