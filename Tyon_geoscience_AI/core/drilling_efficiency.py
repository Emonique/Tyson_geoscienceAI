# core/drilling_efficiency.py
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

class DrillingEfficiencyPredictor:
    """Predicts drilling efficiency for groundwater wells"""
    
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.trained = False
        
    def train(self, X, y):
        """Train model on historical drilling data"""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        self.model.fit(X_train, y_train)
        
        # Validate model performance
        preds = self.model.predict(X_test)
        r2 = r2_score(y_test, preds)
        self.trained = r2 > 0.6  # Only mark as trained if reasonable accuracy
        
        return r2
        
    def predict(self, formation_features):
        """Predict drilling efficiency (meters/hour)"""
        if not self.trained:
            raise RuntimeError("Model not trained or training failed")
        return self.model.predict([formation_features])[0]
