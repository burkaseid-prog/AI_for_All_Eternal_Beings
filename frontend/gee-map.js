// Google Earth Engine Map Integration
// Initialize GEE and display map with dataset visualization

const DATASETS_GEE = {
  "Organic Carbon (g/kg)": {
    asset: "OpenLandMap/SOL/SOL_ORGANIC-CARBON_USDA-6A1C_M/v02",
    visParams: { min: 0, max: 500, palette: ['FFF5E1', 'C7A55D', '654321', '1A1A1A'] }
  },
  "Soil pH (H₂O)": {
    asset: "OpenLandMap/SOL/SOL_PH-H2O_USDA-4C1A2A_M/v02",
    visParams: { min: 3, max: 9, palette: ['FF0000', 'FFFF00', '00FF00', '0000FF'] }
  },
  "Bulk Density (tonnes/m³)": {
    asset: "OpenLandMap/SOL/SOL_BULK-DENSITY_USDA-6A1C_M/v02",
    visParams: { min: 0.8, max: 2.0, palette: ['FFFF00', 'FF8C00', 'FF0000'] }
  },
  "Sand Content (%)": {
    asset: "OpenLandMap/SOL/SOL_SAND-FRACTION_USDA-3A1A1A_M/v02",
    visParams: { min: 0, max: 100, palette: ['FFF5E1', 'FFD89B', 'DEB887', '8B7355'] }
  },
  "Clay Content (%)": {
    asset: "OpenLandMap/SOL/SOL_CLAY-FRACTION_USDA-3A1A1A_M/v02",
    visParams: { min: 0, max: 100, palette: ['FFE4B5', 'FFDAB9', 'DAA520', '8B4513'] }
  },
  "Soil Texture Class": {
    asset: "OpenLandMap/SOL/SOL_TEXTURE-CLASS_USDA-TT_M/v02",
    visParams: { min: 1, max: 12, palette: ['E8D4B0', 'D4A574', 'A68860', '704D34'] }
  }
};

let geeMap = null;
let currentLayer = null;

function initGEEMap() {
  const mapStatus = document.getElementById('mapStatus');
  
  // Check if EE is available
  if (typeof ee === 'undefined') {
    mapStatus.textContent = '❌ GEE API not loaded. Please sign in to Google Earth Engine first.';
    return;
  }

  try {
    // Initialize Earth Engine
    ee.initialize(
      null,
      null,
      function() {
        mapStatus.textContent = '✅ Connected to Google Earth Engine';
        createGEEMap();
      },
      function(error) {
        mapStatus.textContent = '⚠️ GEE auth required. Sign in at code.earthengine.google.com first.';
        console.error('EE initialization error:', error);
      }
    );
  } catch (error) {
    mapStatus.textContent = '⚠️ GEE not available. Ensure you\'re signed into Google Earth Engine.';
    console.error('GEE setup error:', error);
  }
}

function createGEEMap() {
  const mapDiv = document.getElementById('map');
  
  // Create map using Leaflet + GEE tiles
  geeMap = L.map('map').setView([5.2, 12.8], 4);
  
  // Add base layer
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19
  }).addTo(geeMap);

  // Initialize with first dataset
  const firstDataset = Object.keys(DATASETS_GEE)[0];
  visualizeDataset(firstDataset);

  // Add click handler for region selection
  geeMap.on('click', function(e) {
    const { lat, lng } = e.latlng;
    document.getElementById('regionInfo').textContent = 
      `Lat: ${lat.toFixed(2)}, Lon: ${lng.toFixed(2)}`;
  });
}

function visualizeDataset(datasetName) {
  const dataset = DATASETS_GEE[datasetName];
  if (!dataset || !geeMap) return;

  // Remove previous layer
  if (currentLayer) {
    geeMap.removeLayer(currentLayer);
  }

  // Load GEE image
  const image = ee.Image(dataset.asset);
  
  // Create URL for GEE tile layer
  const mapId = image.getMapId(dataset.visParams, function(data) {
    const eeLayer = L.tileLayer(
      'https://earthengine.googleapis.com/map/' + data.mapid + '/{z}/{x}/{y}',
      { attribution: 'Google Earth Engine', maxZoom: 18 }
    );
    
    if (currentLayer) geeMap.removeLayer(currentLayer);
    currentLayer = eeLayer;
    geeMap.addLayer(currentLayer);
  });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
  // Check if Leaflet is loaded
  if (typeof L === 'undefined') {
    console.warn('Leaflet not loaded. Loading dynamically...');
    const leafletCSS = document.createElement('link');
    leafletCSS.rel = 'stylesheet';
    leafletCSS.href = 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css';
    document.head.appendChild(leafletCSS);

    const leafletJS = document.createElement('script');
    leafletJS.src = 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js';
    leafletJS.onload = initGEEMap;
    document.head.appendChild(leafletJS);
  } else {
    initGEEMap();
  }
});

// Export for use in main.js
window.visualizeGEEDataset = visualizeDataset;
