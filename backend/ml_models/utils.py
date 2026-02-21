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
        "asset": "OpenLandMap/SOL/SOL_BULKDENS-FINEEARTH_USDA-4A1H_M/v02",
        "scale": 10,
        "units": "t/m³",
        "description": "Bulk density measured by soil cores aggregated globally.",
        "visualization": {"min": 8, "max": 20, "palette": ["#ffff00", "#ff8c00", "#ff0000"]},
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

def find_dataset(name: str):
    return next((dataset for dataset in DATASETS if dataset["name"] == name), DATASETS[0])
