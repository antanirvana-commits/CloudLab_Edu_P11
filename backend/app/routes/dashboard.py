from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.services.dashboard_service import summary
from app.security.auth import require_roles
from app.models.user import User

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary")
def get_summary(db: Session = Depends(get_db), user: User = Depends(require_roles("admin", "dosen"))):
    return summary(db)
