import numpy as np
import xgboost as xgb
import pandas as pd

class DosingEngine:
    def __init__(self):
        self.CROP_THRESHOLDS = {
            "Rice IR64": {"min_moisture": 60.0, "min_N": 40.0, "min_P": 20.0, "min_K": 20.0},
            "Wheat HD-2967": {"min_moisture": 40.0, "min_N": 30.0, "min_P": 15.0, "min_K": 15.0},
            "Tomato H-86": {"min_moisture": 50.0, "min_N": 35.0, "min_P": 25.0, "min_K": 30.0},
        }
        self.model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
        self.is_trained = False
        self.train()

    def generate_synthetic_data(self):
        np.random.seed(42)
        n = 200
        X = pd.DataFrame({
            'moisture': np.random.uniform(10, 90, n),
            'N': np.random.uniform(10, 80, n),
            'P': np.random.uniform(10, 80, n),
            'K': np.random.uniform(10, 80, n),
            'target_moisture': np.random.uniform(30, 70, n),
            'target_N': np.random.uniform(20, 50, n)
        })
        y = (X['moisture'] < X['target_moisture']).astype(int)
        return X, y

    def train(self):
        X, y = self.generate_synthetic_data()
        self.model.fit(X, y)
        self.is_trained = True

    def decide(self, sensor_data, crop_variety):
        thresholds = self.CROP_THRESHOLDS.get(crop_variety, {
            "min_moisture": 40.0, "min_N": 30.0, "min_P": 20.0, "min_K": 20.0
        })
        
        pump_on = False
        valve_open = False
        nutrient_dose_ml = 0.0
        reasons = []
        
        moisture = sensor_data.get('soil_moisture', 0.0)
        n = sensor_data.get('nitrogen', 0.0)
        
        if moisture < thresholds['min_moisture']:
            pump_on = True
            reasons.append(f"Low soil moisture: {moisture} < {thresholds['min_moisture']}")
            
        if n < thresholds['min_N']:
            valve_open = True
            nutrient_dose_ml = (thresholds['min_N'] - n) * 10.0
            reasons.append(f"Nitrogen deficiency. Dosing {nutrient_dose_ml:.1f}ml")
            
        return {
            "pump_on": pump_on,
            "valve_open": valve_open,
            "nutrient_dose_ml": nutrient_dose_ml,
            "reasons": reasons
        }

engine = DosingEngine()
