import math

def prediction_model(selected, start_year, end_year, lat_min, lon_min, lat_max, lon_max):
    if start_year >= end_year:
        start_year, end_year = end_year - 5, end_year
    points = []
    base = len(selected["name"])
    # The lat/lon parameters are not used in the placeholder model,
    # but they are here to show how a real model would use them.
    for year in range(start_year, end_year + 1):
        value = round(base + (year - start_year) * 0.55 + math.sin(year / 3) * 2.4, 2)
        points.append({"year": year, "value": value})
    return {"dataset": selected["name"], "points": points}
