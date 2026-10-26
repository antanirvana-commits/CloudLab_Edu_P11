from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.practicum import Practicum
from app.schemas.practicum import PracticumCreate, PracticumUpdate

def list_practicums(db: Session):
    return db.query(Practicum).order_by(Practicum.deadline.asc()).all()

def get_practicum(db: Session, practicum_id: int):
    obj = db.get(Practicum, practicum_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Praktikum tidak ditemukan.")
    return obj

def create_practicum(db: Session, payload: PracticumCreate):
    obj = Practicum(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_practicum(db: Session, practicum_id: int, payload: PracticumUpdate):
    obj = get_practicum(db, practicum_id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete_practicum(db: Session, practicum_id: int):
    obj = get_practicum(db, practicum_id)
    db.delete(obj)
    db.commit()
    return {"message": "Praktikum berhasil dihapus."}
