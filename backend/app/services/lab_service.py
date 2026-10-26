from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.lab_event import LabEvent
from app.models.practicum import Practicum
from app.models.group import Group
from app.models.submission import Submission

LABS = [
    {
        "id": "lab-p10",
        "title": "MVP API Cloud-Native",
        "meeting": "Pertemuan 10",
        "level": "Dasar",
        "duration": "45–60 menit",
        "description": "Praktik API modular, persistence, input validation, error handling, environment configuration, dan secret management.",
        "steps": [
            {"id":"health","title":"1. Health Check API","points":10,"description":"Pastikan backend cloud service berjalan dan endpoint /health merespons 200."},
            {"id":"read_api","title":"2. Membaca REST API","points":10,"description":"Ambil daftar praktikum dari endpoint REST."},
            {"id":"create_resource","title":"3. Membuat Resource","points":20,"description":"Buat satu praktikum melalui API dan simpan ke database."},
            {"id":"validation_422","title":"4. Uji Input Validation","points":20,"description":"Kirim payload tidak valid dan amati HTTP 422."},
            {"id":"conflict_409","title":"5. Uji Error Handling","points":20,"description":"Buat data kelompok duplikat dan amati HTTP 409."},
            {"id":"persistence","title":"6. Uji Persistence","points":10,"description":"Pastikan data yang dibuat tetap dapat dibaca kembali dari database."},
            {"id":"secret","title":"7. Environment & Secret","points":10,"description":"Identifikasi konfigurasi yang boleh dan tidak boleh ditulis langsung di source code."}
        ]
    },
    {
        "id": "lab-service-model",
        "title": "IaaS, PaaS, dan SaaS",
        "meeting": "Penguatan Konsep",
        "level": "Dasar",
        "duration": "20–30 menit",
        "description": "Membedakan tanggung jawab pengguna dan penyedia pada tiga model layanan cloud.",
        "steps": [
            {"id":"iaas","title":"IaaS","points":30,"description":"Identifikasi komponen yang dikelola pengguna pada IaaS."},
            {"id":"paas","title":"PaaS","points":30,"description":"Identifikasi komponen yang dikelola platform pada PaaS."},
            {"id":"saas","title":"SaaS","points":40,"description":"Identifikasi karakteristik software siap pakai melalui internet."}
        ]
    }
]

def get_labs():
    return LABS

def get_lab(lab_id: str):
    for lab in LABS:
        if lab["id"] == lab_id:
            return lab
    return None

def record_event(db: Session, lab_id: str, step_id: str, event_type: str, result: str, message: str = "", student_name: str = "Mahasiswa Demo"):
    e = LabEvent(student_name=student_name, lab_id=lab_id, step_id=step_id, event_type=event_type, result=result, message=message)
    db.add(e)
    db.commit()
    db.refresh(e)
    return e

def latest_step_results(db: Session, lab_id: str, student_name: str | None = None):
    q = db.query(LabEvent).filter(LabEvent.lab_id == lab_id)
    if student_name:
        q = q.filter(LabEvent.student_name == student_name)
    events = q.order_by(LabEvent.id.asc()).all()
    results = {}
    for e in events:
        results[e.step_id] = e.result
    return results

def score(db: Session, lab_id: str, student_name: str | None = None):
    lab = get_lab(lab_id)
    if not lab:
        return {"score":0,"completed":0,"total":0}
    results = latest_step_results(db, lab_id, student_name)
    total = sum(s["points"] for s in lab["steps"])
    earned = sum(s["points"] for s in lab["steps"] if results.get(s["id"]) == "PASS")
    completed = sum(1 for s in lab["steps"] if results.get(s["id"]) == "PASS")
    return {"score": earned, "max_score": total, "completed": completed, "total": len(lab["steps"]), "progress": round(completed/len(lab["steps"])*100) if lab["steps"] else 0}

def analytics_for_student(db: Session, student_name: str):
    q = db.query(LabEvent).filter(LabEvent.student_name == student_name)
    total_events = q.count()
    passed = q.filter(LabEvent.result == "PASS").count()
    failed = q.filter(LabEvent.result == "FAIL").count()
    error_events = q.filter(LabEvent.event_type.in_(["validation_error","conflict_error","api_error"])).count()
    recent = q.order_by(LabEvent.id.desc()).limit(20).all()
    return {
        "student_name": student_name,
        "total_events": total_events,
        "passed_events": passed,
        "failed_events": failed,
        "error_events": error_events,
        "recent": [
            {
                "id": e.id, "student_name": e.student_name, "lab_id": e.lab_id, "step_id": e.step_id,
                "event_type": e.event_type, "result": e.result, "message": e.message,
                "created_at": e.created_at.isoformat()
            } for e in recent
        ]
    }

def analytics(db: Session):
    total_events = db.query(LabEvent).count()
    passed = db.query(LabEvent).filter(LabEvent.result == "PASS").count()
    failed = db.query(LabEvent).filter(LabEvent.result == "FAIL").count()
    error_events = db.query(LabEvent).filter(LabEvent.event_type.in_(["validation_error","conflict_error","api_error"])).count()
    recent = db.query(LabEvent).order_by(LabEvent.id.desc()).limit(20).all()
    return {
        "total_events": total_events,
        "passed_events": passed,
        "failed_events": failed,
        "error_events": error_events,
        "recent": [
            {
                "id": e.id, "student_name": e.student_name, "lab_id": e.lab_id, "step_id": e.step_id,
                "event_type": e.event_type, "result": e.result, "message": e.message,
                "created_at": e.created_at.isoformat()
            } for e in recent
        ]
    }
