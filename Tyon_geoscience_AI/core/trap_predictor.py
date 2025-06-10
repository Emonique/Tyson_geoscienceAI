import numpy as np

def compute_trap_likelihood(entropy, rqi, depth, pressure, 
                           application='hydrocarbon'):
    """
    Compute trap likelihood with application-specific thresholds
    """
    base_likelihood = entropy * np.mean(rqi)
    
    # Application-specific adjustments
    if application == 'hydrocarbon':
        capillary_threshold = 0.15 * depth / 1000  # Depth-scaled
        if pressure > capillary_threshold:
            return base_likelihood * 0.7
        return base_likelihood
    
    elif application == 'groundwater':
        # Focus on high conductivity zones
        return base_likelihood * (1 + 0.2 * np.mean(rqi))
    
    elif application == 'contamination':
        # Focus on high entropy (heterogeneity)
        return entropy * 1.5
    
    elif application == 'geothermal':
        # Focus on fracture networks
        return base_likelihood * (1 + 0.3 * entropy)
    
    else:
        return base_likelihood

def detect_leaky_zones(entropy, hydraulic_conductivity, threshold=1e-5):
    """Identify potential leak zones for environmental applications"""
    return entropy * hydraulic_conductivity > threshold

def predict_traps(geo_data, application='hydrocarbon', threshold=0.15):
    """Identify target zones based on application type"""
    results = []
    for data in geo_data:
        likelihood = compute_trap_likelihood(
            data['entropy'],
            data['rqi'],
            data['depth'],
            data['pressure'],
            application
        )
        
        result = {
            'depth': data['depth'],
            'lithology': data['lithology'],
            'confidence': np.clip(likelihood, 0, 1),
            'entropy': data['entropy'],
            'fractal_dim': data['fractal_dim']
        }
        
        # Add leak detection for environmental apps
        if application in ['contamination', 'groundwater']:
            leak_risk = detect_leaky_zones(
                data['entropy'],
                data.get('hydraulic_conductivity', 0)
            )
            result['leak_risk'] = leak_risk
            
        results.append(result)
    
    return [r for r in results if r['confidence'] > threshold]
