"""Financial estimation service for agricultural planning."""

from typing import Dict, Any, List, Optional


def estimate_finances(
    crop: str,
    land_area: float,
    land_unit: str,
    seed_cost: float = 0,
    fertilizer_cost: float = 0,
    pesticide_cost: float = 0,
    labor_cost: float = 0,
    irrigation_cost: float = 0,
    machinery_cost: float = 0,
    transport_cost: float = 0,
    other_expenses: float = 0,
    expected_yield_per_acre: Optional[float] = None,
    expected_price_per_quintal: Optional[float] = None,
    harvest_expenses: float = 0,
    crop_data: Optional[Dict] = None,
) -> Dict[str, Any]:
    """
    Estimate cultivation cost, revenue, and profit/loss with scenario analysis.
    All financial outputs are estimates. Actual results depend on many factors.
    """

    # Convert hectares to acres if needed
    area_in_acres = land_area
    if land_unit == "hectares":
        area_in_acres = land_area * 2.47105

    # Use crop_data defaults if available and user hasn't provided values
    yield_per_acre = expected_yield_per_acre
    price_per_quintal = expected_price_per_quintal

    if crop_data:
        if yield_per_acre is None or yield_per_acre == 0:
            yield_per_acre = crop_data.get("typical_yield_per_acre", 10)
        if price_per_quintal is None or price_per_quintal == 0:
            price_per_quintal = crop_data.get("typical_price_per_quintal", 2000)

        # Fill in missing cost components with estimates
        typical_cost = crop_data.get("typical_cost_per_acre", 15000)
        if seed_cost == 0 and fertilizer_cost == 0 and labor_cost == 0:
            # Distribute typical cost across categories
            seed_cost = typical_cost * 0.15
            fertilizer_cost = typical_cost * 0.25
            pesticide_cost = typical_cost * 0.10
            labor_cost = typical_cost * 0.30
            irrigation_cost = typical_cost * 0.05
            machinery_cost = typical_cost * 0.10
            transport_cost = typical_cost * 0.03
            other_expenses = typical_cost * 0.02

    # Ensure we have valid values
    yield_per_acre = yield_per_acre or 10
    price_per_quintal = price_per_quintal or 2000

    # Per-acre costs
    per_acre_costs = {
        "seed_cost": seed_cost,
        "fertilizer_cost": fertilizer_cost,
        "pesticide_cost": pesticide_cost,
        "labor_cost": labor_cost,
        "irrigation_cost": irrigation_cost,
        "machinery_cost": machinery_cost,
        "transport_cost": transport_cost,
        "other_expenses": other_expenses,
        "harvest_expenses": harvest_expenses,
    }

    # Total costs (per acre × area)
    total_per_acre_cost = sum(per_acre_costs.values())
    total_cultivation_cost = total_per_acre_cost * area_in_acres

    # Expected production and revenue
    expected_total_yield = yield_per_acre * area_in_acres  # quintals
    expected_gross_revenue = expected_total_yield * price_per_quintal

    # Net return
    estimated_net_return = expected_gross_revenue - total_cultivation_cost
    estimated_loss = max(0, -estimated_net_return)

    # Break-even price
    break_even_price = total_cultivation_cost / max(expected_total_yield, 0.01)

    # Return per acre
    return_per_acre = estimated_net_return / max(area_in_acres, 0.01)

    # Scenario analysis
    scenarios = _generate_scenarios(
        total_cultivation_cost, yield_per_acre, price_per_quintal,
        area_in_acres, per_acre_costs
    )

    # Financial risk level
    if estimated_net_return < 0:
        financial_risk_level = "High"
    elif return_per_acre < 5000:
        financial_risk_level = "Moderate-High"
    elif return_per_acre < 15000:
        financial_risk_level = "Moderate"
    else:
        financial_risk_level = "Low"

    return {
        "crop": crop,
        "land_area": land_area,
        "land_unit": land_unit,
        "area_in_acres": round(area_in_acres, 2),
        "cost_breakdown": {k: round(v * area_in_acres, 2) for k, v in per_acre_costs.items()},
        "total_cultivation_cost": round(total_cultivation_cost, 2),
        "expected_yield_per_acre": round(yield_per_acre, 2),
        "expected_total_yield": round(expected_total_yield, 2),
        "expected_price_per_quintal": round(price_per_quintal, 2),
        "expected_gross_revenue": round(expected_gross_revenue, 2),
        "estimated_net_return": round(estimated_net_return, 2),
        "estimated_loss": round(estimated_loss, 2),
        "break_even_price": round(break_even_price, 2),
        "return_per_acre": round(return_per_acre, 2),
        "scenarios": scenarios,
        "financial_risk_level": financial_risk_level,
        "disclaimer": "All financial estimates are approximate and based on typical values and user inputs. "
                      "Actual results depend on crop management, weather conditions, actual yield, "
                      "market prices at time of sale, and many other factors. "
                      "These figures are intended to support planning, not guarantee outcomes.",
    }


def _generate_scenarios(
    total_cost: float,
    yield_per_acre: float,
    price_per_quintal: float,
    area_in_acres: float,
    per_acre_costs: Dict[str, float],
) -> List[Dict[str, Any]]:
    """Generate best, normal, and worst case scenarios."""
    scenarios = []

    configs = [
        {"name": "Best Case (Good Weather)", "yield_factor": 1.2, "price_factor": 1.15},
        {"name": "Normal Case", "yield_factor": 1.0, "price_factor": 1.0},
        {"name": "Below Average (Moderate Stress)", "yield_factor": 0.75, "price_factor": 0.90},
        {"name": "Poor Case (Heavy Rainfall / Drought)", "yield_factor": 0.5, "price_factor": 0.80},
        {"name": "Severe Loss (Crop Failure)", "yield_factor": 0.15, "price_factor": 0.70},
    ]

    for config in configs:
        adj_yield = yield_per_acre * config["yield_factor"]
        adj_price = price_per_quintal * config["price_factor"]
        total_production = adj_yield * area_in_acres
        revenue = total_production * adj_price
        net = revenue - total_cost
        rpa = net / max(area_in_acres, 0.01)

        if net < -total_cost * 0.3:
            risk = "High"
        elif net < 0:
            risk = "Moderate-High"
        elif rpa < 10000:
            risk = "Moderate"
        else:
            risk = "Low"

        scenarios.append({
            "scenario": config["name"],
            "yield_factor": config["yield_factor"],
            "price_factor": config["price_factor"],
            "total_cost": round(total_cost, 2),
            "expected_yield": round(total_production, 2),
            "expected_revenue": round(revenue, 2),
            "net_return": round(net, 2),
            "return_per_acre": round(rpa, 2),
            "risk_level": risk,
        })

    return scenarios
