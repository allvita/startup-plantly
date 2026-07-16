"""
SQLAlchemy ORM models for PlantCare AI.
"""
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    plants = relationship("Plant", back_populates="owner", cascade="all, delete-orphan")


class Plant(Base):
    __tablename__ = "plants"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    name = Column(String, nullable=False)
    species = Column(String, nullable=False)          # "Tomato" / "Potato"
    slug = Column(String, nullable=False)              # "tomato" / "potato"
    accent_color = Column(String, nullable=False)       # secondary accent hex

    health_score = Column(Integer, default=90)
    growth_stage = Column(String, default="Flowering")
    location = Column(String, default="Balcony Garden")
    pot_size = Column(String, default="12 inch terracotta")
    age_days = Column(Integer, default=45)

    image_path = Column(String, default="")

    last_watered = Column(String, default="Today, 7:30 AM")
    last_fertilized = Column(String, default="3 days ago")
    last_pruned = Column(String, default="1 week ago")
    last_neem_spray = Column(String, default="5 days ago")
    expected_harvest = Column(String, default="18 days")

    soil_moisture = Column(Integer, default=63)
    temperature = Column(Float, default=28.0)
    humidity = Column(Integer, default=57)
    sunlight_hours = Column(Float, default=6.3)

    is_active = Column(Boolean, default=True)

    owner = relationship("User", back_populates="plants")
    tasks = relationship("CareTask", back_populates="plant", cascade="all, delete-orphan")
    readings = relationship("SensorReading", back_populates="plant", cascade="all, delete-orphan")


class CareTask(Base):
    __tablename__ = "care_tasks"

    id = Column(Integer, primary_key=True, index=True)
    plant_id = Column(Integer, ForeignKey("plants.id"))

    task_type = Column(String, nullable=False)   # Watering, Sprinkling, Neem Spray, Pruning, Vermicompost, Fertilizer
    icon = Column(String, nullable=False)         # lucide icon name
    time_label = Column(String, nullable=False)   # "7:30 AM"
    date_label = Column(String, nullable=False)   # "Today" / "Tomorrow" / "12 Jul"
    status = Column(String, default="upcoming")   # completed / upcoming / missed
    priority = Column(String, default="normal")   # low / normal / high

    plant = relationship("Plant", back_populates="tasks")


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    plant_id = Column(Integer, ForeignKey("plants.id"))

    day_label = Column(String, nullable=False)   # "Mon", "Tue" ...
    health_score = Column(Integer, default=90)
    soil_moisture = Column(Integer, default=60)
    temperature = Column(Float, default=27.0)
    humidity = Column(Integer, default=55)
    sunlight_hours = Column(Float, default=6.0)
    recorded_at = Column(DateTime, default=datetime.utcnow)

    plant = relationship("Plant", back_populates="readings")
