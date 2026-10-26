from datetime import datetime
from pydantic import BaseModel, HttpUrl, ConfigDict, Field

class SubmissionCreate(BaseModel):
    practicum_id: int = Field(gt=0)
    group_id: int = Field(gt=0)
    repository_url: HttpUrl
    report_url: HttpUrl

class SubmissionOut(BaseModel):
    id: int
    practicum_id: int
    group_id: int
    repository_url: str
    report_url: str
    submitted_at: datetime
    status: str
    model_config = ConfigDict(from_attributes=True)
