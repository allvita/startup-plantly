"""
CRUD + seeding helpers.
"""
import random

from sqlalchemy.orm import Session

from auth import hash_password
from config import settings
from models import CareTask, Plant, SensorReading, User

DAY_LABELS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email.lower().strip()).first()


def get_plants_for_user(db: Session, user_id: int):
    return db.query(Plant).filter(Plant.owner_id == user_id).order_by(Plant.id).all()


def get_plant(db: Session, plant_id: int, user_id: int):
    return (
        db.query(Plant)
        .filter(Plant.id == plant_id, Plant.owner_id == user_id)
        .first()
    )


def get_tasks_for_plant(db: Session, plant_id: int):
    return (
        db.query(CareTask)
        .filter(CareTask.plant_id == plant_id)
        .order_by(CareTask.id)
        .all()
    )


def get_readings_for_plant(db: Session, plant_id: int):
    return (
        db.query(SensorReading)
        .filter(SensorReading.plant_id == plant_id)
        .order_by(SensorReading.id)
        .all()
    )


def overall_health(plants):
    if not plants:
        return 0
    return round(sum(p.health_score for p in plants) / len(plants))


def seed_database(db: Session):
    """Populate the database with the default account + Phase 1 demo data,
    but only if it is empty."""
    if db.query(User).first():
        return

    admin = User(
        name=settings.DEFAULT_ADMIN_NAME,
        email=settings.DEFAULT_ADMIN_EMAIL,
        password_hash=hash_password(settings.DEFAULT_ADMIN_PASSWORD),
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)

    tomato = Plant(
        owner_id=admin.id,
        name="Tomato",
        species="Solanum lycopersicum",
        slug="tomato",
        accent_color="#D95C5C",
        health_score=92,
        growth_stage="Flowering",
        location="Balcony Garden · East Side",
        pot_size="14 inch terracotta",
        age_days=52,
        image_path="/static/images/tomato.svg",
        last_watered="Today, 7:30 AM",
        last_fertilized="3 days ago",
        last_pruned="1 week ago",
        last_neem_spray="5 days ago",
        expected_harvest="18 days",
        soil_moisture=63,
        temperature=28.0,
        humidity=57,
        sunlight_hours=6.3,
    )

    potato = Plant(
        owner_id=admin.id,
        name="Potato",
        species="Solanum tuberosum",
        slug="potato",
        accent_color="#A67C52",
        health_score=88,
        growth_stage="Tuber Bulking",
        location="Balcony Garden · West Side",
        pot_size="16 inch grow bag",
        age_days=61,
        image_path="/static/images/potato.svg",
        last_watered="Yesterday, 6:50 PM",
        last_fertilized="6 days ago",
        last_pruned="2 weeks ago",
        last_neem_spray="4 days ago",
        expected_harvest="27 days",
        soil_moisture=58,
        temperature=26.0,
        humidity=52,
        sunlight_hours=5.4,
    )

    db.add_all([tomato, potato])
    db.commit()
    db.refresh(tomato)
    db.refresh(potato)

    tomato_tasks = [
        ("Watering", "droplets", "7:30 AM", "Today", "completed", "high"),
        ("Neem Spray", "spray-can", "6:00 PM", "Today", "upcoming", "normal"),
        ("Sprinkling", "cloud-drizzle", "9:00 AM", "Tomorrow", "upcoming", "low"),
        ("Pruning", "scissors", "5:00 PM", "Tomorrow", "upcoming", "normal"),
        ("Vermicompost", "leaf", "8:00 AM", "20 Jul", "upcoming", "normal"),
        ("Fertilizer", "flask-conical", "8:30 AM", "24 Jul", "upcoming", "high"),
    ]
    potato_tasks = [
        ("Watering", "droplets", "6:50 PM", "Yesterday", "completed", "normal"),
        ("Sprinkling", "cloud-drizzle", "7:00 AM", "Today", "upcoming", "normal"),
        ("Vermicompost", "leaf", "9:30 AM", "Tomorrow", "upcoming", "high"),
        ("Neem Spray", "spray-can", "5:30 PM", "19 Jul", "upcoming", "normal"),
        ("Pruning", "scissors", "4:00 PM", "22 Jul", "upcoming", "low"),
        ("Fertilizer", "flask-conical", "8:00 AM", "26 Jul", "upcoming", "normal"),
    ]

    for plant, task_set in ((tomato, tomato_tasks), (potato, potato_tasks)):
        for task_type, icon, time_label, date_label, status, priority in task_set:
            db.add(
                CareTask(
                    plant_id=plant.id,
                    task_type=task_type,
                    icon=icon,
                    time_label=time_label,
                    date_label=date_label,
                    status=status,
                    priority=priority,
                )
            )

    # 7 days of realistic simulated sensor history per plant
    random.seed(42)
    for plant, base_health, base_soil, base_temp, base_hum, base_sun in (
        (tomato, 86, 58, 27.0, 52, 5.8),
        (potato, 82, 54, 25.5, 48, 5.0),
    ):
        for i, day in enumerate(DAY_LABELS):
            drift = i * 1.0
            db.add(
                SensorReading(
                    plant_id=plant.id,
                    day_label=day,
                    health_score=min(99, round(base_health + drift + random.uniform(-1.5, 1.5))),
                    soil_moisture=max(30, round(base_soil + random.uniform(-4, 6))),
                    temperature=round(base_temp + random.uniform(-1.2, 1.8), 1),
                    humidity=max(30, round(base_hum + random.uniform(-3, 5))),
                    sunlight_hours=round(max(2.0, base_sun + random.uniform(-0.8, 1.0)), 1),
                )
            )

    db.commit()
