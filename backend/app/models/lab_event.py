from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database.db import Base

class LabEvent(Base):
    __tablename__ = "lab_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_name: Mapped[str] = mapped_column(String(120), nullable=False, default="Mahasiswa Demo")
    lab_id: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    step_id: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    result: Mapped[str] = mapped_column(String(30), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
