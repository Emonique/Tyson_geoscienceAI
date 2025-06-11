import streamlit as st  # Must be first Streamlit import

# Set page config FIRST - must be before any other Streamlit commands
st.set_page_config(page_title="Tyon Geoscience AI", layout="wide")

import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# ──── CRITICAL FIX: Add project root to Python path ────
current_dir = Path(__file__).resolve().parent  # /Tyon_geoscience_AI/dashboard
project_root = current_dir.parent  # /Tyon_geoscience_AI
sys.path.insert(0, str(project_root))

# Now import your custom modules
try:
    from execution.run_analysis import GeoscienceAnalysisSystem
    from utils.data_loader import load_well_data
except ImportError as e:
    st.error(f"Import Error: {e}")
    st.stop()

# Create reports directory if not exists
os.makedirs("reports", exist_ok=True)

# Dashboard title (now after page config)
st.title("🌋 Tyon Geoscience AI - Subsurface Analysis Dashboard")

# Sidebar controls
with st.sidebar:
    st.header("Configuration")
    application = st.selectbox(
        "Analysis Type",
        ["hydrocarbon", "groundwater", "contamination", "geothermal"],
        index=0,
        help="Select the application domain"
    )

    units = st.radio(
        "Data Units",
        ["metric", "imperial"],
        index=0,
        help="Select measurement units in input data"
    )

    uploaded_file = st.file_uploader(
        "Upload Well Data (CSV)", 
        type="csv",
        help="Upload CSV with depth, porosity, permeability, and lithology columns"
    )

    st.divider()
    st.subheader("Analysis Parameters")

    # Initialize parameters to avoid reference before assignment
    trap_threshold = leak_threshold = temp_threshold = None

    if application == "hydrocarbon":
        trap_threshold = st.slider(
            "Trap Confidence Threshold", 
            0.05, 0.5, 0.15, 0.01,
            help="Minimum confidence for hydrocarbon trap identification"
        )
    elif application == "contamination":
        leak_threshold = st.slider(
            "Leak Risk Threshold", 
            0.1, 1.0, 0.3, 0.05,
            help="Minimum risk level for contamination leak zones"
        )
    elif application == "geothermal":
        temp_threshold = st.slider(
            "Temperature Threshold (°C)", 
            50, 300, 150, 5,
            help="Minimum temperature for geothermal potential"
        )

    run_analysis = st.button("Run Analysis", type="primary")

# Application description
app_descriptions = {
    "hydrocarbon": "Analyze hydrocarbon reservoirs using entropic-fractal methods to identify potential traps",
    "groundwater": "Assess groundwater resources and aquifer characteristics using fractal heterogeneity analysis",
    "contamination": "Identify potential leak zones and contamination pathways in environmental geology",
    "geothermal": "Evaluate geothermal potential through thermodynamic and entropic analysis"
}

st.subheader(f"{application.capitalize()} Analysis")
st.caption(app_descriptions[application])
