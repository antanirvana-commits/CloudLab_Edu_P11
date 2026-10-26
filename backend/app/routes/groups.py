from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.schemas.group import GroupCreate, GroupUpdate, GroupOut
from app.services import group_service
from app.security.auth import require_roles
from app.models.user import User

router = APIRouter(prefix="/groups", tags=["Groups"])

@router.get("", response_model=list[GroupOut])
def get_all(db: Session = Depends(get_db), user: User = Depends(require_roles("admin", "dosen", "mahasiswa"))):
    return group_service.list_groups(db)

@router.post("", response_model=GroupOut, status_code=status.HTTP_201_CREATED)
def create(payload: GroupCreate, db: Session = Depends(get_db), user: User = Depends(require_roles("admin", "dosen"))):
    return group_service.create_group(db, payload)

@router.put("/{group_id}", response_model=GroupOut)
def update(group_id: int, payload: GroupUpdate, db: Session = Depends(get_db), user: User = Depends(require_roles("admin", "dosen"))):
    return group_service.update_group(db, group_id, payload)

@router.delete("/{group_id}")
def delete(group_id: int, db: Session = Depends(get_db), user: User = Depends(require_roles("admin", "dosen"))):
    return group_service.delete_group(db, group_id)
