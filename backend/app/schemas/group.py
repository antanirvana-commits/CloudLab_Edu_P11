from pydantic import BaseModel, Field, ConfigDict

class GroupCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    project_title: str | None = Field(default=None, max_length=200)

class GroupUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    project_title: str | None = Field(default=None, max_length=200)

class GroupOut(GroupCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
