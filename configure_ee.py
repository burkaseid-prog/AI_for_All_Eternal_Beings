#!/usr/bin/env python
"""
Configure Google Earth Engine with ee-sahilyousafp project
"""

import ee
import webbrowser

try:
    # Authenticate with Google
    ee.Authenticate()
    print("✓ Authentication successful!")
    
    # Initialize with the specified project
    ee.Initialize(project='ee-sahilyousafp')
    print("✓ Earth Engine initialized with project: ee-sahilyousafp")
    
    # Verify the initialization
    info = ee.data.getInfo()
    print(f"✓ Configuration complete!")
    print(f"  Project: ee-sahilyousafp")
    
except Exception as e:
    print(f"✗ Error: {e}")
    raise
