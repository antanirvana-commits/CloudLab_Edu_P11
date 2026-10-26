from sqlalchemy.orm import Session
from app.models.student import Student
from app.models.group import Group
from app.models.practicum import Practicum
from app.models.submission import Submission
from app.models.assessment import Assessment

def summary(db: Session):
    return {
        "students": db.query(Student).count(),
        "groups": db.query(Group).count(),
        "practicums": db.query(Practicum).count(),
        "submissions": db.query(Submission).count(),
        "assessments": db.query(Assessment).count(),
        "late_submissions": db.query(Submission).filter(Submission.status == "LATE").count(),
    }
