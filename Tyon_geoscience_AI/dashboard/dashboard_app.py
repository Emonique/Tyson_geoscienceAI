import streamlit as st  # Must be first Streamlit import

# Set page config FIRST - must be before any other Streamlit commands
st.set_page_config(page_title="Tyon Geoscience AI", layout="wide")

# Now proceed with other imports
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

# Initialize system
system = GeoscienceAnalysisSystem(application=application)

# Main dashboard layout
if uploaded_file and run_analysis:
    data = load_well_data(uploaded_file, application=application, units=units)
    df = pd.DataFrame(data)

    with st.expander("Raw Data Preview"):
        st.dataframe(df.head(10))

    # FIXED: Use status container instead of text parameter
    status_container = st.empty()
    progress_bar = st.progress(0)
    status_container.write("Analyzing subsurface data...")

    # Pass parameters to analysis
    analysis_params = {}
    if trap_threshold: analysis_params["trap_threshold"] = trap_threshold
    if leak_threshold: analysis_params["leak_threshold"] = leak_threshold
    if temp_threshold: analysis_params["temp_threshold"] = temp_threshold
    
    results = system.analyze_dataset(data, **analysis_params)
    
    # Update progress with new method
    progress_bar.progress(40)
    status_container.write("Generating visualizations...")

    st.subheader("Integrated Analysis Dashboard")
    col1, col2 = st.columns(2)

    geo_memory = results["data_points"]
    depths = [d['depth'] for d in geo_memory]
    entropies = [d['entropy'] for d in geo_memory]
    fractal_dims = [d['fractal_dim'] for d in geo_memory]
    lithologies = [d['lithology'] for d in geo_memory]

    fig, axs = plt.subplots(3, 2, figsize=(14, 12))
    fig.suptitle("Tyon Geoscience Analysis Dashboard", fontsize=16, fontweight='bold')

    axs[0, 0].plot(entropies, 'o-', color='navy')
    axs[0, 0].set_title("Entropy Evolution")
    axs[0, 0].set_xlabel("Sample Index")
    axs[0, 0].set_ylabel("Entropy (bits)")

    if application == "hydrocarbon":
        rqi_vals = [np.mean(d['rqi']) for d in geo_memory]
        sc = axs[0, 1].scatter(depths, rqi_vals, c=entropies, cmap='viridis', s=80)
        axs[0, 1].set_title("Mean RQI vs Depth")
        axs[0, 1].set_xlabel("Depth (m)")
        axs[0, 1].set_ylabel("Mean RQI")
        fig.colorbar(sc, ax=axs[0, 1], label='Entropy (bits)')
    elif application == "groundwater":
        conductivities = [d.get('hydraulic_conductivity', 0) for d in geo_memory]
        sc = axs[0, 1].scatter(depths, conductivities, c=entropies, cmap='plasma', s=80)
        axs[0, 1].set_title("Hydraulic Conductivity vs Depth")
        axs[0, 1].set_xlabel("Depth (m)")
        axs[0, 1].set_ylabel("K (m/s)")
        fig.colorbar(sc, ax=axs[0, 1], label='Entropy (bits)')
    elif application == "contamination":
        risks = [d.get('contaminant_risk', 0) for d in geo_memory]
        sc = axs[0, 1].scatter(depths, risks, c=entropies, cmap='inferno', s=80)
        axs[0, 1].set_title("Contamination Risk vs Depth")
        axs[0, 1].set_xlabel("Depth (m)")
        axs[0, 1].set_ylabel("Risk Score")
        fig.colorbar(sc, ax=axs[0, 1], label='Entropy (bits)')
    elif application == "geothermal":
        temps = [d.get('temperature', 0) for d in geo_memory]
        sc = axs[0, 1].scatter(depths, temps, c=entropies, cmap='magma', s=80)
        axs[0, 1].set_title("Temperature vs Depth")
        axs[0, 1].set_xlabel("Depth (m)")
        axs[0, 1].set_ylabel("Temperature (°C)")
        fig.colorbar(sc, ax=axs[0, 1], label='Entropy (bits)')

    unique_litho = list(set(lithologies))
    colors = plt.cm.tab10.colors[:len(unique_litho)]

    for i, litho in enumerate(unique_litho):
        litho_dims = [fd for j, fd in enumerate(fractal_dims) if lithologies[j] == litho]
        axs[1, 0].hist(litho_dims, bins=10, alpha=0.7, color=colors[i], label=litho, density=True)

    axs[1, 0].set_title("Fractal Dimension by Lithology")
    axs[1, 0].set_xlabel("Fractal Dimension")
    axs[1, 0].set_ylabel("Density")
    axs[1, 0].legend()

    if application == "geothermal":
        temps = [d.get('temperature', 0) for d in geo_memory]
        ratios = [d.get('heat_capacity_ratio', 0) for d in geo_memory]
        axs[1, 1].plot(depths, temps, 'o-', color='orange', label='Temperature')
        axs[1, 1].set_xlabel("Depth (m)")
        axs[1, 1].set_ylabel("Temperature (°C)", color='orange')
        axs[1, 1].tick_params(axis='y', labelcolor='orange')

        ax2 = axs[1, 1].twinx()
        ax2.plot(depths, ratios, 's-', color='purple', label='Cp/Cv Ratio')
        ax2.set_ylabel("Heat Capacity Ratio", color='purple')
        ax2.tick_params(axis='y', labelcolor='purple')
        axs[1, 1].set_title("Geothermal Profile")
    else:
        pressures = [d.get('pressure', 0) for d in geo_memory]
        axs[1, 1].plot(depths, pressures, 'o-', color='blue')
        axs[1, 1].set_title("Pressure Profile")
        axs[1, 1].set_xlabel("Depth (m)")
        axs[1, 1].set_ylabel("Pressure (MPa)")

    sc = axs[2, 0].scatter(fractal_dims, entropies, c=depths, cmap='viridis', s=80)
    axs[2, 0].set_title("Fractal Dimension vs Entropy")
    axs[2, 0].set_xlabel("Fractal Dimension")
    axs[2, 0].set_ylabel("Entropy (bits)")
    fig.colorbar(sc, ax=axs[2, 0], label='Depth (m)')

    mean_porosities = [np.mean(d['porosity']) for d in geo_memory]
    permeabilities = [d['permeability'] for d in geo_memory]
    sc = axs[2, 1].scatter(mean_porosities, permeabilities, c=entropies, cmap='plasma', s=80)
    axs[2, 1].set_title("Porosity vs Permeability")
    axs[2, 1].set_xlabel("Mean Porosity (%)")
    axs[2, 1].set_ylabel("Permeability (mD)")
    fig.colorbar(sc, ax=axs[2, 1], label='Entropy (bits)')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Update progress
    progress_bar.progress(70)
    status_container.write("Finalizing dashboard...")

    col1, col2 = st.columns([3, 1])
    with col1:
        st.pyplot(fig)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_name = f"reports/{application}_dashboard_{timestamp}.png"
    plt.savefig(report_name, dpi=150)
    plt.close()

    st.subheader("Analysis Results")
    predictions = results["predictions"]

    if predictions:
        st.success(f"✅ Found {len(predictions)} significant zones")
        results_df = pd.DataFrame(predictions)
        results_df = results_df[['depth', 'lithology', 'confidence', 'entropy', 'fractal_dim']]
        results_df['confidence'] = results_df['confidence'].round(3)
        results_df['entropy'] = results_df['entropy'].round(3)
        results_df['fractal_dim'] = results_df['fractal_dim'].round(2)

        if application in ["contamination", "groundwater"]:
            results_df['leak_risk'] = [z.get('leak_risk', False) for z in predictions]

        st.dataframe(results_df.sort_values('confidence', ascending=False))

        if application == "contamination" and any(results_df.get('leak_risk', [])):
            leak_zones = results_df[results_df['leak_risk']]
            st.warning(f"⚠️ High leak risk detected at {len(leak_zones)} depth(s)")
            st.dataframe(leak_zones)
    else:
        st.warning("⚠️ No significant zones detected with current parameters")

    # Final progress update
    progress_bar.progress(100)
    status_container.write("Analysis complete!")
    st.balloons()

    with col2:
        st.download_button(
            label="Download Dashboard",
            data=open(report_name, "rb"),
            file_name=os.path.basename(report_name),
            mime="image/png"
        )

        st.download_button(
            label="Download Results (CSV)",
            data=pd.DataFrame(results["data_points"]).to_csv().encode('utf-8'),
            file_name=f"{application}_results_{timestamp}.csv",
            mime="text/csv"
        )
elif run_analysis:
    st.error("Please upload a data file first")
else:
    st.info("Upload a CSV file and click 'Run Analysis' to begin")

st.divider()
st.subheader("Data Requirements")

app_requirements = {
    "hydrocarbon": """
    **Required Columns:**  
    - Depth (m or ft)  
    - Porosity (%)  
    - Permeability (mD)  
    - Lithology (sandstone, carbonate, shale, etc.)  
    
    **Optional:**  
    - Temperature (°C or °F)  
    """,
    "groundwater": """
    **Required Columns:**  
    - Depth (m or ft)  
    - Porosity (%)  
    - Permeability (mD)  
    - Lithology  
    
    **Recommended:**  
    - Water table depth  
    - Contaminant levels  
    """,
    "contamination": """
    **Required Columns:**  
    - Depth (m or ft)  
    - Porosity (%)  
    - Permeability (mD)  
    - Lithology  
    
    **Recommended:**  
    - Contaminant concentration  
    - Hydraulic conductivity  
    """,
    "geothermal": """
    **Required Columns:**  
    - Depth (m or ft)  
    - Temperature (°C or °F)  
    - Lithology  
    
    **Recommended:**  
    - Thermal conductivity  
    - Heat flow measurements  
    """
}

st.markdown(app_requirements[application])

sample_data = {
    "hydrocarbon": "data/sample_hydrocarbon.csv",
    "groundwater": "data/sample_groundwater.csv",
    "contamination": "data/sample_contamination.csv",
    "geothermal": "data/sample_geothermal.csv"
}

if os.path.exists(sample_data[application]):
    with open(sample_data[application], "rb") as f:
        st.download_button(
            f"Download {application.capitalize()} Sample Data",
            f,
            file_name=f"sample_{application}_data.csv",
            mime="text/csv"
    )
