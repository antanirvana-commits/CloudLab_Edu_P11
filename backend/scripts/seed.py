from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from datetime import datetime, timedelta
from app.database.db import SessionLocal, Base, engine
from app.models.student import Student
from app.models.group import Group
from app.models.practicum import Practicum

Base.metadata.create_all(bind=engine)
db = SessionLocal()

try:
    if not db.query(Student).first():
        db.add_all([
            Student(nim="230001", name="Budi Santoso", email="budi@example.com"),
            Student(nim="230002", name="Siti Rahma", email="siti@example.com"),
        ])
    if not db.query(Group).first():
        db.add_all([
            Group(name="Kelompok 1", project_title="Cloud Attendance System"),
            Group(name="Kelompok 2", project_title="Learning Assignment Management"),
        ])
    if not db.query(Practicum).first():
        db.add(Practicum(
            title="Praktikum API Modular",
            description="Bangun API modular dan hubungkan dengan basis data.",
            deadline=datetime.utcnow() + timedelta(days=7),
        ))
    db.commit()
    print("Seed selesai.")
finally:
    db.close()
