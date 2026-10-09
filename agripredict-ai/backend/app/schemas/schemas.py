"""Pydantic schemas for request/response validation."""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# ============ Farm Schemas ============

class FarmInput(BaseModel):
    farmer_name: Optional[str] = None
    state: str = "Andhra Pradesh"
    district: str
    mandal: Optional[str] = None
    village: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    land_area: float = Field(gt=0, description="Land area")
    land_unit: str = "acres"
    soil_type: str
    irrigation_type: str
    farming_season: str
    previous_crop: Optional[str] = None
    preferred_crops: Optional[List[str]] = None
    planned_sowing_date: Optional[str] = None
    budget: Optional[float] = None
    preferred_language: str = "en"


class FarmResponse(BaseModel):
    id: str
    analysis_id: str
    message: str
    status: str


# ============ Weather Schemas ============

class WeatherRequest(BaseModel):
    latitude: float
    longitude: float
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class CurrentWeather(BaseModel):
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    precipitation: Optional[float] = None
    wind_speed: Optional[float] = None
    weather_code: Optional[int] = None
    description: Optional[str] = None
    fetched_at: Optional[str] = None
    is_demo: bool = False


class DailyWeather(BaseModel):
    date: str
    temp_max: Optional[float] = None
    temp_min: Optional[float] = None
    precipitation: Optional[float] = None
    humidity_mean: Optional[float] = None
    wind_speed_max: Optional[float] = None


class HistoricalWeatherSummary(BaseModel):
    years_analyzed: List[int]
    annual_rainfall: Dict[str, float]
    monthly_avg_rainfall: Dict[str, float]
    monthly_avg_temp_max: Dict[str, float]
    monthly_avg_temp_min: Dict[str, float]
    heavy_rain_days_per_year: Dict[str, int]
    max_consecutive_dry_days: Dict[str, int]
    total_data_points: int
    data_source: str
    daily_data: Optional[List[Dict[str, Any]]] = None


# ============ Crop Schemas ============

class CropRecommendation(BaseModel):
    rank: int
    crop_name: str
    crop_name_te: Optional[str] = None
    suitability_score: float
    season: str
    suitable_soils: List[str]
    water_requirement: str
    crop_duration_days: Optional[int] = None
    major_risks: List[str]
    expected_yield_range: Optional[str] = None
    recommended_sowing: Optional[str] = None
    reason: str
    confidence: str  # high, medium, low
    alternatives: Optional[List[str]] = None


class CropRecommendationRequest(BaseModel):
    farm_id: str
    analysis_id: Optional[str] = None


class CropRecommendationResponse(BaseModel):
    model_config = {'protected_namespaces': ()}
    recommendations: List[CropRecommendation]
    model_info: Dict[str, Any]
    data_sources: List[str]


# ============ Risk Schemas ============

class RiskCategory(BaseModel):
    category: str
    level: str  # Low, Moderate, High, Unknown
    time_period: str
    indicators: List[str]
    explanation: str
    impact: str
    preventive_actions: List[str]
    data_basis: str  # historical, forecast, model, rule-based


class RiskAssessmentRequest(BaseModel):
    farm_id: str
    analysis_id: Optional[str] = None
    crop: Optional[str] = None


class RiskAssessmentResponse(BaseModel):
    overall_risk: str
    risks: List[RiskCategory]
    assessed_at: str
    data_sources: List[str]


# ============ Finance Schemas ============

class FinanceInput(BaseModel):
    farm_id: str
    analysis_id: Optional[str] = None
    crop: str
    land_area: float
    land_unit: str = "acres"
    seed_cost: float = 0
    fertilizer_cost: float = 0
    pesticide_cost: float = 0
    labor_cost: float = 0
    irrigation_cost: float = 0
    machinery_cost: float = 0
    transport_cost: float = 0
    other_expenses: float = 0
    expected_yield_per_acre: Optional[float] = None
    expected_price_per_quintal: Optional[float] = None
    harvest_expenses: float = 0


class FinanceScenario(BaseModel):
    scenario: str  # normal, heavy_rainfall, drought
    yield_factor: float
    price_factor: float
    total_cost: float
    expected_yield: float
    expected_revenue: float
    net_return: float
    return_per_acre: float
    risk_level: str


class FinanceResponse(BaseModel):
    crop: str
    land_area: float
    total_cultivation_cost: float
    expected_gross_revenue: float
    estimated_net_return: float
    estimated_loss: float
    break_even_price: float
    return_per_acre: float
    scenarios: List[FinanceScenario]
    financial_risk_level: str
    disclaimer: str


# ============ Dashboard Schemas ============

class DashboardData(BaseModel):
    farm_summary: Dict[str, Any]
    weather_summary: Dict[str, Any]
    top_crop: Optional[Dict[str, Any]] = None
    top_risk: Optional[Dict[str, Any]] = None
    financial_summary: Optional[Dict[str, Any]] = None
    charts_data: Optional[Dict[str, Any]] = None


# ============ Report Schemas ============

class ReportRequest(BaseModel):
    analysis_id: str
    format: str = "pdf"  # pdf or csv
