import math

def change_detection_model(selected, year_a, year_b):
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
