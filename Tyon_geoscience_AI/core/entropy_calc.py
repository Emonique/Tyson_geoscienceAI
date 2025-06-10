# core/entropy_calc.py
import numpy as np
from scipy.stats import gaussian_kde

class EntropyCalculator:
    """Robust entropy calculation for well log data"""
    
    def __init__(self, min_samples=10, bandwidth='scott'):
        self.min_samples = min_samples
        self.bandwidth = bandwidth
        
    def calculate(self, data):
        """Calculate continuous entropy with validation"""
        if len(data) < self.min_samples:
            return np.nan
            
        try:
            kde = gaussian_kde(data, bw_method=self.bandwidth)
            return kde.entropy()
        except:
            return np.nan
