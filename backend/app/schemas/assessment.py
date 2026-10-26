from pydantic import BaseModel, Field, ConfigDict

class AssessmentCreate(BaseModel):
    submission_id: int = Field(gt=0)
    score: float = Field(ge=0, le=100)
    feedback: str = Field(min_length=3)

class AssessmentUpdate(BaseModel):
    score: float | None = Field(default=None, ge=0, le=100)
    feedback: str | None = Field(default=None, min_length=3)

class AssessmentOut(BaseModel):
    id: int
    submission_id: int
    score: float
    feedback: str
    model_config = ConfigDict(from_attributes=True)
