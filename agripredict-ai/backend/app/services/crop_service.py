"""Crop data and recommendation service."""

import json
from typing import List, Dict, Any, Optional

# Comprehensive crop database for Andhra Pradesh
CROP_DATABASE = [
    {
        "name": "Rice (Paddy)",
        "name_te": "వరి",
        "category": "cereal",
        "seasons": ["kharif", "rabi"],
        "soil_types": ["alluvial", "clayey", "black", "loamy"],
        "min_rainfall_mm": 1000,
        "max_rainfall_mm": 2000,
        "min_temp_c": 20,
        "max_temp_c": 40,
        "optimal_temp_min": 22,
        "optimal_temp_max": 32,
        "water_requirement": "high",
        "crop_duration_days": 120,
        "irrigation_needed": True,
        "typical_yield_per_acre": 20,  # quintals
        "typical_cost_per_acre": 25000,
        "typical_price_per_quintal": 2200,
        "sowing_months": [6, 7, 11, 12],
        "harvest_months": [10, 11, 3, 4],
        "description": "Major cereal crop of AP. Requires standing water for most growth stages.",
    },
    {
        "name": "Groundnut",
        "name_te": "వేరుశెనగ",
        "category": "oilseed",
        "seasons": ["kharif", "rabi"],
        "soil_types": ["red", "sandy", "loamy"],
        "min_rainfall_mm": 500,
        "max_rainfall_mm": 1200,
        "min_temp_c": 20,
        "max_temp_c": 38,
        "optimal_temp_min": 25,
        "optimal_temp_max": 35,
        "water_requirement": "medium",
        "crop_duration_days": 105,
        "irrigation_needed": False,
        "typical_yield_per_acre": 8,
        "typical_cost_per_acre": 18000,
        "typical_price_per_quintal": 5500,
        "sowing_months": [6, 7, 1, 2],
        "harvest_months": [10, 11, 4, 5],
        "description": "Well-suited for red and sandy soils. Important oilseed crop in Rayalaseema.",
    },
    {
        "name": "Cotton",
        "name_te": "పత్తి",
        "category": "commercial",
        "seasons": ["kharif"],
        "soil_types": ["black", "red", "alluvial", "loamy"],
        "min_rainfall_mm": 600,
        "max_rainfall_mm": 1500,
        "min_temp_c": 20,
        "max_temp_c": 42,
        "optimal_temp_min": 25,
        "optimal_temp_max": 35,
        "water_requirement": "medium",
        "crop_duration_days": 165,
        "irrigation_needed": False,
        "typical_yield_per_acre": 8,
        "typical_cost_per_acre": 22000,
        "typical_price_per_quintal": 6500,
        "sowing_months": [6, 7],
        "harvest_months": [11, 12, 1],
        "description": "Major commercial crop. Black soil regions of AP are ideal.",
    },
    {
        "name": "Maize (Corn)",
        "name_te": "మొక్కజొన్న",
        "category": "cereal",
        "seasons": ["kharif", "rabi"],
        "soil_types": ["loamy", "alluvial", "red", "black"],
        "min_rainfall_mm": 500,
        "max_rainfall_mm": 1200,
        "min_temp_c": 18,
        "max_temp_c": 38,
        "optimal_temp_min": 21,
        "optimal_temp_max": 32,
        "water_requirement": "medium",
        "crop_duration_days": 100,
        "irrigation_needed": False,
        "typical_yield_per_acre": 25,
        "typical_cost_per_acre": 15000,
        "typical_price_per_quintal": 2000,
        "sowing_months": [6, 7, 11],
        "harvest_months": [9, 10, 2, 3],
        "description": "Versatile cereal crop grown in many soil types across AP.",
    },
    {
        "name": "Red Gram (Tur Dal)",
        "name_te": "కందులు",
        "category": "pulse",
        "seasons": ["kharif"],
        "soil_types": ["red", "black", "loamy", "sandy"],
        "min_rainfall_mm": 350,
        "max_rainfall_mm": 1000,
        "min_temp_c": 18,
        "max_temp_c": 38,
        "optimal_temp_min": 25,
        "optimal_temp_max": 35,
        "water_requirement": "low",
        "crop_duration_days": 150,
        "irrigation_needed": False,
        "typical_yield_per_acre": 5,
        "typical_cost_per_acre": 12000,
        "typical_price_per_quintal": 7000,
        "sowing_months": [6, 7],
        "harvest_months": [12, 1],
        "description": "Important pulse crop well-suited for dryland farming.",
    },
    {
        "name": "Bengal Gram (Chana)",
        "name_te": "శెనగలు",
        "category": "pulse",
        "seasons": ["rabi"],
        "soil_types": ["black", "loamy", "red"],
        "min_rainfall_mm": 200,
        "max_rainfall_mm": 600,
        "min_temp_c": 10,
        "max_temp_c": 32,
        "optimal_temp_min": 15,
        "optimal_temp_max": 28,
        "water_requirement": "low",
        "crop_duration_days": 100,
        "irrigation_needed": False,
        "typical_yield_per_acre": 6,
        "typical_cost_per_acre": 12000,
        "typical_price_per_quintal": 5500,
        "sowing_months": [10, 11],
        "harvest_months": [2, 3],
        "description": "Major rabi pulse. Requires cool dry weather during growth.",
    },
    {
        "name": "Sunflower",
        "name_te": "పొద్దుతిరుగుడు",
        "category": "oilseed",
        "seasons": ["kharif", "rabi", "zaid"],
        "soil_types": ["black", "red", "loamy", "alluvial"],
        "min_rainfall_mm": 400,
        "max_rainfall_mm": 900,
        "min_temp_c": 18,
        "max_temp_c": 38,
        "optimal_temp_min": 22,
        "optimal_temp_max": 30,
        "water_requirement": "medium",
        "crop_duration_days": 90,
        "irrigation_needed": False,
        "typical_yield_per_acre": 5,
        "typical_cost_per_acre": 14000,
        "typical_price_per_quintal": 5800,
        "sowing_months": [6, 7, 1, 2, 3],
        "harvest_months": [9, 10, 4, 5, 6],
        "description": "Short-duration oilseed crop. Adapts to multiple seasons.",
    },
    {
        "name": "Chilli",
        "name_te": "మిరపకాయ",
        "category": "commercial",
        "seasons": ["kharif", "rabi"],
        "soil_types": ["loamy", "black", "red", "alluvial"],
        "min_rainfall_mm": 500,
        "max_rainfall_mm": 1200,
        "min_temp_c": 18,
        "max_temp_c": 38,
        "optimal_temp_min": 22,
        "optimal_temp_max": 32,
        "water_requirement": "medium",
        "crop_duration_days": 150,
        "irrigation_needed": True,
        "typical_yield_per_acre": 8,
        "typical_cost_per_acre": 35000,
        "typical_price_per_quintal": 12000,
        "sowing_months": [6, 7, 8, 11, 12],
        "harvest_months": [11, 12, 1, 3, 4],
        "description": "Guntur chilli is famous. High-value commercial crop.",
    },
    {
        "name": "Sugarcane",
        "name_te": "చెరకు",
        "category": "commercial",
        "seasons": ["annual"],
        "soil_types": ["alluvial", "loamy", "black", "clayey"],
        "min_rainfall_mm": 1000,
        "max_rainfall_mm": 2500,
        "min_temp_c": 20,
        "max_temp_c": 42,
        "optimal_temp_min": 25,
        "optimal_temp_max": 38,
        "water_requirement": "high",
        "crop_duration_days": 330,
        "irrigation_needed": True,
        "typical_yield_per_acre": 350,  # quintals (cane)
        "typical_cost_per_acre": 50000,
        "typical_price_per_quintal": 300,
        "sowing_months": [1, 2, 3],
        "harvest_months": [12, 1, 2, 3],
        "description": "Long-duration crop requiring consistent water supply.",
    },
    {
        "name": "Tomato",
        "name_te": "టమాట",
        "category": "vegetable",
        "seasons": ["kharif", "rabi"],
        "soil_types": ["red", "loamy", "sandy", "alluvial"],
        "min_rainfall_mm": 400,
        "max_rainfall_mm": 1000,
        "min_temp_c": 15,
        "max_temp_c": 35,
        "optimal_temp_min": 20,
        "optimal_temp_max": 30,
        "water_requirement": "medium",
        "crop_duration_days": 100,
        "irrigation_needed": True,
        "typical_yield_per_acre": 80,
        "typical_cost_per_acre": 40000,
        "typical_price_per_quintal": 1500,
        "sowing_months": [6, 7, 10, 11],
        "harvest_months": [9, 10, 1, 2, 3],
        "description": "High-value vegetable. Price volatile but can give good returns.",
    },
    {
        "name": "Jowar (Sorghum)",
        "name_te": "జొన్న",
        "category": "cereal",
        "seasons": ["kharif", "rabi"],
        "soil_types": ["black", "red", "sandy", "loamy"],
        "min_rainfall_mm": 300,
        "max_rainfall_mm": 900,
        "min_temp_c": 18,
        "max_temp_c": 40,
        "optimal_temp_min": 25,
        "optimal_temp_max": 35,
        "water_requirement": "low",
        "crop_duration_days": 110,
        "irrigation_needed": False,
        "typical_yield_per_acre": 8,
        "typical_cost_per_acre": 10000,
        "typical_price_per_quintal": 2800,
        "sowing_months": [6, 7, 10, 11],
        "harvest_months": [10, 11, 2, 3],
        "description": "Drought-tolerant cereal. Good for dryland/rainfed farming.",
    },
    {
        "name": "Black Gram (Urad)",
        "name_te": "మినుములు",
        "category": "pulse",
        "seasons": ["kharif", "rabi"],
        "soil_types": ["black", "red", "loamy", "alluvial"],
        "min_rainfall_mm": 400,
        "max_rainfall_mm": 900,
        "min_temp_c": 20,
        "max_temp_c": 38,
        "optimal_temp_min": 25,
        "optimal_temp_max": 35,
        "water_requirement": "low",
        "crop_duration_days": 75,
        "irrigation_needed": False,
        "typical_yield_per_acre": 4,
        "typical_cost_per_acre": 10000,
        "typical_price_per_quintal": 7500,
        "sowing_months": [6, 7, 10],
        "harvest_months": [9, 10, 1],
        "description": "Short-duration pulse. Popular in AP for its good market price.",
    },
    {
        "name": "Green Gram (Moong)",
        "name_te": "పెసలు",
        "category": "pulse",
        "seasons": ["kharif", "rabi", "zaid"],
        "soil_types": ["red", "loamy", "sandy", "alluvial"],
        "min_rainfall_mm": 300,
        "max_rainfall_mm": 800,
        "min_temp_c": 20,
        "max_temp_c": 40,
        "optimal_temp_min": 25,
        "optimal_temp_max": 35,
        "water_requirement": "low",
        "crop_duration_days": 65,
        "irrigation_needed": False,
        "typical_yield_per_acre": 3.5,
        "typical_cost_per_acre": 8000,
        "typical_price_per_quintal": 8000,
        "sowing_months": [3, 4, 6, 7],
        "harvest_months": [5, 6, 9, 10],
        "description": "Short-duration, drought-tolerant pulse. Good for intercropping.",
    },
    {
        "name": "Mango",
        "name_te": "మామిడి",
        "category": "fruit",
        "seasons": ["annual"],
        "soil_types": ["red", "loamy", "alluvial", "laterite"],
        "min_rainfall_mm": 500,
        "max_rainfall_mm": 1500,
        "min_temp_c": 15,
        "max_temp_c": 45,
        "optimal_temp_min": 24,
        "optimal_temp_max": 35,
        "water_requirement": "medium",
        "crop_duration_days": 365,
        "irrigation_needed": False,
        "typical_yield_per_acre": 40,
        "typical_cost_per_acre": 30000,
        "typical_price_per_quintal": 3500,
        "sowing_months": [7, 8],
        "harvest_months": [4, 5, 6],
        "description": "Perennial fruit crop. Chittoor and Krishna districts are major producers.",
    },
    {
        "name": "Sesame (Til)",
        "name_te": "నువ్వులు",
        "category": "oilseed",
        "seasons": ["kharif"],
        "soil_types": ["red", "sandy", "loamy"],
        "min_rainfall_mm": 300,
        "max_rainfall_mm": 700,
        "min_temp_c": 22,
        "max_temp_c": 40,
        "optimal_temp_min": 25,
        "optimal_temp_max": 35,
        "water_requirement": "low",
        "crop_duration_days": 85,
        "irrigation_needed": False,
        "typical_yield_per_acre": 3,
        "typical_cost_per_acre": 8000,
        "typical_price_per_quintal": 12000,
        "sowing_months": [6, 7],
        "harvest_months": [9, 10],
        "description": "Drought-tolerant oilseed. Good for dryland farming in Rayalaseema.",
    },
]


def get_all_crops() -> List[Dict]:
    """Return all crops in the database."""
    return CROP_DATABASE


def get_crop_by_name(name: str) -> Optional[Dict]:
    """Find a crop by name (case-insensitive partial match)."""
    name_lower = name.lower()
    for crop in CROP_DATABASE:
        if name_lower in crop["name"].lower():
            return crop
    return None


def compute_crop_suitability(
    crop: Dict,
    soil_type: str,
    irrigation_type: str,
    season: str,
    avg_annual_rainfall: float,
    avg_temp_max: float,
    avg_temp_min: float,
    forecast_rainfall: float = 0,
) -> Dict[str, Any]:
    """
    Compute a suitability score for a crop based on farm conditions.
    This is a transparent, rule-based scoring system.
    """
    score = 0
    max_score = 100
    reasons = []
    risks = []

    # 1. Season match (20 points)
    if season in crop["seasons"] or "annual" in crop["seasons"]:
        score += 20
        reasons.append(f"Suitable for {season} season")
    else:
        reasons.append(f"Not typically grown in {season} season")
        risks.append("Season mismatch")

    # 2. Soil match (20 points)
    soil_lower = soil_type.lower()
    if soil_lower in crop["soil_types"] or soil_lower == "unknown":
        score += 20
        if soil_lower != "unknown":
            reasons.append(f"Well-suited for {soil_type} soil")
        else:
            score -= 5
            reasons.append("Soil type unknown — assuming moderate compatibility")
    else:
        score += 5  # Partial credit
        reasons.append(f"Not ideal for {soil_type} soil, but may grow with management")
        risks.append("Soil may not be optimal")

    # 3. Rainfall match (25 points)
    total_rainfall = avg_annual_rainfall
    if crop["min_rainfall_mm"] <= total_rainfall <= crop["max_rainfall_mm"]:
        score += 25
        reasons.append(f"Rainfall ({total_rainfall:.0f}mm) is within suitable range ({crop['min_rainfall_mm']}-{crop['max_rainfall_mm']}mm)")
    elif total_rainfall < crop["min_rainfall_mm"]:
        deficit = crop["min_rainfall_mm"] - total_rainfall
        partial = max(0, 25 - int(deficit / 50))
        score += partial
        reasons.append(f"Rainfall ({total_rainfall:.0f}mm) is below minimum ({crop['min_rainfall_mm']}mm)")
        risks.append("Insufficient rainfall without irrigation")
    else:
        excess = total_rainfall - crop["max_rainfall_mm"]
        partial = max(0, 25 - int(excess / 100))
        score += partial
        reasons.append(f"Rainfall ({total_rainfall:.0f}mm) exceeds maximum ({crop['max_rainfall_mm']}mm)")
        risks.append("Excess rainfall may cause waterlogging")

    # 4. Temperature match (20 points)
    temp_ok = True
    if avg_temp_max > crop["max_temp_c"] + 3:
        score += 5
        reasons.append(f"Temperature may be too high (max {avg_temp_max:.1f}°C)")
        risks.append("High temperature stress")
        temp_ok = False
    elif avg_temp_min < crop["min_temp_c"] - 3:
        score += 5
        reasons.append(f"Temperature may be too low (min {avg_temp_min:.1f}°C)")
        risks.append("Cold stress risk")
        temp_ok = False

    if temp_ok:
        if crop["optimal_temp_min"] <= avg_temp_max <= crop["optimal_temp_max"]:
            score += 20
            reasons.append(f"Temperature range is optimal ({avg_temp_min:.1f}-{avg_temp_max:.1f}°C)")
        else:
            score += 12
            reasons.append(f"Temperature is acceptable but not optimal")

    # 5. Irrigation match (15 points)
    is_irrigated = irrigation_type not in ["rainfed"]
    if crop["irrigation_needed"] and not is_irrigated:
        score += 3
        reasons.append("This crop typically needs irrigation, but farm is rain-fed")
        risks.append("Irrigation required but not available")
    elif crop["irrigation_needed"] and is_irrigated:
        score += 15
        reasons.append("Irrigation available as needed by crop")
    elif not crop["irrigation_needed"]:
        score += 15
        reasons.append("Crop can grow without irrigation")
        if is_irrigated:
            reasons.append("Available irrigation is a bonus for yield improvement")

    # Normalize
    suitability = min(100, max(0, score))

    # Confidence based on data availability
    confidence = "medium"
    if suitability >= 70:
        confidence = "high"
    elif suitability < 40:
        confidence = "low"

    # Sowing recommendation
    season_months = {
        "kharif": [6, 7, 8, 9, 10],
        "rabi": [10, 11, 12, 1, 2],
        "zaid": [3, 4, 5],
        "annual": list(range(1, 13)),
    }
    sowing_months = [m for m in crop.get("sowing_months", []) if m in season_months.get(season, list(range(1, 13)))]
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    sowing_window = ", ".join([month_names[m - 1] for m in sowing_months]) if sowing_months else "Consult local calendar"

    return {
        "crop_name": crop["name"],
        "crop_name_te": crop.get("name_te", ""),
        "suitability_score": suitability,
        "season": season,
        "suitable_soils": crop["soil_types"],
        "water_requirement": crop["water_requirement"],
        "crop_duration_days": crop["crop_duration_days"],
        "major_risks": risks if risks else ["No major risks identified"],
        "expected_yield_range": f"{crop['typical_yield_per_acre'] * 0.7:.1f} - {crop['typical_yield_per_acre'] * 1.2:.1f} quintals/acre" if crop["typical_yield_per_acre"] else None,
        "recommended_sowing": sowing_window,
        "reason": ". ".join(reasons),
        "confidence": confidence,
        "typical_cost_per_acre": crop.get("typical_cost_per_acre"),
        "typical_price_per_quintal": crop.get("typical_price_per_quintal"),
        "typical_yield_per_acre": crop.get("typical_yield_per_acre"),
        "category": crop.get("category"),
        "description": crop.get("description"),
    }


def recommend_crops(
    soil_type: str,
    irrigation_type: str,
    season: str,
    avg_annual_rainfall: float,
    avg_temp_max: float,
    avg_temp_min: float,
    forecast_rainfall: float = 0,
    preferred_crops: Optional[List[str]] = None,
    top_n: int = 5,
) -> List[Dict[str, Any]]:
    """Recommend top N crops based on farm conditions."""
    results = []

    for crop in CROP_DATABASE:
        result = compute_crop_suitability(
            crop, soil_type, irrigation_type, season,
            avg_annual_rainfall, avg_temp_max, avg_temp_min, forecast_rainfall
        )
        results.append(result)

    # Sort by suitability score
    results.sort(key=lambda x: x["suitability_score"], reverse=True)

    # Rank and add alternatives
    top_results = []
    for i, r in enumerate(results[:top_n]):
        r["rank"] = i + 1
        # Add alternatives from remaining
        alt_names = [x["crop_name"] for x in results[top_n:top_n + 3]]
        r["alternatives"] = alt_names
        top_results.append(r)

    return top_results
