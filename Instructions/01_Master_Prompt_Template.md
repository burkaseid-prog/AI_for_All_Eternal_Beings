# OpenLandMap GEE Prototype -- Master Prompt Template

You are a Google Earth Engine JavaScript developer.

Create a fully working GEE Code Editor application with the following
features:

## 1. DATASETS

Use OpenLandMap datasets from:
https://developers.google.com/earth-engine/datasets/tags/openlandmap

Use syntax pattern:
ee.Image("OpenLandMap/SOL/SOL_ORGANIC-CARBON_USDA-6A1C_M/v02")

Create dictionary:

``` javascript
var datasets = {
  "Organic Carbon": "OpenLandMap/SOL/SOL_ORGANIC-CARBON_USDA-6A1C_M/v02",
  "Soil pH": "OpenLandMap/SOL/SOL_PH-H2O_USDA-4C1A2A_M/v02",
  "Bulk Density": "OpenLandMap/SOL/SOL_BULK-DENSITY_USDA-6A1C_M/v02",
  "Texture": "OpenLandMap/SOL/SOL_TEXTURE-CLASS_USDA-TT_M/v02"
};
```

## 2. AUTO-DETECT TIME

If ImageCollection → extract unique years from system:time_start\
If Image → check band names for year metadata\
Populate year slider dynamically.

## 3. UI

-   Dataset dropdown\
-   Band dropdown\
-   Year slider\
-   Map visualization\
-   Legend

## 4. VISUALIZATION

``` javascript
Map.addLayer(image, {min: 0, max: 100, palette: ['blue','green','brown']}, "Layer");
```

Auto-compute min/max where possible.

## 5. TIME SERIES MODULE

Use ui.Chart.image.series for selected polygon.

## 6. CHANGE DETECTION

Compute:

``` javascript
var change = imageB.subtract(imageA);
```

## 7. ML EXTENSION PLACEHOLDER

Add commented blocks for: - Random forest - Temporal regression -
Determinant overlays

Return full Earth Engine JS code compatible with Code Editor.
