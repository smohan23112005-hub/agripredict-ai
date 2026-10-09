"""Farm API endpoints."""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import json

from app.schemas.schemas import FarmInput, FarmResponse
from app.database.db import get_db
from app.models.db_models import FarmProfile, FarmAnalysis, generate_uuid
from app.services.location_data import resolve_coordinates
from app.services.weather_service import fetch_historical_weather, fetch_current_weather, fetch_forecast
from app.services.crop_service import recommend_crops, get_crop_by_name
from app.services.risk_service import assess_risks
from app.services.finance_service import estimate_finances

router = APIRouter()


@router.post("/analyze")
async def analyze_farm(farm_input: FarmInput, db: Session = Depends(get_db)):
    """
    Complete farm analysis: save farm profile, fetch weather, generate recommendations,
    assess risks, and estimate financials.
    """
    # Resolve coordinates
    lat, lon = resolve_coordinates(
        farm_input.state, farm_input.district,
        farm_input.mandal, farm_input.latitude, farm_input.longitude
    )

    if lat is None or lon is None:
        raise HTTPException(status_code=400, detail="Could not resolve location coordinates. Please check district name.")

    # Save farm profile
    farm_id = generate_uuid()
    farm = FarmProfile(
        id=farm_id,
        farmer_name=farm_input.farmer_name,
        state=farm_input.state,
        district=farm_input.district,
        mandal=farm_input.mandal,
        village=farm_input.village,
        latitude=lat,
        longitude=lon,
        land_area=farm_input.land_area,
        land_unit=farm_input.land_unit,
        soil_type=farm_input.soil_type,
        irrigation_type=farm_input.irrigation_type,
        farming_season=farm_input.farming_season,
        previous_crop=farm_input.previous_crop,
        preferred_crops=json.dumps(farm_input.preferred_crops) if farm_input.preferred_crops else None,
        planned_sowing_date=farm_input.planned_sowing_date,
        budget=farm_input.budget,
        preferred_language=farm_input.preferred_language,
    )
    db.add(farm)

    # Create analysis record
    analysis_id = generate_uuid()
    analysis = FarmAnalysis(
        id=analysis_id,
        farm_id=farm_id,
        status="processing",
    )
    db.add(analysis)
    db.commit()

    try:
        # Step 1: Fetch weather data
        historical = await fetch_historical_weather(lat, lon, years=5)
        current = await fetch_current_weather(lat, lon)
        forecast_data = await fetch_forecast(lat, lon, days=7)

        # Step 2: Compute averages for crop recommendation
        annual_vals = list(historical.get("annual_rainfall", {}).values())
        avg_annual_rainfall = sum(annual_vals) / max(len(annual_vals), 1)

        temp_max_vals = list(historical.get("monthly_avg_temp_max", {}).values())
        temp_min_vals = list(historical.get("monthly_avg_temp_min", {}).values())
        avg_temp_max = sum(temp_max_vals) / max(len(temp_max_vals), 1)
        avg_temp_min = sum(temp_min_vals) / max(len(temp_min_vals), 1)

        forecast_rain = sum(d.get("precipitation", 0) for d in forecast_data.get("forecast", []))

        # Step 3: Crop recommendations
        crop_recs = recommend_crops(
            soil_type=farm_input.soil_type,
            irrigation_type=farm_input.irrigation_type,
            season=farm_input.farming_season,
            avg_annual_rainfall=avg_annual_rainfall,
            avg_temp_max=avg_temp_max,
            avg_temp_min=avg_temp_min,
            forecast_rainfall=forecast_rain,
            preferred_crops=farm_input.preferred_crops,
            top_n=5,
        )

        # Step 4: Risk assessment
        risk_result = assess_risks(
            historical_weather=historical,
            current_weather=current,
            forecast=forecast_data,
            crop=crop_recs[0]["crop_name"] if crop_recs else None,
            season=farm_input.farming_season,
            soil_type=farm_input.soil_type,
        )

        # Step 5: Financial estimate for top crop
        top_crop = crop_recs[0] if crop_recs else None
        finance_result = None
        if top_crop:
            crop_data = get_crop_by_name(top_crop["crop_name"])
            finance_result = estimate_finances(
                crop=top_crop["crop_name"],
                land_area=farm_input.land_area,
                land_unit=farm_input.land_unit,
                crop_data=crop_data,
            )

        # Remove daily_data before storing (too large)
        historical_store = {k: v for k, v in historical.items() if k != "daily_data"}

        # Update analysis
        analysis.weather_data = {
            "historical": historical_store,
            "current": current,
            "forecast": forecast_data,
        }
        analysis.crop_recommendations = crop_recs
        analysis.risk_assessment = risk_result
        analysis.financial_estimates = finance_result
        analysis.data_sources = {
            "weather": historical.get("data_source", "Unknown"),
            "forecast": forecast_data.get("data_source", "Unknown"),
            "crops": "AgriPredict Crop Database + Rule-based scoring",
            "risk": "Rule-based weather risk engine",
            "finance": "Formula-based estimation",
        }
        analysis.status = "completed"
        analysis.completed_at = datetime.utcnow()

        # Build dashboard data
        analysis.dashboard_data = {
            "farm": {
                "district": farm_input.district,
                "state": farm_input.state,
                "land_area": farm_input.land_area,
                "land_unit": farm_input.land_unit,
                "soil_type": farm_input.soil_type,
                "irrigation_type": farm_input.irrigation_type,
                "season": farm_input.farming_season,
            },
            "weather_summary": {
                "avg_annual_rainfall": round(avg_annual_rainfall, 1),
                "current_temp": current.get("temperature"),
                "current_humidity": current.get("humidity"),
                "forecast_days": forecast_data.get("days", 0),
                "data_source": historical.get("data_source"),
            },
            "top_crop": {
                "name": top_crop["crop_name"] if top_crop else "N/A",
                "score": top_crop["suitability_score"] if top_crop else 0,
            } if top_crop else None,
            "top_risk": {
                "category": risk_result["risks"][0]["category"] if risk_result.get("risks") else "N/A",
                "level": risk_result.get("overall_risk", "Unknown"),
            },
            "financial_summary": {
                "total_cost": finance_result.get("total_cultivation_cost", 0) if finance_result else 0,
                "net_return": finance_result.get("estimated_net_return", 0) if finance_result else 0,
                "risk_level": finance_result.get("financial_risk_level", "Unknown") if finance_result else "Unknown",
            },
        }

        db.commit()

        return {
            "id": farm_id,
            "analysis_id": analysis_id,
            "message": "Farm analysis completed successfully",
            "status": "completed",
        }

    except Exception as e:
        analysis.status = "failed"
        db.commit()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get("/sample")
async def get_sample_data():
    """Return sample farm data for hackathon demo."""
    return {
        "farmer_name": "Demo Farmer",
        "state": "Andhra Pradesh",
        "district": "Chittoor",
        "mandal": "Chittoor",
        "land_area": 2,
        "land_unit": "acres",
        "soil_type": "red",
        "irrigation_type": "rainfed",
        "farming_season": "kharif",
        "previous_crop": "Groundnut",
        "preferred_crops": [],
        "planned_sowing_date": "",
        "budget": 50000,
        "preferred_language": "en",
    }
