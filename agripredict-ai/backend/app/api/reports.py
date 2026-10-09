"""Report generation API endpoints."""

import os
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse, PlainTextResponse
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.db_models import FarmAnalysis, FarmProfile
from app.services.report_service import generate_pdf_report, generate_csv_report

router = APIRouter()


def _build_analysis_dict(analysis: FarmAnalysis, farm: FarmProfile) -> dict:
    return {
        "farm": {
            "district": farm.district if farm else "N/A",
            "state": farm.state if farm else "N/A",
            "land_area": farm.land_area if farm else "N/A",
            "land_unit": farm.land_unit if farm else "acres",
            "soil_type": farm.soil_type if farm else "N/A",
            "irrigation_type": farm.irrigation_type if farm else "N/A",
            "farming_season": farm.farming_season if farm else "N/A",
        } if farm else {},
        "weather": analysis.weather_data.get("historical", {}) if analysis.weather_data else {},
        "crops": analysis.crop_recommendations or [],
        "risk": analysis.risk_assessment or {},
        "finance": analysis.financial_estimates or {},
    }


@router.get("/csv/{analysis_id}")
async def get_csv_report(analysis_id: str, db: Session = Depends(get_db)):
    """Direct CSV download route."""
    analysis = db.query(FarmAnalysis).filter(FarmAnalysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    farm = db.query(FarmProfile).filter(FarmProfile.id == analysis.farm_id).first()
    analysis_data = _build_analysis_dict(analysis, farm)
    csv_content = generate_csv_report(analysis_data)
    return PlainTextResponse(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=agripredict_report_{analysis_id[:8]}.csv"},
    )


@router.get("/pdf/{analysis_id}")
async def get_pdf_report(analysis_id: str, lang: str = "en", db: Session = Depends(get_db)):
    """Direct PDF download route."""
    analysis = db.query(FarmAnalysis).filter(FarmAnalysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    farm = db.query(FarmProfile).filter(FarmProfile.id == analysis.farm_id).first()
    analysis_data = _build_analysis_dict(analysis, farm)
    os.makedirs("reports_output", exist_ok=True)
    pdf_path = f"reports_output/agripredict_report_{analysis_id[:8]}.pdf"
    try:
        generate_pdf_report(analysis_data, pdf_path)
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=f"agripredict_report_{analysis_id[:8]}.pdf",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")


@router.get("/{analysis_id}")
async def get_report(analysis_id: str, format: str = "pdf", db: Session = Depends(get_db)):
    """Generate and download a report with format query param."""
    if format.lower() == "csv":
        return await get_csv_report(analysis_id, db)
    return await get_pdf_report(analysis_id, "en", db)
