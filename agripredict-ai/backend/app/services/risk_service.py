"""Weather risk assessment service."""

from typing import Dict, Any, List, Optional
from datetime import datetime


def assess_risks(
    historical_weather: Dict[str, Any],
    current_weather: Dict[str, Any],
    forecast: Dict[str, Any],
    crop: Optional[str] = None,
    season: str = "kharif",
    soil_type: str = "unknown",
) -> Dict[str, Any]:
    """
    Assess weather-related agricultural risks using historical, current, and forecast data.
    Uses a rule-based engine with configurable thresholds.
    """
    risks = []

    # Extract historical stats
    annual_rainfall = historical_weather.get("annual_rainfall", {})
    avg_annual = sum(annual_rainfall.values()) / max(len(annual_rainfall), 1)
    heavy_rain_days = historical_weather.get("heavy_rain_days_per_year", {})
    avg_heavy_days = sum(heavy_rain_days.values()) / max(len(heavy_rain_days), 1)
    consec_dry = historical_weather.get("max_consecutive_dry_days", {})
    avg_dry_spell = sum(consec_dry.values()) / max(len(consec_dry), 1)

    monthly_rainfall = historical_weather.get("monthly_avg_rainfall", {})
    monthly_temp_max = historical_weather.get("monthly_avg_temp_max", {})

    # Extract forecast stats
    forecast_days = forecast.get("forecast", [])
    forecast_total_rain = sum(d.get("precipitation", 0) for d in forecast_days)
    forecast_max_rain = max((d.get("precipitation", 0) for d in forecast_days), default=0)
    forecast_max_temp = max((d.get("temp_max", 0) for d in forecast_days), default=0)
    forecast_min_temp = min((d.get("temp_min", 50) for d in forecast_days), default=20)

    # Season months for context
    season_months = {
        "kharif": ["06", "07", "08", "09", "10"],
        "rabi": ["11", "12", "01", "02", "03"],
        "zaid": ["03", "04", "05", "06"],
        "annual": [f"{m:02d}" for m in range(1, 13)],
    }
    relevant_months = season_months.get(season, season_months["kharif"])

    # ============ Risk 1: Heavy Rainfall ============
    heavy_level = "Low"
    heavy_indicators = []
    if avg_heavy_days > 10:
        heavy_level = "High"
        heavy_indicators.append(f"Average {avg_heavy_days:.0f} heavy rain days/year historically")
    elif avg_heavy_days > 5:
        heavy_level = "Moderate"
        heavy_indicators.append(f"Average {avg_heavy_days:.0f} heavy rain days/year historically")
    else:
        heavy_indicators.append(f"Average {avg_heavy_days:.0f} heavy rain days/year (relatively low)")

    if forecast_max_rain > 50:
        heavy_level = "High"
        heavy_indicators.append(f"Forecast shows {forecast_max_rain:.0f}mm rain expected on a single day")
    elif forecast_max_rain > 20:
        if heavy_level != "High":
            heavy_level = "Moderate"
        heavy_indicators.append(f"Forecast shows {forecast_max_rain:.0f}mm maximum daily rain")

    risks.append({
        "category": "Heavy Rainfall",
        "level": heavy_level,
        "time_period": f"{season.capitalize()} season",
        "indicators": heavy_indicators,
        "explanation": _get_explanation("heavy_rainfall", heavy_level),
        "impact": "Heavy rainfall can damage standing crops, cause lodging, and delay harvesting. Waterlogged fields reduce root health.",
        "preventive_actions": [
            "Ensure proper field drainage channels",
            "Avoid sowing in low-lying areas prone to flooding",
            "Consider raised-bed planting if available",
            "Monitor weather forecasts regularly",
        ],
        "data_basis": "historical + forecast",
    })

    # ============ Risk 2: Waterlogging / Flooding ============
    flood_level = "Low"
    flood_indicators = []
    season_rainfall = sum(monthly_rainfall.get(m, 0) for m in relevant_months)

    if season_rainfall > 800 and soil_type in ["clayey", "black"]:
        flood_level = "High"
        flood_indicators.append(f"Season rainfall ~{season_rainfall:.0f}mm on {soil_type} soil (poor drainage)")
    elif season_rainfall > 600:
        flood_level = "Moderate"
        flood_indicators.append(f"Season rainfall ~{season_rainfall:.0f}mm may cause temporary waterlogging")
    else:
        flood_indicators.append(f"Season rainfall ~{season_rainfall:.0f}mm - waterlogging risk is low")

    risks.append({
        "category": "Waterlogging / Flooding",
        "level": flood_level,
        "time_period": f"{season.capitalize()} season",
        "indicators": flood_indicators,
        "explanation": _get_explanation("waterlogging", flood_level),
        "impact": "Waterlogging deprives roots of oxygen, leading to root rot and yield loss. Clayey and black soils are more prone.",
        "preventive_actions": [
            "Create drainage channels around the field",
            "Choose flood-tolerant crop varieties if available",
            "Avoid heavy irrigation during rainy periods",
            "Consider bunding to prevent excess water entry",
        ],
        "data_basis": "historical + soil assessment",
    })

    # ============ Risk 3: Drought / Dry Spell ============
    drought_level = "Low"
    drought_indicators = []

    if avg_dry_spell > 30:
        drought_level = "High"
        drought_indicators.append(f"Historical dry spells average {avg_dry_spell:.0f} consecutive days")
    elif avg_dry_spell > 15:
        drought_level = "Moderate"
        drought_indicators.append(f"Historical dry spells average {avg_dry_spell:.0f} consecutive days")
    else:
        drought_indicators.append(f"Historical dry spells average {avg_dry_spell:.0f} days (manageable)")

    if avg_annual < 500:
        drought_level = "High"
        drought_indicators.append(f"Average annual rainfall only {avg_annual:.0f}mm (low)")

    risks.append({
        "category": "Drought / Dry Spell",
        "level": drought_level,
        "time_period": f"{season.capitalize()} season",
        "indicators": drought_indicators,
        "explanation": _get_explanation("drought", drought_level),
        "impact": "Prolonged dry spells reduce soil moisture, stunt crop growth, and can cause complete crop failure in rain-fed areas.",
        "preventive_actions": [
            "Invest in drip or supplemental irrigation if possible",
            "Choose drought-tolerant crop varieties",
            "Practice mulching to retain soil moisture",
            "Plan sowing after confirmed monsoon onset",
        ],
        "data_basis": "historical",
    })

    # ============ Risk 4: High Temperature Stress ============
    heat_level = "Low"
    heat_indicators = []

    hot_months = [monthly_temp_max.get(m, 0) for m in relevant_months]
    max_season_temp = max(hot_months) if hot_months else 35

    if max_season_temp > 42:
        heat_level = "High"
        heat_indicators.append(f"Historical peak temperature reaches {max_season_temp:.1f}°C")
    elif max_season_temp > 38:
        heat_level = "Moderate"
        heat_indicators.append(f"Historical peak temperature reaches {max_season_temp:.1f}°C")
    else:
        heat_indicators.append(f"Historical peak temperature is {max_season_temp:.1f}°C (acceptable)")

    if forecast_max_temp > 40:
        heat_level = "High"
        heat_indicators.append(f"Forecast shows temperature up to {forecast_max_temp:.1f}°C")

    risks.append({
        "category": "High Temperature Stress",
        "level": heat_level,
        "time_period": f"{season.capitalize()} season",
        "indicators": heat_indicators,
        "explanation": _get_explanation("heat_stress", heat_level),
        "impact": "High temperatures above 38°C can cause flower drop, pollen sterility, and reduced grain filling in many crops.",
        "preventive_actions": [
            "Provide shade nets for sensitive crops",
            "Increase irrigation frequency during heat waves",
            "Apply mulch to reduce soil temperature",
            "Consider heat-tolerant varieties",
        ],
        "data_basis": "historical + forecast",
    })

    # ============ Risk 5: Unfavorable Sowing Conditions ============
    sow_level = "Low"
    sow_indicators = []

    # Check if sowing period has adequate moisture
    sow_months = relevant_months[:2] if relevant_months else ["06", "07"]
    sow_rain = sum(monthly_rainfall.get(m, 0) for m in sow_months)

    if sow_rain < 50:
        sow_level = "High"
        sow_indicators.append(f"Sowing period rainfall ~{sow_rain:.0f}mm (very low for germination)")
    elif sow_rain < 100:
        sow_level = "Moderate"
        sow_indicators.append(f"Sowing period rainfall ~{sow_rain:.0f}mm (may need irrigation)")
    else:
        sow_indicators.append(f"Sowing period rainfall ~{sow_rain:.0f}mm (adequate)")

    risks.append({
        "category": "Unfavorable Sowing Conditions",
        "level": sow_level,
        "time_period": "Sowing period",
        "indicators": sow_indicators,
        "explanation": _get_explanation("sowing", sow_level),
        "impact": "Insufficient moisture at sowing time can lead to poor germination and uneven crop stand.",
        "preventive_actions": [
            "Wait for confirmed adequate moisture before sowing",
            "Pre-irrigate the field if possible",
            "Use seed treatment for better germination",
            "Sow at the recommended depth for moisture retention",
        ],
        "data_basis": "historical",
    })

    # ============ Risk 6: Harvest Period Risk ============
    harvest_level = "Low"
    harvest_indicators = []

    harvest_months = relevant_months[-2:] if len(relevant_months) >= 2 else relevant_months
    harvest_rain = sum(monthly_rainfall.get(m, 0) for m in harvest_months)

    if harvest_rain > 200:
        harvest_level = "High"
        harvest_indicators.append(f"Harvest period rainfall ~{harvest_rain:.0f}mm (may damage ripe crops)")
    elif harvest_rain > 100:
        harvest_level = "Moderate"
        harvest_indicators.append(f"Harvest period rainfall ~{harvest_rain:.0f}mm (plan harvest timing carefully)")
    else:
        harvest_indicators.append(f"Harvest period rainfall ~{harvest_rain:.0f}mm (favorable)")

    risks.append({
        "category": "Harvest Period Weather Risk",
        "level": harvest_level,
        "time_period": "Harvest period",
        "indicators": harvest_indicators,
        "explanation": _get_explanation("harvest", harvest_level),
        "impact": "Rain during harvest can cause grain spoilage, reduce quality, and increase post-harvest losses.",
        "preventive_actions": [
            "Plan harvest date based on weather forecast",
            "Arrange drying facilities in advance",
            "Consider early-maturing varieties to avoid late-season rain",
            "Harvest in stages if possible",
        ],
        "data_basis": "historical",
    })

    # Overall risk
    levels = [r["level"] for r in risks]
    if levels.count("High") >= 2:
        overall = "High"
    elif "High" in levels or levels.count("Moderate") >= 3:
        overall = "Moderate-High"
    elif "Moderate" in levels:
        overall = "Moderate"
    else:
        overall = "Low"

    return {
        "overall_risk": overall,
        "risks": risks,
        "assessed_at": datetime.now().isoformat(),
        "data_sources": [
            historical_weather.get("data_source", "Unknown"),
            forecast.get("data_source", "Unknown"),
            "Rule-based assessment engine",
        ],
    }


def _get_explanation(risk_type: str, level: str) -> str:
    """Get human-readable risk explanation."""
    explanations = {
        "heavy_rainfall": {
            "High": "Historical data and/or forecasts indicate significant heavy rainfall events. Fields may experience damage during intense rain episodes.",
            "Moderate": "Moderate heavy rainfall is expected based on historical patterns. Some precautions are advisable.",
            "Low": "Heavy rainfall risk appears low based on available data. Normal precautions should suffice.",
        },
        "waterlogging": {
            "High": "The combination of expected rainfall and soil type creates a high risk of waterlogging. Drainage preparation is strongly recommended.",
            "Moderate": "Some waterlogging risk exists. Monitoring drainage conditions is advisable.",
            "Low": "Waterlogging risk is low based on rainfall and soil conditions.",
        },
        "drought": {
            "High": "Historical data shows frequent and prolonged dry spells. Irrigation or drought-tolerant crops are strongly recommended.",
            "Moderate": "Occasional dry spells are observed historically. Supplemental irrigation may be needed.",
            "Low": "Adequate rainfall is expected. Drought risk appears manageable.",
        },
        "heat_stress": {
            "High": "Temperatures may exceed safe limits for many crops. Heat management practices are essential.",
            "Moderate": "Temperatures may occasionally stress crops. Monitor weather and provide water during heat events.",
            "Low": "Temperature conditions appear favorable for most crops.",
        },
        "sowing": {
            "High": "Sowing conditions may be unfavorable due to insufficient moisture. Consider irrigation or delayed sowing.",
            "Moderate": "Sowing conditions are uncertain. Monitor moisture levels before planting.",
            "Low": "Sowing conditions appear favorable based on historical moisture patterns.",
        },
        "harvest": {
            "High": "Harvest period may coincide with significant rainfall. Plan harvest timing carefully.",
            "Moderate": "Some rain during harvest is possible. Arrange drying and storage in advance.",
            "Low": "Harvest period weather conditions appear favorable.",
        },
    }
    return explanations.get(risk_type, {}).get(level, "Assessment based on available data.")
