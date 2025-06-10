# core/rqi_calculation.py
import numpy as np

class ReservoirQualityIndex:
    """Domain-specific quality metrics"""
    
    @staticmethod
    def hydrocarbon(porosity, permeability):
        """Standard RQI for O&G (Amaefule 1993)"""
        return 0.0314 * np.sqrt(permeability / porosity)
    
    @staticmethod 
    def groundwater(porosity, permeability):
        """Flow Capacity Index (FCI) for aquifers"""
        # Combines porosity and permeability into single productivity metric
        return permeability * porosity / 1000  # Normalized scale
    
    @staticmethod
    def geothermal(porosity, permeability, temp_grad):
        """Energy Potential Index (EPI)"""
        return (permeability * porosity * temp_grad) / 1e6
