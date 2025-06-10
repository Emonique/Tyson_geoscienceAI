import numpy as np

def calculate_pressure(depth, fluid_density=1000, matrix_density=2650, units='metric'):
    """
    Calculate reservoir pressure with unit conversion
    Returns pressure in MPa
    """
    if units == 'imperial':
        depth_m = depth * 0.3048  # Convert feet to meters
    else:
        depth_m = depth  # Already in meters
    
    lithostatic = matrix_density * 9.81 * depth_m / 1e6  # MPa
    hydrostatic = fluid_density * 9.81 * depth_m / 1e6   # MPa
    return 0.4 * lithostatic + 0.6 * hydrostatic  # Weighted average

def calculate_temperature(depth, surface_temp=25, gradient=3.1, 
                         units='metric'):
    """
    Calculate formation temperature
    Returns temperature in °C
    """
    if units == 'imperial':
        depth_km = depth * 0.0003048  # Convert feet to km
    else:
        depth_km = depth / 1000  # Convert meters to km
        
    return surface_temp + gradient * depth_km

def compute_rqi(porosity, permeability, porosity_units='pct'):
    """
    Compute Reservoir Quality Index (RQI)
    - porosity_units: 'pct' for percentage, 'frac' for fractional
    """
    if porosity_units == 'pct':
        porosity_frac = np.array(porosity) / 100.0
    else:
        porosity_frac = np.array(porosity)
        
    return 0.0314 * np.sqrt(permeability / porosity_frac)

def hydraulic_conductivity(permeability_md, fluid_density=1000, 
                          dynamic_viscosity=0.001):
    """
    Convert permeability (mD) to hydraulic conductivity (m/s)
    for groundwater applications
    """
    permeability_si = permeability_md * 9.869233e-16  # Convert mD to m²
    return (permeability_si * fluid_density * 9.81) / dynamic_viscosity

def heat_capacity_ratio(temperature, pressure, fluid_type='water'):
    """
    Compute heat capacity ratio for geothermal applications
    """
    if fluid_type == 'water':
        # Simplified water properties
        Cp = 4180 + 10 * (temperature - 25)  # J/kg·K
        Cv = Cp - 9.6e-4 * pressure  # Approximate
        return Cp / Cv
    else:
        return 1.3  # Default for brine/other fluids
