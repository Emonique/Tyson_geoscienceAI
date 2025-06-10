# core/zone_detector.py
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

class ZoneDetector:
    """Identifies optimal zones using anomaly detection"""
    
    def __init__(self, contamination=0.1):
        self.contamination = contamination
        
    def detect(self, geo_memory):
        """Find target zones from analysis results"""
        if len(geo_memory) < 10:
            return []
            
        # Feature engineering
        features = np.array([
            [r['entropy'], 
             r['quality_index'],
             r['fractal_dim']] 
            for r in geo_memory
        ])
        
        # Standardization
        scaler = StandardScaler()
        X = scaler.fit_transform(features)
        
        # Anomaly detection
        clf = IsolationForest(
            contamination=self.contamination, 
            random_state=42
        )
        anomalies = clf.fit_predict(X)
        
        # Combine with quality threshold
        quality_scores = np.array([r['quality_index'] for r in geo_memory])
        quality_threshold = np.percentile(quality_scores, 75)
        
        return [
            r for i, r in enumerate(geo_memory)
            if (r['quality_index'] > quality_threshold) and (anomalies[i] == 1)
      ]
