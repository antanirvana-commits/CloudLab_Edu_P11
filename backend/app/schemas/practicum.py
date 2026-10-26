from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict, field_validator


class PracticumBase(BaseModel):
    title: str = Field(min_length=4, max_length=180)
    description: str = Field(min_length=10, max_length=2000)
    deadline: datetime

    @field_validator("deadline")
    @classmethod
    def normalize_deadline(cls, value: datetime):
        if value.tzinfo is not None:
            value = value.astimezone(timezone.utc).replace(tzinfo=None)
        return value


class PracticumCreate(PracticumBase):
    @field_validator("deadline")
    @classmethod
    def validate_future_deadline(cls, value: datetime):
        if value <= datetime.now(timezone.utc).replace(tzinfo=None):
            raise ValueError("Deadline harus berada di masa depan.")
        return value


class PracticumUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=4, max_length=180)
    description: str | None = Field(default=None, min_length=10, max_length=2000)
    deadline: datetime | None = None

    @field_validator("deadline")
    @classmethod
    def validate_deadline(cls, value):
        if value is None:
            return value
        if value.tzinfo is not None:
            value = value.astimezone(timezone.utc).replace(tzinfo=None)
        if value <= datetime.now(timezone.utc).replace(tzinfo=None):
            raise ValueError("Deadline harus berada di masa depan.")
        return value


class PracticumOut(PracticumBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
