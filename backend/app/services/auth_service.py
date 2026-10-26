from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.user import User
from app.schemas.auth import LoginRequest, ProfileUpdate
from app.security.auth import verify_password, create_token, hash_password
from app.config.settings import get_settings

settings = get_settings()


def _demo_accounts():
    return {
        "admin": {
            "full_name": "Administrator CloudLab",
            "email": "admin@cloudlab.example.com",
            "role": "admin",
            "password": settings.demo_admin_password_value,
        },
        "dosen": {
            "full_name": "Dosen CloudLab",
            "email": "dosen@cloudlab.example.com",
            "role": "dosen",
            "password": settings.demo_dosen_password_value,
        },
        "mahasiswa": {
            "full_name": "Mahasiswa CloudLab",
            "email": "mahasiswa@cloudlab.example.com",
            "role": "mahasiswa",
            "password": settings.demo_mahasiswa_password_value,
        },
    }


def _normalize_demo_user(user: User, username: str) -> None:
    cfg = _demo_accounts()[username]
    # Untuk akun demo kelas, prioritaskan kestabilan demonstrasi dibanding mempertahankan profil legacy.
    user.username = username
    user.full_name = cfg["full_name"]
    user.email = cfg["email"]
    user.role = cfg["role"]
    user.is_active = True
    salt, pwd_hash = hash_password(cfg["password"])
    user.password_salt = salt
    user.password_hash = pwd_hash


def authenticate(db: Session, payload: LoginRequest):
    key = payload.username.strip().lower()

    # Untuk akun demo, sinkronkan pada saat login juga. Ini membuat aplikasi tahan terhadap
    # database lama yang berisi role/email/hash tidak konsisten.
    if key in _demo_accounts():
        user = db.query(User).filter(User.username == key).first()
        if not user:
            cfg = _demo_accounts()[key]
            salt, pwd_hash = hash_password(cfg["password"])
            user = User(
                username=key,
                full_name=cfg["full_name"],
                email=cfg["email"],
                role=cfg["role"],
                password_salt=salt,
                password_hash=pwd_hash,
                is_active=True,
            )
            db.add(user)
        else:
            _normalize_demo_user(user, key)
        db.commit()
        db.refresh(user)
    else:
        user = db.query(User).filter((User.username == key) | (User.email == key)).first()

    if not user or not user.is_active or not verify_password(payload.password, user.password_salt, user.password_hash):
        raise HTTPException(status_code=401, detail="Username/email atau password salah.")

    # Normalisasi minimum untuk data legacy non-demo agar token/response tidak rusak.
    user.username = str(user.username or "").strip().lower()
    user.full_name = str(user.full_name or user.username or "CloudLab User").strip()
    user.email = str(user.email or f"{user.username}@legacy.local").strip().lower()
    user.role = str(user.role or "mahasiswa").strip().lower()
    if user.role not in {"admin", "dosen", "mahasiswa"}:
        user.role = "mahasiswa"
    db.commit()
    db.refresh(user)
    return user, create_token(user)


def update_profile(db: Session, user: User, payload: ProfileUpdate):
    email = str(payload.email).strip().lower()
    duplicate = db.query(User).filter(User.email == email, User.id != user.id).first()
    if duplicate:
        raise HTTPException(status_code=409, detail="Email sudah digunakan akun lain.")
    user.full_name = payload.full_name.strip()
    user.email = email
    db.commit()
    db.refresh(user)
    return user


def ensure_demo_users(db: Session):
    for username, cfg in _demo_accounts().items():
        user = db.query(User).filter(User.username == username).first()
        if not user:
            salt, pwd_hash = hash_password(cfg["password"])
            user = User(
                username=username,
                full_name=cfg["full_name"],
                email=cfg["email"],
                role=cfg["role"],
                password_salt=salt,
                password_hash=pwd_hash,
                is_active=True,
            )
            db.add(user)
        else:
            _normalize_demo_user(user, username)
    db.commit()
