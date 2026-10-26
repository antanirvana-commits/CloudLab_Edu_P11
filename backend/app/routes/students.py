from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.schemas.student import StudentCreate, StudentUpdate, StudentOut
from app.services import student_service
from app.security.auth import require_roles
from app.models.user import User

router = APIRouter(prefix="/students", tags=["Students"])

@router.get("", response_model=list[StudentOut])
def get_all(db: Session = Depends(get_db), user: User = Depends(require_roles("admin", "dosen"))):
    return student_service.list_students(db)

@router.post("", response_model=StudentOut, status_code=status.HTTP_201_CREATED)
def create(payload: StudentCreate, db: Session = Depends(get_db), user: User = Depends(require_roles("admin"))):
    return student_service.create_student(db, payload)

@router.put("/{student_id}", response_model=StudentOut)
def update(student_id: int, payload: StudentUpdate, db: Session = Depends(get_db), user: User = Depends(require_roles("admin"))):
    return student_service.update_student(db, student_id, payload)

@router.delete("/{student_id}")
def delete(student_id: int, db: Session = Depends(get_db), user: User = Depends(require_roles("admin"))):
    return student_service.delete_student(db, student_id)
