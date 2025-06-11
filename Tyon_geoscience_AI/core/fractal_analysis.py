import numpy as np
from sklearn.linear_model import LinearRegression

class FractalAnalyzer:
    """Fractal dimension analysis for subsurface characterization"""
    
    def __init__(self, min_samples=5):
        self.min_samples = min_samples
        
    def calculate(self, data):
        """Compute fractal dimension (Hurst exponent)"""
        if len(data) < self.min_samples:
            return np.nan
            
        try:
            x = np.arange(1, len(data)+1).reshape(-1,1)
            y = np.log(np.array(data) + 1e-6)
            model = LinearRegression().fit(np.log(x), y)
            return -model.coef_[0][0]  # Negative slope = fractal dimension
        except:
            return np.nan

def compute_fractal_dimension(data, min_samples=5):
    """Compute fractal dimension using FractalAnalyzer class"""
    analyzer = FractalAnalyzer(min_samples=min_samples)
    return analyzer.calculate(data)
