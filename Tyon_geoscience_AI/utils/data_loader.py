import pandas as pd
import numpy as np

def detect_application(df):
    """Infer application type based on column presence"""
    cols = df.columns.str.lower()
    if cols.str.contains('temperature').any():
        return 'geothermal'
    if cols.str.contains('contaminant|risk').any():
        return 'contamination'
    if cols.str.contains('hydraulic|aquifer').any():
        return 'groundwater'
    if 'porosity' in cols.values and 'permeability' in cols.values:
        return 'hydrocarbon'
    return 'unknown'

def load_well_data(filepath, application=None, units='metric'):
    """
    Load well data from CSV with flexible column mapping and application auto-detection
    """
    df = pd.read_csv(filepath)

    # Normalize column names
    col_map = {}
    for col in df.columns:
        lower_col = col.strip().lower()
        if 'depth' in lower_col:
            col_map[col] = 'depth'
        elif 'poro' in lower_col:
            col_map[col] = 'porosity'
        elif 'perm' in lower_col:
            col_map[col] = 'permeability'
        elif 'lith' in lower_col or 'rock' in lower_col:
            col_map[col] = 'lithology'
        elif 'temp' in lower_col:
            col_map[col] = 'temperature'
        elif 'conductivity' in lower_col and 'hydraulic' in lower_col:
            col_map[col] = 'hydraulic_conductivity'
        elif 'risk' in lower_col or 'contaminant' in lower_col:
            col_map[col] = 'contaminant_risk'

    df = df.rename(columns=col_map)

    # Handle missing lithology
    if 'lithology' not in df.columns:
        df['lithology'] = 'sandstone'

    # Convert units if needed
    if units == 'imperial':
        if 'depth' in df.columns:
            df['depth'] *= 0.3048
        if 'permeability' in df.columns:
            df['permeability'] *= 0.986923
        if 'temperature' in df.columns:
            df['temperature'] = (df['temperature'] - 32) * 5.0 / 9.0

    # Detect application if not provided
    if application is None or application == 'auto':
        application = detect_application(df)

    # Validate required columns per application
    required = []
    if application == 'geothermal':
        required = ['depth', 'temperature']
    elif application in ['contamination', 'groundwater', 'hydrocarbon']:
        required = ['depth', 'porosity', 'permeability']
    else:
        raise ValueError(f"Could not detect a valid application type. Columns: {list(df.columns)}")

    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns for {application} analysis: {', '.join(missing)}")

    return df.to_dict('records')
