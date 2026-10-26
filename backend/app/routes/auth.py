from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.schemas.auth import LoginRequest, ProfileUpdate
from app.security.auth import get_current_user
from app.models.user import User
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


def _user_payload(user: User) -> dict:
    return {
        "id": int(user.id),
        "username": str(user.username or ""),
        "full_name": str(user.full_name or user.username or "CloudLab User"),
        "email": str(user.email or ""),
        "role": str(user.role or "mahasiswa").lower(),
        "is_active": bool(user.is_active),
    }


@router.post("/login")
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user, token = auth_service.authenticate(db, payload)
    response.set_cookie(
        key="cloudlab_session",
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=8 * 3600,
        path="/",
    )
    # Sengaja dikembalikan sebagai dict biasa agar data legacy tidak memicu ResponseValidationError.
    return {"access_token": token, "token_type": "bearer", "user": _user_payload(user)}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("cloudlab_session", path="/")
    return {"status": "logged_out"}


@router.get("/me")
def me(user: User = Depends(get_current_user)):
    return _user_payload(user)


@router.patch("/me")
def update_me(payload: ProfileUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    updated = auth_service.update_profile(db, user, payload)
    return _user_payload(updated)
