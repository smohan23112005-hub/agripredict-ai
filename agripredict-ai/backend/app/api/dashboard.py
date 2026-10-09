"""Dashboard API endpoints."""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.db_models import FarmAnalysis, FarmProfile

router = APIRouter()


@router.get("/{analysis_id}")
async def get_dashboard(analysis_id: str, db: Session = Depends(get_db)):
    """Get dashboard data for an analysis."""
    analysis = db.query(FarmAnalysis).filter(FarmAnalysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    farm = db.query(FarmProfile).filter(FarmProfile.id == analysis.farm_id).first()

    return {
        "analysis_id": analysis_id,
        "status": analysis.status,
        "farm": {
            "id": farm.id if farm else None,
            "farmer_name": farm.farmer_name if farm else None,
            "district": farm.district if farm else None,
            "state": farm.state if farm else None,
            "land_area": farm.land_area if farm else None,
            "land_unit": farm.land_unit if farm else None,
            "soil_type": farm.soil_type if farm else None,
            "irrigation_type": farm.irrigation_type if farm else None,
            "farming_season": farm.farming_season if farm else None,
            "latitude": farm.latitude if farm else None,
            "longitude": farm.longitude if farm else None,
        } if farm else {},
        "weather": analysis.weather_data,
        "crops": analysis.crop_recommendations,
        "risk": analysis.risk_assessment,
        "finance": analysis.financial_estimates,
        "dashboard": analysis.dashboard_data,
        "data_sources": analysis.data_sources,
        "created_at": analysis.created_at.isoformat() if analysis.created_at else None,
        "completed_at": analysis.completed_at.isoformat() if analysis.completed_at else None,
    }
