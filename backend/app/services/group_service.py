from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.group import Group
from app.schemas.group import GroupCreate, GroupUpdate

def list_groups(db: Session):
    return db.query(Group).order_by(Group.id.desc()).all()

def get_group(db: Session, group_id: int):
    obj = db.get(Group, group_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kelompok tidak ditemukan.")
    return obj

def create_group(db: Session, payload: GroupCreate):
    if db.query(Group).filter(Group.name == payload.name).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Nama kelompok sudah digunakan.")
    obj = Group(**payload.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

def update_group(db: Session, group_id: int, payload: GroupUpdate):
    obj = get_group(db, group_id)
    data = payload.model_dump(exclude_unset=True)
    if "name" in data:
        duplicate = db.query(Group).filter(Group.name == data["name"], Group.id != group_id).first()
        if duplicate:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Nama kelompok sudah digunakan.")
    for k, v in data.items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

def delete_group(db: Session, group_id: int):
    obj = get_group(db, group_id)
    db.delete(obj); db.commit()
    return {"message": "Kelompok berhasil dihapus."}
