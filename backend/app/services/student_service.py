from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate

def list_students(db: Session):
    return db.query(Student).order_by(Student.id.desc()).all()

def get_student(db: Session, student_id: int):
    obj = db.get(Student, student_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mahasiswa tidak ditemukan.")
    return obj

def create_student(db: Session, payload: StudentCreate):
    duplicate = db.query(Student).filter(or_(Student.nim == payload.nim, Student.email == payload.email)).first()
    if duplicate:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="NIM atau email sudah terdaftar.")
    obj = Student(**payload.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

def update_student(db: Session, student_id: int, payload: StudentUpdate):
    obj = get_student(db, student_id)
    data = payload.model_dump(exclude_unset=True)
    if "nim" in data or "email" in data:
        duplicate = db.query(Student).filter(
            Student.id != student_id,
            or_(Student.nim == data.get("nim", obj.nim), Student.email == data.get("email", obj.email))
        ).first()
        if duplicate:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="NIM atau email sudah digunakan.")
    for k, v in data.items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

def delete_student(db: Session, student_id: int):
    obj = get_student(db, student_id)
    db.delete(obj); db.commit()
    return {"message": "Mahasiswa berhasil dihapus."}
