import logging
from pathlib import Path
from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException
from datetime import datetime, timezone

from app.config.settings import get_settings
from app.database.db import Base, SessionLocal, engine, get_db
from app import models
from app.models.user import User
from app.routes import auth, students, groups, practicums, submissions, assessments, dashboard, labs, system
from app.security.auth import require_roles
from app.services.auth_service import ensure_demo_users

settings = get_settings()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("cloudlab")
Base.metadata.create_all(bind=engine)

with SessionLocal() as seed_db:
    ensure_demo_users(seed_db)

app = FastAPI(
    title="CloudLab Edu",
    version=settings.app_version,
    description="Cloud-Native Learning Lab untuk pembelajaran Komputasi Awan",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(students.router, prefix="/api")
app.include_router(groups.router, prefix="/api")
app.include_router(practicums.router, prefix="/api")
app.include_router(submissions.router, prefix="/api")
app.include_router(assessments.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(labs.router, prefix="/api")
app.include_router(system.router, prefix="/api")

backend_dir = Path(__file__).resolve().parents[1]
frontend_dir = Path(settings.frontend_dir)
if not frontend_dir.is_absolute():
    frontend_dir = (backend_dir / frontend_dir).resolve()

for mount_path, folder in [
    ("/static", "static"),
    ("/public", "public"),
    ("/admin", "admin"),
    ("/dosen", "dosen"),
    ("/mahasiswa", "mahasiswa"),
]:
    target = frontend_dir / folder
    if target.exists():
        app.mount(mount_path, StaticFiles(directory=target, html=True), name=f"frontend-{folder}")

@app.middleware("http")
async def request_logger(request: Request, call_next):
    response = await call_next(request)
    logger.info("%s %s -> %s", request.method, request.url.path, response.status_code)
    return response

def error_payload(code: str, detail, request: Request):
    return {
        "error": code,
        "detail": detail,
        "path": request.url.path,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder(error_payload("VALIDATION_ERROR", exc.errors(), request)),
    )


@app.exception_handler(StarletteHTTPException)
async def http_error_handler(request: Request, exc: StarletteHTTPException):
    code_map = {
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        409: "CONFLICT",
        500: "INTERNAL_SERVER_ERROR",
        503: "SERVICE_UNAVAILABLE",
    }
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(error_payload(code_map.get(exc.status_code, f"HTTP_{exc.status_code}"), exc.detail, request)),
        headers=getattr(exc, "headers", None),
    )


@app.exception_handler(SQLAlchemyError)
async def db_error_handler(request: Request, exc: SQLAlchemyError):
    logger.exception("Database error")
    return JSONResponse(
        status_code=500,
        content=error_payload("DATABASE_ERROR", "Terjadi kesalahan pada basis data.", request),
    )

@app.get("/health", tags=["System"])
def health():
    payload = {
        "status": "unhealthy" if settings.simulate_health_failure else "healthy",
        "service": "cloudlab-backend",
        "environment": settings.app_env,
        "product": "CloudLab Edu",
        "version": settings.app_version,
    }
    if settings.simulate_health_failure:
        return JSONResponse(status_code=503, content=payload)
    return payload

@app.get("/version", tags=["System"])
def version():
    return {"version": settings.app_version, "environment": settings.app_env}

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse("/public/login.html")

@app.get("/docs", include_in_schema=False)
def admin_docs(user: User = Depends(require_roles("admin"))):
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="CloudLab Edu - Admin API Docs",
        swagger_ui_parameters={"persistAuthorization": True},
    )

@app.get("/openapi.json", include_in_schema=False)
def protected_openapi(user: User = Depends(require_roles("admin"))):
    return get_openapi(title=app.title, version=app.version, description=app.description, routes=app.routes)
