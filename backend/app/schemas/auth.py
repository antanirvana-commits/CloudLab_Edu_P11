from pydantic import BaseModel, EmailStr, Field
from typing import Literal

Role = Literal["admin", "dosen", "mahasiswa"]

class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=160)
    password: str = Field(min_length=8, max_length=128)

class UserOut(BaseModel):
    id: int
    username: str
    full_name: str
    # Output dibuat kompatibel dengan data legacy.
    # Validasi email tetap diterapkan pada ProfileUpdate/input baru.
    email: str
    role: Role
    is_active: bool

    model_config = {"from_attributes": True}

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

class ProfileUpdate(BaseModel):
    full_name: str = Field(min_length=3, max_length=120)
    email: EmailStr
