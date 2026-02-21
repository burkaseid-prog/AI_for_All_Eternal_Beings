import math

def correlation_model(selected):
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
