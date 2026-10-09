"""SQLAlchemy database models for AgriPredict AI."""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database.db import Base


def generate_uuid():
    return str(uuid.uuid4())


class FarmProfile(Base):
    __tablename__ = "farm_profiles"

    id = Column(String, primary_key=True, default=generate_uuid)
    farmer_name = Column(String, nullable=True)
    state = Column(String, nullable=False, default="Andhra Pradesh")
    district = Column(String, nullable=False)
    mandal = Column(String, nullable=True)
    village = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    land_area = Column(Float, nullable=False)
    land_unit = Column(String, default="acres")
    soil_type = Column(String, nullable=False)
    irrigation_type = Column(String, nullable=False)
    farming_season = Column(String, nullable=False)
    previous_crop = Column(String, nullable=True)
    preferred_crops = Column(Text, nullable=True)  # JSON string
    planned_sowing_date = Column(String, nullable=True)
    budget = Column(Float, nullable=True)
    preferred_language = Column(String, default="en")
    created_at = Column(DateTime, default=datetime.utcnow)

    analyses = relationship("FarmAnalysis", back_populates="farm")


class FarmAnalysis(Base):
    __tablename__ = "farm_analyses"

    id = Column(String, primary_key=True, default=generate_uuid)
    farm_id = Column(String, ForeignKey("farm_profiles.id"), nullable=False)
    status = Column(String, default="pending")  # pending, processing, completed, failed
    weather_data = Column(JSON, nullable=True)
    crop_recommendations = Column(JSON, nullable=True)
    risk_assessment = Column(JSON, nullable=True)
    financial_estimates = Column(JSON, nullable=True)
    dashboard_data = Column(JSON, nullable=True)
    data_sources = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    farm = relationship("FarmProfile", back_populates="analyses")


class WeatherCache(Base):
    __tablename__ = "weather_cache"

    id = Column(String, primary_key=True, default=generate_uuid)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    data_type = Column(String, nullable=False)  # historical, current, forecast
    start_date = Column(String, nullable=True)
    end_date = Column(String, nullable=True)
    data = Column(JSON, nullable=False)
    fetched_at = Column(DateTime, default=datetime.utcnow)


class CropInfo(Base):
    __tablename__ = "crop_info"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False, unique=True)
    name_te = Column(String, nullable=True)  # Telugu name
    category = Column(String, nullable=True)  # cereal, pulse, oilseed, vegetable, fruit, commercial
    seasons = Column(Text, nullable=True)  # JSON list of suitable seasons
    soil_types = Column(Text, nullable=True)  # JSON list of suitable soils
    min_rainfall_mm = Column(Float, nullable=True)
    max_rainfall_mm = Column(Float, nullable=True)
    min_temp_c = Column(Float, nullable=True)
    max_temp_c = Column(Float, nullable=True)
    optimal_temp_min = Column(Float, nullable=True)
    optimal_temp_max = Column(Float, nullable=True)
    water_requirement = Column(String, nullable=True)  # low, medium, high
    crop_duration_days = Column(Integer, nullable=True)
    irrigation_needed = Column(Boolean, default=False)
    typical_yield_per_acre = Column(Float, nullable=True)  # quintals
    typical_cost_per_acre = Column(Float, nullable=True)  # INR
    typical_price_per_quintal = Column(Float, nullable=True)  # INR
    sowing_months = Column(Text, nullable=True)  # JSON list
    harvest_months = Column(Text, nullable=True)  # JSON list
    description = Column(Text, nullable=True)


class ModelMetadata(Base):
    __tablename__ = "model_metadata"

    id = Column(String, primary_key=True, default=generate_uuid)
    model_name = Column(String, nullable=False)
    model_type = Column(String, nullable=False)
    version = Column(String, nullable=True)
    dataset_source = Column(String, nullable=True)
    training_samples = Column(Integer, nullable=True)
    accuracy = Column(Float, nullable=True)
    f1_score = Column(Float, nullable=True)
    features = Column(Text, nullable=True)
    limitations = Column(Text, nullable=True)
    trained_at = Column(DateTime, default=datetime.utcnow)
