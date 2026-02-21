import math
from datetime import datetime

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="OpenLandMap Analytics Backend",
    description="Provides dataset metadata, statistics, and placeholder analytics for the dashboard.",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

DATASETS = [
    {
        "name": "Organic Carbon (g/kg)",
        "asset": "OpenLandMap/SOL/SOL_ORGANIC-CARBON_USDA-6A1C_M/v02",
        "units": "g/kg",
        "description": "Organic carbon concentration measured by OpenLandMap.",
        "visualization": {"min": 0, "max": 500, "palette": ["#fff5e1", "#c7a55d", "#654321", "#1a1a1a"]},
    },
    {
        "name": "Soil pH (H₂O)",
        "asset": "OpenLandMap/SOL/SOL_PH-H2O_USDA-4C1A2A_M/v02",
        "units": "pH",
        "description": "Water-extracted soil pH level from USDA calibration.",
        "visualization": {"min": 3, "max": 9, "palette": ["#ff0000", "#ffff00", "#00ff00", "#0000ff"]},
    },
    {
        "name": "Bulk Density (tonnes/m³)",
        "asset": "OpenLandMap/SOL/SOL_BULK-DENSITY_USDA-6A1C_M/v02",
        "units": "t/m³",
        "description": "Bulk density measured by soil cores aggregated globally.",
        "visualization": {"min": 0.8, "max": 2.0, "palette": ["#ffff00", "#ff8c00", "#ff0000"]},
    },
    {
        "name": "Sand Content (%)",
        "asset": "OpenLandMap/SOL/SOL_SAND-FRACTION_USDA-3A1A1A_M/v02",
        "units": "%",
        "description": "Sand fraction derived from OpenLandMap secondary data.",
        "visualization": {"min": 0, "max": 100, "palette": ["#fff5e1", "#ffd89b", "#deb887", "#8b7355"]},
    },
    {
        "name": "Clay Content (%)",
        "asset": "OpenLandMap/SOL/SOL_CLAY-FRACTION_USDA-3A1A1A_M/v02",
        "units": "%",
        "description": "Clay fraction derived from OpenLandMap secondary data.",
        "visualization": {"min": 0, "max": 100, "palette": ["#ffe4b5", "#ffdab9", "#daa520", "#8b4513"]},
    },
    {
        "name": "Soil Texture Class",
        "asset": "OpenLandMap/SOL/SOL_TEXTURE-CLASS_USDA-TT_M/v02",
        "units": "Class",
        "description": "Soil texture classification (1-12) from USDA training data.",
        "visualization": {"min": 1, "max": 12, "palette": ["#e8d4b0", "#d4a574", "#a68860", "#704d34"]},
    },
]


def _find_dataset(name: str):
    return next((dataset for dataset in DATASETS if dataset["name"] == name), DATASETS[0])


def _now_iso():
    return datetime.utcnow().isoformat() + "Z"


@app.get("/api/status")
def status():
    return {"status": "ok", "timestamp": _now_iso()}


@app.get("/api/datasets")
def list_datasets():
    return {"items": DATASETS}


@app.get("/api/statistics")
def statistics(dataset: str = Query(...), lat: float = 0.0, lon: float = 0.0):
    selected = _find_dataset(dataset)
    base = (len(selected["name"]) * 1.2 + abs(lat) + abs(lon)) % 80
    mean = round(base + 12 + math.sin(lat + lon), 2)
    min_value = round(mean - 5 + math.cos(lat - lon), 2)
    max_value = round(mean + 6 + math.sin(lat * 0.3), 2)
    std_dev = round((max_value - min_value) / 3, 2)
    return {
        "dataset": selected["name"],
        "lat": lat,
        "lon": lon,
        "statistics": {"mean": mean, "min": min_value, "max": max_value, "stdDev": std_dev},
        "generated": _now_iso(),
    }


@app.get("/api/analysis/time-series")
def time_series(
    dataset: str = Query(...),
    start_year: int = 2000,
    end_year: int = 2023,
):
    selected = _find_dataset(dataset)
    if start_year >= end_year:
        start_year, end_year = end_year - 5, end_year
    points = []
    base = len(selected["name"])
    for year in range(start_year, end_year + 1):
        value = round(base + (year - start_year) * 0.55 + math.sin(year / 3) * 2.4, 2)
        points.append({"year": year, "value": value})
    return {"dataset": selected["name"], "points": points}


@app.get("/api/analysis/change-detection")
def change_detection(
    dataset: str = Query(...),
    year_a: int = 2000,
    year_b: int = 2023,
):
    selected = _find_dataset(dataset)
    a, b = sorted((year_a, year_b))
    trend = len(selected["name"]) * 0.4
    value_a = round(10 + (a - 2000) * 0.7 + math.sin(a) * 0.3 + trend, 2)
    value_b = round(value_a + (b - a) * 0.6 + math.cos(b) * 0.2, 2)
    return {
        "dataset": selected["name"],
        "earlier_year": a,
        "later_year": b,
        "earlier_value": value_a,
        "later_value": value_b,
        "delta": round(value_b - value_a, 2),
    }


@app.get("/api/analysis/correlation")
def correlation(dataset: str = Query(...)):
    selected = _find_dataset(dataset)
    base = len(selected["name"])
    return {
        "dataset": selected["name"],
        "correlation": {
            "precipitation": round(0.6 + base * 0.02, 2),
            "landcover": round(-0.25 + (base % 5) * 0.03, 2),
            "temperature": round(0.4 + math.sin(base) * 0.1, 2),
            "population": round(-0.1 + math.cos(base) * 0.05, 2),
        },
    }


@app.get("/api/analysis/forecast")
def forecast(dataset: str = Query(...), years: int = 5):
    selected = _find_dataset(dataset)
    current_year = datetime.utcnow().year
    forecast = []
    base = len(selected["name"])
    for index in range(1, years + 1):
        year = current_year + index
        value = round(base + (year - 2000) * 0.5 + math.cos(index) * 1.8, 2)
        forecast.append({"year": year, "value": value})
    return {"dataset": selected["name"], "forecast": forecast}
