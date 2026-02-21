import math

def time_series_model(selected, start_year, end_year):
    if start_year >= end_year:
        start_year, end_year = end_year - 5, end_year
    points = []
    base = len(selected["name"])
    for year in range(start_year, end_year + 1):
        value = round(base + (year - start_year) * 0.55 + math.sin(year / 3) * 2.4, 2)
        points.append({"year": year, "value": value})
    return {"dataset": selected["name"], "points": points}
