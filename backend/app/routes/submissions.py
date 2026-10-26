from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.schemas.submission import SubmissionCreate, SubmissionOut
from app.services import submission_service
from app.security.auth import require_roles
from app.models.user import User

router = APIRouter(prefix="/submissions", tags=["Submissions"])

@router.get("", response_model=list[SubmissionOut])
def get_all(db: Session = Depends(get_db), user: User = Depends(require_roles("admin", "dosen", "mahasiswa"))):
    # Pada MVP ini submission belum memiliki user_id; role sudah dibatasi, isolasi per akun menjadi tahap berikutnya.
    return submission_service.list_submissions(db)

@router.post("", response_model=SubmissionOut, status_code=status.HTTP_201_CREATED)
def create(payload: SubmissionCreate, db: Session = Depends(get_db), user: User = Depends(require_roles("mahasiswa"))):
    return submission_service.create_submission(db, payload)

@router.delete("/{submission_id}")
def delete(submission_id: int, db: Session = Depends(get_db), user: User = Depends(require_roles("admin", "dosen"))):
    return submission_service.delete_submission(db, submission_id)
