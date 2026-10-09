"""Weather service using Open-Meteo API with demo data fallback."""

import httpx
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from app.config import settings

OPEN_METEO_HISTORICAL = f"{settings.OPEN_METEO_BASE_URL}/archive"
OPEN_METEO_FORECAST = f"{settings.OPEN_METEO_BASE_URL}/forecast"


async def fetch_current_weather(lat: float, lon: float) -> Dict[str, Any]:
    """Fetch current weather from Open-Meteo."""
    try:
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m,weather_code",
            "timezone": "Asia/Kolkata",
        }
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(OPEN_METEO_FORECAST, params=params)
            if resp.status_code == 200:
                data = resp.json()
                current = data.get("current", {})
                return {
                    "temperature": current.get("temperature_2m"),
                    "humidity": current.get("relative_humidity_2m"),
                    "precipitation": current.get("precipitation"),
                    "wind_speed": current.get("wind_speed_10m"),
                    "weather_code": current.get("weather_code"),
                    "description": _weather_code_desc(current.get("weather_code")),
                    "fetched_at": datetime.now().isoformat(),
                    "is_demo": False,
                }
    except Exception as e:
        print(f"[WARN] Current weather fetch failed: {e}")

    return _demo_current_weather()


async def fetch_forecast(lat: float, lon: float, days: int = 7) -> Dict[str, Any]:
    """Fetch weather forecast from Open-Meteo."""
    try:
        params = {
            "latitude": lat,
            "longitude": lon,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max",
            "timezone": "Asia/Kolkata",
            "forecast_days": min(days, 16),
        }
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(OPEN_METEO_FORECAST, params=params)
            if resp.status_code == 200:
                data = resp.json()
                daily = data.get("daily", {})
                dates = daily.get("time", [])
                result = []
                for i, date in enumerate(dates):
                    result.append({
                        "date": date,
                        "temp_max": _safe_get(daily, "temperature_2m_max", i),
                        "temp_min": _safe_get(daily, "temperature_2m_min", i),
                        "precipitation": _safe_get(daily, "precipitation_sum", i),
                        "precip_probability": _safe_get(daily, "precipitation_probability_max", i),
                        "wind_speed_max": _safe_get(daily, "wind_speed_10m_max", i),
                    })
                return {
                    "forecast": result,
                    "days": len(result),
                    "data_source": "Open-Meteo Forecast API",
                    "is_demo": False,
                }
    except Exception as e:
        print(f"[WARN] Forecast fetch failed: {e}")

    return _demo_forecast(days)


async def fetch_historical_weather(lat: float, lon: float, years: int = 5) -> Dict[str, Any]:
    """Fetch historical weather data from Open-Meteo Archive API."""
    today = datetime.now()
    all_daily = []
    annual_rainfall = {}
    monthly_rainfall = {}
    monthly_temp_max = {}
    monthly_temp_min = {}
    heavy_rain_days = {}
    data_source = "Open-Meteo Archive API"
    is_demo = False

    for year_offset in range(1, years + 1):
        year = today.year - year_offset
        start = f"{year}-01-01"
        end = f"{year}-12-31"

        try:
            params = {
                "latitude": lat,
                "longitude": lon,
                "start_date": start,
                "end_date": end,
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,relative_humidity_2m_mean",
                "timezone": "Asia/Kolkata",
            }
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.get(OPEN_METEO_HISTORICAL, params=params)
                if resp.status_code == 200:
                    data = resp.json()
                    daily = data.get("daily", {})
                    dates = daily.get("time", [])

                    year_rainfall = 0
                    year_heavy_days = 0

                    for i, date in enumerate(dates):
                        precip = _safe_get(daily, "precipitation_sum", i) or 0
                        t_max = _safe_get(daily, "temperature_2m_max", i)
                        t_min = _safe_get(daily, "temperature_2m_min", i)
                        humidity = _safe_get(daily, "relative_humidity_2m_mean", i)

                        month = date[5:7]  # "MM"

                        year_rainfall += precip
                        if precip >= 64.5:  # IMD heavy rainfall threshold
                            year_heavy_days += 1

                        # Monthly accumulation
                        month_key = f"{year}-{month}"
                        monthly_rainfall[month_key] = monthly_rainfall.get(month_key, 0) + precip
                        if t_max is not None:
                            monthly_temp_max.setdefault(month_key, []).append(t_max)
                        if t_min is not None:
                            monthly_temp_min.setdefault(month_key, []).append(t_min)

                        all_daily.append({
                            "date": date,
                            "precipitation": precip,
                            "temp_max": t_max,
                            "temp_min": t_min,
                            "humidity": humidity,
                        })

                    annual_rainfall[str(year)] = round(year_rainfall, 1)
                    heavy_rain_days[str(year)] = year_heavy_days
                    continue
        except Exception as e:
            print(f"[WARN] Historical data for {year} failed: {e}")

        # If API failed for this year, fall back to demo
        is_demo = True
        demo = _demo_year_data(year, lat, lon)
        all_daily.extend(demo["daily"])
        annual_rainfall[str(year)] = demo["annual_rainfall"]
        heavy_rain_days[str(year)] = demo["heavy_rain_days"]
        for mk, mv in demo["monthly_rainfall"].items():
            monthly_rainfall[mk] = mv
        for mk, mv in demo["monthly_temp_max"].items():
            monthly_temp_max[mk] = mv
        for mk, mv in demo["monthly_temp_min"].items():
            monthly_temp_min[mk] = mv

    if is_demo:
        data_source = "Open-Meteo Archive API + Demo fallback"

    # Compute monthly averages
    month_names = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    avg_monthly_rainfall = {}
    avg_monthly_temp_max = {}
    avg_monthly_temp_min = {}

    for m in month_names:
        rain_vals = [v for k, v in monthly_rainfall.items() if k.endswith(f"-{m}")]
        avg_monthly_rainfall[m] = round(sum(rain_vals) / len(rain_vals), 1) if rain_vals else 0

        tmax_vals = []
        for k, v in monthly_temp_max.items():
            if k.endswith(f"-{m}"):
                tmax_vals.extend(v)
        avg_monthly_temp_max[m] = round(sum(tmax_vals) / len(tmax_vals), 1) if tmax_vals else 0

        tmin_vals = []
        for k, v in monthly_temp_min.items():
            if k.endswith(f"-{m}"):
                tmin_vals.extend(v)
        avg_monthly_temp_min[m] = round(sum(tmin_vals) / len(tmin_vals), 1) if tmin_vals else 0

    # Compute max consecutive dry days per year
    consec_dry = {}
    for year_str in annual_rainfall.keys():
        year_daily = [d for d in all_daily if d["date"].startswith(year_str)]
        max_dry = 0
        current_dry = 0
        for d in sorted(year_daily, key=lambda x: x["date"]):
            if (d.get("precipitation") or 0) < 2.5:
                current_dry += 1
                max_dry = max(max_dry, current_dry)
            else:
                current_dry = 0
        consec_dry[year_str] = max_dry

    return {
        "years_analyzed": sorted([int(y) for y in annual_rainfall.keys()]),
        "annual_rainfall": annual_rainfall,
        "monthly_avg_rainfall": avg_monthly_rainfall,
        "monthly_avg_temp_max": avg_monthly_temp_max,
        "monthly_avg_temp_min": avg_monthly_temp_min,
        "heavy_rain_days_per_year": heavy_rain_days,
        "max_consecutive_dry_days": consec_dry,
        "total_data_points": len(all_daily),
        "data_source": data_source,
        "daily_data": all_daily,
    }


def _safe_get(data: dict, key: str, index: int):
    """Safely get a value from a list in a dict."""
    lst = data.get(key, [])
    if lst and index < len(lst):
        return lst[index]
    return None


def _weather_code_desc(code: int) -> str:
    """Convert WMO weather code to description."""
    codes = {
        0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Foggy", 48: "Depositing rime fog",
        51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        71: "Slight snowfall", 73: "Moderate snowfall", 75: "Heavy snowfall",
        80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
        95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Thunderstorm with heavy hail",
    }
    return codes.get(code, "Unknown") if code is not None else "Unknown"


def _demo_current_weather() -> Dict[str, Any]:
    """Generate demo current weather data."""
    return {
        "temperature": 31.2,
        "humidity": 68,
        "precipitation": 0.0,
        "wind_speed": 8.5,
        "weather_code": 2,
        "description": "Partly cloudy",
        "fetched_at": datetime.now().isoformat(),
        "is_demo": True,
    }


def _demo_forecast(days: int = 7) -> Dict[str, Any]:
    """Generate demo forecast data."""
    import random
    random.seed(42)
    forecast = []
    base = datetime.now()
    for i in range(days):
        day = base + timedelta(days=i)
        forecast.append({
            "date": day.strftime("%Y-%m-%d"),
            "temp_max": round(30 + random.uniform(-3, 5), 1),
            "temp_min": round(22 + random.uniform(-2, 3), 1),
            "precipitation": round(random.choice([0, 0, 0, 2.5, 8, 15, 25, 0, 1, 5]), 1),
            "precip_probability": random.randint(10, 80),
            "wind_speed_max": round(random.uniform(5, 20), 1),
        })
    return {
        "forecast": forecast,
        "days": len(forecast),
        "data_source": "Demo Data (illustrative)",
        "is_demo": True,
    }


def _demo_year_data(year: int, lat: float, lon: float) -> Dict[str, Any]:
    """Generate demo historical data for one year."""
    import random
    import math
    random.seed(year * 100 + int(lat * 10))

    daily = []
    monthly_rainfall = {}
    monthly_temp_max = {}
    monthly_temp_min = {}
    annual_rain = 0
    heavy_days = 0

    # Seasonal pattern: monsoon heavy Jun-Oct
    for month in range(1, 13):
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1]
        if month == 2 and year % 4 == 0:
            days_in_month = 29

        month_key = f"{year}-{month:02d}"
        month_rain = 0
        month_tmax = []
        month_tmin = []

        # Monsoon factor
        is_monsoon = month in [6, 7, 8, 9, 10]
        base_rain = 12 if is_monsoon else 1.5
        base_temp_max = 32 if is_monsoon else 35
        base_temp_min = 23 if is_monsoon else 18

        if month in [12, 1, 2]:
            base_temp_max = 30
            base_temp_min = 16

        for day in range(1, days_in_month + 1):
            rain = max(0, round(random.expovariate(1 / base_rain), 1))
            if not is_monsoon and random.random() > 0.3:
                rain = 0
            t_max = round(base_temp_max + random.uniform(-3, 3), 1)
            t_min = round(base_temp_min + random.uniform(-2, 2), 1)
            humidity = round(65 + random.uniform(-15, 15) + (10 if is_monsoon else 0), 1)

            daily.append({
                "date": f"{year}-{month:02d}-{day:02d}",
                "precipitation": rain,
                "temp_max": t_max,
                "temp_min": t_min,
                "humidity": min(100, max(20, humidity)),
            })

            month_rain += rain
            annual_rain += rain
            month_tmax.append(t_max)
            month_tmin.append(t_min)
            if rain >= 64.5:
                heavy_days += 1

        monthly_rainfall[month_key] = round(month_rain, 1)
        monthly_temp_max[month_key] = month_tmax
        monthly_temp_min[month_key] = month_tmin

    return {
        "daily": daily,
        "annual_rainfall": round(annual_rain, 1),
        "heavy_rain_days": heavy_days,
        "monthly_rainfall": monthly_rainfall,
        "monthly_temp_max": monthly_temp_max,
        "monthly_temp_min": monthly_temp_min,
    }
