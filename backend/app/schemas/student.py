from pydantic import BaseModel, EmailStr, Field, ConfigDict

class StudentCreate(BaseModel):
    nim: str = Field(min_length=5, max_length=30)
    name: str = Field(min_length=3, max_length=120)
    email: EmailStr

class StudentUpdate(BaseModel):
    nim: str | None = Field(default=None, min_length=5, max_length=30)
    name: str | None = Field(default=None, min_length=3, max_length=120)
    email: EmailStr | None = None

class StudentOut(StudentCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
