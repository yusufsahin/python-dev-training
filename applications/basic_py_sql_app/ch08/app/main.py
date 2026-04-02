from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.exceptions import AppValidationError
from app.routers import departments, students

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="School API", version="1.0.0", lifespan=lifespan)

origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AppValidationError)
async def app_validation_handler(_, exc: AppValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"errors": exc.messages},
    )


@app.get("/api/v1")
async def api_root():
    return {
        "name": "school-api",
        "version": 1,
        "endpoints": {
            "health": "/api/v1/health",
            "departments": "/api/v1/departments",
            "students": "/api/v1/students",
        },
    }


@app.get("/api/v1/health")
async def health():
    return {"status": "ok"}


app.include_router(departments.router, prefix="/api/v1")
app.include_router(students.router, prefix="/api/v1")

_dist = Path(__file__).resolve().parent.parent / "frontend" / "dist"
if _dist.is_dir() and (_dist / "index.html").is_file():
    app.mount("/", StaticFiles(directory=str(_dist), html=True), name="spa")
