from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError

from app.infrastructure.db.base import Base
from app.infrastructure.db.seed import seed_from_legacy_json
from app.infrastructure.db.session import SessionLocal, engine
from app.interfaces.http.routers.cari import router as cari_router
from app.interfaces.http.routers.health import router as health_router
from app.interfaces.http.routers.teklif import router as teklif_router
from app.interfaces.http.routers.urun import router as urun_router


def create_app() -> FastAPI:
    app = FastAPI(title="Teklif API", version="0.1.0")
    app.include_router(health_router)
    app.include_router(cari_router)
    app.include_router(urun_router)
    app.include_router(teklif_router)
    app.include_router(health_router, prefix="/api", include_in_schema=False)
    app.include_router(cari_router, prefix="/api", include_in_schema=False)
    app.include_router(urun_router, prefix="/api", include_in_schema=False)
    app.include_router(teklif_router, prefix="/api", include_in_schema=False)

    @app.on_event("startup")
    def startup() -> None:
        try:
            Base.metadata.create_all(bind=engine)
            with SessionLocal() as session:
                seed_from_legacy_json(session)
        except SQLAlchemyError:
            # API yine de acilabilsin; migration/DB kurulumu disaridan yonetilir.
            pass

    return app


app = create_app()
