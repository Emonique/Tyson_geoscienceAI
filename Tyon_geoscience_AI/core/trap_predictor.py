import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

class ZoneDetector:
    """Identifies optimal zones using anomaly detection with application-specific thresholds"""
    
    def __init__(self, application='hydrocarbon', trap_threshold=0.15, leak_threshold=0.3, temp_threshold=150):
        self.application = application
        # Set application-specific thresholds
        if application == 'hydrocarbon':
            self.quality_threshold = trap_threshold
        elif application == 'contamination':
            self.quality_threshold = leak_threshold
        elif application == 'geothermal':
            self.quality_threshold = temp_threshold
        else:  # groundwater and others
            self.quality_threshold = 0.3  # Default
            
        self.contamination = 0.1  # For IsolationForest
        
    def detect(self, geo_memory):
        """Find target zones from analysis results"""
        if len(geo_memory) < 10:
            return []
            
        # Feature engineering - use application-specific quality metrics
        features = []
        quality_scores = []
        
        for r in geo_memory:
            if self.application == 'hydrocarbon':
                quality = r.get('rqi', 0)
            elif self.application == 'groundwater':
                quality = r.get('hydraulic_conductivity', 0)
            elif self.application == 'contamination':
                quality = r.get('contaminant_risk', 0)
            elif self.application == 'geothermal':
                quality = r.get('temperature', 0)
            else:
                quality = 0
                
            features.append([r['entropy'], quality, r['fractal_dim']])
            quality_scores.append(quality)
        
        # Convert to arrays
        features = np.array(features)
        quality_scores = np.array(quality_scores)
        
        # Standardization
        scaler = StandardScaler()
        X = scaler.fit_transform(features)
        
        # Anomaly detection
        clf = IsolationForest(
            contamination=self.contamination, 
            random_state=42
        )
        anomalies = clf.fit_predict(X)
        
        # Return points that meet quality threshold AND are anomalies
        return [
            r for i, r in enumerate(geo_memory)
            if (quality_scores[i] > self.quality_threshold) and (anomalies[i] == -1)
        ]

# Unified prediction function
def predict_traps(geo_memory, application, trap_threshold=0.15, leak_threshold=0.3, temp_threshold=150):
    detector = ZoneDetector(
        application=application,
        trap_threshold=trap_threshold,
        leak_threshold=leak_threshold,
        temp_threshold=temp_threshold
    )
    return detector.detect(geo_memory)
