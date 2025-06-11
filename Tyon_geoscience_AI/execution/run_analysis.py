import os
import sys

# Add this at the top of your script - BEFORE other imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, parent_dir)

import numpy as np
from core.fractal_analysis import compute_fractal_dimension
from core import entropy_calc, rqi_model, trap_predictor
from utils import data_loader, data_simulator, unit_converter

class GeoscienceAnalysisSystem:
    """Integrated analysis system for geological applications"""
    
    def __init__(self, application='hydrocarbon'):
        self.geo_memory = []
        self.application = application
        # Initialize thresholds to None
        self.trap_threshold = None
        self.leak_threshold = None
        self.temp_threshold = None
    
    def analyze_point(self, data_point):
        """Analyze a single data point"""
        depth = data_point['depth']
        lithology = data_point.get('lithology', 'sandstone')
        
        # Generate or use provided porosity data
        if 'porosity' in data_point:
            porosity = data_point['porosity']
            if not isinstance(porosity, list):
                porosity = [porosity]  # Ensure array format
        else:
            # If base_porosity is not provided, use a default based on lithology
            base_poro = data_point.get('base_porosity', 20)  # Default to 20%
            porosity = data_simulator.simulate_porosity(
                depth, 
                base_poro, 
                lithology
            )
        
        # Get permeability
        permeability = data_point.get('permeability', 100)
        
        # Core calculations - FIXED INDENTATION HERE
        fractal_dim = compute_fractal_dimension(porosity)
        geo_entropy = entropy_calc.shannon_entropy(porosity)  # Line 48 - fixed
        
        # Calculate pressure and temperature if not provided
        if 'pressure' not in data_point:
            data_point['pressure'] = rqi_model.calculate_pressure(depth)
        if 'temperature' not in data_point and self.application == 'geothermal':
            data_point['temperature'] = rqi_model.calculate_temperature(depth)
        
        # Application-specific metrics
        result = {
            'depth': depth,
            'lithology': lithology,
            'porosity': porosity,
            'permeability': permeability,
            'fractal_dim': fractal_dim,
            'entropy': geo_entropy,
            'pressure': data_point['pressure'],
        }
        
        # Add application-specific properties
        if self.application == 'hydrocarbon' or self.application == 'groundwater':
            rqi = rqi_model.compute_rqi(np.mean(porosity), permeability)
            result['rqi'] = rqi
            
            if self.application == 'groundwater':
                hc = rqi_model.hydraulic_conductivity(permeability)
                result['hydraulic_conductivity'] = hc
                
        elif self.application == 'contamination':
            # Generate environmental data if not provided
            if 'contaminant_risk' not in data_point:
                env_data = data_simulator.generate_environmental_data(depth, lithology)
                result['contaminant_risk'] = env_data['contaminant_risk']
            else:
                result['contaminant_risk'] = data_point['contaminant_risk']
                
        elif self.application == 'geothermal':
            temperature = data_point.get('temperature', rqi_model.calculate_temperature(depth))
            hc_ratio = rqi_model.heat_capacity_ratio(temperature, data_point['pressure'])
            result['temperature'] = temperature
            result['heat_capacity_ratio'] = hc_ratio
        
        return result
    
    def analyze_dataset(self, dataset):
        """Analyze a full dataset"""
        self.geo_memory = []
        for data_point in dataset:
            analyzed_point = self.analyze_point(data_point)
            self.geo_memory.append(analyzed_point)
        
        # Now run trap prediction on the entire analyzed dataset
        predictions = trap_predictor.predict_traps(
            self.geo_memory, 
            application=self.application,
            trap_threshold=self.trap_threshold,
            leak_threshold=self.leak_threshold,
            temp_threshold=self.temp_threshold
        )
        
        return {
            "data_points": self.geo_memory,
            "predictions": predictions
            }
