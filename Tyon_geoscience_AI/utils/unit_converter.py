def convert(value, from_unit, to_unit):
    """Handle common unit conversions in geoscience"""
    # Length conversions
    if from_unit == 'ft' and to_unit == 'm':
        return value * 0.3048
    if from_unit == 'm' and to_unit == 'ft':
        return value * 3.28084
    
    # Temperature conversions
    if from_unit == 'C' and to_unit == 'F':
        return (value * 9/5) + 32
    if from_unit == 'F' and to_unit == 'C':
        return (value - 32) * 5/9
    
    # Pressure conversions
    if from_unit == 'psi' and to_unit == 'MPa':
        return value * 0.00689476
    if from_unit == 'MPa' and to_unit == 'psi':
        return value / 0.00689476
    
    # Permeability conversions
    if from_unit == 'mD' and to_unit == 'm²':
        return value * 9.869233e-16
    if from_unit == 'm²' and to_unit == 'mD':
        return value / 9.869233e-16
    
    return value  # No conversion needed
