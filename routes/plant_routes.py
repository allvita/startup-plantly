"""
Secondary pages: My Plants, Plant Detail, Calendar, Analytics, Settings, Profile.
"""
from datetime import datetime

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from auth import get_current_user, require_auth_redirect
from crud import (
    get_plant,
    get_plants_for_user,
    get_readings_for_plant,
    get_tasks_for_plant,
    overall_health,
)
from database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def _base_ctx(request: Request, db: Session, user):
    plants = get_plants_for_user(db, user.id)
    return {
        "request": request,
        "user": user,
        "plants": plants,
        "today": datetime.now().strftime("%A, %d %B"),
        "overall_health": overall_health(plants),
    }


@router.get("/plants")
def my_plants(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return require_auth_redirect()
    ctx = _base_ctx(request, db, user)
    return templates.TemplateResponse("my_plants.html", ctx)


@router.get("/plants/{plant_id}/details")
def plant_details(plant_id: int, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return require_auth_redirect()

    plant = get_plant(db, plant_id, user.id)
    if not plant:
        return RedirectResponse(url="/plants", status_code=303)

    ctx = _base_ctx(request, db, user)
    ctx["active_plant"] = plant
    return templates.TemplateResponse("plant_details.html", ctx)


@router.get("/calendar")
def calendar(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return require_auth_redirect()

    ctx = _base_ctx(request, db, user)
    tasks_by_plant = []
    for plant in ctx["plants"]:
        tasks_by_plant.append({
            "plant": plant,
            "tasks": get_tasks_for_plant(db, plant.id),
        })
    ctx["tasks_by_plant"] = tasks_by_plant
    return templates.TemplateResponse("calendar.html", ctx)


@router.get("/analytics")
def analytics(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return require_auth_redirect()
    ctx = _base_ctx(request, db, user)

    plant_series = []
    for plant in ctx["plants"]:
        readings = get_readings_for_plant(db, plant.id)
        plant_series.append({
            "plant": plant,
            "labels": [r.day_label for r in readings],
            "health": [r.health_score for r in readings],
            "soil": [r.soil_moisture for r in readings],
        })
    ctx["plant_series"] = plant_series
    return templates.TemplateResponse("analytics.html", ctx)


@router.get("/settings")
def settings_page(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return require_auth_redirect()
    ctx = _base_ctx(request, db, user)
    return templates.TemplateResponse("settings.html", ctx)


@router.get("/profile")
def profile(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return require_auth_redirect()
    ctx = _base_ctx(request, db, user)
    return templates.TemplateResponse("profile.html", ctx)
