"""Crop recommendation API endpoints."""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.db_models import FarmAnalysis
from app.services.crop_service import get_all_crops

router = APIRouter()


@router.get("/list")
async def list_crops():
    """List all available crops."""
    crops = get_all_crops()
    return {
        "crops": [
            {
                "name": c["name"],
                "name_te": c.get("name_te", ""),
                "category": c.get("category", ""),
                "seasons": c.get("seasons", []),
                "water_requirement": c.get("water_requirement", ""),
                "crop_duration_days": c.get("crop_duration_days"),
            }
            for c in crops
        ]
    }


@router.post("/recommend")
async def recommend(request: dict, db: Session = Depends(get_db)):
    """Get crop recommendations for a farm analysis."""
    analysis_id = request.get("analysis_id")
    if not analysis_id:
        raise HTTPException(status_code=400, detail="analysis_id is required")

    analysis = db.query(FarmAnalysis).filter(FarmAnalysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    if not analysis.crop_recommendations:
        raise HTTPException(status_code=404, detail="Crop recommendations not yet generated")

    return {
        "recommendations": analysis.crop_recommendations,
        "model_info": {
            "type": "Rule-based scoring with crop database",
            "features": ["soil_type", "irrigation", "season", "rainfall", "temperature"],
            "limitations": "Scores are based on general crop requirements and historical weather averages. "
                          "Local micro-climate conditions and specific soil chemistry are not considered.",
        },
        "data_sources": ["AgriPredict Crop Database", "Open-Meteo Historical Weather"],
    }
