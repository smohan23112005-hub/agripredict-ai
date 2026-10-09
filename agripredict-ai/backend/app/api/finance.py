"""Financial estimation API endpoints."""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.db_models import FarmAnalysis, FarmProfile
from app.services.finance_service import estimate_finances
from app.services.crop_service import get_crop_by_name
from app.schemas.schemas import FinanceInput

router = APIRouter()


@router.post("/estimate")
async def estimate(finance_input: FinanceInput, db: Session = Depends(get_db)):
    """Estimate financial outcomes for a crop."""
    crop_data = get_crop_by_name(finance_input.crop)

    result = estimate_finances(
        crop=finance_input.crop,
        land_area=finance_input.land_area,
        land_unit=finance_input.land_unit,
        seed_cost=finance_input.seed_cost,
        fertilizer_cost=finance_input.fertilizer_cost,
        pesticide_cost=finance_input.pesticide_cost,
        labor_cost=finance_input.labor_cost,
        irrigation_cost=finance_input.irrigation_cost,
        machinery_cost=finance_input.machinery_cost,
        transport_cost=finance_input.transport_cost,
        other_expenses=finance_input.other_expenses,
        expected_yield_per_acre=finance_input.expected_yield_per_acre,
        expected_price_per_quintal=finance_input.expected_price_per_quintal,
        harvest_expenses=finance_input.harvest_expenses,
        crop_data=crop_data,
    )

    # Update analysis if provided
    if finance_input.analysis_id:
        analysis = db.query(FarmAnalysis).filter(FarmAnalysis.id == finance_input.analysis_id).first()
        if analysis:
            analysis.financial_estimates = result
            db.commit()

    return result
