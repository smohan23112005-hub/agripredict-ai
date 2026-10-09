"""Health check endpoint."""

from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "AgriPredict AI",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
    }


@router.get("/locations")
async def get_locations():
    """Get available locations (AP districts)."""
    from app.services.location_data import AP_DISTRICTS, SOIL_TYPES, IRRIGATION_TYPES, FARMING_SEASONS
    districts = []
    for name, data in AP_DISTRICTS.items():
        districts.append({
            "name": name,
            "latitude": data["lat"],
            "longitude": data["lon"],
            "mandals": data.get("mandals", []),
        })
    return {
        "state": "Andhra Pradesh",
        "districts": districts,
        "soil_types": SOIL_TYPES,
        "irrigation_types": IRRIGATION_TYPES,
        "farming_seasons": FARMING_SEASONS,
    }
