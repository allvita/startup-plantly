"""
Dashboard page + HTMX partial for plant switching + JSON chart data API.
"""
from datetime import datetime

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
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
from insights import build_insights, build_next_action

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def _greeting() -> str:
    hour = datetime.now().hour
    if hour < 12:
        return "Good Morning"
    if hour < 17:
        return "Good Afternoon"
    return "Good Evening"


def _plant_context(db: Session, plant, plants):
    tasks = get_tasks_for_plant(db, plant.id)
    readings = get_readings_for_plant(db, plant.id)
    return {
        "plant": plant,
        "plants": plants,
        "tasks": tasks,
        "insights": build_insights(plant),
        "next_action": build_next_action(plant),
        "chart_labels": [r.day_label for r in readings],
        "chart_health": [r.health_score for r in readings],
        "chart_soil": [r.soil_moisture for r in readings],
        "chart_temp": [r.temperature for r in readings],
        "chart_humidity": [r.humidity for r in readings],
        "chart_sunlight": [r.sunlight_hours for r in readings],
    }


@router.get("/")
def dashboard(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return require_auth_redirect()

    plants = get_plants_for_user(db, user.id)
    if not plants:
        return templates.TemplateResponse(
            "dashboard.html",
            {
                "request": request,
                "user": user,
                "plants": [],
                "greeting": _greeting(),
                "today": datetime.now().strftime("%A, %d %B"),
                "overall_health": 0,
            },
        )

    active_plant = plants[0]
    ctx = _plant_context(db, active_plant, plants)

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": user,
            "greeting": _greeting(),
            "today": datetime.now().strftime("%A, %d %B"),
            "overall_health": overall_health(plants),
            **ctx,
        },
    )


@router.get("/plants/{plant_id}/panel")
def plant_panel(plant_id: int, request: Request, db: Session = Depends(get_db)):
    """HTMX endpoint: returns just the plant-specific dashboard panel."""
    user = get_current_user(request, db)
    if not user:
        return require_auth_redirect()

    plants = get_plants_for_user(db, user.id)
    plant = get_plant(db, plant_id, user.id)
    if not plant:
        return JSONResponse({"error": "Plant not found"}, status_code=404)

    ctx = _plant_context(db, plant, plants)
    return templates.TemplateResponse(
        "partials/dashboard_panel.html",
        {"request": request, **ctx},
    )


@router.get("/api/plants/{plant_id}/chart-data")
def chart_data(plant_id: int, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return JSONResponse({"error": "Unauthorized"}, status_code=401)

    plant = get_plant(db, plant_id, user.id)
    if not plant:
        return JSONResponse({"error": "Plant not found"}, status_code=404)

    readings = get_readings_for_plant(db, plant.id)
    return JSONResponse({
        "labels": [r.day_label for r in readings],
        "health": [r.health_score for r in readings],
        "soil": [r.soil_moisture for r in readings],
        "temperature": [r.temperature for r in readings],
        "humidity": [r.humidity for r in readings],
        "sunlight": [r.sunlight_hours for r in readings],
        "accent": plant.accent_color,
    })
