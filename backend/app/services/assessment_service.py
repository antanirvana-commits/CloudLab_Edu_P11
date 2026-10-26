from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.assessment import Assessment
from app.models.submission import Submission
from app.schemas.assessment import AssessmentCreate, AssessmentUpdate

def list_assessments(db: Session):
    return db.query(Assessment).order_by(Assessment.id.desc()).all()

def get_assessment(db: Session, assessment_id: int):
    obj = db.get(Assessment, assessment_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Penilaian tidak ditemukan.")
    return obj

def create_assessment(db: Session, payload: AssessmentCreate):
    submission = db.get(Submission, payload.submission_id)
    if not submission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Submission tidak ditemukan.")
    if db.query(Assessment).filter(Assessment.submission_id == payload.submission_id).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Submission ini sudah dinilai.")
    obj = Assessment(**payload.model_dump())
    db.add(obj)
    submission.status = "ASSESSED"
    db.commit(); db.refresh(obj)
    return obj

def update_assessment(db: Session, assessment_id: int, payload: AssessmentUpdate):
    obj = get_assessment(db, assessment_id)
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

def delete_assessment(db: Session, assessment_id: int):
    obj = get_assessment(db, assessment_id)
    submission = db.get(Submission, obj.submission_id)
    if submission:
        submission.status = "SUBMITTED"
    db.delete(obj); db.commit()
    return {"message": "Penilaian berhasil dihapus."}
