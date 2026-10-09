"""Risk assessment API endpoints."""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.db_models import FarmAnalysis

router = APIRouter()


@router.post("/assess")
async def assess_risk(request: dict, db: Session = Depends(get_db)):
    """Get risk assessment for a farm analysis."""
    analysis_id = request.get("analysis_id")
    if not analysis_id:
        raise HTTPException(status_code=400, detail="analysis_id is required")

    analysis = db.query(FarmAnalysis).filter(FarmAnalysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    if not analysis.risk_assessment:
        raise HTTPException(status_code=404, detail="Risk assessment not yet generated")

    return analysis.risk_assessment
