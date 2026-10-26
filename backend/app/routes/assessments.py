from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.schemas.assessment import AssessmentCreate, AssessmentUpdate, AssessmentOut
from app.services import assessment_service
from app.security.auth import require_roles
from app.models.user import User

router = APIRouter(prefix="/assessments", tags=["Assessments"])

@router.get("", response_model=list[AssessmentOut])
def get_all(db: Session = Depends(get_db), user: User = Depends(require_roles("admin", "dosen"))):
    return assessment_service.list_assessments(db)

@router.post("", response_model=AssessmentOut, status_code=status.HTTP_201_CREATED)
def create(payload: AssessmentCreate, db: Session = Depends(get_db), user: User = Depends(require_roles("dosen"))):
    return assessment_service.create_assessment(db, payload)

@router.put("/{assessment_id}", response_model=AssessmentOut)
def update(assessment_id: int, payload: AssessmentUpdate, db: Session = Depends(get_db), user: User = Depends(require_roles("dosen"))):
    return assessment_service.update_assessment(db, assessment_id, payload)

@router.delete("/{assessment_id}")
def delete(assessment_id: int, db: Session = Depends(get_db), user: User = Depends(require_roles("admin", "dosen"))):
    return assessment_service.delete_assessment(db, assessment_id)
