from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.schemas.practicum import PracticumCreate, PracticumUpdate, PracticumOut
from app.services import practicum_service
from app.security.auth import require_roles
from app.models.user import User

router = APIRouter(prefix="/practicums", tags=["Practicums"])

@router.get("", response_model=list[PracticumOut])
def get_all(db: Session = Depends(get_db), user: User = Depends(require_roles("admin", "dosen", "mahasiswa"))):
    return practicum_service.list_practicums(db)

@router.get("/{practicum_id}", response_model=PracticumOut)
def get_one(practicum_id: int, db: Session = Depends(get_db), user: User = Depends(require_roles("admin", "dosen", "mahasiswa"))):
    return practicum_service.get_practicum(db, practicum_id)

@router.post("", response_model=PracticumOut, status_code=status.HTTP_201_CREATED)
def create(payload: PracticumCreate, db: Session = Depends(get_db), user: User = Depends(require_roles("admin", "dosen"))):
    return practicum_service.create_practicum(db, payload)

@router.put("/{practicum_id}", response_model=PracticumOut)
def update(practicum_id: int, payload: PracticumUpdate, db: Session = Depends(get_db), user: User = Depends(require_roles("admin", "dosen"))):
    return practicum_service.update_practicum(db, practicum_id, payload)

@router.delete("/{practicum_id}")
def delete(practicum_id: int, db: Session = Depends(get_db), user: User = Depends(require_roles("admin", "dosen"))):
    return practicum_service.delete_practicum(db, practicum_id)
