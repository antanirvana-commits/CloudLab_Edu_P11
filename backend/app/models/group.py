from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.database.db import Base

class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    project_title: Mapped[str | None] = mapped_column(String(200), nullable=True)
