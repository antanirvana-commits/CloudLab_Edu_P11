"""Repair akun demo CloudLab Edu tanpa menghapus data praktikum.

Jalankan dari folder backend:
    python scripts/repair_auth.py
"""
from pathlib import Path
import shutil
import sqlite3
import sys
from datetime import datetime

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from sqlalchemy import text
from app.config.settings import get_settings
from app.database.db import SessionLocal
from app.services.auth_service import ensure_demo_users

settings = get_settings()


def _sqlite_db_path() -> Path | None:
    if not settings.database_url.startswith("sqlite"):
        return None
    raw = settings.database_url.replace("sqlite:///", "", 1)
    db_path = Path(raw)
    if not db_path.is_absolute():
        db_path = (BACKEND_DIR / db_path).resolve()
    return db_path


def backup_sqlite_if_needed():
    db_path = _sqlite_db_path()
    if not db_path or not db_path.exists():
        return None
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = db_path.with_name(f"{db_path.stem}_backup_auth_{stamp}{db_path.suffix}")
    shutil.copy2(db_path, backup)
    return backup


def inspect_users_table():
    db_path = _sqlite_db_path()
    if not db_path or not db_path.exists():
        return
    con = sqlite3.connect(db_path)
    try:
        cols = [r[1] for r in con.execute("PRAGMA table_info(users)").fetchall()]
        required = {"id", "username", "full_name", "email", "role", "password_salt", "password_hash", "is_active"}
        missing = required - set(cols)
        if missing:
            raise RuntimeError(
                "Tabel users menggunakan schema lama dan kehilangan kolom: " + ", ".join(sorted(missing))
            )
    finally:
        con.close()


def main():
    backup = backup_sqlite_if_needed()
    if backup:
        print(f"Backup database: {backup}")
    inspect_users_table()
    with SessionLocal() as db:
        ensure_demo_users(db)
        rows = db.execute(text(
            "SELECT username, email, role, is_active FROM users "
            "WHERE username IN ('admin','dosen','mahasiswa') ORDER BY username"
        )).fetchall()
        print("Akun demo setelah repair:")
        for row in rows:
            print(f"- {row.username}: {row.email} | role={row.role} | active={row.is_active}")
    print("Repair auth selesai.")


if __name__ == "__main__":
    main()
