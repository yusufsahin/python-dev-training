from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import auth, cart, catalog, orders

app = FastAPI(title="Storium API")

_settings = get_settings()
_origins = [o.strip() for o in _settings.cors_origins.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(catalog.router, prefix="/api")
app.include_router(cart.router, prefix="/api")
app.include_router(orders.router, prefix="/api")


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}
