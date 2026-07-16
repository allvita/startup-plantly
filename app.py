"""
PlantCare AI — Phase 1
FastAPI application entrypoint.

Run with:
    uvicorn app:app --reload
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from config import settings
from database import Base, SessionLocal, engine
from routes import auth_routes, dashboard_routes, plant_routes
import crud

# Create tables on first run
Base.metadata.create_all(bind=engine)

# Seed the database with the default account + demo plants
db = SessionLocal()
try:
    crud.seed_database(db)
finally:
    db.close()

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    session_cookie=settings.SESSION_COOKIE_NAME,
    max_age=settings.SESSION_MAX_AGE,
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_routes.router)
app.include_router(dashboard_routes.router)
app.include_router(plant_routes.router)
