import math
from datetime import datetime

def forecast_model(selected, years):
    current_year = datetime.utcnow().year
    forecast = []
    base = len(selected["name"])
    for index in range(1, years + 1):
        year = current_year + index
        value = round(base + (year - 2000) * 0.5 + math.cos(index) * 1.8, 2)
        forecast.append({"year": year, "value": value})
    return {"dataset": selected["name"], "forecast": forecast}
