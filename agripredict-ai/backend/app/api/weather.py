"""Weather API endpoints."""

from fastapi import APIRouter, Query, HTTPException
from app.services.weather_service import fetch_current_weather, fetch_forecast, fetch_historical_weather
from app.services.location_data import resolve_coordinates

router = APIRouter()


@router.get("/current")
async def get_current_weather(
    latitude: float = Query(..., description="Latitude"),
    longitude: float = Query(..., description="Longitude"),
):
    """Get current weather for a location."""
    data = await fetch_current_weather(latitude, longitude)
    return data


@router.get("/forecast")
async def get_forecast(
    latitude: float = Query(..., description="Latitude"),
    longitude: float = Query(..., description="Longitude"),
    days: int = Query(7, ge=1, le=16, description="Forecast days"),
):
    """Get weather forecast for a location."""
    data = await fetch_forecast(latitude, longitude, days)
    return data


@router.get("/history")
async def get_history(
    latitude: float = Query(..., description="Latitude"),
    longitude: float = Query(..., description="Longitude"),
    years: int = Query(5, ge=1, le=10, description="Number of historical years"),
):
    """Get historical weather data for a location."""
    data = await fetch_historical_weather(latitude, longitude, years)
    # Remove daily_data from response to reduce size (keep it for internal use)
    response = {k: v for k, v in data.items() if k != "daily_data"}
    return response
