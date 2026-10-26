import base64
import hashlib
import hmac
import json
import os
import time
from typing import Callable

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.config.settings import get_settings
from app.database.db import get_db
from app.models.user import User

settings = get_settings()
bearer = HTTPBearer(auto_error=False)


def _b64e(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def _b64d(text: str) -> bytes:
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


def hash_password(password: str, salt_hex: str | None = None) -> tuple[str, str]:
    salt = bytes.fromhex(salt_hex) if salt_hex else os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 210_000)
    return salt.hex(), digest.hex()


def verify_password(password: str, salt_hex: str | None, expected_hash: str | None) -> bool:
    """Verifikasi password tanpa membiarkan data hash legacy/rusak memicu HTTP 500."""
    try:
        if not salt_hex or not expected_hash:
            return False
        _, actual = hash_password(password, salt_hex)
        return hmac.compare_digest(actual, expected_hash)
    except (TypeError, ValueError):
        return False


def create_token(user: User, ttl_seconds: int = 8 * 3600) -> str:
    payload = {
        "sub": user.username,
        "uid": user.id,
        "role": user.role,
        "name": user.full_name,
        "email": user.email,
        "exp": int(time.time()) + ttl_seconds,
    }
    body = _b64e(json.dumps(payload, separators=(",", ":"), sort_keys=True).encode())
    sig = hmac.new(settings.app_secret_value.encode(), body.encode(), hashlib.sha256).digest()
    return f"{body}.{_b64e(sig)}"


def decode_token(token: str) -> dict:
    try:
        body, sig_text = token.split(".", 1)
        expected = hmac.new(settings.app_secret_value.encode(), body.encode(), hashlib.sha256).digest()
        if not hmac.compare_digest(expected, _b64d(sig_text)):
            raise ValueError("bad signature")
        payload = json.loads(_b64d(body))
        if int(payload.get("exp", 0)) < int(time.time()):
            raise ValueError("expired")
        return payload
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sesi tidak valid atau sudah berakhir.") from exc


def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: Session = Depends(get_db),
) -> User:
    token = credentials.credentials if credentials else request.cookies.get("cloudlab_session")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Silakan login terlebih dahulu.")
    payload = decode_token(token)
    user = db.query(User).filter(User.username == payload.get("sub")).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Akun tidak aktif atau tidak ditemukan.")
    return user


def require_roles(*roles: str) -> Callable:
    def dependency(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Role Anda tidak memiliki akses ke fitur ini.")
        return user
    return dependency


def token_user(token: str, db: Session) -> User:
    payload = decode_token(token)
    user = db.query(User).filter(User.username == payload.get("sub")).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Sesi tidak valid.")
    return user
